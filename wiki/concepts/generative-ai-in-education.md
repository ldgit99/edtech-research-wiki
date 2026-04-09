---
type: concept
summary: LLM 등 생성형 AI를 교수학습 맥락에 적용하는 연구 및 실천 영역
tags: [#ai-education, #learning-theory, #technology-integration]
created: 2026-04-09
updated: 2026-04-09
source-count: 18
language: both
---

# 교육에서의 생성형 AI (Generative AI in Education)

**요약**: ChatGPT, Gemini 등 대규모 언어모델(LLM)을 기반으로 한 생성형 AI를 교수학습 환경에 통합하는 연구 분야. 2023년 이후 교육공학의 가장 활발한 연구 주제로 부상했다.

---

## 정의

생성형 AI(Generative AI, GenAI)는 텍스트, 이미지, 코드 등 새로운 콘텐츠를 생성할 수 있는 AI 시스템을 총칭한다. 교육 맥락에서는 주로 **대규모 언어모델(LLM)**을 활용한 챗봇, 자동 피드백 시스템, 질문 생성, 학습 동반자(learning companion) 역할로 연구된다.

---

## 핵심 연구 흐름

### 1. 학습 효과성 연구
- GenAI 피드백 vs. 교사 피드백 vs. 전문가 피드백 비교 연구가 활발
- **결과**: GenAI 피드백은 즉각성과 규모에서 우수하나, 교사/전문가 피드백의 복합적 맥락 이해에는 미치지 못함
- 관련 논문: [[raw/inbox/2026-01-13-openalex-a-comparative-study-of-expert--ai--and-n.md]]

### 2. 학습자 행위성(Learner Agency)
- GenAI가 생성한 텍스트를 학습자가 어떻게 수정·활용하는가
- 학습자 주도적 활용 시 비판적 사고 촉진 가능성
- 수동적 수용 시 학습 심화 저해 위험
- 관련 논문: [[raw/inbox/2026-01-09-openalex-learner-agency-in-revising--scp-genai--s.md]]

### 3. 자기조절학습(SRL) 지원
- GenAI 챗봇이 자기조절학습 스캐폴딩 역할 수행 가능
- 목표 설정, 모니터링, 반성 단계에서 AI 지원 효과 연구
- 관련 논문: [[raw/inbox/2026-03-15-openalex-a-gai-based-chatbot-for-scaffolding-self.md]]
- 참고: [[concepts/self-regulated-learning]]

### 4. 참여도(Engagement) 및 정서
- LLM 챗봇 지원 학습에서 **GenAI 역량**과 **정서**가 참여도의 핵심 매개변수
- 관련 논문: [[raw/inbox/2026-02-11-openalex-engagement-in-llm-chatbot-supported-lear.md]]

### 5. 부정행위(Academic Dishonesty)
- GenAI 도입 이후 2년차 부정행위 패턴 변화 추적
- 고등학생 대상 종단 연구: 활용 목적이 부정행위에서 학습 보조로 변화 추세
- 관련 논문: [[raw/inbox/2026-02-03-openalex-cheating-in-the-second-year-of-generativ.md]]

### 6. 거시적 연구 동향 (bibliometric)
- 2026년 현재 GenAI 교육 연구는 중국, 미국, 영국 중심으로 급성장
- 고등교육 > 중등교육 > 초등교육 순으로 연구 집중
- 관련 논문: [[raw/inbox/2026-01-09-openalex-generative-ai-in-higher-education--a-bib.md]]

---

## 교수설계 함의

| 설계 원칙 | GenAI 적용 방향 |
|---|---|
| 스캐폴딩 | 점진적 AI 지원 축소 (fading) 설계 |
| 피드백 | 즉각적 형성평가 제공, 교사 피드백 보완재 |
| 메타인지 | AI와의 대화를 통한 반성적 사고 유도 |
| 학습자 통제 | AI 출력을 '출발점'으로 제시, 수정 권한 부여 |

---

## 비판 및 한계

- **환각(Hallucination)**: 사실과 다른 정보 생성 위험 → 비판적 리터러시 교육 필수
- **형평성**: AI 접근성 격차(디지털 디바이드) 심화 가능성 → [[concepts/digital-divide]]
- **의존성**: 과도한 AI 의존으로 인지 역량 약화 가능성
- **개인정보**: 학습 데이터 활용 윤리 문제

---

## 관련 개념

- [[concepts/ai-literacy]] — AI 리터러시: GenAI 활용을 위한 전제 역량
- [[concepts/ai-tutoring-systems]] — AI 튜터링 시스템: GenAI의 전통적 ITS와의 관계
- [[concepts/feedback-in-learning]] — 피드백: AI 피드백의 교육적 효과
- [[concepts/self-regulated-learning]] — 자기조절학습: GenAI 스캐폴딩의 이론적 기반
- [[concepts/learning-analytics]] — 학습 분석: GenAI 활용 데이터 분석

---

## 소스

- [[raw/inbox/2026-01-09-openalex-generative-ai-in-higher-education--a-bib.md]] — 고등교육 GenAI 서지계량 분석
- [[raw/inbox/2026-01-09-openalex-learner-agency-in-revising--scp-genai--s.md]] — 학습자 행위성
- [[raw/inbox/2026-01-14-openalex-large-language-models-for-education--an.md]] — LLM 교육 오픈소스 패러다임
- [[raw/inbox/2026-01-19-openalex-generative-ai--a-double-edged-sword-for.md]] — 양날의 검: GenAI의 이중성
- [[raw/inbox/2026-02-03-openalex-cheating-in-the-second-year-of-generativ.md]] — 부정행위 종단 연구
- [[raw/inbox/2026-02-11-openalex-engagement-in-llm-chatbot-supported-lear.md]] — 참여도와 정서
- [[raw/inbox/2026-03-07-openalex-scaffolding-critical-thinking-with-gener.md]] — 비판적 사고 스캐폴딩
- [[raw/inbox/2026-02-25-openalex-potential-risks-of-generative-artificial.md]] — GenAI의 잠재적 위험
- [[raw/inbox/2026-02-25-openalex-an-empirical-longitudinal-study-of-ai-in.md]] — 교사 PCK 변화 종단 연구
