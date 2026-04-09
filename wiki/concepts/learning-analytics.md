---
type: concept
summary: 학습자 데이터를 측정·수집·분석하여 학습과 교육환경을 최적화하는 연구 및 실천
tags: [#learning-analytics, #research-methodology, #ai-education, #technology-integration]
created: 2026-04-09
updated: 2026-04-09
source-count: 14
language: both
---

# 학습 분석학 (Learning Analytics)

**요약**: 학습자와 학습 맥락에 관한 데이터를 측정·수집·분석·보고하여, 학습과 그 환경을 이해하고 최적화하기 위한 분야. (LAK 공식 정의, 2011)

---

## 정의 및 역사

**학습 분석학(Learning Analytics, LA)**은 2011년 1st International Conference on Learning Analytics and Knowledge(LAK)에서 공식 용어로 정착했다. 교육 데이터 마이닝(Educational Data Mining, EDM)과 유사하나, LA는 **실천적 개입(actionable intervention)**을 더 강조한다.

| 구분 | 학습 분석학(LA) | 교육 데이터 마이닝(EDM) |
|---|---|---|
| 목적 | 교육 개선 및 학습자 지원 | 패턴 발견 및 이론 구축 |
| 접근 | 해석적·맥락적 | 통계·알고리즘 중심 |
| 커뮤니티 | 교육공학, 교사 | 컴퓨터과학, 데이터과학 |

---

## 핵심 연구 흐름 (2026 현재)

### 1. 멀티모달 학습 분석 (Multimodal LA)
가장 빠르게 성장하는 하위 분야. 시선추적, 생체신호, 제스처, 음성 등 다양한 채널의 데이터를 통합 분석한다.
- 안면 인식 + EEG + 행동 데이터 결합
- 협동학습 중 신체적 동기화(physiological synchrony) 측정
- 관련 논문: [[raw/inbox/2026-01-13-openalex-a-systematic-review-of-multimodal-learni.md]]
- 참고: [[concepts/multimodal-learning-analytics]]

### 2. 공정성과 편향 (Fairness & Bias)
- LA 예측 모델의 민족적·사회경제적 편향 문제 급부상
- 공정 AI 원칙을 LA에 적용하는 연구 증가
- 관련 논문: [[raw/inbox/2026-02-25-openalex-learning-analytics-to-uncover-ethnic-bia.md]]
- [[raw/inbox/2026-01-18-openalex-fair-ai-in-educational-predictions--a-mu.md]]

### 3. 시뮬레이션 기반 학습에서의 LA
- 의학교육, 군사훈련 등 고위험 시뮬레이션 환경에서 LA 활용 급증
- 12개 핵심 휴리스틱 개발 (시뮬레이션 기반 전문 학습용)
- 관련 논문: [[raw/inbox/2026-03-20-openalex-12-heuristics-for-learning-analytics-in.md]]

### 4. 협동학습 분석 (Collaborative LA)
- 그룹 역동성, 공유된 메타인지, 공동 지식 구축 과정 추적
- 시간적 네트워크 분석(temporal network analysis) 방법론 적용
- 관련 논문: [[raw/inbox/2026-03-22-openalex-temporal-network-analysis-of-collaborati.md]]

### 5. 생성형 AI 역량 심화
- 21세기 역량 측정 및 분석에 LA + GenAI 결합
- 관련 논문: [[raw/inbox/2026-02-25-openalex-advancing-21st-century-professional-comp.md]]
- [[raw/inbox/2026-03-15-openalex-assessing-21st-century-competencies.md]]

---

## 방법론

학습 분석학에서 주로 사용되는 분석 방법:

```
시퀀스 분석     → 학습 경로 추적
클러스터링      → 학습자 프로파일링
네트워크 분석   → 협동학습 상호작용
예측 모델링     → 학습 위험 조기 경보
텍스트 마이닝   → 토론 게시판, 에세이 분석
멀티모달 융합   → 이종 데이터 통합
```

---

## 교육적 적용

- **조기 경보 시스템(EWS)**: 이탈 위험 학습자 식별
- **적응형 학습(Adaptive Learning)**: 개별 학습 경로 조정
- **교사 대시보드**: 수업 중 실시간 학습 상태 모니터링
- **학습 포트폴리오**: 장기 역량 성장 추적

---

## 한계 및 윤리적 쟁점

- **프라이버시 침해**: 학습 과정의 전면적 데이터화에 대한 우려
- **환원주의**: 측정 가능한 것만 가치 있다는 편향
- **예측의 자기실현**: 위험 학습자 낙인 효과
- **교사 자율성 침해**: 알고리즘이 교사 판단 대체 위험

---

## 관련 개념

- [[concepts/multimodal-learning-analytics]] — 멀티모달 LA의 심화 내용
- [[concepts/generative-ai-in-education]] — GenAI와 LA의 교차점
- [[concepts/collaborative-learning]] — 협동학습 분석의 맥락
- [[concepts/self-regulated-learning]] — SRL 과정 추적에 LA 활용
- [[methodologies/learning-analytics-methods]] — 구체적 분석 방법론

---

## 소스

- [[raw/inbox/2026-01-13-openalex-a-systematic-review-of-multimodal-learni.md]]
- [[raw/inbox/2026-01-12-openalex-tracing-scientific-reasoning-as-process.md]]
- [[raw/inbox/2026-01-20-openalex-tracking-college-student-s-learning-gain.md]]
- [[raw/inbox/2026-02-25-openalex-learning-analytics-to-uncover-ethnic-bia.md]]
- [[raw/inbox/2026-03-20-openalex-12-heuristics-for-learning-analytics-in.md]]
- [[raw/inbox/2026-03-22-openalex-temporal-network-analysis-of-collaborati.md]]
- [[raw/inbox/2026-02-26-openalex-ai-self-efficacy-and-knowledge-graph-int.md]]
