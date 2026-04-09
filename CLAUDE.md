# EDTECH RESEARCH WIKI — 스키마 및 관행 v1.0

> 이 파일은 인간(연구자)만 수정할 수 있다. LLM은 읽기만 한다.  
> 마지막 수정: 2026-04-09

---

## 목적

교육공학 이론, 연구방법론, 핵심 연구자, 학술 논쟁을 추적하는
**자기유지형(self-maintaining) 지식베이스**. 국내외 교육공학 학술 문헌을
수집·컴파일하여 복잡한 연구 질문에 즉각 응답할 수 있는 지식 구조를 구축한다.

---

## 디렉토리 레이아웃

```
raw/papers/     : 학술 논문 마크다운 변환본 (읽기 전용)
raw/articles/   : 웹 아티클 클리핑 (읽기 전용)
raw/conference/ : 학회 발표 자료 (읽기 전용)
raw/transcripts/: 강의·강연 트랜스크립트 (읽기 전용)
raw/inbox/      : 자동 수집 미처리 대기 (컴파일 전 검토)
raw/pending/    : 관련성 검토 대기
raw/rejected/   : 제외된 문서
raw/attachments/: 이미지, 도표 및 HWP/HWPX 원본
wiki/           : LLM이 생성·유지하는 모든 파일 (이 폴더만 수정 가능)
outputs/        : 보고서, 슬라이드, 시각화 결과물
scripts/        : 수집·변환 자동화 스크립트
```

---

## wiki 페이지 유형 및 프론트매터

### 개념 페이지 (`wiki/concepts/*.md`)

```yaml
---
type: concept
summary: <한 문장 정의 (50자 이내)>
tags: [#learning-theory, #design-principle, #assessment]
created: YYYY-MM-DD
updated: YYYY-MM-DD
source-count: <참조한 raw/ 소스 수>
language: [ko, en, both]
---
```

**필수 섹션**: 정의 / 핵심 원칙 / 이론적 맥락 / 관련 개념 / 비판 및 한계 / 소스

### 연구자 페이지 (`wiki/researchers/*.md`)

```yaml
---
type: researcher
summary: <연구자 한 줄 소개>
affiliation: <소속 기관>
research-areas: [<분야1>, <분야2>]
nationality: [ko, us, uk, ...]
active-period: YYYY-YYYY
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**필수 섹션**: 핵심 기여 / 주요 저작 / 이론적 입장 / 관련 연구자 / 소스

### 이론 페이지 (`wiki/theories/*.md`)

```yaml
---
type: theory
summary: <이론 한 줄 설명>
proposer: <제안자>
year: YYYY
paradigm: [cognitive, behaviorist, constructivist, connectivist, social]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

**필수 섹션**: 핵심 명제 / 학습 원칙 / 교수설계 함의 / 실증 근거 / 비판 / 관련 이론

### 방법론 페이지 (`wiki/methodologies/*.md`)

```yaml
---
type: methodology
summary: <방법론 한 줄 설명>
paradigm: [qualitative, quantitative, mixed, design-based]
data-type: [text, numeric, mixed, artifact]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 논쟁 페이지 (`wiki/debates/*.md`)

```yaml
---
type: debate
summary: <논쟁 핵심 한 줄>
status: [ongoing, resolved, superseded]
positions: [position-a, position-b]
key-figures: [researcher1, researcher2]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### 쿼리 응답 페이지 (`wiki/queries/*.md`)

```yaml
---
type: query-response
query: "<원래 질문>"
sources-used: [wiki/concepts/..., wiki/theories/...]
created: YYYY-MM-DD
---
```

### 합성 분석 페이지 (`wiki/syntheses/*.md`)

```yaml
---
type: synthesis
summary: <합성 주제 한 줄>
themes: [theme1, theme2]
source-count: <분석한 소스 수>
created: YYYY-MM-DD
---
```

---

## 컴파일 규칙

1. **원자성**: 각 wiki 페이지는 하나의 개념/엔티티/이론만 다룬다
2. **출처 인용**: 모든 주장에 `[[raw/papers/filename]]` 소스 링크 포함
3. **교차참조 우선**: 기존 wiki 페이지와 가능한 많이 `[[wikilink]]` 연결
4. **갱신 우선**: 새 페이지 생성 전 기존 페이지 갱신 여부 반드시 확인
5. **모순 분리**: 소스 간 상충 주장은 `wiki/debates/` 페이지로 별도 생성
6. **날짜 형식**: ISO 8601 (YYYY-MM-DD) 엄수
7. **태그 어휘**: 새 태그 도입 시 `wiki/index.md` 태그 섹션에 등록
8. **한국어 논문**: 영문 키워드도 함께 기재 (국제 연결을 위해)
9. **이미지**: `raw/attachments/` 에서 참조, 직접 복사 금지
10. **파일명**: 소문자, 하이픈 구분, 공백 없음 (예: `connectivism-theory.md`)

---

## HWPX 처리 규칙

- `.hwp` 파일: `scripts/convert_hwp.py` → `.hwpx` 변환 후 `text_extract.py` 실행
- `.hwpx` 파일: 직접 `text_extract.py` 실행 (`--format markdown`)
- 추출된 마크다운: `raw/papers/` 또는 `raw/conference/` 에 저장
- 원본 `.hwp/.hwpx` 파일: `raw/attachments/originals/` 에 반드시 보관
- 보고서 출력 요청 시: `templates/report/` 템플릿 사용
- 공문서 출력 요청 시: `templates/gonmun/` + Workflow G 적용
- 모든 HWPX 생성 후: `fix_namespaces.py` 필수 실행

---

## 쿼리 운용 규칙

1. `wiki/index.md` 탐색 → 관련 wiki 페이지 식별
2. 관련 페이지 전체 독해 (요약만 읽지 말 것)
3. 응답에 wiki 페이지 인용: `[[concepts/connectivism]]`
4. 유용한 응답은 `wiki/queries/YYYY-MM-DD-<slug>.md` 로 저장
5. 답을 모르거나 소스 부족 시: 지식 갭을 명시하고 수집 방향 제안

---

## 린트 규칙

- 데드 링크 자동 수정
- 소스 없는 주장 표시: `[출처 필요]`
- 6개월 이상 미갱신 페이지: `[검토 필요]` 태그 추가
- 5개 미만 링크를 가진 개념 페이지: 고아 경고 발생
- `compiled: false` 프론트매터를 가진 `raw/inbox/` 파일: 컴파일 대상으로 표시

---

## 절대 금지 사항

- `raw/` 내 파일 수정 절대 금지 (읽기 전용)
- 이 `CLAUDE.md` 파일 수정 금지 (인간만 수정 가능)
- 인간이 직접 작성한 `01-Personal/` 노트 접근 금지
- Git 커밋 없이 wiki 대규모 변경 금지
- 출처 없는 사실 주장 생성 금지 (환각 방지)

---

## 태그 어휘 (등록된 태그)

```
#learning-theory        학습이론
#design-principle       교수설계 원칙
#instructional-design   교수설계
#assessment             평가
#technology-integration 기술 통합
#higher-education       고등교육
#k12                    초중등교육
#research-methodology   연구방법론
#qualitative            질적 연구
#quantitative           양적 연구
#mixed-methods          혼합 연구
#ai-education           AI 교육 활용
#learning-analytics     학습 분석학
#constructivism         구성주의
#connectivism           연결주의
#behaviorism            행동주의
#cognitivism            인지주의
#self-regulated-learning 자기조절학습
#collaborative-learning 협동학습
#distance-education     원격교육
#korean-education       한국 교육
```
