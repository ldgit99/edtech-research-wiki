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
- [2026-04-09 21:33] [COLLECT-START] days_back=7
- [2026-04-09 21:33] [COLLECT-DONE] 신규=9편, inbox총=184편

## 2026-04-09 (수집 및 합성 세션)

- [COLLECT] collect_all.py 실행: 신규 9편 수집 (OpenAlex 10편 시도, arXiv 43편 시도)
  - inbox 총계: 175 → 184편
- [COMPILE] 신규 9편 compiled: true 표시 (전체 184편 완료)
- [UPDATE] wiki 페이지 소스 수 갱신 (feedback+2, gamification+1, adaptive+1, human-ai+1, ai-tutoring+1)
- [SYNTHESIS] outputs/synthesis-2026-04-09.md 생성 (크로스 테마 합성 분석)

## 2026-04-09 (3차 컴파일 세션)

- [COMPILE] 3차 컴파일 완료: 4개 wiki 페이지 추가 생성
  - concepts/: neuroscience-in-education
  - researchers/: mohammed-saqr, ryan-baker
  - debates/: genai-and-creativity
- [UPDATE] wiki/syntheses/synthesis-2026-04-09.md 생성 (합성 분석 공식 위치 등록)
- [UPDATE] wiki/index.md 갱신 (33페이지, 8명 연구자, 2개 논쟁)
- [UPDATE] DASHBOARD.md Phase 3 반영

## 2026-04-09 (4차 확장 세션)

- [COMPILE] 4차 확장: 2개 wiki 페이지 추가 생성
  - concepts/: social-robots-in-education
  - researchers/: dragan-gasevic
- [FIX] 깨진 wikilink 1개 수정 (learning-analytics.md, shane-dawson.md)
- [UPDATE] wiki/index.md 갱신 (35페이지, 연구자 9명)
- [UPDATE] DASHBOARD.md Phase 3 반영
- [2026-04-09 21:50] [HWPX-INGEST-START] 소스=D:\OneDrive\Documents\Obsidian Vault\03-Resources\edtech-research\raw\attachments\test-folder, 파일수=2
- [2026-04-09 21:50] [HWPX-INGEST-DONE] 성공=0/2
- [2026-04-09 21:51] [HWPX-INGEST-START] 소스=raw\attachments\test-folder, 파일수=2
- [2026-04-09 21:51] [HWPX-INGEST-DONE] 성공=2/2
- [2026-04-09 21:51] [HWPX-INGEST-START] 소스=raw\attachments\test-folder, 파일수=2
- [2026-04-09 21:51] [HWPX-INGEST-DONE] 성공=2/2
- [2026-04-09 21:52] [HWPX-INGEST-START] 소스=raw\attachments, 파일수=1
- [2026-04-09 21:52] [HWPX-INGEST-DONE] 성공=1/1

## 2026-04-09 (HWPX 파이프라인 수정)

- [FIX] hwpx_batch_ingest.py: extract_text()에서 subprocess stdout 인코딩 버그 수정
  (Windows CP949/UTF-8 충돌 → 임시 파일 경유 방식으로 변경)
- [FIX] hwpx_batch_ingest.py: 테이블 셀 중복 출력 제거 (dedup_nested_lines 추가)
- [FIX] hwpx_batch_ingest.py: Windows 대소문자 glob 중복 처리
- [IMPROVE] wrap_frontmatter: 파일명 대신 문서 첫 줄을 제목으로 사용
- [TEST] MD→HWPX→MD 파이프라인 전체 검증 완료 (한국어 정상 추출 확인)
