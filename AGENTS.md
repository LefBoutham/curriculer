# Curriculer Agent Instructions

This repository is a public base for Markdown-first, LLM-assisted course workspaces. It contains `_Course Scaffold/`, which is the template for creating new courses.

## Architecture

- `_Course Scaffold/` is the reusable course template.
- Each top-level course folder should represent one course when this scaffold is copied into a learning workspace.
- A mature course should usually contain:
  - `AGENTS.md` for course-specific agent instructions.
  - `CONTEXT.md` for course language, scope, and decisions.
  - `00 Curriculum Index.md` as the course map.
  - Numbered section folders such as `01 Foundations`.
  - Section-level `flashcards/Flashcards.md`.
  - Section-level `quizes/Quiz.md` and `quizes/Quiz.html`.
  - `Glossary/00 Glossary Index.md` when learner-facing terms need stable definitions.
  - `_attachments/` for course assets and source files.

## Creating A New Course

Start from `_Course Scaffold/`.

Default setup flow:

1. Copy `_Course Scaffold/` to a new top-level folder named after the course.
2. Rename scaffold placeholders in the copied course:
   - `00 Curriculum Index.md`
   - `CONTEXT.md`
   - `AGENTS.md`
3. Use `00 Course Setup Grill.md` to clarify the course goal, audience, scope, and section plan.
4. Replace `01 Section Template/` with real numbered course sections.
5. Keep changes local to the copied course folder unless the user explicitly asks to alter the scaffold or repository conventions.

Do not modify `_Course Scaffold/` when creating a normal course. Only change the scaffold when improving the template itself.

## Study And Review Conventions

Follow the course-level `AGENTS.md` when one exists. If a course does not have one yet, use `_Course Scaffold/AGENTS.md` as the fallback convention.

General rules:

- Prefer Markdown and simple embedded HTML.
- Keep quiz HTML self-contained.
- Preserve the existing folder spelling `quizes` unless the user asks to rename it.
- Use YAML frontmatter on study sets and quizzes when adding review metadata.
- Update `last_reviewed`, `next_review`, `review_count`, `confidence`, and status manually when the learner reports study performance.
