# Changelog

## v0.3.0

- Clean reviews now move farther apart. For confidence 4 or 5, the next interval is the larger of the base interval and twice the previous interval, up to 180 days. Confidence 3 or lower goes back to the base schedule. The previous interval comes from the existing `last_reviewed` and `next_review` fields, so there is no new field.
- Confidence 5 now needs fluent recall as well as clean recall: quick, with no hesitation and no working it out again. A clean but slow answer is 4. The base interval for 5 is now 14 days; the growing interval replaces the old 14 to 30 day range.
- The learner's own report, or their own marks on flashcards, now supports at most confidence 4. Confidence 5 and `mastered` need an attempt the tutor checked, or a quiz score.
- Added a worked example of two clean reviews to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version. A course's own `AGENTS.md` wins over the skill, so also copy the new Review Rules section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`, and the new Confidence and Mastered entries into each course's `CONTEXT.md`. Review dates already in the courses need no change.

## v0.2.0

- Moved the `course-study-coach` skill from `.codex/skills/` to `.agents/skills/` and added a `.claude/skills/` symlink so Codex and Claude Code both find it.
- Added base-repo guardrails to keep real courses and learner review history out of the public scaffold repository.
- Strengthened scaffold setup, review metadata, and course contract conventions.
- Added lightweight validation for scaffold structure, frontmatter, placeholders, links, and quiz HTML.

## v0.1.0

- Initial public scaffold base.
- Added the `course-study-coach` Codex skill.
- Added Markdown templates for course indexes, lessons, exercises, flashcards, quizzes, glossary, review dashboard, and course setup.
