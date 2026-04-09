#!/usr/bin/env python3
"""
EdTech Research Wiki — 웹 대시보드 생성기
wiki 데이터를 읽어 dashboard.html 생성

사용법: python generate_dashboard.py
출력: ../dashboard.html  (브라우저로 바로 열기 가능)
"""

import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
WIKI = ROOT / "wiki"
LOG_FILE = ROOT / "log.md"
OUTPUT = ROOT / "dashboard.html"
INBOX = ROOT / "raw" / "inbox"

SKIP_DIRS = {"syntheses", "queries"}
SKIP_FILES = {"index.md", "index-dynamic.md"}

TYPE_LABEL = {
    "concept": "개념",
    "researcher": "연구자",
    "theory": "이론",
    "methodology": "방법론",
    "debate": "논쟁",
    "other": "기타",
}
TYPE_COLOR = {
    "concept": "#6366f1",
    "researcher": "#10b981",
    "theory": "#f59e0b",
    "methodology": "#3b82f6",
    "debate": "#ef4444",
    "other": "#8b5cf6",
}


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
        pages.append({
            "path": str(rel).replace("\\", "/"),
            "type": meta.get("type", rel.parts[0] if len(rel.parts) > 1 else "other"),
            "title": title,
            "summary": meta.get("summary", ""),
            "source_count": int(meta.get("source-count", 0) or 0),
            "created": meta.get("created", ""),
            "updated": meta.get("updated", ""),
        })
    pages.sort(key=lambda p: p["source_count"], reverse=True)
    return pages


def get_recent_log(n: int = 15) -> list:
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


