---
type: concept
summary: 학습자의 수행에 대한 정보를 제공하여 이해를 심화하고 학습 방향을 조정하게 하는 교수학습 핵심 메커니즘
tags: [#learning-theory, #instructional-design, #ai-education, #assessment]
created: 2026-04-09
updated: 2026-04-09
source-count: 11
language: both
---

# 피드백 (Feedback in Learning)

**요약**: 학습자의 수행 결과에 대해 정보를 제공하여 오류를 교정하고, 이해를 심화하며, 후속 학습 전략을 조정하게 하는 교수학습의 핵심 요소.

---

## 정의 및 이론적 기반

Hattie & Timperley(2007)의 메타분석은 피드백을 학습에 영향을 미치는 가장 강력한 요인 중 하나로 규명했다(d=0.73). 피드백은 세 가지 핵심 질문에 답해야 한다:

1. **Where am I going?** (목표와의 거리)
2. **How am I going?** (현재 진행 상황)
3. **Where to next?** (다음 단계 방향)

---

## 피드백 유형 분류

### 지시성에 따른 분류 (2026 신흥 분류)
- **지시적 피드백(Directive)**: 오류를 직접 교정 → 즉각적 수행 향상
- **메타인지적 피드백(Metacognitive)**: 사고 과정을 반성하도록 유도 → 장기적 역량
- **혼합형(Blended)**: 두 유형의 결합이 참여도·자신감·성과에 가장 효과적
- 관련 논문: [[raw/inbox/2026-02-10-openalex-directive--metacognitive--or-a-blend-of.md]]

### 제공 주체에 따른 분류
| 유형 | 특징 | 한계 |
|---|---|---|
| 교사 피드백 | 맥락 이해 깊음, 관계적 | 즉각성·규모의 한계 |
| 전문가 피드백 | 도메인 권위 | 접근성 부족 |
| AI 피드백 | 즉각성·확장성 우수 | 맥락 이해 한계 |
| 동료 피드백 | 학습자 관점, 협동 촉진 | 품질 편차 |
| 자기 피드백 | 메타인지 촉진 | 편향 가능성 |

비교 연구 결과: 교사·전문가·AI 피드백 간 학습 성과 비교
- 관련 논문: [[raw/inbox/2026-01-13-openalex-a-comparative-study-of-expert--ai--and-n.md]]

---

## AI 피드백 연구 동향 (2026)

### 자동 작문 평가(AWE: Automatic Writing Evaluation)
- 10년간 AWE 연구 메타 합성: 효과성 분야별 편차 존재
- 관련 논문: [[raw/inbox/2026-03-04-openalex-a-meta-synthesis-of-automatic-writing-ev.md]]

### AI 동료 피드백 지원
- AI가 동료 피드백 제공을 지원하나 교사의 채택률은 낮음
- 교육학적 타당성 vs. 실제 사용 간 격차
- 관련 논문: [[raw/inbox/2026-02-12-openalex-ai-assistance-in-peer-feedback-provision.md]]

### LLM 에세이 평가 프레임워크
- 신뢰성, 정렬, 인과 추론 측면에서 LLM의 에세이 평가 역량 검토
- 관련 논문: [[raw/inbox/2026-03-07-openalex-a-framework-for-evaluation-of-large-lang.md]]

---

## 타이밍과 지연 효과

- 즉각 피드백 vs. 지연 피드백: 학습 맥락에 따라 최적 타이밍 다름
- VR 훈련에서 **지연 신호(delayed signaling)** 효과:
  절차적 기술 학습에서 즉각 피드백보다 효과적인 경우
- 관련 논문: [[raw/inbox/2026-01-14-openalex-timing-matters--using-delayed-signaling.md]]

---

## 동료 피드백과 자기 평가

- 동료 피드백 + 자기 평가 결합이 글쓰기 향상에 시너지 효과
- 관련 논문: [[raw/inbox/2026-01-27-openalex-effects-of-peer-feedback-and-self-assess.md]]

---

## 피드백의 간격 효과 (Spaced Feedback)

- 심리학적 개념 학습에서 **분산 연습(spaced instruction)**의 효과
- 대인 간 뇌 동기화(interpersonal brain synchronization)와 학습 인식 연구
- 관련 논문: [[raw/inbox/2026-01-12-openalex-spaced-instruction-for-psychological-con.md]]

---

## 비판 및 한계

- 피드백이 항상 긍정적 효과를 내지 않음 (Kluger & DeNisi, 1996: 38%는 부정적 효과)
- 학습자의 정서 상태, 자기효능감에 따라 피드백 수용 편차 큼
- AI 피드백의 일반성 vs. 개인화 간 긴장

---

## 관련 개념

- [[concepts/self-regulated-learning]] — 피드백이 SRL의 모니터링·조절 단계에 영향
- [[concepts/generative-ai-in-education]] — AI 피드백의 교육적 활용
- [[concepts/collaborative-learning]] — 동료 피드백의 맥락

---

## 소스 (최신 추가)

### 사회적·시간적 비교 피드백
- 부정적 피드백 자체는 괜찮지만 사회적·시간적 비교를 동시에 제공하면 성과 저하
- 관련 논문: [[raw/inbox/2026-04-02-openalex-negative-feedback-is-fine--but-don-t-mix.md]]

---

## 소스

- [[raw/inbox/2026-01-13-openalex-a-comparative-study-of-expert--ai--and-n.md]]
- [[raw/inbox/2026-02-10-openalex-directive--metacognitive--or-a-blend-of.md]]
- [[raw/inbox/2026-01-14-openalex-timing-matters--using-delayed-signaling.md]]
- [[raw/inbox/2026-01-27-openalex-effects-of-peer-feedback-and-self-assess.md]]
- [[raw/inbox/2026-03-04-openalex-a-meta-synthesis-of-automatic-writing-ev.md]]
- [[raw/inbox/2026-02-12-openalex-ai-assistance-in-peer-feedback-provision.md]]
- [[raw/inbox/2026-03-07-openalex-a-framework-for-evaluation-of-large-lang.md]]
- [[raw/inbox/2026-01-12-openalex-spaced-instruction-for-psychological-con.md]]
- [[raw/inbox/2026-03-03-openalex-feedback-source-and-target-matter--stude.md]]
