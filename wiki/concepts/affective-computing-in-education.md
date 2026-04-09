---
type: concept
summary: 학습자의 감정·생리적 상태를 인식·해석하여 학습 지원에 활용하는 기술 및 연구 영역
tags: [#multimodal-learning-analytics, #ai-education, #learning-analytics, #instructional-design]
created: 2026-04-09
updated: 2026-04-09
source-count: 5
language: both
---

# 교육에서의 감정 컴퓨팅 (Affective Computing in Education)

**요약**: Rosalind Picard(1997)가 제안한 감정 컴퓨팅(Affective Computing)의 교육 응용. 학습자의 표정·음성·생체신호·행동 패턴을 AI가 실시간 분석하여 감정 상태(불안, 몰입, 혼란, 좌절)를 추론하고 개인화된 학습 개입을 제공하는 연구 영역.

---

## 주요 감지 기술

| 기술 | 측정 대상 | 교육 적용 |
|---|---|---|
| **fNIRS** | 전전두엽 혈류 (인지 부하) | 창의적 사고 학습 모니터링 |
| **EEG 하이퍼스캐닝** | 뇌파 동기화 | 대학생 학습 이득 추적 |
| **안면 표정 인식** | 7가지 기본 감정 | 창의성 학습에서 감정 변화 |
| **생리적 동기화** | 심박·피부전도 | 의대생 협력 훈련 평가 |
| **음성 분석** | 피치·속도·감정 톤 | 온라인 수업 참여도 |

---

## 2026년 주요 연구

### 신경과학 + AI가 피드백에 미치는 영향
- 체계적 문헌 검토: 신경과학적 피드백 메커니즘과 AI 피드백의 교차
- 도파민·보상 회로와 즉각 피드백의 연결 이해
- 관련 논문: [[raw/inbox/2026-01-16-openalex-the-impact-of-neuroscience-and-artificia.md]]

### GenAI의 창의적 사고 효과 (fNIRS + 안면 표정)
- fNIRS와 안면 표정 분석을 동시 활용한 창의성 학습 연구
- GenAI가 "양날의 검": 창의성 향상 vs. 인지 부하 증가
- 관련 논문: [[raw/inbox/2026-01-19-openalex-generative-ai--a-double-edged-sword-for.md]]

### 고등교육에서의 감정 AI 체계적 고찰
- Internet and Higher Education 게재: 감정 AI 적용 현황·과제 검토
- 주요 과제: 프라이버시, 편향, 감정 표현의 문화적 차이
- 관련 논문: [[raw/inbox/2026-02-26-openalex-emotional-artificial-intelligence-in-hig.md]]

### ITS에서의 감정 다이나믹스 (멀티모달)
- 지능형 교수 시스템에서 학습자 감정의 시계열 패턴 분석
- 좌절→몰입→성취 전환 과정의 멀티모달 신호 매핑
- 관련 논문: [[raw/inbox/2026-01-31-openalex-how-knowledge-structures-transform-into.md]]

### 의대생 생리적 동기화
- 의대 위기 관리 시뮬레이션에서 팀 생리적 동기화
- 리더 성과와 팀원 생리 신호 동기화 간의 관계
- 관련 논문: [[raw/inbox/2026-01-13-openalex-interleaved-practice-in-physics-benefits.md]]

---

## 설계 고려사항

### 윤리적 쟁점
```
감정 AI 교육 적용의 딜레마
┌──────────────────────────┐
│ 잠재적 이점               │
│ • 조기 개입 가능           │
│ • 개인화 최적화             │
│ • 학습 난이도 조절          │
└──────────────────────────┘
        ↕ 긴장
┌──────────────────────────┐
│ 우려 사항                 │
│ • 지속 감시 불안감          │
│ • 감정 데이터 프라이버시     │
│ • 문화적 편향 (서구 중심)    │
│ • 감정 인식 정확도 한계      │
└──────────────────────────┘
```

---

## 관련 개념

- [[concepts/multimodal-learning-analytics]] — 감정 데이터의 MMLA 통합
- [[concepts/feedback-in-learning]] — 감정 인식 기반 적응 피드백
- [[concepts/ai-tutoring-systems]] — 감정 인식 ITS 설계
- [[concepts/self-regulated-learning]] — 감정 조절과 SRL의 연계

---

## 소스

- [[raw/inbox/2026-01-16-openalex-the-impact-of-neuroscience-and-artificia.md]]
- [[raw/inbox/2026-01-19-openalex-generative-ai--a-double-edged-sword-for.md]]
- [[raw/inbox/2026-02-26-openalex-emotional-artificial-intelligence-in-hig.md]]
- [[raw/inbox/2026-01-20-openalex-tracking-college-student-s-learning-gain.md]]
- [[raw/inbox/2026-02-24-openalex-enhancing-inhibition-ability-through-sit.md]]
