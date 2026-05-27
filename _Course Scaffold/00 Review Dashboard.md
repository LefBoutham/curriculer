# Review Dashboard

Use this dashboard with the Dataview plugin.

## Due Reviews

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence, notes
FROM "COURSE_NAME"
WHERE (type = "study-set" OR type = "quiz") AND next_review <= date(today)
SORT next_review ASC
```

## Lesson Checkpoint

```dataview
TABLE study_status, last_studied, study_count
FROM "COURSE_NAME"
WHERE study_status = "studied"
SORT order DESC
LIMIT 5
```

## Unstudied Lessons

```dataview
TABLE order, study_status
FROM "COURSE_NAME"
WHERE study_status != "studied" AND order
SORT order ASC
```

## All Study Sets

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence
FROM "COURSE_NAME"
WHERE type = "study-set" OR type = "quiz"
SORT section ASC, type ASC
```
