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

# OpenAlex 교육공학 핵심 학술지 ID (검증된 ID)
JOURNALS = {
    "Computers & Education":
        "S4210172634",
    "British Journal of Educational Technology":
        "S110346167",
    "Learning and Instruction":
        "S78398831",
    "Educational Technology Research & Development":
        "S114840262",
    "Internet and Higher Education":
        "S166850901",
    "Journal of Learning Analytics":
        "S2764890288",
    "Computers and Education AI":
        "S4210183364",
}

HEADERS = {
    "User-Agent": "edtech-wiki-collector/1.0 (mailto:researcher@example.com)"
}


def collect(days_back: int = 7) -> int:
    since = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    total = 0
    print(f"수집 기간: {since} 이후")

    for journal_name, journal_id in JOURNALS.items():
        params = {
            "filter": f"locations.source.id:{journal_id},from_publication_date:{since}",
            "select": "id,title,authorships,publication_date,doi,primary_location,open_access",
            "per-page": "25",
        }
        try:
            resp = requests.get(
                "https://api.openalex.org/works",
                params=params, headers=HEADERS, timeout=15
            )
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
    doi = paper.get("doi", "")
    openalex_id = paper.get("id", "")
    oa_info = paper.get("open_access") or {}
    oa_url = oa_info.get("oa_url") or "" if isinstance(oa_info, dict) else ""

    content = f"""---
type: raw-paper
source: openalex
journal: "{journal_name}"
doi: "{doi}"
collected: "{datetime.now().strftime('%Y-%m-%d')}"
publication-date: "{date}"
authors: "{authors}"
compiled: false
---

# {title}

**저자**: {authors}
**학술지**: {journal_name}
**발행일**: {date}
**DOI**: {doi}

## 초록

초록은 DOI 링크에서 확인하세요.

## 원문 링크

- OpenAlex: {openalex_id}
- DOI: https://doi.org/{doi.replace('https://doi.org/', '') if doi else ''}
{f'- 오픈 액세스: {oa_url}' if oa_url else ''}
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    count = collect(days_back=days)
    print(f"\n총 {count}편 수집 완료 → {WIKI_RAW}")
