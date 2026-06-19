# Review Dashboard

YAML frontmatter is the source of truth for review state. Use this dashboard with the Dataview plugin as a convenience, not as required course infrastructure.

After copying the scaffold, replace `COURSE_NAME` with the copied course folder path used by Dataview.

## Manual Review Queue

Use this table when Dataview is unavailable.

| Artifact | Type | Status | Last Reviewed | Next Review | Confidence | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `01 Section Template/exercises/Exercises.md` | exercises | not started | | | | |
| `01 Section Template/flashcards/Flashcards.md` | study-set | not started | | | | |
| `01 Section Template/quizes/Quiz.md` | quiz | not started | | | | |

## Due Reviews

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence, notes
FROM "COURSE_NAME"
WHERE (type = "exercises" OR type = "study-set" OR type = "quiz") AND next_review <= date(today)
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

## All Reviewable Sets

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence
FROM "COURSE_NAME"
WHERE type = "exercises" OR type = "study-set" OR type = "quiz"
SORT section ASC, type ASC
```

## Missing Review Dates

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence, notes
FROM "COURSE_NAME"
WHERE (type = "exercises" OR type = "study-set" OR type = "quiz") AND status != "not started" AND !next_review
SORT section ASC, type ASC
```

## Lowest Confidence

```dataview
TABLE status, last_reviewed, next_review, review_count, confidence, notes
FROM "COURSE_NAME"
WHERE (type = "exercises" OR type = "study-set" OR type = "quiz") AND confidence
SORT confidence ASC, next_review ASC
LIMIT 10
```

## Weak Spot Notes

```dataview
TABLE status, last_reviewed, next_review, confidence, notes
FROM "COURSE_NAME"
WHERE (type = "exercises" OR type = "study-set" OR type = "quiz") AND notes
SORT next_review ASC
```
