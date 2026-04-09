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
| **단계** | Phase 3 — 심화 확장 진행 중 |
| **wiki 페이지 총수** | **35** |
| **개념(Concepts)** | 20 |
| **이론(Theories)** | 2 |
| **방법론(Methodologies)** | 2 |
| **연구자(Researchers)** | 9 |
| **논쟁(Debates)** | 2 |
| **합성 분석** | 1편 (wiki/syntheses/) |
| **inbox 논문** | 0편 대기 (184편 전체 완료) |
| **마지막 컴파일** | 2026-04-09 |

---

## 전체 작동 흐름

```
[자동 수집]                 [컴파일 ✓]             [활용]
────────────                ──────────             ──────
OpenAlex: 132편  ──→  inbox  wiki/ 29페이지  ──→   /wiki query
arXiv: 43편      ──→  175편  ─────────────→        /kb-reflect
RISS: 0편(대기)   ✅ 전체 완료             →        슬라이드 생성
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
- [x] **[완료]** 2차 컴파일 (29페이지, 7개 신규 개념 + 2명 신규 연구자)
- [x] **[완료]** 새 논문 수집 9편 + 3차 컴파일 (33페이지, 2명 추가 연구자 + 1 논쟁 + 1 개념)
- [x] **[완료]** 합성 분석 생성 (`wiki/syntheses/synthesis-2026-04-09.md`)
- [ ] **[다음]** 주간 수집 스케줄 설정: `python scripts/collect_all.py`
- [ ] **[권장]** RISS API 키 발급 → 국내 논문 수집 시작
- [ ] **[선택]** HWP 파일 처리: `python scripts/hwpx_batch_ingest.py <폴더>`

---

## 2차 컴파일에서 추가된 내용 (2026-04-09)

### 신규 개념 페이지 (7개)
| 페이지 | 소스 수 |
|---|---|
| [[concepts/computational-thinking]] | 5 |
| [[concepts/student-engagement]] | 6 |
| [[concepts/equity-in-education]] | 5 |
| [[concepts/affective-computing-in-education]] | 5 |
| [[concepts/adaptive-learning]] | 5 |
| [[concepts/human-ai-collaboration]] | 6 |
| [[concepts/ai-ethics-in-education]] | 6 |

### 신규 연구자 페이지 (2명)
- [[researchers/wanli-xing]] — UT Arlington, 공정 AI·GenAI 에이전트
- [[researchers/isabel-hilliger]] — PUC Chile, LA 제도화·학생 성공

---

## 명령어 빠른 참조

| 목적 | 명령 |
|---|---|
| 논문 추가 수집 | `python scripts/collect_all.py` |
| HWP/HWPX 변환 | `python scripts/hwpx_batch_ingest.py <폴더>` |
| 지식 질문 | Claude Code에게 직접 질문 |
| 건전성 검사 | wiki 링크 깨진 것 확인 |
