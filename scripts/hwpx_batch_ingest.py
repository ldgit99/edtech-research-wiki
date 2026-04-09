#!/usr/bin/env python3
"""
HWP/HWPX 문서 일괄 변환 및 wiki raw/ 수집
hwpx-skill (https://github.com/jkf87/hwpx-skill) 기반

사용법:
  python hwpx_batch_ingest.py <폴더경로>
  python hwpx_batch_ingest.py "C:/Users/user/Downloads/논문"

처리 흐름:
  .hwp  → convert_hwp.py → .hwpx → text_extract.py → raw/papers/*.md
  .hwpx → text_extract.py → raw/papers/*.md
  원본  → raw/attachments/originals/ 보관
"""

import sys
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

WIKI_ROOT    = Path(__file__).parent.parent
RAW_PAPERS   = WIKI_ROOT / "raw" / "papers"
ORIGINALS    = WIKI_ROOT / "raw" / "attachments" / "originals"
HWPX_SKILL   = Path(__file__).parent / "hwpx-skill" / "scripts"
LOG_FILE     = WIKI_ROOT / "log.md"

RAW_PAPERS.mkdir(parents=True, exist_ok=True)
ORIGINALS.mkdir(parents=True, exist_ok=True)


def log(msg: str) -> None:
    entry = f"- [{datetime.now().strftime('%Y-%m-%d %H:%M')}] {msg}\n"
    print(entry.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def check_hwpx_skill() -> bool:
    convert = HWPX_SKILL / "convert_hwp.py"
    extract = HWPX_SKILL / "text_extract.py"
    if not convert.exists() or not extract.exists():
        print(f"[오류] hwpx-skill 스크립트를 찾을 수 없습니다: {HWPX_SKILL}")
        print("  scripts/hwpx-skill/ 폴더에 jkf87/hwpx-skill이 클론되어 있어야 합니다.")
        return False
    return True


def hwp_to_hwpx(hwp_path: Path, out_dir: Path) -> Path | None:
    """바이너리 .hwp를 .hwpx로 변환"""
    out_path = out_dir / (hwp_path.stem + ".hwpx")
    cmd = [
        sys.executable,
        str(HWPX_SKILL / "convert_hwp.py"),
        str(hwp_path),
        "-o", str(out_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and out_path.exists():
            return out_path
        else:
            print(f"    [변환 실패] {hwp_path.name}: {result.stderr[:150]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"    [타임아웃] {hwp_path.name}")
        return None
    except Exception as e:
        print(f"    [오류] {hwp_path.name}: {e}")
        return None


def extract_text(hwpx_path: Path) -> str | None:
    """HWPX에서 마크다운 텍스트 추출 (임시 파일 경유로 CP949/UTF-8 충돌 방지)"""
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as tmp:
        tmp_path = Path(tmp.name)

    cmd = [
        sys.executable,
        str(HWPX_SKILL / "text_extract.py"),
        str(hwpx_path),
        "--format", "markdown",
        "--output", str(tmp_path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if result.returncode == 0 and tmp_path.exists():
            content = tmp_path.read_text(encoding="utf-8")
            tmp_path.unlink(missing_ok=True)
            if content.strip():
                return content
        print(f"    [추출 실패] {hwpx_path.name}: {result.stderr[:150]}")
        tmp_path.unlink(missing_ok=True)
        return None
    except Exception as e:
        print(f"    [오류] {hwpx_path.name}: {e}")
        tmp_path.unlink(missing_ok=True)
        return None


def dedup_nested_lines(content: str) -> str:
    """HWPX 추출 시 테이블 셀이 중복 출력되는 문제 제거.

    text_extract.py --format markdown 은 테이블 셀을 일반 텍스트로 한 번,
    2-space 들여쓰기 네스티드로 또 한 번 출력한다.
    동일 내용이 인접한 경우 들여쓰기 버전을 제거.
    """
    lines = content.split("\n")
    flat = [l.strip() for l in lines]
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if line.startswith("  ") and stripped:
            # 앞쪽 비들여쓰기 구간에 동일 내용이 있으면 중복
            prev_flat = flat[max(0, i - len(lines)):i]
            if stripped in prev_flat:
                continue
        result.append(line)
    return "\n".join(result)


def wrap_frontmatter(content: str, source_file: Path, original_ext: str) -> str:
    """추출된 텍스트에 wiki 프론트매터 추가"""
    date = datetime.now().strftime("%Y-%m-%d")
    # 첫 줄을 실제 제목으로 활용 (있는 경우)
    first_line = content.strip().split("\n")[0].strip() if content.strip() else ""
    title = first_line if first_line else source_file.stem.replace("-", " ").replace("_", " ")
    # 중복 테이블 셀 제거
    content = dedup_nested_lines(content)

    header = f"""---
type: raw-paper
source: hwpx
original-file: "{source_file.name}"
original-format: "{original_ext}"
collected: "{date}"
compiled: false
---

# {title}

> 원본 파일: `raw/attachments/originals/{source_file.name}`
> 변환일: {date}

---

"""
    return header + content


def process_file(filepath: Path) -> bool:
    """단일 HWP/HWPX 파일 처리"""
    ext = filepath.suffix.lower()
    date = datetime.now().strftime("%Y-%m-%d")
    out_filename = f"{date}-{filepath.stem[:50]}.md"
    out_path = RAW_PAPERS / out_filename

    if out_path.exists():
        print(f"    [스킵] 이미 처리됨: {out_filename}")
        return True

    print(f"  처리 중: {filepath.name}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # HWP이면 먼저 HWPX로 변환
        if ext == ".hwp":
            print(f"    .hwp → .hwpx 변환 중...")
            hwpx_path = hwp_to_hwpx(filepath, tmp)
            if not hwpx_path:
                return False
        elif ext == ".hwpx":
            hwpx_path = filepath
        else:
            print(f"    [스킵] 지원하지 않는 형식: {ext}")
            return False

        # 텍스트 추출
        print(f"    텍스트 추출 중...")
        extracted = extract_text(hwpx_path)
        if not extracted:
            return False

        # 프론트매터 추가
        final = wrap_frontmatter(extracted, filepath, ext)
        out_path.write_text(final, encoding="utf-8")

    # 원본 보관
    dest_original = ORIGINALS / filepath.name
    if not dest_original.exists():
        shutil.copy2(filepath, dest_original)
        print(f"    원본 보관: {dest_original.name}")

    print(f"    완료: {out_path.name}")
    return True


def batch_ingest(source_dir: Path) -> None:
    if not source_dir.exists():
        print(f"[오류] 폴더를 찾을 수 없습니다: {source_dir}")
        sys.exit(1)

    if not check_hwpx_skill():
        sys.exit(1)

    # case-insensitive 수집 후 중복 제거 (Windows 대소문자 무감)
    seen = set()
    files = []
    for pat in ("*.hwp", "*.hwpx", "*.HWP", "*.HWPX"):
        for f in source_dir.glob(pat):
            key = f.resolve()
            if key not in seen:
                seen.add(key)
                files.append(f)

    if not files:
        print(f"[정보] {source_dir}에 HWP/HWPX 파일이 없습니다.")
        return

    print(f"\n=== HWPX 일괄 수집 시작: {len(files)}개 파일 ===")
    log(f"[HWPX-INGEST-START] 소스={source_dir}, 파일수={len(files)}")

    success = 0
    for f in files:
        if process_file(f):
            success += 1

    print(f"\n=== 완료: {success}/{len(files)}개 처리 ===")
    print(f"결과 위치: {RAW_PAPERS}")
    print(f"\n다음 단계: Claude Code에서 /llm-wiki:wiki compile 실행하세요")
    log(f"[HWPX-INGEST-DONE] 성공={success}/{len(files)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python hwpx_batch_ingest.py <폴더경로>")
        print("예시:  python hwpx_batch_ingest.py C:/Users/user/Downloads/논문모음")
        sys.exit(1)

    source = Path(sys.argv[1])
    batch_ingest(source)
