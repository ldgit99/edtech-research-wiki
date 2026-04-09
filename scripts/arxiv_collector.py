#!/usr/bin/env python3
"""
arXiv cs.CY (Computers and Society) 섹션에서 교육공학 관련 논문 수집
사용법: python arxiv_collector.py
"""

import feedparser
import sys
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent
WIKI_RAW  = WIKI_ROOT / "raw" / "inbox"
WIKI_RAW.mkdir(parents=True, exist_ok=True)

# 교육공학 관련 arXiv 카테고리
ARXIV_FEEDS = {
    "cs.CY": "https://rss.arxiv.org/rss/cs.CY",   # Computers and Society
    "cs.HC": "https://rss.arxiv.org/rss/cs.HC",   # Human-Computer Interaction
}

# 교육공학 키워드 필터 (소문자)
KEYWORDS = [
    "education", "learning", "pedagogy", "student", "teacher",
    "instructional", "curriculum", "knowledge", "adaptive learning",
    "intelligent tutoring", "llm education", "ai tutor",
    "educational technology", "e-learning", "blended learning",
    "classroom", "assessment", "feedback", "literacy",
    "distance education", "online learning", "mooc",
    "learning analytics", "educational data", "cognitive load",
    "self-regulated", "collaborative learning", "scaffolding",
]


def collect() -> int:
    total = 0
    for category, feed_url in ARXIV_FEEDS.items():
        print(f"  fetching arXiv {category}...")
        try:
            feed = feedparser.parse(feed_url)
            matched = 0
            for entry in feed.entries:
                text = (
                    entry.get("title", "") + " " + entry.get("summary", "")
                ).lower()
                if any(kw in text for kw in KEYWORDS):
                    _save(entry, category)
                    matched += 1
            print(f"  [OK] arXiv {category}: {matched}편 (전체 {len(feed.entries)}편 중 필터)")
            total += matched
        except Exception as e:
            print(f"  [오류] arXiv {category}: {e}")
    return total


def _safe_date(raw: str) -> str:
    """다양한 날짜 형식을 YYYY-MM-DD로 정규화"""
    if not raw:
        return datetime.now().strftime("%Y-%m-%d")
    # feedparser published: "Thu, 09 Apr 2026 00:00:00 +0000" 또는 "2026-04-09T..."
    for fmt in ("%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw[:len(fmt)+5].strip(), fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    # fallback: 숫자만 추출해서 첫 10자
    digits = "".join(c if c.isdigit() or c == "-" else " " for c in raw)
    parts = digits.split()
    if parts and len(parts[0]) == 4:  # year first
        return datetime.now().strftime("%Y-%m-%d")
    return datetime.now().strftime("%Y-%m-%d")


def _safe_arxiv_id(raw_id: str) -> str:
    """arXiv ID에서 파일명에 사용 불가한 문자 제거"""
    # "oai:arXiv.org:2604.06200v1" → "2604.06200v1"
    part = raw_id.split(":")[-1]
    # Windows 파일명에 사용 불가한 문자 제거: : / \ * ? " < > |
    return "".join(c for c in part if c not in r':/\*?"<>|')


def _save(entry: dict, category: str) -> None:
    pub = entry.get("published", "")
    date = _safe_date(pub)
    arxiv_id = _safe_arxiv_id(entry.get("id", "unknown"))
    filename = f"{date}-arxiv-{arxiv_id}.md"
    path = WIKI_RAW / filename

    if path.exists():
        return

    title = entry.get("title", "").strip().replace("\n", " ")
    authors = ", ".join(a.get("name", "") for a in entry.get("authors", []))
    abstract = entry.get("summary", "").strip().replace("\n", " ")
    link = entry.get("link", "")

    content = f"""---
type: raw-paper
source: arxiv
category: "{category}"
arxiv-id: "{arxiv_id}"
collected: "{datetime.now().strftime('%Y-%m-%d')}"
publication-date: "{date}"
authors: "{authors}"
compiled: false
---

# {title}

**저자**: {authors}
**카테고리**: {category}
**arXiv ID**: {arxiv_id}
**발행일**: {date}

## 초록

{abstract}

## 원문

{link}
"""
    path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    count = collect()
    print(f"\n총 {count}편 수집 → {WIKI_RAW}")