def build_html(pages: list, log_entries: list, inbox: dict) -> str:
    # --- 집계 ---
    type_counts: dict = {}
    for p in pages:
        t = p["type"]
        type_counts[t] = type_counts.get(t, 0) + 1

    total_pages = len(pages)
    total_sources = sum(p["source_count"] for p in pages)
    concepts = type_counts.get("concept", 0)
    researchers = type_counts.get("researcher", 0)
    debates = type_counts.get("debate", 0)

    # Chart.js 데이터
    donut_labels = json.dumps([TYPE_LABEL.get(k, k) for k in type_counts])
    donut_data = json.dumps(list(type_counts.values()))
    donut_colors = json.dumps([TYPE_COLOR.get(k, "#94a3b8") for k in type_counts])

    bar_labels = json.dumps([p["title"][:20] for p in pages[:15]])
    bar_data = json.dumps([p["source_count"] for p in pages[:15]])
    bar_colors = json.dumps([TYPE_COLOR.get(p["type"], "#94a3b8") for p in pages[:15]])

    # 페이지 테이블 행
    rows_html = ""
    for p in pages:
        badge_color = TYPE_COLOR.get(p["type"], "#8b5cf6")
        label = TYPE_LABEL.get(p["type"], p["type"])
        rows_html += f"""
        <tr>
          <td class="py-2 px-3">
            <span class="badge" style="background:{badge_color}">{label}</span>
          </td>
          <td class="py-2 px-3 title-cell">{p['title']}</td>
          <td class="py-2 px-3 summary-cell text-gray">{p['summary']}</td>
          <td class="py-2 px-3 text-center">
            <span class="src-badge">{p['source_count']}</span>
          </td>
          <td class="py-2 px-3 text-gray text-small">{p['updated'] or p['created']}</td>
        </tr>"""

    # 로그 항목
    log_html = ""
    for entry in log_entries:
        # 날짜 추출
        dm = re.match(r"- \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)", entry)
        if dm:
            date_str, msg = dm.group(1), dm.group(2)
        else:
            date_str, msg = "", entry.lstrip("- ")
        # 태그 색상
        tag_m = re.match(r"\[([A-Z\-]+)\] (.+)", msg)
        if tag_m:
            tag, rest = tag_m.group(1), tag_m.group(2)
            tag_colors = {
                "AUTO-COMPILE-START": "#6366f1", "AUTO-COMPILE-DONE": "#10b981",
                "COLLECT": "#3b82f6", "FIX": "#ef4444",
                "IMPROVE": "#f59e0b", "TEST": "#8b5cf6",
            }
            tc = tag_colors.get(tag, "#64748b")
            log_html += f"""
            <div class="log-entry">
              <span class="log-tag" style="background:{tc}">{tag}</span>
              <span class="log-msg">{rest[:80]}</span>
              <span class="log-date">{date_str}</span>
            </div>"""
        else:
            log_html += f"""
            <div class="log-entry">
              <span class="log-msg">{msg[:90]}</span>
              <span class="log-date">{date_str}</span>
            </div>"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EdTech Research Wiki — Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0f172a; --surface: #1e293b; --border: #334155;
    --text: #f1f5f9; --muted: #94a3b8; --accent: #6366f1;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'Segoe UI', system-ui, sans-serif;
         font-size: 14px; line-height: 1.6; }}
  a {{ color: var(--accent); text-decoration: none; }}
  .container {{ max-width: 1280px; margin: 0 auto; padding: 24px 20px; }}

  /* Header */
  .header {{ display: flex; justify-content: space-between; align-items: center;
             margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid var(--border); }}
  .header h1 {{ font-size: 20px; font-weight: 700; }}
  .header h1 span {{ color: var(--accent); }}
  .last-updated {{ font-size: 12px; color: var(--muted); }}

  /* Stat cards */
  .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                 gap: 12px; margin-bottom: 28px; }}
  .stat-card {{ background: var(--surface); border: 1px solid var(--border);
                border-radius: 10px; padding: 16px; }}
  .stat-card .label {{ font-size: 11px; color: var(--muted); text-transform: uppercase;
                        letter-spacing: .05em; margin-bottom: 6px; }}
  .stat-card .value {{ font-size: 32px; font-weight: 700; }}
  .stat-card .sub {{ font-size: 11px; color: var(--muted); margin-top: 2px; }}
  .accent {{ color: #6366f1; }} .green {{ color: #10b981; }} .amber {{ color: #f59e0b; }}
  .red {{ color: #ef4444; }} .blue {{ color: #3b82f6; }}

  /* Charts row */
  .charts-row {{ display: grid; grid-template-columns: 280px 1fr; gap: 16px; margin-bottom: 28px; }}
  .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 18px; }}
  .card-title {{ font-size: 13px; font-weight: 600; margin-bottom: 14px; color: var(--muted);
                 text-transform: uppercase; letter-spacing: .05em; }}
  .chart-wrap {{ position: relative; height: 220px; }}

  /* Bottom row */
  .bottom-row {{ display: grid; grid-template-columns: 1fr 360px; gap: 16px; }}

  /* Table */
  .table-scroll {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead th {{ font-size: 11px; font-weight: 600; color: var(--muted); text-transform: uppercase;
              letter-spacing: .04em; padding: 8px 12px; text-align: left;
              border-bottom: 1px solid var(--border); }}
  tbody tr {{ border-bottom: 1px solid #1e293b; transition: background .15s; }}
  tbody tr:hover {{ background: #ffffff08; }}
  td {{ vertical-align: middle; }}
  .badge {{ display: inline-block; padding: 2px 7px; border-radius: 99px;
            font-size: 10px; font-weight: 600; color: #fff; white-space: nowrap; }}
  .src-badge {{ display: inline-block; background: #1e3a5f; color: #60a5fa;
                padding: 1px 8px; border-radius: 99px; font-size: 12px; font-weight: 600; }}
  .title-cell {{ font-weight: 500; max-width: 200px; white-space: nowrap;
                 overflow: hidden; text-overflow: ellipsis; }}
  .summary-cell {{ max-width: 280px; white-space: nowrap; overflow: hidden;
                   text-overflow: ellipsis; }}
  .text-gray {{ color: var(--muted); }}
  .text-small {{ font-size: 12px; }}
  .text-center {{ text-align: center; }}

  /* Log */
  .log-entry {{ display: flex; align-items: baseline; gap: 8px; padding: 8px 0;
                border-bottom: 1px solid #1e293b; }}
  .log-entry:last-child {{ border-bottom: none; }}
  .log-tag {{ flex-shrink: 0; display: inline-block; padding: 1px 6px; border-radius: 4px;
              font-size: 10px; font-weight: 700; color: #fff; }}
  .log-msg {{ flex: 1; font-size: 13px; color: var(--text); }}
  .log-date {{ flex-shrink: 0; font-size: 11px; color: var(--muted); }}

  /* Inbox progress */
  .progress-bar {{ background: #334155; border-radius: 99px; height: 6px; margin: 8px 0 4px; }}
  .progress-fill {{ height: 6px; border-radius: 99px; background: #10b981; }}

  @media (max-width: 900px) {{
    .charts-row {{ grid-template-columns: 1fr; }}
    .bottom-row {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <h1>EdTech Research Wiki <span>Dashboard</span></h1>
    <span class="last-updated">마지막 갱신: {now}</span>
  </div>

  <!-- Stats -->
  <div class="stats-grid">
    <div class="stat-card">
      <div class="label">총 Wiki 페이지</div>
      <div class="value accent">{total_pages}</div>
    </div>
    <div class="stat-card">
      <div class="label">총 소스 논문</div>
      <div class="value green">{total_sources}</div>
    </div>
    <div class="stat-card">
      <div class="label">개념 페이지</div>
      <div class="value blue">{concepts}</div>
    </div>
    <div class="stat-card">
      <div class="label">연구자 페이지</div>
      <div class="value amber">{researchers}</div>
    </div>
    <div class="stat-card">
      <div class="label">논쟁/Debate</div>
      <div class="value red">{debates}</div>
    </div>
    <div class="stat-card">
      <div class="label">Inbox 처리</div>
      <div class="value" style="color:#10b981">{inbox['compiled']}</div>
      <div class="sub">미처리: {inbox['uncompiled']}편</div>
      <div class="progress-bar">
        <div class="progress-fill" style="width:{int(inbox['compiled']/(inbox['total'] or 1)*100)}%"></div>
      </div>
    </div>
  </div>

  <!-- Charts -->
  <div class="charts-row">
    <div class="card">
      <div class="card-title">페이지 유형 분포</div>
      <div class="chart-wrap">
        <canvas id="donutChart"></canvas>
      </div>
    </div>
    <div class="card">
      <div class="card-title">소스 수 상위 15 페이지</div>
      <div class="chart-wrap">
        <canvas id="barChart"></canvas>
      </div>
    </div>
  </div>

  <!-- Bottom: table + log -->
  <div class="bottom-row">
    <div class="card">
      <div class="card-title">Wiki 페이지 목록</div>
      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th>유형</th><th>제목</th><th>요약</th>
              <th style="text-align:center">소스</th><th>갱신일</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
      </div>
    </div>
    <div class="card">
      <div class="card-title">최근 활동 로그</div>
      {log_html}
    </div>
  </div>

</div>

<script>
const donutCtx = document.getElementById('donutChart').getContext('2d');
new Chart(donutCtx, {{
  type: 'doughnut',
  data: {{
    labels: {donut_labels},
    datasets: [{{ data: {donut_data}, backgroundColor: {donut_colors},
                 borderWidth: 2, borderColor: '#0f172a' }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{
      legend: {{ position: 'bottom', labels: {{ color: '#94a3b8', font: {{ size: 11 }},
                 padding: 10, boxWidth: 10 }} }}
    }}
  }}
}});

const barCtx = document.getElementById('barChart').getContext('2d');
new Chart(barCtx, {{
  type: 'bar',
  data: {{
    labels: {bar_labels},
    datasets: [{{ label: '소스 수', data: {bar_data},
                  backgroundColor: {bar_colors}, borderRadius: 4 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    indexAxis: 'y',
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }} }},
      y: {{ ticks: {{ color: '#cbd5e1', font: {{ size: 11 }} }}, grid: {{ display: false }} }}
    }}
  }}
}});
</script>
</body>
</html>
"""


def main():
    print("대시보드 생성 중...")
    pages = get_wiki_pages()
    log_entries = get_recent_log(15)
    inbox = get_inbox_stats()
    html = build_html(pages, log_entries, inbox)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"완료: {OUTPUT}")
    print(f"  페이지 {len(pages)}개, 소스 {sum(p['source_count'] for p in pages)}편")


if __name__ == "__main__":
    main()
