#!/usr/bin/env python3
"""
EdTech Research Wiki — 확장 대시보드 생성기
브라우저로 바로 열 수 있는 정적 HTML 생성

포함 섹션:
  1. 통계 카드 (gap 토픽 포함)
  2. 논문 발행 타임라인 + 연구 공백 패널
  3. 유형 분포 도넛 + 토픽 성숙도 스캐터
  4. 개념 네트워크 (D3.js force graph)
  5. 연구자 × 개념 커버리지 히트맵
  6. 저널 분포 + Debate 트래커
  7. 자동 연구 질문 (OpenAI, 7일 캐시)
  8. 전체 페이지 테이블
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
WIKI = ROOT / "wiki"
LOG_FILE = ROOT / "log.md"
OUTPUT = ROOT / "dashboard.html"
INBOX = ROOT / "raw" / "inbox"
QUESTIONS_CACHE = Path(__file__).parent / ".research_questions.json"

SKIP_DIRS = {"syntheses", "queries"}
SKIP_FILES = {"index.md", "index-dynamic.md"}

TYPE_LABEL = {"concept": "개념", "researcher": "연구자", "theory": "이론",
              "methodology": "방법론", "debate": "논쟁", "other": "기타"}
TYPE_COLOR = {"concept": "#6366f1", "researcher": "#10b981", "theory": "#f59e0b",
              "methodology": "#3b82f6", "debate": "#ef4444", "other": "#8b5cf6"}


# ── 데이터 수집 ──────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    meta = {}
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return meta
    for line in m.group(1).splitlines():
        kv = re.match(r'^([\w-]+):\s*"?([^"#\n]*)"?', line)
        if kv:
            meta[kv.group(1)] = kv.group(2).strip()
    return meta


def get_wiki_pages() -> list:
    pages = []
    for f in sorted(WIKI.rglob("*.md")):
        rel = f.relative_to(WIKI)
        if rel.parts[0] in SKIP_DIRS or f.name in SKIP_FILES:
            continue
        text = f.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        h1 = re.search(r"^# (.+)$", text, re.MULTILINE)
        title = h1.group(1) if h1 else f.stem
        links = re.findall(r'\[\[([^\]|]+)', text)
        wiki_links = [l for l in links if "raw/inbox" not in l]
        pages.append({
            "path": str(rel).replace("\\", "/"),
            "slug": f.stem,
            "type": meta.get("type", rel.parts[0] if len(rel.parts) > 1 else "other"),
            "title": title,
            "summary": meta.get("summary", ""),
            "source_count": int(meta.get("source-count", 0) or 0),
            "created": meta.get("created", ""),
            "updated": meta.get("updated", ""),
            "link_count": len(wiki_links),
            "raw_text": text,
        })
    return pages


def get_network_data(pages: list) -> tuple:
    id_map = {}
    for i, p in enumerate(pages):
        slug_path = p["path"].replace(".md", "")
        id_map[slug_path] = i
        id_map[p["slug"]] = i

    nodes = [{"id": i, "label": p["title"], "type": p["type"],
               "source_count": p["source_count"], "path": p["path"]}
             for i, p in enumerate(pages)]

    edges = []
    edge_set = set()
    for src_i, p in enumerate(pages):
        links = re.findall(r'\[\[([^\]|]+)', p["raw_text"])
        for link in links:
            if "raw/inbox" in link:
                continue
            link_clean = link.strip().rstrip("/")
            tgt_i = id_map.get(link_clean) or id_map.get(link_clean.split("/")[-1])
            if tgt_i is None or tgt_i == src_i:
                continue
            key = (min(src_i, tgt_i), max(src_i, tgt_i))
            if key not in edge_set:
                edge_set.add(key)
                edges.append({"source": key[0], "target": key[1]})
    return nodes, edges


def get_heatmap_data(pages: list) -> dict:
    researchers = [p for p in pages if p["type"] == "researcher"]
    concepts = [p for p in pages if p["type"] in ("concept", "theory", "methodology", "debate")]
    if not researchers or not concepts:
        return {"researchers": [], "concepts": [], "matrix": []}

    concept_idx = {c["slug"]: i for i, c in enumerate(concepts)}
    matrix = [[0] * len(concepts) for _ in range(len(researchers))]

    for r_i, r in enumerate(researchers):
        links = re.findall(r'\[\[([^\]|]+)', r["raw_text"])
        for link in links:
            if "raw/inbox" in link:
                continue
            slug = link.strip().split("/")[-1]
            c_i = concept_idx.get(slug)
            if c_i is not None:
                matrix[r_i][c_i] = 1
    return {
        "researchers": [r["title"] for r in researchers],
        "concepts": [c["title"] for c in concepts],
        "matrix": matrix,
    }


def get_pub_timeline() -> list:
    counts = defaultdict(int)
    for f in INBOX.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^publication-date:\s*"?(\d{4}-\d{2})', text, re.MULTILINE)
        if m:
            counts[m.group(1)] += 1
    return [{"month": k, "count": v} for k, v in sorted(counts.items())]


def get_journal_distribution() -> list:
    counts = defaultdict(int)
    for f in INBOX.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^journal:\s*"?([^"#\n]+)"?', text, re.MULTILINE)
        if m:
            j = m.group(1).strip()[:45]
            counts[j] += 1
    return [{"name": k, "count": v}
            for k, v in sorted(counts.items(), key=lambda x: -x[1])[:10]]


def get_source_distribution() -> dict:
    counts = defaultdict(int)
    for f in INBOX.glob("*.md"):
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^source:\s*"?(\S+)"?', text, re.MULTILINE)
        if m:
            counts[m.group(1)] += 1
    return dict(counts)


def get_debate_info(pages: list) -> list:
    debates = []
    for p in pages:
        if p["type"] != "debate":
            continue
        text = p["raw_text"]
        # 첫 본문 단락 추출
        body = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL).strip()
        body = re.sub(r'^# .+$', '', body, flags=re.MULTILINE).strip()
        first_para = ""
        for line in body.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-") and not line.startswith("*"):
                first_para = line[:200]
                break
        debates.append({
            "title": p["title"],
            "summary": p["summary"],
            "source_count": p["source_count"],
            "snippet": first_para,
        })
    return debates


def get_research_questions(pages: list, gap_pages: list, journals: list) -> list:
    """OpenAI API로 연구 질문 생성 (7일 캐시)"""
    # 캐시 확인
    if QUESTIONS_CACHE.exists():
        try:
            cache = json.loads(QUESTIONS_CACHE.read_text(encoding="utf-8"))
            cached_at = datetime.fromisoformat(cache.get("generated_at", "2000-01-01"))
            if datetime.now() - cached_at < timedelta(days=7):
                return cache.get("questions", [])
        except Exception:
            pass

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return []

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        top_pages = sorted(pages, key=lambda p: -p["source_count"])[:8]
        top_info = ", ".join(f"{p['title']}({p['source_count']}편)" for p in top_pages)
        gap_info = ", ".join(p["title"] for p in gap_pages[:6])
        journal_info = ", ".join(j["name"] for j in journals[:5])
        debates_info = ", ".join(p["title"] for p in pages if p["type"] == "debate")

        prompt = f"""당신은 교육공학 연구 전문가입니다. 아래 연구 Wiki 현황을 분석하여 연구 질문을 제안하세요.

