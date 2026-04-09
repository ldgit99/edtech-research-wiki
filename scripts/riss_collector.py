#!/usr/bin/env python3
"""
국내 교육공학 학술지 논문 수집 (RISS Open API)
API 키 발급: https://scienceon.kisti.re.kr/srch/selectPORSrchFnct.do?cn=FNCT000557

사용법:
  RISS_API_KEY=your_key python riss_collector.py [year]
  python riss_collector.py 2026

환경변수 설정 (Windows):
  set RISS_API_KEY=your_key_here
  또는 .env 파일 사용
"""

import os
import sys
import requests
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent
WIKI_RAW  = WIKI_ROOT / "raw" / "inbox"
WIKI_RAW.mkdir(parents=True, exist_ok=True)

# RISS API 키 (환경변수 또는 직접 설정)
RISS_API_KEY = os.environ.get("RISS_API_KEY", "")

# 국내 교육공학 주요 학술지
KR_JOURNALS = [
    "교육공학연구",
    "교육정보미디어연구",
    "교육학연구",
    "아시아교육연구",
    "한국교육",
    "멀티미디어언어교육",
    "교육과학연구",
    "교육심리연구",
]


def collect(year: int = None) -> int:
    if not RISS_API_KEY or RISS_API_KEY == "":
        print("  [경고] RISS_API_KEY 미설정. 환경변수를 설정하세요.")
        print("  API 키 발급: https://scienceon.kisti.re.kr")
        return 0

    if year is None:
        year = datetime.now().year

    total = 0
    for journal in KR_JOURNALS:
        try:
            url = "https://openapi.riss.kr/api/search/article"
            params = {
                "key": RISS_API_KEY,
                "query": journal,
                "target": "jtitle",
                "start": 0,
                "display": 20,
                "startYear": year,
                "endYear": year,
                "output": "json",
            }
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("resultList", [])
            for item in items:
                _save(item, journal)
            print(f"  [OK] {journal} ({year}): {len(items)}편")
            total += len(items)
        except Exception as e:
            print(f"  [오류] {journal}: {e}")

    return total


def _save(item: dict, journal: str) -> None:
    title = item.get("title", "제목없음")
    pub_year = item.get("year", str(datetime.now().year))
    control_no = item.get("control_no", "")
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in title[:35])
    slug = slug.strip("-")
    filename = f"{pub_year}-riss-{slug}.md"
    path = WIKI_RAW / filename

    if path.exists():
        return

    authors = item.get("author", "N/A")
    abstract = item.get("abstract") or "초록 없음"
    link = f"https://www.riss.kr/link?id={control_no}" if control_no else ""

    content = f"""---
type: raw-paper
source: riss
journal: "{journal}"
collected: "{datetime.now().strftime('%Y-%m-%d')}"
publication-year: {pub_year}
authors: "{authors}"
language: ko
riss-id: "{control_no}"
compiled: false
---

# {title}

**저자**: {authors}
**학술지**: {journal}
**발행연도**: {pub_year}
**RISS ID**: {control_no}

## 초록

{abstract}

## 원문 링크

{link}
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    year = int(sys.argv[1]) if len(sys.argv) > 1 else None
    count = collect(year=year)
    print(f"\n총 {count}편 수집 → {WIKI_RAW}")
