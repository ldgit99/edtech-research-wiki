#!/usr/bin/env python3
"""
EdTech Research Wiki — 연구 동향 보고서 생성기
GPT-4o-mini로 수집된 논문을 분석하여 보고서 HTML 생성

사용법: python generate_report.py
출력:   ../report.html
캐시:   .report_cache.json (7일)
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

ROOT   = Path(__file__).parent.parent
INBOX  = ROOT / "raw" / "inbox"
WIKI   = ROOT / "wiki"
OUTPUT = ROOT / "report.html"
CACHE  = Path(__file__).parent / ".report_cache.json"


# ── 데이터 수집 ──────────────────────────────────────────────────

def collect_papers() -> list:
    papers = []
    for f in sorted(INBOX.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        def get(key):
            m = re.search(rf'^{key}:\s*"?([^"\n]+)"?', text, re.MULTILINE)
            return m.group(1).strip() if m else ""
        h1 = re.search(r'^# (.+)$', text, re.MULTILINE)
        title = h1.group(1).strip() if h1 else f.stem
        papers.append({
            "title":   title[:100],
            "journal": get("journal")[:50],
            "date":    get("publication-date")[:7],
            "authors": get("authors")[:60],
            "source":  get("source"),
        })
    return papers


def collect_wiki_topics() -> list:
    topics = []
    skip = {"syntheses", "queries"}
    skip_files = {"index.md", "index-dynamic.md"}
    for f in sorted(WIKI.rglob("*.md")):
        rel = f.relative_to(WIKI)
        if rel.parts[0] in skip or f.name in skip_files:
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^summary:\s*"?([^"\n]+)"?', text, re.MULTILINE)
        summary = m.group(1) if m else ""
        sc = re.search(r'^source-count:\s*(\d+)', text, re.MULTILINE)
        tp = re.search(r'^type:\s*(\S+)', text, re.MULTILINE)
        h1 = re.search(r'^# (.+)$', text, re.MULTILINE)
        title = h1.group(1).strip() if h1 else f.stem
        topics.append({
            "title":        title,
            "type":         tp.group(1) if tp else "concept",
            "source_count": int(sc.group(1)) if sc else 0,
            "summary":      summary[:80],
        })
    return sorted(topics, key=lambda x: -x["source_count"])


# ── GPT 보고서 생성 ──────────────────────────────────────────────

def build_prompt(papers: list, topics: list) -> str:
    # 저널별 그룹핑
    journals = defaultdict(int)
    by_year  = defaultdict(int)
    for p in papers:
        if p["journal"]:
            journals[p["journal"]] += 1
        if p["date"]:
            by_year[p["date"][:4]] += 1

    top_journals = sorted(journals.items(), key=lambda x: -x[1])[:10]
    journal_str  = "\n".join(f"  - {j}: {c}편" for j, c in top_journals)
    year_str     = "\n".join(f"  - {y}년: {c}편" for y, c in sorted(by_year.items()))

    # 논문 목록 (제목 + 저널)
    paper_list = "\n".join(
        f"  [{i+1}] {p['date']} | {p['journal'] or 'N/A'} | {p['title']}"
        for i, p in enumerate(papers)
    )

    # 토픽 목록
    topic_list = "\n".join(
        f"  - [{t['type']}] {t['title']} ({t['source_count']}편): {t['summary']}"
        for t in topics
    )

    return f"""당신은 교육공학(EdTech) 분야 연구 동향 분석 전문가입니다.
아래 데이터를 바탕으로 한국어 연구 동향 보고서를 작성하세요.

## 수집된 논문 ({len(papers)}편)

### 주요 학술지 분포
{journal_str}

### 발행 연도 분포
{year_str}

### 전체 논문 목록
{paper_list}

## 현재 Wiki 토픽 ({len(topics)}개, 소스 수 기준 정렬)
{topic_list}

---

## 보고서 작성 지침

다음 JSON 형식으로만 응답하세요:

