---
type: concept
summary: 시선추적·생체신호·동작·음성 등 다채널 데이터를 통합하여 학습 과정을 분석하는 방법론
tags: [#learning-analytics, #research-methodology, #technology-integration]
created: 2026-04-09
updated: 2026-04-09
source-count: 7
language: both
---

# 멀티모달 학습 분석학 (Multimodal Learning Analytics)

**요약**: 시선추적, EEG, 생체신호, 음성, 제스처 등 복수의 데이터 채널을 동시에 수집·융합하여 학습 과정의 숨겨진 패턴을 발견하는 LA의 하위 분야.

---

## 정의

**멀티모달 학습 분석학(MMLA)**은 단일 데이터 소스의 한계를 넘어 이종(heterogeneous) 데이터를 통합하여 학습 과정을 전체론적으로 이해하는 방법론이다. Blikstein & Worsley(2016)가 체계화했다.

---

## 주요 데이터 채널

| 채널 | 측정 도구 | 분석 대상 |
|---|---|---|
| 시선(Gaze) | 안구추적기(eye-tracker) | 주의, 인지 부하 |
| 생체신호 | EEG, GSR, fNIRS | 각성, 인지 상태 |
| 신체 동작 | Kinect, 웨어러블 | 참여, 협동 |
| 음성·언어 | 마이크, NLP | 대화 분석, 감정 |
| 행동 로그 | LMS 로그 | 학습 전략 |
| 얼굴 표정 | 카메라+CV | 감정, 집중도 |

---

## 컴퓨터 지원 협동학습(CSCL)에서의 MMLA

inbox 논문 분석에 따르면, MMLA의 가장 활발한 적용 분야는 **컴퓨터 지원 협동학습(CSCL)**이다:

1. **공동 시각 주의(Joint Visual Attention)**: 팀원 간 동일 화면/객체 주시 여부 → 협동 품질 예측
2. **신체적 동기화(Physiological Synchrony)**: 팀원 간 생체신호 동기화 → 팀 응집력·성과와 상관
3. **체화 학습(Embodied Learning)**: 신체 움직임과 인지 학습의 연결 분석

관련 논문:
- [[raw/inbox/2026-01-13-openalex-a-systematic-review-of-multimodal-learni.md]] — CSCL에서 MMLA 체계적 검토
- [[raw/inbox/2026-01-09-openalex-physiological-synchrony-amongst-medical.md]] — 의학 시뮬레이션 신체 동기화
- [[raw/inbox/2026-02-03-openalex-connecting-joint-visual-attention--commu.md]] — 공동 시각 주의
- [[raw/inbox/2026-02-02-openalex-analyzing-embodied-learning-in-classroom.md]] — 체화 학습 AI 분석

---

## 분석 방법론

```
데이터 수집 → 전처리(동기화·세그먼트) → 특징 추출 → 융합 → 해석
               ↓
        시간적 정렬이 핵심 과제
        (다른 샘플링 레이트 조화)
```

**융합 전략**:
- **초기 융합(Early Fusion)**: 특징 추출 전 데이터 결합
- **후기 융합(Late Fusion)**: 각 채널 분석 후 결과 통합
- **하이브리드 융합**: 단계별 선택적 결합

---

## 한계 및 도전

- **기기 침습성**: 학습자 경험 방해 가능성
- **데이터 동기화**: 다채널 간 시간 정렬 기술적 복잡성
- **해석 복잡성**: 측정값 ↔ 인지 상태 간 매핑 불명확
- **생태학적 타당도**: 실험실 vs. 실제 교실 환경 차이
- **프라이버시**: 생체·얼굴 데이터의 민감성

---

## 관련 개념

- [[concepts/learning-analytics]] — MMLA의 상위 개념
- [[concepts/collaborative-learning]] — CSCL: MMLA의 주 적용 맥락
- [[concepts/virtual-reality-in-education]] — VR 환경에서의 MMLA 적용

---

## 소스

- [[raw/inbox/2026-01-13-openalex-a-systematic-review-of-multimodal-learni.md]]
- [[raw/inbox/2026-01-09-openalex-physiological-synchrony-amongst-medical.md]]
- [[raw/inbox/2026-02-03-openalex-connecting-joint-visual-attention--commu.md]]
- [[raw/inbox/2026-02-02-openalex-analyzing-embodied-learning-in-classroom.md]]
- [[raw/inbox/2026-01-29-openalex-from-heartbeats-to-actions--multimodal-l.md]]
- [[raw/inbox/2026-01-30-openalex-multimodal-perspectives-on-affective-dyn.md]]
- [[raw/inbox/2026-03-02-openalex-implementing-multimodal-learning-analyti.md]]
