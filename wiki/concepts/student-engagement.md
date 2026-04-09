---
type: concept
summary: 학습자가 학습 활동에 인지적·행동적·정서적으로 참여하는 정도 및 과정
tags: [#learning-analytics, #self-regulated-learning, #assessment, #higher-education]
created: 2026-04-09
updated: 2026-04-09
source-count: 6
language: both
---

# 학습자 참여 (Student Engagement)

**요약**: 학습자가 학습 활동에 투자하는 에너지·노력·관심의 총체. Fredricks et al.(2004)의 3차원 모델(행동적·인지적·정서적 참여)이 널리 사용되며, 디지털 학습 환경에서는 학습 분석학을 통해 다차원 참여를 자동 측정하는 연구가 활발하다.

---

## 참여의 3차원 모델

```
┌─────────────────────────────────┐
│        학습자 참여               │
├─────────┬──────────┬────────────┤
│ 행동적   │ 인지적   │ 정서적     │
│ 출석, 과제│ 전략 사용│ 흥미, 귀속감│
│ 시간 투자 │ 메타인지 │ 불안, 기쁨 │
└─────────┴──────────┴────────────┘
```

---

## 2026년 주요 연구 결과

### 모바일 앱 참여 프로파일 연구
- 학습 앱에서 참여 패턴 클러스터링 → 4개 프로파일 식별
- 참여 프로파일 ↔ 자기조절학습(SRL) ↔ 학업 성과 연결
- 단순 사용 시간보다 참여의 질·패턴이 예측력 높음
- 관련 논문: [[raw/inbox/2026-01-21-openalex-student-engagement-profiles-in-a-mobile.md]]

### 학습 분석학의 단기·장기 효과
- 소셜 어노테이션에서 LA 피드백: 단기 참여 향상, 장기 지속 효과 불명확
- "단기 이득, 장기 격차" 문제: LA 개입의 지속 가능성 질문
- 관련 논문: [[raw/inbox/2026-02-17-openalex-short-term-gains--long-term-gaps--unpack.md]]

### 과제 시간 초월 지표 (Beyond Time on Task)
- 시간 기반 측정의 한계: 체류 시간 ≠ 실제 참여
- JLA: 학습 과정의 질적 참여 지표 개발 방향 제안
- 관련 논문: [[raw/inbox/2026-03-18-openalex-beyond-time-on-task.md]]

### LLM 챗봇 기반 학습에서의 참여
- GenAI 역량 및 감정이 LLM 챗봇 지원 학습의 참여에 핵심 역할
- 챗봇 사용 중 감정 조절·메타인지가 참여 결정 요인
- 관련 논문: [[raw/inbox/2026-02-12-openalex-integrating-artificial-intelligence-and.md]]

---

## 디지털 환경에서의 참여 측정

| 측정 방법 | 데이터 소스 | 측정 차원 |
|---|---|---|
| 클릭스트림 분석 | LMS 로그 | 행동적 |
| 자연어 처리 | 토론 게시물 | 인지적·정서적 |
| 생체신호 | EEG, fNIRS, 심박 | 정서적·인지적 |
| 멀티모달 | 카메라+생체+로그 | 복합 |

---

## 참여와 자기조절학습의 관계

- 높은 참여 → SRL 전략 활성화 → 심층 학습 (선순환)
- 참여 저하 → 표면 전략·회피 → 성과 저하
- AI 도구 과의존 시 인지 참여 감소 가능성 (비판적 성찰 필요)

---

## 관련 개념

- [[concepts/self-regulated-learning]] — 참여와 SRL의 상호 강화
- [[concepts/learning-analytics]] — 참여 데이터 수집·분석
- [[concepts/feedback-in-learning]] — 피드백이 참여에 미치는 영향
- [[concepts/gamification-in-education]] — 게임 요소와 행동적 참여

---

## 소스

- [[raw/inbox/2026-01-21-openalex-student-engagement-profiles-in-a-mobile.md]]
- [[raw/inbox/2026-02-17-openalex-short-term-gains--long-term-gaps--unpack.md]]
- [[raw/inbox/2026-03-18-openalex-beyond-time-on-task.md]]
- [[raw/inbox/2026-02-12-openalex-integrating-artificial-intelligence-and.md]]
- [[raw/inbox/2026-02-17-openalex-exploring-the-impact-of-students--intera.md]]
- [[raw/inbox/2026-03-07-openalex-longitudinal-relationships-between-stude.md]]
