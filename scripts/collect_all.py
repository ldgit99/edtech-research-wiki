#!/usr/bin/env python3
"""
교육공학 논문 통합 수집 스크립트 (Windows 호환)
사용법: python collect_all.py [days_back]

모든 소스를 순차적으로 수집하고 결과를 log.md에 기록한다.
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path

WIKI_ROOT = Path(__file__).parent.parent
SCRIPTS   = Path(__file__).parent
LOG_FILE  = WIKI_ROOT / "log.md"


def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- [{timestamp}] {msg}\n"
    print(entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def run_script(name: str, args: list = None) -> bool:
    cmd = [sys.executable, str(SCRIPTS / name)] + (args or [])
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=str(WIKI_ROOT)
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                print(f"    {line}")
        if result.returncode != 0 and result.stderr:
            print(f"    [stderr] {result.stderr[:200]}")
        return result.returncode == 0
    except Exception as e:
        print(f"    [실패] {name}: {e}")
        return False


def count_inbox() -> int:
    inbox = WIKI_ROOT / "raw" / "inbox"
    return len(list(inbox.glob("*.md")))


def main():
    days = sys.argv[1] if len(sys.argv) > 1 else "7"
    print(f"\n{'='*50}")
    print(f"교육공학 논문 자동 수집 시작: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*50}\n")

    log(f"[COLLECT-START] days_back={days}")

    before = count_inbox()

    # 1. OpenAlex 국제 학술지
    print("[1/3] OpenAlex 국제 학술지 수집...")
    ok1 = run_script("openalex_collector.py", [days])

    # 2. arXiv 교육 섹션
    print("\n[2/3] arXiv cs.CY 교육 섹션 수집...")
    ok2 = run_script("arxiv_collector.py")

    # 3. RISS 국내 학술지
    print("\n[3/3] RISS 국내 학술지 수집...")
    ok3 = run_script("riss_collector.py")

    after = count_inbox()
    new_count = after - before

    print(f"\n{'='*50}")
    print(f"수집 완료: {new_count}편 신규 추가")
    print(f"inbox 전체: {after}편")
    print(f"{'='*50}")
    print(f"\n다음 단계: Claude Code에서 /llm-wiki:wiki compile 실행하세요")

    log(f"[COLLECT-DONE] 신규={new_count}편, inbox총={after}편")


if __name__ == "__main__":
    main()
