#!/usr/bin/env python3
"""
EdTech Research Wiki — 자동 컴파일러
새로운 inbox 논문을 OpenAI API로 분석하여 wiki 페이지에 자동 반영

사용법:
  python auto_compile.py              # 전체 미컴파일 논문 처리
  python auto_compile.py --dry-run    # 실제 파일 수정 없이 계획만 출력
  python auto_compile.py --limit 10   # 최대 N편만 처리

환경변수:
  OPENAI_API_KEY  (필수)
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from openai import OpenAI

# ── 경로 설정 ────────────────────────────────────────────────────
ROOT        = Path(__file__).parent.parent
INBOX       = ROOT / "raw" / "inbox"
WIKI        = ROOT / "wiki"
LOG_FILE    = ROOT / "log.md"
INDEX_FILE  = WIKI / "index.md"
DASHBOARD   = ROOT / "DASHBOARD.md"

OPENAI_MODEL = "gpt-4o-mini"   # 빠르고 저렴한 모델 사용


# ── 헬퍼 ────────────────────────────────────────────────────────
def log(msg: str) -> None:
    entry = f"- [{datetime.now().strftime('%Y-%m-%d %H:%M')}] {msg}\n"
    print(entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def get_uncompiled() -> list[Path]:
    files = []
    for f in sorted(INBOX.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        if "compiled: false" in text:
            files.append(f)
    return files


def parse_paper_meta(path: Path) -> dict:
    """inbox 논문에서 메타데이터 추출"""
    text = path.read_text(encoding="utf-8")
    meta = {}
    for key in ("title", "authors", "journal", "publication-date", "doi", "arxiv-id", "category"):
        m = re.search(rf'^{key}:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        if m:
            meta[key] = m.group(1).strip()
    m = re.search(r'^# (.+)$', text, re.MULTILINE)
    if m:
        meta["title"] = m.group(1).strip()
    meta["filename"] = path.name
    return meta


def get_existing_wiki_pages() -> dict:
    """현재 wiki 페이지 목록 반환 {경로: 요약}"""
    pages = {}
    for f in WIKI.rglob("*.md"):
        rel = f.relative_to(WIKI)
        if rel.parts[0] in ("syntheses", "queries"):
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^summary:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        summary = m.group(1) if m else ""
        pages[str(rel).replace("\\", "/")] = summary
    return pages


def ask_llm(client: OpenAI, papers: list[dict], wiki_pages: dict) -> list[dict]:
    """OpenAI에게 논문 → wiki 페이지 매핑 요청"""

    wiki_list = "\n".join(f"- {k}: {v}" for k, v in wiki_pages.items())
    papers_text = "\n\n".join(
        f"[{i+1}] 파일명: {p['filename']}\n"
        f"    제목: {p.get('title', 'N/A')}\n"
        f"    저자: {p.get('authors', 'N/A')}\n"
        f"    학술지/카테고리: {p.get('journal', p.get('category', 'N/A'))}"
        for i, p in enumerate(papers)
    )

    prompt = f"""당신은 교육공학 연구 wiki의 자동 컴파일러입니다.

## 기존 wiki 페이지 목록
{wiki_list}

## 새로 추가된 inbox 논문들
{papers_text}

## 지시사항
각 논문을 분석하여 JSON 배열로 응답하세요. 각 항목:
{{
  "filename": "원본 파일명",
  "action": "add_to_existing" | "create_new" | "skip",
  "target_page": "기존 페이지 경로 (action=add_to_existing인 경우)",
  "new_page_slug": "새 페이지 slug (action=create_new인 경우, 영문 소문자 하이픈)",
  "new_page_type": "concept|researcher|theory|methodology|debate (create_new인 경우)",
  "new_page_title_ko": "새 페이지 한국어 제목 (create_new인 경우)",
  "new_page_summary_ko": "한국어 요약 1문장 (create_new인 경우)",
  "reason": "판단 근거 한 줄"
}}

규칙:
- editorial board, corrigendum, function art 같은 비연구 문서는 "skip"
- 기존 페이지와 주제가 겹치면 "add_to_existing"
- 완전히 새로운 주제이고 3편 이상 논문이 있을 것 같으면 "create_new"
- 단독 논문이고 기존 페이지에 포함 가능하면 "add_to_existing"

JSON만 반환하세요. 설명 없이."""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an EdTech research wiki compiler. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content.strip()
    parsed = json.loads(raw)
    # response_format=json_object 는 최상위가 객체일 수 있으므로 배열 추출
    if isinstance(parsed, list):
        return parsed
    for v in parsed.values():
        if isinstance(v, list):
            return v
    return []


def append_source_to_wiki(wiki_path: Path, inbox_filename: str) -> None:
    """기존 wiki 페이지의 소스 섹션에 논문 링크 추가"""
    text = wiki_path.read_text(encoding="utf-8")
    link = f"- [[raw/inbox/{inbox_filename}]]"

    if inbox_filename in text:
        return  # 이미 있음

    text = re.sub(
        r'(source-count:\s*)(\d+)',
        lambda m: m.group(1) + str(int(m.group(2)) + 1),
        text, count=1
    )

    if "## 소스" in text:
        text = text.rstrip() + f"\n{link}\n"
    else:
        text = text.rstrip() + f"\n\n## 소스\n\n{link}\n"

    wiki_path.write_text(text, encoding="utf-8")


def create_new_wiki_page(slug: str, page_type: str, title_ko: str,
                         summary_ko: str, inbox_filename: str) -> Path:
    """새 wiki 페이지 생성"""
    type_dir_map = {
        "concept": WIKI / "concepts",
        "researcher": WIKI / "researchers",
        "theory": WIKI / "theories",
        "methodology": WIKI / "methodologies",
        "debate": WIKI / "debates",
    }
    out_dir = type_dir_map.get(page_type, WIKI / "concepts")
    out_path = out_dir / f"{slug}.md"

    if out_path.exists():
        append_source_to_wiki(out_path, inbox_filename)
        return out_path

    date = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
type: {page_type}
summary: {summary_ko}
tags: []
created: {date}
updated: {date}
source-count: 1
language: both
---

# {title_ko}

**요약**: {summary_ko}

---

*(자동 생성 페이지 — 추가 내용 컴파일 대기)*

---

## 관련 개념


---

## 소스

- [[raw/inbox/{inbox_filename}]]
"""
    out_path.write_text(content, encoding="utf-8")
    return out_path