## Wiki 현황
- 주요 토픽 (소스 수 기준): {top_info}
- 연구 공백 (소스 부족): {gap_info}
- 현재 논쟁 중인 주제: {debates_info if debates_info else '없음'}
- 주요 학술지: {journal_info}

## 요청
위 현황을 바탕으로 5개의 구체적이고 실현 가능한 연구 질문을 생성하세요.
각 질문은:
1. 연구 공백을 채우거나 성숙한 토픽을 확장하는 것
2. 혼합 방법론(정량+정성) 적용 가능한 것
3. 위 학술지에 게재 가능한 수준의 것

JSON 배열로만 반환: ["질문1", "질문2", "질문3", "질문4", "질문5"]"""

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=1024,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Return a JSON object with key 'questions' containing an array of 5 research question strings in Korean."},
                {"role": "user", "content": prompt}
            ]
        )
        raw = json.loads(resp.choices[0].message.content)
        questions = raw.get("questions", [])
        if isinstance(questions, list) and questions:
            QUESTIONS_CACHE.write_text(json.dumps({
                "generated_at": datetime.now().isoformat(),
                "questions": questions
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            return questions
    except Exception as e:
        print(f"  [연구 질문 생성 실패] {e}")
    return []


def get_recent_log(n: int = 12) -> list:
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    entries = [l.strip() for l in lines if l.strip().startswith("- [")]
    return entries[-n:][::-1]


def get_inbox_stats() -> dict:
    if not INBOX.exists():
        return {"total": 0, "compiled": 0, "uncompiled": 0}
    total = compiled = 0
    for f in INBOX.glob("*.md"):
        total += 1
        if "compiled: true" in f.read_text(encoding="utf-8"):
            compiled += 1
    return {"total": total, "compiled": compiled, "uncompiled": total - compiled}


# ── HTML 생성 ────────────────────────────────────────────────────

def build_html(pages, nodes, edges, heatmap, timeline, journals,
               src_dist, debates, questions, log_entries, inbox) -> str:

    type_counts = defaultdict(int)
    for p in pages:
        type_counts[p["type"]] += 1

    total_pages = len(pages)
    total_sources = sum(p["source_count"] for p in pages)
    gap_pages = [p for p in pages if p["source_count"] <= 2]

    pages_clean = [{k: v for k, v in p.items() if k != "raw_text"} for p in pages]
    pages_sorted = sorted(pages_clean, key=lambda p: -p["source_count"])

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── 데이터 JSON 직렬화 ────────────────────────────────────────
    j_nodes  = json.dumps(nodes, ensure_ascii=False)
    j_edges  = json.dumps(edges, ensure_ascii=False)
    j_heat   = json.dumps(heatmap, ensure_ascii=False)
    j_tl     = json.dumps(timeline, ensure_ascii=False)
    j_jnl    = json.dumps(journals, ensure_ascii=False)
    j_src    = json.dumps(src_dist, ensure_ascii=False)
    j_types  = json.dumps(dict(type_counts), ensure_ascii=False)
    j_top15  = json.dumps([{"title": p["title"][:22], "count": p["source_count"],
                             "type": p["type"]} for p in pages_sorted[:15]], ensure_ascii=False)
    j_scatter= json.dumps([{"title": p["title"][:20], "x": p["source_count"],
                             "y": p["link_count"], "type": p["type"]}
                            for p in pages_clean], ensure_ascii=False)
    j_gap    = json.dumps([{"title": p["title"], "type": p["type"],
                             "source_count": p["source_count"]}
                            for p in gap_pages], ensure_ascii=False)

    type_labels = json.dumps([TYPE_LABEL.get(k, k) for k in type_counts])
    type_colors = json.dumps([TYPE_COLOR.get(k, "#94a3b8") for k in type_counts])
    type_data   = json.dumps(list(type_counts.values()))

    # ── 연구 공백 HTML ────────────────────────────────────────────
    gap_html = ""
    for g in gap_pages:
        badge_color = TYPE_COLOR.get(g["type"], "#94a3b8")
        label = TYPE_LABEL.get(g["type"], g["type"])
        dots = "●" * g["source_count"] + "○" * (3 - g["source_count"])
        gap_html += f"""<div class="gap-item">
          <span class="badge sm" style="background:{badge_color}">{label}</span>
          <span class="gap-title">{g['title']}</span>
          <span class="gap-dots" title="{g['source_count']}편">{dots}</span>
        </div>"""

    # ── 연구 질문 HTML ────────────────────────────────────────────
    q_html = ""
    if questions:
        for i, q in enumerate(questions, 1):
            q_html += f'<div class="q-item"><span class="q-num">Q{i}</span><span class="q-text">{q}</span></div>'
    else:
        q_html = '<p class="muted small">OPENAI_API_KEY 설정 시 자동 생성됩니다.</p>'

    # ── Debate HTML ───────────────────────────────────────────────
    db_html = ""
    for d in debates:
        db_html += f"""<div class="debate-item">
          <div class="debate-title">{d['title']}</div>
          <div class="debate-summary muted small">{d['summary']}</div>
          <div class="debate-count small">소스 {d['source_count']}편</div>
        </div>"""
    if not db_html:
        db_html = '<p class="muted small">Debate 페이지 없음</p>'

    # ── 로그 HTML ─────────────────────────────────────────────────
    log_html = ""
    TAG_C = {"AUTO-COMPILE-START": "#6366f1", "AUTO-COMPILE-DONE": "#10b981",
             "COLLECT": "#3b82f6", "FIX": "#ef4444", "IMPROVE": "#f59e0b",
             "TEST": "#8b5cf6", "HWPX-INGEST-DONE": "#10b981"}
    for entry in log_entries:
        dm = re.match(r"- \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)", entry)
        date_str, msg = (dm.group(1), dm.group(2)) if dm else ("", entry.lstrip("- "))
        tag_m = re.match(r"\[([A-Z\-]+)\] (.+)", msg)
        if tag_m:
            tag, rest = tag_m.group(1), tag_m.group(2)
            tc = TAG_C.get(tag, "#64748b")
            log_html += f'<div class="log-entry"><span class="log-tag" style="background:{tc}">{tag}</span><span class="log-msg">{rest[:70]}</span><span class="log-date">{date_str}</span></div>'
        else:
            log_html += f'<div class="log-entry"><span class="log-msg">{msg[:80]}</span><span class="log-date">{date_str}</span></div>'

    # ── 페이지 테이블 HTML ────────────────────────────────────────
    rows_html = ""
    for p in pages_sorted:
        bc = TYPE_COLOR.get(p["type"], "#8b5cf6")
        lb = TYPE_LABEL.get(p["type"], p["type"])
        maturity = "🟢 성숙" if p["source_count"] >= 5 else "🟡 성장" if p["source_count"] >= 3 else "🔴 공백"
        rows_html += f"""<tr>
          <td class="py-2 px-3"><span class="badge" style="background:{bc}">{lb}</span></td>
          <td class="py-2 px-3 fw500">{p['title']}</td>
          <td class="py-2 px-3 muted small ellipsis" style="max-width:260px">{p['summary']}</td>
          <td class="py-2 px-3 center"><span class="src-badge">{p['source_count']}</span></td>
          <td class="py-2 px-3 center small">{p['link_count']}</td>
          <td class="py-2 px-3 center small">{maturity}</td>
          <td class="py-2 px-3 muted small">{p['updated'] or p['created']}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EdTech Research Wiki — Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<style>
