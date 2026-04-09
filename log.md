# Wiki 운용 로그

> 이 파일은 append-only (추가 전용)입니다. 기존 항목 수정 금지.

---

## 2026-04-09

- [INIT] wiki 초기화 완료
- [INIT] CLAUDE.md 스키마 v1.0 작성
- [INIT] 디렉토리 구조 생성: raw/, wiki/, outputs/, scripts/
- [INIT] 수집 스크립트 설치: openalex_collector.py, riss_collector.py, arxiv_collector.py
- [INIT] HWPX 처리 스크립트 설치: hwpx_batch_ingest.sh
- [INIT] wiki/index.md 초기 버전 생성

## 2026-04-09 (컴파일 세션)

- [COMPILE] 1차 컴파일 완료: 18개 wiki 페이지 생성
  - concepts/: generative-ai-in-education, learning-analytics, multimodal-learning-analytics,
    ai-literacy, self-regulated-learning, feedback-in-learning, virtual-reality-in-education,
    collaborative-learning, gamification-in-education, teacher-professional-development, ai-tutoring-systems
  - theories/: tpack, growth-mindset
  - methodologies/: design-based-research, systematic-review-methodology
  - researchers/: shane-dawson, fan-ouyang, gwo-jen-hwang, bertrand-schneider
  - debates/: human-vs-ai-feedback
- [COMPILE] 58개 inbox 논문 compiled: true 표시
- [UPDATE] wiki/index.md 갱신 (18페이지 목록)
- [UPDATE] DASHBOARD.md 현황 반영

## 2026-04-09 (2차 컴파일 세션)

- [COMPILE] 2차 컴파일 완료: 9개 wiki 페이지 추가 생성
  - concepts/: computational-thinking, student-engagement, equity-in-education,
    affective-computing-in-education, adaptive-learning, human-ai-collaboration, ai-ethics-in-education
  - researchers/: wanli-xing, isabel-hilliger
- [COMPILE] 나머지 117편 inbox 논문 전체 compiled: true 표시 (총 175편 완료)
- [UPDATE] wiki/index.md 갱신 (29페이지 목록)
- [UPDATE] DASHBOARD.md 현황 반영 (Phase 2 완료)
- [SCRIPT] scripts/compile_batch2.py 생성 및 실행
