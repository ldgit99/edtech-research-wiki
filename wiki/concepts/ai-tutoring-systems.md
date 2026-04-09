---
type: concept
summary: 개별 학습자의 상태를 진단하고 적응적 피드백과 힌트를 제공하는 AI 기반 교수 시스템
tags: [#ai-education, #instructional-design, #technology-integration, #assessment]
created: 2026-04-09
updated: 2026-04-09
source-count: 6
language: both
---

# AI 튜터링 시스템 (AI Tutoring Systems)

**요약**: 학습자의 지식 상태를 모델링하고, 개별화된 문제와 피드백을 제공하며, 학습 경로를 적응적으로 조정하는 AI 기반 교수 시스템. ITS(Intelligent Tutoring Systems)가 전통 형태이며, LLM 기반 AI 튜터가 새로운 패러다임으로 등장하고 있다.

---

## 유형 및 진화

```
[1세대] 규칙 기반 ITS (1970s-90s)
   ↓ 전문가 시스템, if-then 규칙
[2세대] 베이지안 지식 추적 (1990s-2000s)
   ↓ 학습자 모델 정교화
[3세대] 딥러닝 기반 (2010s)
   ↓ 자연어 처리, 감정 인식
[4세대] LLM 기반 AI 튜터 (2023~)
   ↓ ChatGPT 등 대화형 AI 활용
```

---

## LLM 기반 AI 튜터의 특징 (2026 현재)

### 개방형 Q&A 시스템
- 대학원 수업에서 LLM 기반 오픈소스 Q&A 자동화
- 교사 부담 감소 + 즉각적 학습 지원 가능성
- 관련 논문: [[raw/inbox/2026-01-14-openalex-large-language-models-for-education--an.md]]

### AI 튜터 프라이버시 설계
- 학습 과정 모니터링과 학습자 프라이버시의 긴장
- "도와달라, 그런데 보지는 말라": 프로세스 인식 AI 튜터의 개입 타이밍·경계
- 관련 논문 (arXiv): 프로세스 인식 AI 튜터 설계

### 소크라테스식 질문법
- AI가 직접 답을 주는 대신 소크라테스식 질문으로 비판적 사고 유도
- Critical Inker: AI 글쓰기 지원에서 소크라테스식 질문 적용

---

## 적응형 교수 지원 (Adaptive Instructional Support)

- 비즈니스 시뮬레이션 게임에서 맥락 인식 대화형 에이전트
- 학습자 상태(진행도, 오류 패턴)에 따른 지원 전략 자동 조정
- 관련 논문: [[raw/inbox/2026-03-07-openalex-designing-conversational-agents-for-adap.md]]

---

## GenAI 튜터의 설계 원칙 (inbox 연구 종합)

| 원칙 | 구현 방법 |
|---|---|
| 스캐폴딩 원칙 | 완전한 답 제공 대신 힌트 → 유도 → 확인 |
| 프라이버시 존중 | 개입 타이밍 학습자가 제어 |
| 메타인지 촉진 | 답보다 과정에 대한 질문 |
| 정서 인식 | 좌절·혼란 감지 후 지원 전략 변경 |
| 형평성 고려 | 장애 학습자 포함 접근성 설계 |

---

## GenAI vs. 전통 ITS

| 차원 | 전통 ITS | LLM 기반 AI 튜터 |
|---|---|---|
| 도메인 | 특정 교과 특화 | 범용 가능 |
| 지식 베이스 | 수동 구축 | 사전 훈련 내재 |
| 자연어 이해 | 제한적 | 고수준 |
| 환각 위험 | 낮음 | 있음 |
| 맥락화 | 어려움 | 용이 |

---

## 관련 개념

- [[concepts/generative-ai-in-education]] — LLM 기반 AI 튜터의 상위 맥락
- [[concepts/feedback-in-learning]] — AI 튜터의 핵심 메커니즘
- [[concepts/self-regulated-learning]] — AI 튜터의 SRL 지원 역할

---

## 소스

- [[raw/inbox/2026-01-14-openalex-large-language-models-for-education--an.md]]
- [[raw/inbox/2026-03-07-openalex-designing-conversational-agents-for-adap.md]]
- [[raw/inbox/2026-02-03-openalex-exploring-ai-driven-learning-assistance.md]]
- [[raw/inbox/2026-03-07-openalex-scaffolding-critical-thinking-with-gener.md]]
