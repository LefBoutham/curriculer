# Changelog

## v0.7.0

- The setup grill is short and friendly. The learner gives the goal. Then the tutor asks one short question at a time: the learner's starting level, then the sources to follow, then anything to leave out. It never numbers the questions or says how many are left. Then it proposes a section plan and asks whether to build it.
- The tutor no longer asks about lesson size, practice shape, exercise, flashcard and quiz style, review cadence, completion standard, maintenance or the glossary. It gives each its recommended answer, fitted to the goal, and ends it with "(assumed by the tutor)" in `CONTEXT.md` and the grill. It lists them once, with the plan, so the learner can change any.
- Once the starting level and sources are answered, the learner can ask to build right away, for example with "Just create the course". The tutor then assumes every answer still open and builds.
- `00 Course Setup Grill.md` has unnumbered headings in three groups (Ask, Propose, Defaults) and an Answer line under each. `CONTEXT.md` keeps its Course Contract fields and says how assumed answers are marked. Added a setup example to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `_Course Scaffold/` with this version, and replace the setup-grill step in the workspace's root `AGENTS.md` ("Use `00 Course Setup Grill.md` to clarify …") with step 3 of "Creating A New Course" in this repo's `AGENTS.md`. Courses that are already built need no change, and a course still being set up can keep its own copy of the grill. The skill is unchanged.

## v0.6.1

- Withdraws v0.6.0, which went out by mistake after bridge lessons were put on hold. The tutor can already write a lesson and flashcards from the course's own templates; for now it should offer to, not do it on its own. The skill, the scaffold, the validator and the docs are back to v0.5.3. The v0.6.0 entry below stays as a record.

Upgrading an existing learning workspace: if you installed v0.6.0, replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version, and remove the Bridge Lessons section and the Bridge Lesson entry you copied into each course's `AGENTS.md` and `CONTEXT.md`. Bridge lessons a tutor already added can stay: they are ordinary lessons with a letter after their number. If you stayed on v0.5.x, there is nothing to do.

## v0.6.0

- The course grows with the learner. When the learner says they don't understand a question or what it builds on, or an answer shows a missing prerequisite, the tutor doesn't give the answer. It asks one or two short questions to find the missing prerequisite, teaches it with a worked example, asks a fresh question on it, and goes back to the question. Then it repairs the course. If a lesson already teaches the idea, the tutor adds that lesson to the `prerequisites` of the lesson that needed it and brings its flashcards back for review tomorrow. If none does, it adds one short **bridge lesson** just before the lesson that needed it, such as `01a NULL Values.md`, with 2 to 4 flashcards, and says so in one line. The rules are in the skill's new Repairing The Course section and a new Bridge Lessons section of `_Course Scaffold/AGENTS.md`.
- A bridge lesson has a letter after its number and a new `added_for` field that links the lesson that needed it. It is listed in its section index under Lessons and Prerequisites, and in its section's Curriculum Graph row. Repairs only add: lessons are never renumbered, renamed, moved, or deleted.
- The validator now checks bridge lessons in `--mode course`: the number, `added_for`, and the links from the section index, the flashcards, and the Curriculum Graph. The new `--since <commit>` fails if a lesson the course had at that commit is gone. `scripts/test_validate_curriculer.py` tests these checks.
- Added a **Bridge Lesson** entry to `CONTEXT.md`, and an example to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version. A course's own `AGENTS.md` wins over the skill, so also copy the new Bridge Lessons section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`, and the Bridge Lesson entry into each course's `CONTEXT.md`. Existing lessons need no change. A tool that lists lessons by a number and a space should also accept one letter after the number, and sort `03` before `03a` before `04`.

## v0.5.3

- The README no longer says "Your tutor is only as good as the model and the sources you give it." The line under the opening now says only that the course is plain files you can read and correct.

Upgrading an existing learning workspace: nothing to do. The scaffold, the skill and the rules are unchanged.

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
