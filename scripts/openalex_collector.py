#!/usr/bin/env python3
"""
국제 교육공학 학술지 신착 논문 자동 수집 (OpenAlex API)
사용법: python openalex_collector.py [days_back]
예시:  python openalex_collector.py 7   (최근 7일치 수집)
"""

import requests
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows 경로 사용
WIKI_ROOT = Path(__file__).parent.parent
WIKI_RAW  = WIKI_ROOT / "raw" / "inbox"
WIKI_RAW.mkdir(parents=True, exist_ok=True)

# OpenAlex 교육공학 핵심 학술지 ID
JOURNALS = {
    "Computers & Education":
        "S4210172010",
    "British Journal of Educational Technology":
        "S4210174990",
    "Learning and Instruction":
        "S4210194127",
    "Educational Technology Research & Development":
        "S4210196801",
    "Computers in Human Behavior":
        "S4210179490",
    "Internet and Higher Education":
        "S4210177891",
    "Journal of Learning Analytics":
        "S4210163803",
    "Educational Psychologist":
        "S4210200040",
}

HEADERS = {
    "User-Agent": "edtech-wiki-collector/1.0 (mailto:researcher@example.com)"
}


def collect(days_back: int = 7) -> int:
    since = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    total = 0
    print(f"수집 기간: {since} 이후")

    for journal_name, journal_id in JOURNALS.items():
        url = (
            "https://api.openalex.org/works"
            f"?filter=primary_location.source.id:{journal_id},"
            f"from_publication_date:{since}"
            "&select=id,title,abstract,authorships,publication_date,doi,concepts"
            "&per-page=25"
        )
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            papers = resp.json().get("results", [])
            for paper in papers:
                _save(paper, journal_name)
            print(f"  [OK] {journal_name}: {len(papers)}편")
            total += len(papers)
        except Exception as e:
            print(f"  [오류] {journal_name}: {e}")

    return total


def _save(paper: dict, journal_name: str) -> None:
    date = paper.get("publication_date") or datetime.now().strftime("%Y-%m-%d")
    title = paper.get("title", "제목없음")
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in title[:40].lower())
    slug = slug.strip("-")
    filename = f"{date}-openalex-{slug}.md"
    path = WIKI_RAW / filename

    if path.exists():
        return  # 중복 스킵

    authors = ", ".join(
        a.get("author", {}).get("display_name", "")
        for a in paper.get("authorships", [])
    )
    concepts = ", ".join(
        c["display_name"] for c in paper.get("concepts", [])[:6]
    )
    doi = paper.get("doi", "")
    openalex_id = paper.get("id", "")
    abstract = paper.get("abstract") or "초록 없음"

    content = f"""---
type: raw-paper
source: openalex
journal: "{journal_name}"
doi: "{doi}"
collected: "{datetime.now().strftime('%Y-%m-%d')}"
publication-date: "{date}"
authors: "{authors}"
concepts: [{concepts}]
compiled: false
---

# {title}

**저자**: {authors}
**학술지**: {journal_name}
**발행일**: {date}
**DOI**: {doi}
**키워드**: {concepts}

## 초록

{abstract}

## 원문

{openalex_id}
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    count = collect(days_back=days)
    print(f"\n총 {count}편 수집 완료 → {WIKI_RAW}")