{{
  "executive_summary": "2-3문장 핵심 요약",
  "trends": [
    {{
      "title": "동향 제목",
      "description": "2-3문장 설명. 구체적인 논문/저널 언급 포함.",
      "evidence": "관련 토픽명이나 논문 제목 2-3개"
    }}
  ],
  "clusters": [
    {{
      "name": "연구 클러스터명",
      "topics": ["토픽1", "토픽2"],
      "description": "이 클러스터의 연구 흐름 1-2문장"
    }}
  ],
  "gaps": [
    {{
      "area": "공백 영역",
      "description": "왜 공백인지 1-2문장",
      "opportunity": "이 공백을 어떻게 채울 수 있는지 구체적 제안"
    }}
  ],
  "methodology": {{
    "dominant": "현재 지배적인 방법론과 그 이유",
    "emerging": "새롭게 등장하는 방법론",
    "missing": "활용되지 않고 있는 방법론과 적용 가능 영역"
  }},
  "recommendations": [
    {{
      "question": "구체적 연구 질문",
      "rationale": "왜 이 연구가 필요한지 (공백/동향 근거)",
      "method": "추천 연구방법론",
      "journals": ["투고 추천 학술지1", "학술지2"]
    }}
  ]
}}

규칙:
- trends: 4-5개, clusters: 3-4개, gaps: 4-5개, recommendations: 5개
- 모든 내용은 실제 논문 데이터에 근거할 것
- 한국어로 작성, 학술적 문체
- JSON만 반환, 다른 텍스트 없음"""


def call_gpt(prompt: str) -> dict:
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경변수 없음")

    client = OpenAI(api_key=api_key)
    print("  GPT-4o-mini 분석 중...")
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=4096,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an EdTech research analyst. Return only valid JSON matching the requested schema."},
            {"role": "user",   "content": prompt}
        ]
    )
    usage = resp.usage
    cost  = (usage.prompt_tokens * 0.15 + usage.completion_tokens * 0.60) / 1_000_000
    print(f"  토큰: 입력 {usage.prompt_tokens} / 출력 {usage.completion_tokens} | 비용 ${cost:.4f}")
    return json.loads(resp.choices[0].message.content)


def get_report_data(papers: list, topics: list) -> dict:
    # 캐시 확인
    if CACHE.exists():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
            cached_at = datetime.fromisoformat(cache.get("generated_at", "2000-01-01"))
            paper_count = cache.get("paper_count", 0)
            if datetime.now() - cached_at < timedelta(days=7) and paper_count == len(papers):
                print("  캐시 사용 (7일 이내, 논문 수 동일)")
                return cache["data"]
        except Exception:
            pass

    data = call_gpt(build_prompt(papers, topics))
    CACHE.write_text(json.dumps({
        "generated_at": datetime.now().isoformat(),
        "paper_count": len(papers),
        "data": data
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    return data


# ── HTML 렌더링 ──────────────────────────────────────────────────

def render_html(data: dict, papers: list, topics: list) -> str:
    now = datetime.now().strftime("%Y년 %m월 %d일")

    # ── 통계 ─────────────────────────────────────────────────────
    journals = defaultdict(int)
    by_month = defaultdict(int)
    for p in papers:
        if p["journal"]: journals[p["journal"]] += 1
        if p["date"]:    by_month[p["date"]] += 1

    top5_journals = sorted(journals.items(), key=lambda x: -x[1])[:5]
    gap_topics    = [t for t in topics if t["source_count"] <= 2]
    mature_topics = [t for t in topics if t["source_count"] >= 5]

    # ── 섹션별 HTML ───────────────────────────────────────────────
    def trends_html():
        out = ""
        colors = ["#6366f1","#10b981","#f59e0b","#3b82f6","#ef4444"]
        for i, t in enumerate(data.get("trends", [])):
            c = colors[i % len(colors)]
            out += f"""
            <div class="trend-card">
              <div class="trend-num" style="background:{c}">{i+1}</div>
              <div class="trend-body">
                <div class="trend-title">{t['title']}</div>
                <div class="trend-desc">{t['description']}</div>
                <div class="trend-evidence">근거: {t['evidence']}</div>
              </div>
            </div>"""
        return out

    def clusters_html():
        out = ""
        for cl in data.get("clusters", []):
            tags = "".join(f'<span class="tag">{tp}</span>' for tp in cl.get("topics", []))
            out += f"""
            <div class="cluster-card">
              <div class="cluster-name">{cl['name']}</div>
              <div class="cluster-tags">{tags}</div>
              <div class="cluster-desc">{cl['description']}</div>
            </div>"""
        return out

    def gaps_html():
        out = ""
        for g in data.get("gaps", []):
            out += f"""
            <div class="gap-card">
              <div class="gap-area">🔴 {g['area']}</div>
              <div class="gap-desc">{g['description']}</div>
              <div class="gap-opp">💡 {g['opportunity']}</div>
            </div>"""
        return out

    def method_html():
        m = data.get("methodology", {})
        return f"""
        <div class="method-grid">
          <div class="method-item dominant">
            <div class="method-label">지배적 방법론</div>
            <div>{m.get('dominant','')}</div>
          </div>
          <div class="method-item emerging">
            <div class="method-label">부상 중인 방법론</div>
            <div>{m.get('emerging','')}</div>
          </div>
          <div class="method-item missing">
            <div class="method-label">활용 부족 방법론</div>
            <div>{m.get('missing','')}</div>
          </div>
        </div>"""

    def recs_html():
        out = ""
        for i, r in enumerate(data.get("recommendations", []), 1):
            journals_str = " · ".join(r.get("journals", []))
            out += f"""
            <div class="rec-card">
              <div class="rec-header">
                <span class="rec-num">추천 {i}</span>
                <span class="rec-method">{r['method']}</span>
              </div>
              <div class="rec-question">"{r['question']}"</div>
              <div class="rec-rationale">{r['rationale']}</div>
              <div class="rec-journals">📰 {journals_str}</div>
            </div>"""
        return out

    def stat_bar(label, value, total, color):
        pct = int(value / total * 100) if total else 0
        return f"""<div class="stat-row">
          <span class="stat-label">{label}</span>
          <div class="stat-bar-wrap">
            <div class="stat-bar-fill" style="width:{pct}%;background:{color}"></div>
          </div>
          <span class="stat-val">{value}</span>
        </div>"""

    journal_bars = "".join(
        stat_bar(j[:35], c, len(papers), "#6366f1")
        for j, c in top5_journals
    )
    topic_bars = "".join(
        stat_bar(t["title"][:30], t["source_count"],
                 max(t["source_count"] for t in topics), "#10b981")
        for t in topics[:8]
    )

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EdTech 연구 동향 보고서</title>
<style>
:root{{
  --bg:#f8fafc; --white:#ffffff; --bdr:#e2e8f0;
  --txt:#1e293b; --muted:#64748b; --accent:#6366f1;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--txt);font-family:'Segoe UI',system-ui,sans-serif;
      font-size:14px;line-height:1.75}}
.page{{max-width:960px;margin:0 auto;padding:40px 24px}}

/* Cover */
.cover{{background:linear-gradient(135deg,#1e293b 0%,#312e81 100%);
        color:#fff;padding:48px 40px;border-radius:16px;margin-bottom:32px}}
.cover-tag{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;
            color:#a5b4fc;margin-bottom:12px}}
.cover h1{{font-size:28px;font-weight:800;line-height:1.3;margin-bottom:8px}}
.cover .sub{{color:#cbd5e1;font-size:14px;margin-bottom:24px}}
.cover-stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;
              border-top:1px solid #ffffff20;padding-top:24px}}
.cs-item .cs-val{{font-size:28px;font-weight:700;color:#a5b4fc}}
.cs-item .cs-lbl{{font-size:11px;color:#94a3b8;margin-top:2px}}

/* Executive summary */
.exec-summary{{background:#fff;border:1px solid var(--bdr);border-left:4px solid var(--accent);
               border-radius:8px;padding:20px 24px;margin-bottom:28px;
               font-size:15px;line-height:1.8;color:#334155}}

/* Section */
.section{{margin-bottom:36px}}
.section-header{{display:flex;align-items:center;gap:10px;margin-bottom:16px;
                  padding-bottom:10px;border-bottom:2px solid var(--bdr)}}
.section-icon{{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;
               justify-content:center;font-size:16px}}
.section-title{{font-size:17px;font-weight:700}}
.section-count{{font-size:11px;color:var(--muted);background:#f1f5f9;
                padding:2px 8px;border-radius:99px;margin-left:auto}}

/* Trend cards */
.trend-card{{display:flex;gap:14px;background:#fff;border:1px solid var(--bdr);
             border-radius:10px;padding:16px;margin-bottom:10px}}
.trend-num{{width:28px;height:28px;border-radius:8px;color:#fff;font-weight:700;
            font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.trend-title{{font-weight:600;font-size:14px;margin-bottom:5px}}
.trend-desc{{color:#475569;line-height:1.65;margin-bottom:6px}}
.trend-evidence{{font-size:11px;color:var(--muted);background:#f8fafc;
                  padding:4px 8px;border-radius:4px;border-left:2px solid #cbd5e1}}

/* Clusters */
.clusters-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:12px}}
.cluster-card{{background:#fff;border:1px solid var(--bdr);border-radius:10px;padding:16px}}
.cluster-name{{font-weight:700;font-size:14px;margin-bottom:8px;color:var(--accent)}}
.cluster-tags{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:10px}}
.tag{{background:#ede9fe;color:#5b21b6;padding:2px 8px;border-radius:99px;
       font-size:11px;font-weight:500}}
.cluster-desc{{color:#475569;font-size:13px;line-height:1.6}}

/* Gaps */
.gap-card{{background:#fff;border:1px solid #fecaca;border-radius:10px;
            padding:16px;margin-bottom:10px}}
.gap-area{{font-weight:700;font-size:14px;color:#dc2626;margin-bottom:6px}}
.gap-desc{{color:#475569;margin-bottom:8px;line-height:1.65}}
.gap-opp{{background:#f0fdf4;border-left:3px solid #22c55e;padding:8px 12px;
           border-radius:0 6px 6px 0;font-size:13px;color:#166534}}

/* Methodology */
.method-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.method-item{{background:#fff;border:1px solid var(--bdr);border-radius:10px;padding:16px}}
.method-label{{font-size:11px;font-weight:700;text-transform:uppercase;
               letter-spacing:.05em;margin-bottom:8px}}
.dominant .method-label{{color:#6366f1}}
.emerging .method-label{{color:#10b981}}
.missing .method-label{{color:#f59e0b}}
.method-item>div:last-child{{color:#475569;font-size:13px;line-height:1.65}}

/* Recommendations */
.rec-card{{background:#fff;border:1px solid var(--bdr);border-radius:10px;
            padding:18px;margin-bottom:12px}}
.rec-header{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
.rec-num{{background:var(--accent);color:#fff;padding:2px 10px;border-radius:99px;
           font-size:11px;font-weight:700}}
.rec-method{{background:#ede9fe;color:#5b21b6;padding:2px 8px;border-radius:99px;
              font-size:11px}}
.rec-question{{font-size:15px;font-weight:600;color:#1e293b;margin-bottom:8px;
               line-height:1.5;font-style:italic}}
.rec-rationale{{color:#475569;line-height:1.65;margin-bottom:8px}}
.rec-journals{{font-size:12px;color:var(--muted)}}

/* Stat bars */
.stat-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.stat-label{{width:200px;font-size:12px;color:#475569;flex-shrink:0;
              white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.stat-bar-wrap{{flex:1;background:#f1f5f9;border-radius:99px;height:8px;overflow:hidden}}
.stat-bar-fill{{height:8px;border-radius:99px;transition:width .3s}}
.stat-val{{width:30px;text-align:right;font-size:12px;font-weight:600;color:#334155}}

/* Stats side-by-side */
.stats-row{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:28px}}
.stats-box{{background:#fff;border:1px solid var(--bdr);border-radius:10px;padding:16px}}
.stats-box-title{{font-size:12px;font-weight:700;text-transform:uppercase;
                   letter-spacing:.05em;color:var(--muted);margin-bottom:12px}}

/* Footer */
.footer{{text-align:center;color:var(--muted);font-size:12px;
          margin-top:40px;padding-top:20px;border-top:1px solid var(--bdr)}}

@media(max-width:700px){{
  .cover-stats{{grid-template-columns:repeat(2,1fr)}}
  .clusters-grid,.method-grid,.stats-row{{grid-template-columns:1fr}}
}}
@media print{{
  body{{background:#fff}}
  .page{{padding:20px}}
}}
</style>
</head>
<body>
<div class="page">

<!-- Cover -->
<div class="cover">
  <div class="cover-tag">EdTech Research Landscape Report</div>
  <h1>교육공학 연구 동향 분석 보고서</h1>
  <div class="sub">수집 논문 자동 분석 · GPT-4o-mini · {now} 생성</div>
  <div class="cover-stats">
    <div class="cs-item"><div class="cs-val">{len(papers)}</div><div class="cs-lbl">수집 논문</div></div>
    <div class="cs-item"><div class="cs-val">{len(topics)}</div><div class="cs-lbl">Wiki 토픽</div></div>
    <div class="cs-item"><div class="cs-val">{len(mature_topics)}</div><div class="cs-lbl">성숙 토픽 (≥5편)</div></div>
    <div class="cs-item"><div class="cs-val">{len(gap_topics)}</div><div class="cs-lbl">연구 공백 (≤2편)</div></div>
  </div>
</div>

<!-- Executive Summary -->
<div class="exec-summary">
  <strong>핵심 요약 —</strong> {data.get('executive_summary', '')}
</div>

<!-- Stats -->
<div class="stats-row">
  <div class="stats-box">
    <div class="stats-box-title">주요 학술지 (상위 5)</div>
    {journal_bars}
  </div>
  <div class="stats-box">
    <div class="stats-box-title">토픽별 소스 집중도 (상위 8)</div>
    {topic_bars}
  </div>
</div>

<!-- Trends -->
<div class="section">
  <div class="section-header">
    <div class="section-icon" style="background:#ede9fe">📈</div>
    <div class="section-title">연구 동향</div>
    <span class="section-count">{len(data.get('trends',[]))}개 동향 식별</span>
  </div>
  {trends_html()}
</div>

<!-- Clusters -->
<div class="section">
  <div class="section-header">
    <div class="section-icon" style="background:#d1fae5">🔗</div>
    <div class="section-title">연구 클러스터</div>
    <span class="section-count">{len(data.get('clusters',[]))}개 클러스터</span>
  </div>
  <div class="clusters-grid">{clusters_html()}</div>
</div>

<!-- Gaps -->
<div class="section">
  <div class="section-header">
    <div class="section-icon" style="background:#fee2e2">🔍</div>
    <div class="section-title">연구 공백 및 기회</div>
    <span class="section-count">{len(data.get('gaps',[]))}개 공백 식별</span>
  </div>
  {gaps_html()}
</div>

<!-- Methodology -->
<div class="section">
  <div class="section-header">
    <div class="section-icon" style="background:#fef9c3">⚗️</div>
    <div class="section-title">방법론 동향</div>
  </div>
  {method_html()}
</div>

<!-- Recommendations -->
<div class="section">
  <div class="section-header">
    <div class="section-icon" style="background:#dbeafe">💡</div>
    <div class="section-title">추천 연구 방향</div>
    <span class="section-count">{len(data.get('recommendations',[]))}개 제안</span>
  </div>
  {recs_html()}
</div>

<div class="footer">
  본 보고서는 {len(papers)}편의 수집 논문을 GPT-4o-mini로 자동 분석하여 생성되었습니다.<br>
  EdTech Research Wiki · {now} · <a href="dashboard.html" style="color:#6366f1">대시보드 보기</a>
</div>

</div>
</body>
</html>
"""


# ── 메인 ────────────────────────────────────────────────────────
def main():
    import traceback
    print("\n=== EdTech 연구 동향 보고서 생성 ===")
    try:
        print("논문 데이터 수집 중...")
        papers = collect_papers()
        topics = collect_wiki_topics()
        print(f"  논문 {len(papers)}편 · 토픽 {len(topics)}개 로드")

        print("보고서 데이터 생성 중...")
        data = get_report_data(papers, topics)
        print(f"  섹션: 동향 {len(data.get('trends',[]))}개, 공백 {len(data.get('gaps',[]))}개, 추천 {len(data.get('recommendations',[]))}개")

        print("HTML 렌더링 중...")
        html = render_html(data, papers, topics)

        print(f"파일 저장 중: {OUTPUT}")
        OUTPUT.write_text(html, encoding="utf-8")
        print(f"✓ 완료: {OUTPUT}")
        print(f"  파일 크기: {OUTPUT.stat().st_size // 1024}KB")
    except Exception as e:
        print(f"\n[오류] {type(e).__name__}: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