def mark_compiled(inbox_path: Path) -> None:
    text = inbox_path.read_text(encoding="utf-8")
    text = text.replace("compiled: false", "compiled: true", 1)
    inbox_path.write_text(text, encoding="utf-8")


def update_index_count(delta_pages: int, delta_sources: int) -> None:
    text = INDEX_FILE.read_text(encoding="utf-8")
    def inc(m):
        return m.group(1) + str(int(m.group(2)) + delta_pages)
    text = re.sub(r'(total-pages:\s*)(\d+)', inc, text, count=1)
    def inc2(m):
        return m.group(1) + str(int(m.group(2)) + delta_sources)
    text = re.sub(r'(total-sources:\s*)(\d+)', inc2, text, count=1)
    INDEX_FILE.write_text(text, encoding="utf-8")


def git_commit_and_push(new_pages: int, compiled_count: int) -> None:
    repo = ROOT
    subprocess.run(["git", "add", "-A"], cwd=repo)
    msg = (
        f"auto-compile: {compiled_count}편 처리, {new_pages}개 페이지 신규/갱신\n\n"
        f"Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
    )
    subprocess.run(["git", "commit", "-m", msg], cwd=repo)
    result = subprocess.run(["git", "push", "origin", "master"], cwd=repo)
    if result.returncode == 0:
        print("  [PUSH] GitHub 업로드 완료 → Pages 대시보드 갱신됨")
    else:
        print("  [WARN] git push 실패 — 로컬 커밋은 유지됨")


# ── 메인 ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[오류] OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
        print("  set OPENAI_API_KEY=sk-...")
        return

    client = OpenAI(api_key=api_key)

    uncompiled = get_uncompiled()[:args.limit]
    if not uncompiled:
        print("[정보] 컴파일할 논문이 없습니다.")
        return

    print(f"\n=== 자동 컴파일 시작: {len(uncompiled)}편 ===")
    log(f"[AUTO-COMPILE-START] 대상={len(uncompiled)}편")

    wiki_pages = get_existing_wiki_pages()
    papers = [parse_paper_meta(f) for f in uncompiled]

    # 배치 처리 (25편씩)
    BATCH = 25
    all_decisions = []
    for i in range(0, len(papers), BATCH):
        batch = papers[i:i+BATCH]
        print(f"  GPT 분석 중... ({i+1}~{i+len(batch)}편)")
        decisions = ask_llm(client, batch, wiki_pages)
        all_decisions.extend(decisions)

    if args.dry_run:
        print("\n[DRY-RUN] 실제 파일 수정 없음")
        for d in all_decisions:
            print(f"  {d['action']:20s} {d['filename'][:50]} → {d.get('target_page') or d.get('new_page_slug','')}")
        return

    # 실행
    compiled_count = 0
    new_pages = 0
    fname_map = {p["filename"]: uncompiled[i] for i, p in enumerate(papers)}

    for d in all_decisions:
        fname = d.get("filename", "")
        inbox_path = fname_map.get(fname)
        if not inbox_path:
            continue

        action = d.get("action", "skip")

        if action == "skip":
            mark_compiled(inbox_path)
            compiled_count += 1

        elif action == "add_to_existing":
            target = d.get("target_page", "")
            wiki_path = WIKI / target.replace("/", os.sep)
            if wiki_path.exists():
                append_source_to_wiki(wiki_path, fname)
                mark_compiled(inbox_path)
                compiled_count += 1
                print(f"  [ADD] {fname[:45]} → {target}")
            else:
                print(f"  [WARN] 페이지 없음: {target}")

        elif action == "create_new":
            slug = d.get("new_page_slug", "")
            if slug:
                create_new_wiki_page(
                    slug,
                    d.get("new_page_type", "concept"),
                    d.get("new_page_title_ko", slug),
                    d.get("new_page_summary_ko", ""),
                    fname
                )
                wiki_pages[f"{d.get('new_page_type','concepts')}/{slug}.md"] = d.get("new_page_summary_ko", "")
                mark_compiled(inbox_path)
                compiled_count += 1
                new_pages += 1
                print(f"  [NEW] {fname[:45]} → {slug}")

    # 인덱스 갱신 + 커밋
    if new_pages > 0:
        update_index_count(new_pages, 0)

    git_commit_and_push(new_pages, compiled_count)
    log(f"[AUTO-COMPILE-DONE] 처리={compiled_count}편, 신규페이지={new_pages}개")
    print(f"\n=== 완료: {compiled_count}편 처리, {new_pages}개 신규 페이지 ===")

    # 대시보드 재생성 후 push
    dashboard_script = ROOT / "scripts" / "generate_dashboard.py"
    if dashboard_script.exists():
        subprocess.run([sys.executable, str(dashboard_script)], cwd=ROOT)
        subprocess.run(["git", "add", "dashboard.html"], cwd=ROOT)
        subprocess.run(["git", "commit", "-m", "chore: dashboard.html 갱신"], cwd=ROOT)
        subprocess.run(["git", "push", "origin", "master"], cwd=ROOT)


if __name__ == "__main__":
    main()
