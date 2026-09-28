# Changelog

## v0.5.2

- The README's opening line now names the methods Curriculer is built on (prerequisites, mastery, automaticity and spaced retrieval) instead of calling them "the best scientifically proven learning methods". The "Why" section explains each one and links its source. A new line under it says the tutor is only as good as the model and the sources you give it, and that the course is plain files you can read and correct.

Upgrading an existing learning workspace: nothing to do. The scaffold, the skill and the rules are unchanged.

## v0.5.1

- The README's "How To Use It" now copies the `course-study-coach` skill into the learning workspace, in `.agents/skills/` with a `.claude/skills/` link, as well as the scaffold. It says to open the agent at the workspace root, and how to copy the skill on Windows. Before, a workspace set up from the README had courses but no skill. `AGENTS.md`, `00 Courses Index.md` and `_Course Scaffold/README.md` say the same.

Upgrading an existing learning workspace: courses need no change. If the agent doesn't know `course-study-coach`, copy the skill into the workspace root as "How To Use It" shows.

## v0.5.0

- Lessons now teach with a worked example. The lesson template's "Example" is now "Worked Example": one concrete problem solved in numbered steps, each saying why. "Practice" follows as a similar task with different details that the learner does alone, with its answer in a `<details>` block. The tutor goes through the worked example one step at a time, and goes straight to practice when the learner can already do the task.
- Course building keeps confusable concepts apart. When two concepts are easy to confuse, they are not taught in back-to-back lessons: at least one other lesson sits between them. The section that teaches the later one gets one flashcard or exercise that asks the learner to tell them apart. There is no new frontmatter.
- The rules are in a new Building Lessons section of `_Course Scaffold/AGENTS.md`, and in the setup grill's Section Model and Lesson Granularity answers. Added a worked example and a distinction card to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version. A course's own `AGENTS.md` wins over the skill, and a copied course no longer has the lesson template, so also copy the new Building Lessons section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`. Existing lessons can keep their "Example" section; new lessons use the new shape.

## v0.4.0

- The tutor now checks prerequisites before new material. Before the first lesson of a new section, it reads the review state of the sections that section builds on: the ones named in its section index, its Curriculum Graph row, or the lesson's `prerequisites`, or else every earlier section. A reviewed set that needs practice, has confidence 2 or lower, or is overdue gets a short targeted review first, and the session close says what the check found. Sets that were never reviewed are skipped. There is no new frontmatter.
- Added a **Prerequisite** entry to `CONTEXT.md`, and an example of the check to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version. A course's own `AGENTS.md` wins over the skill, so also copy the new Prerequisite Check section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`, and the Prerequisite entry into each course's `CONTEXT.md`.

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
