# Course Agent Instructions

This folder is an Obsidian course scaffold. It is meant to be copied, renamed, and filled in for a specific course.

Do not record real learner progress in this scaffold folder. Learner `last_reviewed`, `next_review`, `review_count`, `confidence`, `last_studied`, or `study_count` values belong only in copied courses.

## Mission

Help the learner build and study a coherent course. Preserve the course language in `CONTEXT.md`, generate useful lesson material, and keep exercises, flashcards, and quizzes aligned with the actual curriculum.

## Required Context Files

- Read `CONTEXT.md` before making structural or terminology changes.
- Use `00 Course Setup Grill.md` when the course direction is unclear.
- Use `docs/adr/` only for hard-to-reverse, surprising, trade-off-driven decisions.

## Course Structure

- `00 Curriculum Index.md` is the course map.
- `Glossary/00 Glossary Index.md` is the learner-facing term index.
- Numbered folders are course sections.
- Each numbered section should contain lesson notes plus:
  - `exercises/Exercises.md`
  - `flashcards/Flashcards.md`
  - `quizes/Quiz.md`
  - `quizes/Quiz.html`
- `_attachments/` is for course assets and source files.
- `_attachments/00 Source Index.md` is for trusted source material.

## Glossary

The glossary starts empty. Add terms only when the learner asks for a term to be added or when a term has become important enough to deserve a stable learner-facing definition.

Keep `CONTEXT.md` and `Glossary/` distinct:

- `CONTEXT.md` defines the course-building language and domain boundaries for LLMs.
- `Glossary/` defines course subject terms for the learner.

When adding a glossary term:

1. Create `Glossary/Term Name.md`.
2. Add a concise definition at the top.
3. Add examples, related terms, and source links only when useful.
4. Add an entry to `Glossary/00 Glossary Index.md` in this format:

```md
- [[Term Name]] — one-line meaning.
```

When the learner asks to link a term, update meaningful mentions in course files to point to the glossary note:

```md
[[Glossary/Term Name|Term Name]]
```

Do not link every repeated occurrence mechanically. Link the first meaningful occurrence in a section or any occurrence where the learner is likely to want the definition.

## Lesson Progress Metadata

Use lesson frontmatter to track the learner's most recent checkpoint. This is separate from spaced repetition.

Lesson frontmatter:

```yaml
---
title: "Lesson Title"
section: "01 Section Name"
source:
order: 1.1
type: lesson
study_status: not started
last_studied:
study_count: 0
prerequisites:
depends_on:
mastery_evidence:
---
```

Allowed `study_status` values:

- `not started`
- `studied`

When a lesson has been covered in a study session:

- Set `study_status: studied`.
- Set `last_studied` to today's date in `YYYY-MM-DD`.
- Increment `study_count` by 1.

The LLM should update lesson progress frontmatter directly at the end of a study session when the learner has gone through the lesson. This progress update is separate from exercise, flashcard, or quiz review scheduling.

Use lesson progress metadata to find the learner's most recent checkpoint. Keep spaced repetition scheduling on exercises, flashcards, and quizzes unless the learner asks for per-lesson review scheduling.

## Spaced Repetition Metadata

Use YAML frontmatter on reviewable study notes. Prefer section-level tracking over per-card or per-exercise tracking unless the user asks for granularity.

Exercise frontmatter:

```yaml
---
type: exercises
course: COURSE_NAME
section: "01 Section Name"
status: not started
last_reviewed:
next_review:
review_count: 0
confidence:
notes:
---
```

Flashcard frontmatter:

```yaml
---
type: study-set
course: COURSE_NAME
section: "01 Section Name"
status: not started
last_reviewed:
next_review:
review_count: 0
confidence:
notes:
---
```

Quiz frontmatter:

```yaml
---
type: quiz
course: COURSE_NAME
section: "01 Section Name"
status: not started
last_reviewed:
next_review:
review_count: 0
confidence:
last_score:
best_score:
notes:
---
```

Allowed `status` values:

- `not started`
- `needs practice`
- `needs review`
- `mastered`

For `not started` artifacts, `confidence` may be blank. Set numeric confidence only after learner evidence exists.

## Review Rules

When the learner reports performance, the LLM should update review frontmatter directly.

- `confidence: 0` or `1`: `status: needs practice`, review tomorrow
- `confidence: 2` or `3`: `status: needs review`, review in 3 days
- `confidence: 4`: `status: needs review`, review in 7 days
- `confidence: 5`: `status: mastered`, review in 14 to 30 days

Use reviewable artifact confidence, grouped by section, rather than inventing section-level confidence.

Do not mark an artifact as `mastered` if the learner needed a full explanation. Ask a fresh nearby retrieval prompt first and require clean independent recall or application.

When updating review metadata:

- Set `last_reviewed` to today's date in `YYYY-MM-DD`.
- Set `next_review` from the schedule unless the learner asks otherwise.
- Increment `review_count` by 1.
- Update `confidence`.
- For quizzes, update `last_score` and `best_score` when score is known.
- Keep `notes` short and actionable.

## Flashcards

Use Obsidian-friendly collapsible HTML:

```html
<details>
<summary>Question?</summary>

Answer.

</details>
```

Prefer recall prompts over recognition prompts. A weak prompt asks "What is X?" A stronger prompt asks the learner to distinguish X from a nearby concept or apply X in a small scenario.

## Exercises

Use exercises for applied practice that proves the learner can do the work without just recognizing an answer. Keep one section-level `exercises/Exercises.md` by default.

Exercise files should:

- include setup or prerequisites when needed
- ask the learner to produce an answer, command, explanation, artifact, or solution
- include portable `<details>` answer blocks or checks where useful
- stay scoped to the section unless intentionally reviewing older material

Record repeated misses in a short repair log or review notes section with the missed concept, evidence, likely cause, and repair made or proposed.

## Quizzes

Keep `Quiz.html` self-contained. `Quiz.md` embeds it for Obsidian with:

```html
<iframe src="Quiz.html" title="Section Quiz" width="100%" height="900"></iframe>
```

If Obsidian does not render local iframes, the learner can open `Quiz.html` directly.

Keep a human-readable question inventory in `Quiz.md`; treat `Quiz.html` as a self-contained interactive mirror. Do not add remote scripts, CDNs, analytics, hidden persistence, network calls, minified bundles, or required build steps.

## Context Discipline

When a term is resolved, update `CONTEXT.md` immediately. Do not batch terminology changes.

Call out ambiguous language:

> You said "module", but `CONTEXT.md` uses **Section** for the top-level course unit. Do you mean **Section** or something smaller?

Keep `CONTEXT.md` about course domain language, not implementation details.

If a learner-facing subject term conflicts with `CONTEXT.md`, resolve the ambiguity before adding or linking the glossary term.

## Editing Guidance

- Keep edits local to the copied course folder.
- Do not alter the scaffold's intent unless the user is changing the scaffold itself.
- Prefer Markdown and simple embedded HTML that Obsidian can render.
- Keep generated quiz HTML self-contained.
- Preserve the `quizes` folder spelling unless the user asks to rename it.
- Treat YAML frontmatter as canonical review state. Dataview dashboards are only query helpers.
- Use Markdown, YAML frontmatter, Obsidian-compatible links, `<details>`, local iframes, and unminified self-contained quiz HTML by default.
- Require an ADR for databases, hosted services, build steps, opaque generated files, proprietary formats, or remote quiz dependencies.
