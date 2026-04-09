---
type: dashboard
updated: 2026-04-09
---

# EdTech Research Wiki — 대시보드

> Obsidian에서 Dataview 플러그인이 활성화되어 있으면 아래 표가 자동 갱신됩니다.

---

## 현재 상태

| 항목 | 값 |
|---|---|
| **단계** | Phase 1 — 초기 컴파일 완료 ✓ |
| **wiki 페이지 총수** | **18** |
| **개념(Concepts)** | 11 |
| **이론(Theories)** | 2 |
| **방법론(Methodologies)** | 2 |
| **연구자(Researchers)** | 4 |
| **논쟁(Debates)** | 1 |
| **inbox 대기 논문** | 175편 (추가 컴파일 필요) |
| **마지막 컴파일** | 2026-04-09 |

---

## 전체 작동 흐름

```
[자동 수집]                 [컴파일 ✓]             [활용]
────────────                ──────────             ──────
OpenAlex: 132편  ──→  inbox  wiki/ 18페이지         /wiki query
arXiv: 43편      ──→  175편  ─────────────→        /kb-reflect
RISS: 0편(대기)           (추가 실행 필요)          슬라이드 생성
HWP 파일        ──→                                HWPX 보고서
       ↑                            ↓
  collect_all.py              git 자동 커밋
```

---

## Wiki 페이지 현황 (Dataview)

### 유형별 페이지 수

```dataview
TABLE WITHOUT ID
  type AS "유형",
  length(rows) AS "페이지 수"
FROM "03-Resources/edtech-research/wiki"
WHERE type != "index" AND type != "dashboard" AND type != "index-dynamic"
GROUP BY type
SORT length(rows) DESC
```

### 최근 생성/갱신 페이지

```dataview
TABLE
  summary AS "요약",
  type AS "유형"
FROM "03-Resources/edtech-research/wiki"
WHERE type != "index" AND type != "dashboard" AND type != "index-dynamic"
SORT file.mtime DESC
LIMIT 15
```

---

## 수집 현황

### 소스별 수집 편수

```dataview
TABLE WITHOUT ID
  source AS "소스",
  length(rows) AS "수집 편수"
FROM "03-Resources/edtech-research/raw/inbox"
GROUP BY source
SORT length(rows) DESC
```

### inbox 최신 논문 (미컴파일)

```dataview
TABLE
  journal AS "학술지",
  publication-date AS "발행일"
FROM "03-Resources/edtech-research/raw/inbox"
WHERE compiled = false
SORT publication-date DESC
LIMIT 15
```

---

## 지식 네트워크 밀도

```dataview
TABLE WITHOUT ID
  file.name AS "페이지",
  length(file.outlinks) AS "아웃링크",
  length(file.inlinks) AS "인링크"
FROM "03-Resources/edtech-research/wiki"
WHERE type != "index" AND type != "dashboard"
SORT length(file.inlinks) DESC
LIMIT 10
```

---

## 다음 할 일

- [x] **[완료]** 초기 wiki 컴파일 (18페이지 생성)
- [ ] **[다음]** 추가 논문 175편 컴파일 (개념·연구자 확장)
- [ ] **[권장]** RISS API 키 발급 → 국내 논문 수집 시작
- [ ] **[선택]** HWP 파일 처리: `python scripts/hwpx_batch_ingest.py <폴더>`
- [ ] **[월간]** `/kb-reflect` 실행 → 합성 분석 생성

---

## 명령어 빠른 참조

| 목적 | 명령 |
|---|---|
| 논문 추가 수집 | `python scripts/collect_all.py` |
| HWP/HWPX 변환 | `python scripts/hwpx_batch_ingest.py <폴더>` |
| 지식 질문 | Claude Code에게 직접 질문 |
| 건전성 검사 | wiki 링크 깨진 것 확인 |
