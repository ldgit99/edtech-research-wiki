---
type: concept
summary: 학습자의 현재 수준·행동·맥락에 따라 학습 경로·내용·지원을 동적으로 조정하는 학습 시스템
tags: [#ai-education, #instructional-design, #learning-analytics, #assessment]
created: 2026-04-09
updated: 2026-04-09
source-count: 6
language: both
---

# 적응형 학습 (Adaptive Learning)

**요약**: 학습자의 지식 수준, 학습 속도, 선호도, 오류 패턴을 실시간 분석하여 최적화된 학습 경로와 자료를 자동 제공하는 시스템 및 설계 원칙. AI 기반 적응형 학습은 기존 규칙 기반 분기(branching)에서 ML/DL 기반 동적 개인화로 진화하고 있다.

---

## 적응형 학습의 수준

```
수준 1: 속도 적응
  - 학습자가 마스터하면 다음 단계 진행
  - Mastery Learning 기반

수준 2: 경로 적응
  - 성과에 따라 다른 콘텐츠 경로 선택
  - 의사결정 트리 또는 BKT 기반

수준 3: 콘텐츠 적응
  - 동일 개념을 다른 형태(텍스트/영상/시각화)로 제시
  - 학습 스타일·선호도 반영

수준 4: AI 동적 적응
  - 실시간 데이터로 경로+콘텐츠+난이도 동시 최적화
  - DKT(Deep Knowledge Tracing), RL 기반
```

---

## 2026년 주요 연구

### ML/DL 기반 학업 성과 예측
- 머신러닝, 딥러닝, 설명 가능한 AI(XAI)를 활용한 학생 성과 예측 종합 리뷰
- XAI: 예측 결과의 해석 가능성이 교사 신뢰에 핵심
- 관련 논문: [[raw/inbox/2026-01-23-openalex-predicting-student-performance--a-compre.md]]

### AI 자기효능감 + 지식 그래프 피드백
- 고등교육에서 AI 자기효능감이 지식 그래프 통합 GenAI 피드백 효과 조절
- Gwo-Jen Hwang 참여 연구: 학습자 AI 자기효능감에 따른 개인화 피드백 최적화
- 관련 논문: [[raw/inbox/2026-02-26-openalex-ai-self-efficacy-and-knowledge-graph-int.md]]

### 커뮤니티 중심 ITS 설계 (가치 민감적 설계)
- 커뮤니티 칼리지 학생·교수진과 함께하는 학생 중심 ITS 설계
- 가치 민감적 설계(VSD) 방법론 적용: 학습자 목소리 통합
- 관련 논문: [[raw/inbox/2026-02-19-openalex-value-sensitive-design-in-action--design.md]]

### 모델 기반 교수 실천 지원
- AI 강화 VR 교수 시뮬레이션에서 모델 기반 지원이 교사 자기효능감에 미치는 효과
- 관련 논문: [[raw/inbox/2026-02-17-openalex-model-based-support-for-teaching-practic.md]]

### 맥락 인식 대화형 에이전트 (비즈니스 시뮬레이션)
- 학습자 상태 인식 대화형 에이전트가 비즈니스 게임 학습 결과 향상
- 관련 논문: [[raw/inbox/2026-03-07-openalex-designing-conversational-agents-for-adap.md]]

---

## 핵심 기술 구성 요소

| 구성 요소 | 기능 | 알고리즘 예시 |
|---|---|---|
| **학습자 모델** | 현재 지식 상태 추정 | BKT, DKT, DKVMN |
| **도메인 모델** | 지식 구조 표현 | 지식 그래프, 온톨로지 |
| **적응 엔진** | 다음 학습 항목 선택 | 강화학습, 협력 필터링 |
| **인터페이스** | 학습자와 상호작용 | 대화형 AI, 멀티모달 UI |

---

## 설명 가능한 AI(XAI)의 중요성

- 교사·학습자가 AI 추천을 이해하고 신뢰하려면 설명 필요
- "블랙박스" 모델의 교육적 한계: 교사 전문성과의 충돌
- XAI 기법: LIME, SHAP, 어텐션 시각화

---

## 관련 개념

- [[concepts/ai-tutoring-systems]] — 적응형 학습의 대표적 구현체
- [[concepts/learning-analytics]] — 적응 결정의 데이터 기반
- [[concepts/self-regulated-learning]] — 적응 시스템과 SRL 지원
- [[concepts/feedback-in-learning]] — 적응형 피드백 메커니즘

---

## 소스

- [[raw/inbox/2026-01-23-openalex-predicting-student-performance--a-compre.md]]
- [[raw/inbox/2026-02-26-openalex-ai-self-efficacy-and-knowledge-graph-int.md]]
- [[raw/inbox/2026-02-19-openalex-value-sensitive-design-in-action--design.md]]
- [[raw/inbox/2026-02-17-openalex-model-based-support-for-teaching-practic.md]]
- [[raw/inbox/2026-03-29-openalex-matching-the-moderator-role-with-task-le.md]]