:root{{--bg:#0f172a;--surf:#1e293b;--surf2:#273548;--bdr:#334155;--txt:#f1f5f9;--muted:#94a3b8;--accent:#6366f1}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--txt);font-family:'Segoe UI',system-ui,sans-serif;font-size:13px;line-height:1.6}}
.container{{max-width:1400px;margin:0 auto;padding:20px}}
.hdr{{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px;padding-bottom:14px;border-bottom:1px solid var(--bdr)}}
.hdr h1{{font-size:18px;font-weight:700}} .hdr h1 span{{color:var(--accent)}}
.muted{{color:var(--muted)}} .small{{font-size:11px}} .fw500{{font-weight:500}} .center{{text-align:center}}
.ellipsis{{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}

/* Cards */
.stats-grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:20px}}
.card{{background:var(--surf);border:1px solid var(--bdr);border-radius:10px;padding:14px}}
.card-title{{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px;font-weight:600}}
.stat-card .lbl{{font-size:10px;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin-bottom:4px}}
.stat-card .val{{font-size:28px;font-weight:700}}
.stat-card .sub{{font-size:11px;color:var(--muted);margin-top:2px}}
.prog-bar{{background:#334155;border-radius:99px;height:5px;margin:6px 0 2px}}
.prog-fill{{height:5px;border-radius:99px;background:#10b981}}
.badge{{display:inline-block;padding:2px 6px;border-radius:99px;font-size:10px;font-weight:600;color:#fff}}
.badge.sm{{font-size:9px;padding:1px 5px}}
.src-badge{{background:#1e3a5f;color:#60a5fa;padding:1px 7px;border-radius:99px;font-size:12px;font-weight:600;display:inline-block}}

/* Grid layouts */
.row2{{display:grid;gap:14px;margin-bottom:14px}}
.row2.c2{{grid-template-columns:1fr 1fr}}
.row2.c3{{grid-template-columns:1fr 1fr 1fr}}
.row2.c13{{grid-template-columns:1fr 3fr}}
.row2.c31{{grid-template-columns:3fr 1fr}}
.row2.c23{{grid-template-columns:2fr 3fr}}

/* Charts */
.chart-wrap{{position:relative;height:220px}}
.chart-wrap.tall{{height:280px}}
.chart-wrap.sm{{height:180px}}

/* Gap panel */
.gap-item{{display:flex;align-items:center;gap:6px;padding:5px 0;border-bottom:1px solid #1e293b}}
.gap-item:last-child{{border-bottom:none}}
.gap-title{{flex:1;font-size:12px}}
.gap-dots{{color:#f59e0b;font-size:10px;letter-spacing:1px}}

/* Network */
#network{{width:100%;height:420px;background:var(--surf2);border-radius:8px;overflow:hidden}}
.node-tooltip{{position:absolute;background:#1e293b;border:1px solid #334155;border-radius:6px;padding:6px 10px;font-size:12px;pointer-events:none;display:none;z-index:100}}

/* Heatmap */
.heatmap-scroll{{overflow-x:auto;max-height:320px;overflow-y:auto}}
.heatmap-table{{border-collapse:collapse;font-size:10px}}
.heatmap-table th{{padding:3px 6px;text-align:center;white-space:nowrap;color:var(--muted);font-weight:500;position:sticky;top:0;background:var(--surf);z-index:10}}
.heatmap-table th.row-hdr{{left:0;text-align:right;padding-right:8px;background:var(--surf)}}
.heatmap-table td{{width:22px;height:22px;text-align:center}}
.heatmap-table td.rn{{white-space:nowrap;padding-right:8px;text-align:right;color:var(--muted);font-size:11px;position:sticky;left:0;background:var(--surf)}}
.hm-cell{{width:16px;height:16px;border-radius:3px;margin:auto}}

/* Debate */
.debate-item{{padding:8px 0;border-bottom:1px solid #1e293b}}
.debate-item:last-child{{border-bottom:none}}
.debate-title{{font-weight:600;font-size:13px;margin-bottom:3px}}
.debate-summary{{margin-bottom:2px}}
.debate-count{{color:#60a5fa}}

/* Research questions */
.q-item{{display:flex;gap:10px;padding:8px 0;border-bottom:1px solid #1e293b;align-items:flex-start}}
.q-item:last-child{{border-bottom:none}}
.q-num{{flex-shrink:0;background:var(--accent);color:#fff;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;margin-top:2px}}
.q-text{{font-size:13px;line-height:1.5}}

/* Log */
.log-entry{{display:flex;align-items:baseline;gap:7px;padding:6px 0;border-bottom:1px solid #1e293b}}
.log-entry:last-child{{border-bottom:none}}
.log-tag{{flex-shrink:0;padding:1px 5px;border-radius:4px;font-size:9px;font-weight:700;color:#fff}}
.log-msg{{flex:1;color:var(--txt);font-size:12px}}
.log-date{{flex-shrink:0;font-size:10px;color:var(--muted)}}

/* Table */
.tbl-wrap{{overflow-x:auto}}
table{{width:100%;border-collapse:collapse}}
thead th{{font-size:10px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;padding:7px 12px;text-align:left;border-bottom:1px solid var(--bdr)}}
tbody tr{{border-bottom:1px solid #1e293b;transition:background .15s}}
tbody tr:hover{{background:#ffffff06}}
td{{vertical-align:middle}}
.collapsible{{cursor:pointer;user-select:none}}
.collapsible:after{{content:" ▾";font-size:10px;color:var(--muted)}}
.collapsed .collapsible:after{{content:" ▸"}}
.collapse-body{{transition:max-height .3s ease}}

@media(max-width:1100px){{
  .stats-grid{{grid-template-columns:repeat(3,1fr)}}
  .row2.c3,.row2.c2,.row2.c13,.row2.c31,.row2.c23{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="hdr">
  <h1>EdTech Research Wiki <span>Dashboard</span></h1>
  <span class="muted small">갱신: {now}</span>
</div>

<!-- Stats Cards -->
<div class="stats-grid">
  <div class="card stat-card">
    <div class="lbl">Wiki 페이지</div>
    <div class="val" style="color:#6366f1">{total_pages}</div>
  </div>
  <div class="card stat-card">
    <div class="lbl">총 소스</div>
    <div class="val" style="color:#10b981">{total_sources}</div>
  </div>
  <div class="card stat-card">
    <div class="lbl">개념 페이지</div>
    <div class="val" style="color:#3b82f6">{type_counts.get('concept',0)}</div>
  </div>
  <div class="card stat-card">
    <div class="lbl">연구자</div>
    <div class="val" style="color:#f59e0b">{type_counts.get('researcher',0)}</div>
  </div>
  <div class="card stat-card">
    <div class="lbl">논쟁/Debate</div>
    <div class="val" style="color:#ef4444">{type_counts.get('debate',0)}</div>
  </div>
  <div class="card stat-card">
    <div class="lbl">연구 공백</div>
    <div class="val" style="color:#f59e0b">{len(gap_pages)}</div>
    <div class="sub">소스 ≤ 2편</div>
    <div class="prog-bar"><div class="prog-fill" style="width:{int(inbox['compiled']/(inbox['total'] or 1)*100)}%;background:#f59e0b"></div></div>
    <div class="sub">inbox {inbox['compiled']}/{inbox['total']}</div>
  </div>
</div>

<!-- Row: Timeline + Gap -->
<div class="row2 c23">
  <div class="card">
    <div class="card-title">논문 발행 타임라인 (publication-date 기준)</div>
    <div class="chart-wrap"><canvas id="timelineChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-title">🔴 연구 공백 토픽 (소스 ≤ 2편)</div>
    {gap_html}
  </div>
</div>

<!-- Row: Donut + Scatter + Bar -->
<div class="row2 c3">
  <div class="card">
    <div class="card-title">페이지 유형 분포</div>
    <div class="chart-wrap sm"><canvas id="donutChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-title">토픽 성숙도 (소스 수 × 연결 수)</div>
    <div class="chart-wrap sm"><canvas id="scatterChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-title">소스 수 상위 15 페이지</div>
    <div class="chart-wrap sm"><canvas id="barChart"></canvas></div>
  </div>
</div>

<!-- Concept Network -->
<div class="card" style="margin-bottom:14px">
  <div class="card-title">개념 연결망 — 드래그·줌 가능 | 노드 크기 = 소스 수</div>
  <div id="network"></div>
  <div class="node-tooltip" id="tooltip"></div>
</div>

<!-- Row: Heatmap + Log -->
<div class="row2 c2" style="margin-bottom:14px">
  <div class="card">
    <div class="card-title">연구자 × 개념 커버리지 히트맵</div>
    <div class="heatmap-scroll">
      <table class="heatmap-table" id="heatmapTable"></table>
    </div>
  </div>
  <div class="card">
    <div class="card-title">최근 활동 로그</div>
    {log_html}
  </div>
</div>

<!-- Row: Journals + Source dist + Debates -->
<div class="row2 c3" style="margin-bottom:14px">
  <div class="card">
    <div class="card-title">저널 분포 (상위 10)</div>
    <div class="chart-wrap"><canvas id="journalChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-title">수집 소스 분포</div>
    <div class="chart-wrap"><canvas id="srcChart"></canvas></div>
  </div>
  <div class="card">
    <div class="card-title">💬 Debate 트래커</div>
    {db_html}
  </div>
</div>

<!-- Research Questions -->
<div class="card" style="margin-bottom:14px">
  <div class="card-title">🤖 자동 연구 질문 제안 (GPT-4o-mini, 7일 캐시)</div>
  {q_html}
</div>

<!-- Table -->
<div class="card" id="tableSection" class="collapsed">
  <div class="card-title collapsible" onclick="toggleTable()">전체 Wiki 페이지 목록</div>
  <div id="tableBody" style="display:none;margin-top:12px">
    <div class="tbl-wrap">
      <table>
        <thead><tr>
          <th>유형</th><th>제목</th><th>요약</th>
          <th class="center">소스</th><th class="center">링크</th>
          <th class="center">성숙도</th><th>갱신일</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>
</div>

</div><!-- /container -->

<script>
// ── 데이터 ───────────────────────────────────────────────────────
const NODES   = {j_nodes};
const EDGES   = {j_edges};
const HEATMAP = {j_heat};
const TIMELINE= {j_tl};
const JOURNALS= {j_jnl};
const SRC_DIST= {j_src};
const TYPE_COUNTS = {j_types};
const TOP15   = {j_top15};
const SCATTER = {j_scatter};
const GAP     = {j_gap};

const TYPE_COLOR = {json.dumps(TYPE_COLOR)};
const TYPE_LABEL = {json.dumps(TYPE_LABEL)};

// ── Helpers ──────────────────────────────────────────────────────
const C = (id) => document.getElementById(id).getContext('2d');
const darkGrid = {{ color: '#1e293b' }};
const tickStyle = {{ color: '#94a3b8', font: {{ size: 10 }} }};

// ── 1. Timeline ──────────────────────────────────────────────────
new Chart(C('timelineChart'), {{
  type: 'line',
  data: {{
    labels: TIMELINE.map(d => d.month),
    datasets: [{{ label: '논문 수', data: TIMELINE.map(d => d.count),
      borderColor: '#6366f1', backgroundColor: '#6366f120',
      fill: true, tension: 0.3, pointRadius: 3 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ ...tickStyle, maxTicksLimit: 12 }}, grid: darkGrid }},
      y: {{ ticks: tickStyle, grid: darkGrid }}
    }}
  }}
}});

// ── 2. Donut ─────────────────────────────────────────────────────
const typeLabels = {type_labels};
const typeData   = {type_data};
const typeColors = {type_colors};
new Chart(C('donutChart'), {{
  type: 'doughnut',
  data: {{ labels: typeLabels, datasets: [{{ data: typeData,
    backgroundColor: typeColors, borderWidth: 2, borderColor: '#0f172a' }}] }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'bottom', labels: {{
      color: '#94a3b8', font: {{ size: 10 }}, padding: 8, boxWidth: 8
    }} }} }}
  }}
}});

// ── 3. Scatter ───────────────────────────────────────────────────
new Chart(C('scatterChart'), {{
  type: 'scatter',
  data: {{
    datasets: Object.keys(TYPE_COLOR).map(t => ({{
      label: TYPE_LABEL[t] || t,
      data: SCATTER.filter(p => p.type === t).map(p => ({{ x: p.x, y: p.y, title: p.title }})),
      backgroundColor: TYPE_COLOR[t] + 'cc', pointRadius: 6
    }}))
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ labels: {{ color: '#94a3b8', font: {{ size: 10 }}, boxWidth: 8 }} }},
      tooltip: {{ callbacks: {{ label: ctx => `${{ctx.raw.title}} (소스:${{ctx.raw.x}}, 링크:${{ctx.raw.y}})` }} }}
    }},
    scales: {{
      x: {{ title: {{ display: true, text: '소스 수', color: '#64748b', font: {{ size: 10 }} }},
           ticks: tickStyle, grid: darkGrid }},
      y: {{ title: {{ display: true, text: '연결 수', color: '#64748b', font: {{ size: 10 }} }},
           ticks: tickStyle, grid: darkGrid }}
    }}
  }}
}});

// ── 4. Bar (top 15) ──────────────────────────────────────────────
new Chart(C('barChart'), {{
  type: 'bar',
  data: {{
    labels: TOP15.map(p => p.title),
    datasets: [{{ data: TOP15.map(p => p.count),
      backgroundColor: TOP15.map(p => TYPE_COLOR[p.type] || '#8b5cf6'),
      borderRadius: 3 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false, indexAxis: 'y',
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: tickStyle, grid: darkGrid }},
      y: {{ ticks: {{ ...tickStyle, font: {{ size: 10 }} }}, grid: {{ display: false }} }}
    }}
  }}
}});

// ── 5. D3 Network ────────────────────────────────────────────────
(function() {{
  const el = document.getElementById('network');
  const W = el.clientWidth, H = el.clientHeight || 420;
  const svg = d3.select('#network').append('svg').attr('width', W).attr('height', H);
  const g = svg.append('g');
  svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', e => g.attr('transform', e.transform)));

  const nodesD = NODES.map(d => ({{ ...d }}));
  const edgesD = EDGES.map(d => ({{ ...d }}));

  const sim = d3.forceSimulation(nodesD)
    .force('link', d3.forceLink(edgesD).id(d => d.id).distance(80))
    .force('charge', d3.forceManyBody().strength(-120))
    .force('center', d3.forceCenter(W/2, H/2))
    .force('collision', d3.forceCollide(18));

  const link = g.append('g').selectAll('line').data(edgesD).join('line')
    .attr('stroke', '#334155').attr('stroke-width', 1.2).attr('stroke-opacity', 0.7);

  const node = g.append('g').selectAll('circle').data(nodesD).join('circle')
    .attr('r', d => Math.max(6, Math.min(18, 5 + d.source_count * 1.2)))
    .attr('fill', d => TYPE_COLOR[d.type] || '#8b5cf6')
    .attr('stroke', '#0f172a').attr('stroke-width', 1.5)
    .style('cursor', 'pointer')
    .call(d3.drag()
      .on('start', (e, d) => {{ if (!e.active) sim.alphaTarget(0.3).restart(); d.fx=d.x; d.fy=d.y; }})
      .on('drag',  (e, d) => {{ d.fx=e.x; d.fy=e.y; }})
      .on('end',   (e, d) => {{ if (!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }}));

  const tooltip = document.getElementById('tooltip');
  node.on('mouseover', (e, d) => {{
    tooltip.style.display = 'block';
    tooltip.style.left = (e.pageX + 10) + 'px';
    tooltip.style.top  = (e.pageY - 20) + 'px';
    tooltip.innerHTML = `<b>${{d.label}}</b><br><span style="color:#94a3b8">${{TYPE_LABEL[d.type]||d.type}} · 소스 ${{d.source_count}}편</span>`;
  }}).on('mousemove', e => {{
    tooltip.style.left = (e.pageX + 10) + 'px';
    tooltip.style.top  = (e.pageY - 20) + 'px';
  }}).on('mouseout', () => {{ tooltip.style.display = 'none'; }});

  const label = g.append('g').selectAll('text').data(nodesD).join('text')
    .text(d => d.label.length > 12 ? d.label.slice(0,12)+'…' : d.label)
    .attr('font-size', 9).attr('fill', '#cbd5e1').attr('dy', d => -Math.max(6, Math.min(18, 5 + d.source_count*1.2)) - 3)
    .attr('text-anchor', 'middle').style('pointer-events', 'none');

  sim.on('tick', () => {{
    link.attr('x1', d=>d.source.x).attr('y1', d=>d.source.y)
        .attr('x2', d=>d.target.x).attr('y2', d=>d.target.y);
    node.attr('cx', d=>d.x).attr('cy', d=>d.y);
    label.attr('x', d=>d.x).attr('y', d=>d.y);
  }});
}})();

// ── 6. Heatmap ───────────────────────────────────────────────────
(function() {{
  const {{ researchers, concepts, matrix }} = HEATMAP;
  if (!researchers.length) return;
  const tbl = document.getElementById('heatmapTable');
  // Header row
  let hdr = '<tr><th class="row-hdr">연구자 \\ 개념</th>';
  concepts.forEach(c => {{ hdr += `<th title="${{c}}">${{c.slice(0,8)}}</th>`; }});
  hdr += '</tr>';
  tbl.innerHTML = hdr;
  // Data rows
  researchers.forEach((r, ri) => {{
    let row = `<tr><td class="rn">${{r}}</td>`;
    matrix[ri].forEach(val => {{
      const bg = val ? '#6366f1' : '#1e293b';
      row += `<td><div class="hm-cell" style="background:${{bg}}" title="${{val?'있음':'없음'}}"></div></td>`;
    }});
    row += '</tr>';
    tbl.innerHTML += row;
  }});
}})();

// ── 7. Journals ──────────────────────────────────────────────────
new Chart(C('journalChart'), {{
  type: 'bar',
  data: {{
    labels: JOURNALS.map(j => j.name.slice(0,28)),
    datasets: [{{ data: JOURNALS.map(j => j.count),
      backgroundColor: '#3b82f6cc', borderRadius: 3 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false, indexAxis: 'y',
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: tickStyle, grid: darkGrid }},
      y: {{ ticks: {{ ...tickStyle, font: {{ size: 9 }} }}, grid: {{ display: false }} }}
    }}
  }}
}});

// ── 8. Source distribution ───────────────────────────────────────
const srcKeys = Object.keys(SRC_DIST);
const srcVals = Object.values(SRC_DIST);
new Chart(C('srcChart'), {{
  type: 'doughnut',
  data: {{
    labels: srcKeys,
    datasets: [{{ data: srcVals,
      backgroundColor: ['#6366f1','#10b981','#f59e0b','#3b82f6'],
      borderWidth: 2, borderColor: '#0f172a' }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'bottom', labels: {{
      color: '#94a3b8', font: {{ size: 11 }}, padding: 10, boxWidth: 10
    }} }} }}
  }}
}});

// ── Table toggle ─────────────────────────────────────────────────
function toggleTable() {{
  const body = document.getElementById('tableBody');
  body.style.display = body.style.display === 'none' ? 'block' : 'none';
}}
</script>
</body>
</html>
"""


# ── 메인 ────────────────────────────────────────────────────────
def main():
    print("확장 대시보드 생성 중...")
    pages       = get_wiki_pages()
    nodes, edges = get_network_data(pages)
    heatmap     = get_heatmap_data(pages)
    timeline    = get_pub_timeline()
    journals    = get_journal_distribution()
    src_dist    = get_source_distribution()
    debates     = get_debate_info(pages)
    log_entries = get_recent_log(12)
    inbox       = get_inbox_stats()

    gap_pages   = [p for p in pages if p["source_count"] <= 2]
    questions   = get_research_questions(pages, gap_pages, journals)

    html = build_html(pages, nodes, edges, heatmap, timeline, journals,
                      src_dist, debates, questions, log_entries, inbox)
    OUTPUT.write_text(html, encoding="utf-8")

    print(f"완료: {OUTPUT}")
    print(f"  페이지 {len(pages)}개 | 소스 {sum(p['source_count'] for p in pages)}편")
    print(f"  네트워크 노드 {len(nodes)}개 엣지 {len(edges)}개")
    print(f"  연구 공백 {len(gap_pages)}개 | 연구 질문 {len(questions)}개")


if __name__ == "__main__":
    main()
