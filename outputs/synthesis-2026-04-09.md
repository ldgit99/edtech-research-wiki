---
type: synthesis
created: 2026-04-09
wiki-version: 29-pages
source-count: 184
tags: [#ai-education, #learning-analytics, #synthesis]
---

# EdTech Research 합성 분석 — 2026년 1분기

> 생성: 2026-04-09 | 기반 wiki: 29페이지 | 소스: 184편

---

## 1. 2026년 교육공학 연구의 3대 축

```
        [생성형 AI]
           △
          / \
         /   \
        /     \
[학습분석학]—[형평성·윤리]
```

2026년 상반기 교육공학 연구는 세 축을 중심으로 재편되고 있다:

1. **생성형 AI(GenAI)의 교수학습 통합**: 단순 도구 사용에서 인간-AI 협력 패러다임으로 전환
2. **학습 분석학의 심화**: 멀티모달 데이터, 과정 중심, 형평성 내재화
3. **AI 윤리·형평성**: 알고리즘 공정성, K-12 GenAI 위험, 디지털 격차

---

## 2. 핵심 교차 테마

### 테마 A: "AI는 도구인가, 파트너인가?"

- [[concepts/human-ai-collaboration]] 연구가 보여주듯, 현재 교육용 LLM은 대부분 '복종-수행-반복' 패턴에 머물고 있다 (Saqr et al., 2026)
- [[concepts/ai-tutoring-systems]]의 소크라테스식 질문법과 [[concepts/feedback-in-learning]]의 메타인지 피드백이 연결: **AI가 답을 주는 대신 생각을 유도**하는 방향으로 수렴
- [[debates/human-vs-ai-feedback]]의 잠정 결론: 정형적 도메인은 AI, 비정형은 인간, 최적은 혼합 모델

**시사점**: AI 교육 설계의 핵심 질문은 "AI가 무엇을 할 수 있는가"가 아니라 "인간의 어떤 역할을 보존해야 하는가"

---

### 테마 B: 데이터에서 형평성으로

- [[concepts/learning-analytics]]는 점점 형평성 렌즈를 내재화: 집단별 분석, 공정 예측 모델
- [[concepts/equity-in-education]]과 [[concepts/multimodal-learning-analytics]]의 교차: MMLA가 성별·언어 다양성에 따른 협력 격차를 드러냄
- [[concepts/affective-computing-in-education]]의 감정 인식 → 취약 학습자 조기 탐지의 가능성과 감시 위험의 긴장

**시사점**: "누구의" 학습 데이터인가, "누구를 위한" 분석인가를 설계 단계에서 결정해야 함

---

### 테마 C: 자기조절학습의 재발견

- [[concepts/self-regulated-learning]] ↔ [[concepts/student-engagement]]: 참여 프로파일이 SRL 전략과 높은 상관
- [[concepts/adaptive-learning]]에서 Roger Azevedo 등의 실시간 과정 데이터 활용: SRL 지원의 새로운 경로
- [[concepts/ai-tutoring-systems]]의 스캐폴딩 원칙과 SRL의 점진적 자율화가 일치

**시사점**: GenAI 환경에서 SRL은 더욱 중요해졌다. AI 의존 vs. SRL 발달의 균형이 핵심 설계 과제

---

### 테마 D: 21세기 역량의 재정의

- [[concepts/computational-thinking]] + [[concepts/ai-literacy]] + [[concepts/ai-ethics-in-education]] → "AI 시대 시민 역량" 묶음
- [[concepts/teacher-professional-development]]에서 TPACK의 확장 논의: AI 통합 교수 역량
- [[concepts/collaborative-learning]]에서 [[concepts/human-ai-collaboration]]으로: 협력의 개념 확장

**시사점**: 단일 역량보다 **역량 묶음(competency bundle)**으로 교육과정 재설계 필요

---

## 3. 연구자 네트워크 분석

| 연구자 | 핵심 주제 | 주요 협력자 |
|---|---|---|
| [[researchers/shane-dawson]] | LA, 고등교육, 21세기 역량 | Wanli Xing, Ryan Baker |
| [[researchers/fan-ouyang]] | CSCL, MMLA | Bertrand Schneider |
| [[researchers/gwo-jen-hwang]] | 모바일 학습, 게임, GenAI 피드백 | 독자적 연구팀 |
| [[researchers/bertrand-schneider]] | 생체신호 MMLA | Fan Ouyang |
| [[researchers/wanli-xing]] | 공정 AI, GenAI 에이전트 | Shane Dawson |
| [[researchers/isabel-hilliger]] | LA 제도화, 참여 측정 | Jorge Baier |

**주목할 패턴**: Shane Dawson과 Wanli Xing이 JLA를 중심으로 LA + 형평성 + GenAI를 연결하는 브리지 역할

---

## 4. 2026년 상반기 방법론 트렌드

```
[전통적 방법]              [신흥 방법]
────────────               ──────────
설문·인터뷰       →        다모달 생체신호 측정
단일 결과 변수    →        과정 데이터(로그·EEG·시선)
집단 간 비교      →        개인 내 종단 분석
단일 이론 적용    →        혼합 방법론, 계산 방법론
```

- **멀티모달 LA**가 방법론적 주류로 부상
- **과정 기반 측정**(beyond time-on-task, SRL 과정 추적)의 확산
- **계산 기반 이론(Computational Grounded Theory)**의 CSCL 적용 시작

---

## 5. 미해결 논쟁 및 연구 공백

### 아직 명확히 해결되지 않은 논쟁
1. **AI 피드백 vs. 인간 피드백**: 도메인 특정적 답변은 있지만 전반적 합의 부재 → [[debates/human-vs-ai-feedback]]
2. **GenAI의 창의성 효과**: 향상 vs. 저해, fNIRS 연구들이 혼재된 결과

### 주목할 연구 공백 (Gap)
1. **장기 효과 연구**: 대부분 단기 실험, GenAI 사용의 6개월·1년 후 효과 불명
2. **비서구권 맥락**: 연구의 80%가 서구·동아시아 중심, 글로벌 남반구 부족
3. **교사 경험 중심 연구**: 학습자 관점 연구 대비 교사 관점 연구 희소
4. **다학년 종단 연구**: 초·중·고 연결된 AI 리터러시 발달 추적 부재

---

## 6. 실천적 함의

### 교육 현장
- AI 도구 도입 전 **AI 리터러시 + 비판적 사고 교육** 선행 필요
- 피드백 설계: **혼합 모델**(AI 1차 + 교사 2차)이 비용·효과 최적
- 참여 측정: 단순 체류 시간이 아닌 **질적 참여 지표** 개발·활용

### 연구 설계
- 형평성 분석을 **사후 분석이 아닌 설계 단계**에서 통합
- 계산 방법론 도입 시 **인간-in-the-loop** 해석 단계 포함
- 단기 실험 결과 일반화 경계 명시

---

## 7. 다음 컴파일 우선순위

1. **신규 개념 후보**: `#neuroscience-education`, `#social-robots`, `#blockchain-education`
2. **신규 연구자**: Mohammed Saqr (핀란드, LA + SNA), Ryan S. Baker (CMU, AIED)
3. **신규 논쟁**: "GenAI가 창의성을 향상시키는가, 저해하는가?"
4. **합성 심화**: 연구자 협력 네트워크 그래프 분석

---

*이 합성 분석은 wiki 페이지 및 inbox 논문을 기반으로 생성되었습니다.*
*다음 합성: 새 논문 30편 이상 추가 후 재실행 권장*
