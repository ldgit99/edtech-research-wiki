---
type: index-dynamic
created: 2026-04-09
---

# EDTECH WIKI — 동적 인덱스 (Dataview)

> Dataview 플러그인이 필요합니다. 실시간으로 wiki 상태를 반영합니다.

---

## 최근 컴파일된 페이지 (최근 30일)

```dataview
TABLE
  summary AS "요약",
  tags AS "태그",
  source-count AS "소스",
  updated AS "갱신"
FROM "03-Resources/edtech-research/wiki"
WHERE type != "index" AND type != "index-dynamic" AND type != "query-response"
SORT file.mtime DESC
LIMIT 20
```

---

## 개념 페이지 목록

```dataview
TABLE
  summary AS "요약",
  tags AS "태그",
  source-count AS "소스 수"
FROM "03-Resources/edtech-research/wiki/concepts"
SORT file.name ASC
```

---

## 이론 페이지 목록

```dataview
TABLE
  summary AS "요약",
  proposer AS "제안자",
  year AS "연도",
  paradigm AS "패러다임"
FROM "03-Resources/edtech-research/wiki/theories"
SORT year ASC
```

---

## 연구자 목록

```dataview
TABLE
  summary AS "소개",
  affiliation AS "소속",
  research-areas AS "연구 분야"
FROM "03-Resources/edtech-research/wiki/researchers"
SORT file.name ASC
```

---

## 미컴파일 소스 (inbox)

```dataview
TABLE
  journal AS "학술지",
  source AS "출처",
  publication-date AS "발행일",
  collected AS "수집일"
FROM "03-Resources/edtech-research/raw/inbox"
WHERE compiled = false
SORT collected DESC
LIMIT 30
```

---

## 최근 쿼리 응답

```dataview
TABLE
  query AS "질문",
  created AS "날짜"
FROM "03-Resources/edtech-research/wiki/queries"
SORT created DESC
LIMIT 10
```

---

## Wiki 건강 지표

```dataview
TABLE WITHOUT ID
  "전체 wiki 페이지" AS 항목,
  length(rows) AS 수
FROM "03-Resources/edtech-research/wiki"
WHERE type != "index" AND type != "index-dynamic"
FLATTEN type AS 타입
GROUP BY 타입
```
