# Curriculer Agent Instructions

This repository is a public base for Markdown-first, LLM-assisted course workspaces. It contains `_Course Scaffold/`, which is the template for creating new courses.

This base repository must not contain real courses or learner review history. Real courses belong in downstream/local learning workspaces created from the scaffold.

## Architecture

- `_Course Scaffold/` is the reusable course template.
- Each top-level course folder in a downstream learning workspace should represent one course when this scaffold is copied there.
- A mature course should usually contain:
  - `AGENTS.md` for course-specific agent instructions.
  - `CONTEXT.md` for course language, scope, and decisions.
  - `00 Curriculum Index.md` as the course map.
  - Numbered section folders such as `01 Foundations`.
  - Section-level `exercises/Exercises.md`.
  - Section-level `flashcards/Flashcards.md`.
  - Section-level `quizes/Quiz.md` and `quizes/Quiz.html`.
  - `Glossary/00 Glossary Index.md` when learner-facing terms need stable definitions.
  - `_attachments/` for course assets and source files.

## Creating A New Course

Start from `_Course Scaffold/`, but copy it into a downstream/local learning workspace, not into this public base repository.

Default setup flow:

1. Copy `_Course Scaffold/` to a new top-level folder named after the course in a downstream/local learning workspace. If the workspace root has no `.agents/skills/course-study-coach/` yet, copy the skill there too, with the `.claude/skills/course-study-coach` link, as "How To Use It" in `README.md` shows.
2. Rename scaffold placeholders in the copied course:
   - `00 Curriculum Index.md`
   - `CONTEXT.md`
   - `AGENTS.md`
   - `00 Review Dashboard.md`
   - `Glossary/00 Glossary Index.md`
   - section lesson, exercise, flashcard, and quiz frontmatter
3. Run `00 Course Setup Grill.md` with the learner: one short question at a time, never numbered or counted, starting with their level and then what the course is for. After those two, offer to build right away. Otherwise ask about sources only when `_attachments/` is empty, then propose the section plan. Give every other answer its recommended value, marked as assumed, and mention them in one sentence.
4. Replace `01 Section Template/` with real numbered course sections.
5. Keep changes local to the copied course folder unless the user explicitly asks to alter the scaffold or repository conventions.

Do not modify `_Course Scaffold/` when creating a normal course. Only change the scaffold when improving the template itself.

## Study And Review Conventions

Follow the course-level `AGENTS.md` when one exists. If a course does not have one yet, use `_Course Scaffold/AGENTS.md` as the fallback convention.

Use the repo-scoped `course-study-coach` skill in `.agents/skills/course-study-coach/` for LLM-led study sessions, reviews, exercises, study sets, quizzes, diagnostic starting-point checks, active-recall tutoring, and review metadata updates.

When a learner lacks a prerequisite that no lesson teaches, the skill offers to add one short bridge lesson, such as `01a NULL Values.md`, with a few flashcards, and adds it when the learner agrees. Repairs only add: they never renumber, rename, move, or delete a lesson. The rules are under Bridge Lessons in `_Course Scaffold/AGENTS.md`.

Base repository guardrails:

- Do not add real course folders to this repository.
- Do not write learner `last_reviewed`, `next_review`, `review_count`, `confidence`, `last_studied`, or `study_count` values into `_Course Scaffold/`.
- Examples in this repository must be short synthetic snippets, not a full sample course.
- Keep repo skills in `.agents/skills/<name>/`, which Codex reads. Claude Code reads `.claude/skills/`, so `.claude/skills/<name>` is a symlink to `../../.agents/skills/<name>`. Edit only the `.agents/skills/` copy and do not add a second copy.
- Before changing scaffold conventions, check that the change remains Markdown-first, local-first, human-editable, agent-friendly, and does not require a database, hosted service, build step, opaque generated file, or remote quiz dependency.
- Use `docs/adr/` only for hard-to-reverse, surprising, trade-off-driven convention changes.

General rules:

- Prefer Markdown and simple embedded HTML.
- Keep quiz HTML self-contained.
- Preserve the existing folder spelling `quizes` unless the user asks to rename it.
- Use YAML frontmatter on exercises, study sets, and quizzes when adding review metadata.
- Have the LLM update `last_reviewed`, `next_review`, `review_count`, `confidence`, and status directly when the learner reports study performance.
