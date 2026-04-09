---
type: concept
summary: 사회적 배경·장애·지역·언어에 관계없이 양질의 교육 기회를 보장하는 원칙과 실천
tags: [#k12, #higher-education, #ai-education, #instructional-design]
created: 2026-04-09
updated: 2026-04-09
source-count: 5
language: both
---

# 교육 형평성 (Equity in Education)

**요약**: 모든 학습자가 출발점의 차이를 극복하고 의미 있는 학습 결과에 도달할 수 있도록 자원·지원·기회를 차별 배분하는 원칙. 형평성(equity)은 동등함(equality)과 구분되며, 디지털 전환 시대에는 기술 접근성·알고리즘 편향·글로벌 남북 격차가 새로운 형평성 이슈로 부상했다.

---

## 주요 형평성 차원

### 1. 디지털 격차 (Digital Divide)
- 디지털·비디지털 읽기 개입이 독일 초등학교 학습 격차에 미치는 영향
- 디지털 도구가 격차를 좁히는가, 넓히는가 — 실증적 검증 필요
- 관련 논문: [[raw/inbox/2026-02-11-openalex-bridging-the-digital-divide--effects-of.md]]

### 2. 알고리즘 공정성 (Algorithmic Fairness)
- 교육 예측 AI에서 다집단 공정성: 강화학습 기반 Fair AI 접근
- 성별·인종·사회경제적 배경에 따른 예측 편향 제거
- 관련 논문: [[raw/inbox/2026-01-18-openalex-fair-ai-in-educational-predictions--a-mu.md]]

### 3. 장애 학습자 포용
- 생성형 AI가 장애 학생의 학습 주도성(agency)을 지원하는가?
- 호주 중등학교 사례: AI가 접근성 도구로 기능하는 조건 탐색
- 관련 논문: [[raw/inbox/2026-01-24-openalex-can-generative--scp-ai--scp--support-the.md]]

### 4. 글로벌 남반구 (Global South)
- 시에라리온 초등 EdTech 개입의 차이이중차분(DiD) 연구
- 자원 부족 환경에서 기술 보조 학습의 실제 효과 검증
- 관련 논문: [[raw/inbox/2026-04-02-openalex-assessing-different-implementation-modal.md]]

### 5. 성별·언어 다양성 (MMLA 관점)
- MMLA를 통한 협력학습에서 성별·언어 다양성에 따른 참여 격차 분석
- 포용적 학습 분석을 위한 다집단 분석 방법론 제안
- 관련 논문: [[raw/inbox/2026-01-18-openalex-toward-an-inclusive-understanding-of-col.md]]

---

## 형평성과 AI의 긴장 관계

```
AI의 잠재적 기여          AI의 잠재적 위협
──────────────────        ──────────────────
개인화된 지원 확장   ←→   편향된 알고리즘 예측
저비용 교육 기회     ←→   디지털 인프라 의존
장애인 접근성 도구   ←→   다중 장벽 제거 미흡
글로벌 자료 접근     ←→   영어 중심 지식 편향
```

---

## Fair AI 설계 원칙

| 원칙 | 정의 | 구현 방법 |
|---|---|---|
| **개인 공정성** | 유사한 개인에게 유사한 결과 | 거리 기반 공정성 메트릭 |
| **집단 공정성** | 집단 간 예측 오류 균등 | 다집단 강화학습 최적화 |
| **처우 공정성** | 보호 속성 기반 차별 없음 | 보호 변수 제거/분리 |
| **반사실적 공정성** | 반사실 상황에서도 동일 결과 | 인과 추론 기반 모델 |

---

## 관련 개념

- [[concepts/learning-analytics]] — 형평성 분석을 위한 LA 도구
- [[concepts/multimodal-learning-analytics]] — 다집단 MMLA 방법론
- [[concepts/ai-literacy]] — 형평한 AI 리터러시 교육
- [[concepts/collaborative-learning]] — 다양성 포용적 협력학습

---

## 소스

- [[raw/inbox/2026-02-11-openalex-bridging-the-digital-divide--effects-of.md]]
- [[raw/inbox/2026-01-18-openalex-fair-ai-in-educational-predictions--a-mu.md]]
- [[raw/inbox/2026-01-24-openalex-can-generative--scp-ai--scp--support-the.md]]
- [[raw/inbox/2026-04-02-openalex-assessing-different-implementation-modal.md]]
- [[raw/inbox/2026-01-18-openalex-toward-an-inclusive-understanding-of-col.md]]
