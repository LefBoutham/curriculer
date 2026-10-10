# Changelog

## v0.11.0

- **An upgrade command.** `python3 scripts/upgrade_workspace.py /path/to/learning-workspace` brings a learning workspace up to this release, following the upgrade steps below. It replaces the skill and `_Course Scaffold/`, refreshes the `.claude/skills/` link or copy, and removes the old `.codex/skills/` copy. In the root `AGENTS.md`, it updates the setup steps and study paragraphs that releases changed. In each course, it brings the rule sections that releases asked you to copy, Building Lessons, Review Rules, Prerequisite Check, Section Opener and Bridge Lessons, and their `CONTEXT.md` entries up to date. It never touches a course's other sections, its lessons, flashcards, exercises or quizzes, or review dates. It backs up what it changes in the workspace's `.curriculer/backups/`, says what it changed and what is left for you, and records the release in `.curriculer/version`. A second run finds nothing to do. `--check` reports without changing anything, and `--commit` commits the upgrade, and only the upgrade, in the workspace's Git repository.
- `scripts/test_upgrade_workspace.py` tests it on a workspace an old release left, and checks that each step still finds its text in this release.

Upgrading an existing learning workspace: run `python3 scripts/upgrade_workspace.py /path/to/learning-workspace` from this release. It does the steps of every release since v0.2.0. A rule section you changed in a course's `AGENTS.md` is replaced too, and its old text is in the backup.

## v0.10.1

- **A check for course repairs.** `scripts/eval_bridge_lesson.py` plays a learner who taps "I don't understand the question or what it builds on" on a short synthetic course, with Claude Code as the tutor. It passes when the tutor offers a bridge lesson before adding one, adds it once the learner agrees, places and links it so the course check passes, and keeps every lesson: no renumbering, renaming, moving or deleting. Run it after changing Repairing The Course or Bridge Lessons, as `CONTRIBUTING.md` says. `scripts/test_eval_bridge_lesson.py` tests its checks with a scripted tutor, and checks that the skill and `_Course Scaffold/AGENTS.md` still say to offer first and only add.

Upgrading an existing learning workspace: nothing to do. The check is in this repo's `scripts/`.

## v0.10.0

- **A section opener.** A learner who starts a section cold meets its new names and its first hard idea at once. So from a course's second section on, once the prerequisite check is done, the tutor opens the section in about five short sentences: where it sits in the course map and what it builds on, the question it answers, its main parts by name, how its lessons connect, and a question that lesson 1 will answer, for the learner to try first. A wrong try is expected, and lesson 1 shows the answer. There is no opener in section 1 or in a section already started, and the learner can skip it. It draws on pre-training, advance organisers and the pretesting effect. The rules are in a new Section Opener section of the skill and of `_Course Scaffold/AGENTS.md`. An app with its own section intro, such as a narrated one, follows its own rules instead.
- Added a **Section Opener** entry to `CONTEXT.md`, and a Section Opener example to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version. A course's own `AGENTS.md` wins over the skill, so also copy the new Section Opener section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`, after its Prerequisite Check, and the Section Opener entry into each course's `CONTEXT.md`. Add the new paragraph under Study And Review Conventions to the workspace's root `AGENTS.md`.

## v0.9.0

- **The first lesson in minutes.** Building a course used to write every section's lessons, exercises, flashcards and quizzes before the first question, which took 13 to 17 minutes. Now the build writes the course contract, the source list, the full course map, section 1's index and lesson 1, then starts lesson 1 and asks its first question in the same reply. The plan is still made in full: every section and lesson, in prerequisite order, with confusable concepts apart.
- **Planned lessons.** The map lists every section and, under it, every lesson, with the number and title its file will have. A lesson or section that isn't written yet is plain text, not a link. The tutor writes a planned lesson when the learner reaches it, then links it. It adds a lesson's flashcards when the learner has studied it, and a section's exercises and quiz once every lesson in it is studied. A set that already has a `next_review` comes back by tomorrow when it gets new cards, as for a bridge lesson. "Write the rest now" writes everything at once. The rules are in a new Planned Lessons section of `_Course Scaffold/AGENTS.md`, and the skill's New Lessons follows them.
- **Templates at the workspace root.** Later sections' flashcards, exercises and quizzes are made from `_Course Scaffold/01 Section Template/` in the workspace, so "How To Use It" in the README copies the scaffold there too.
- **The course check** (`--mode course`) now checks the map and the section indexes: a lesson linked there must be written, and a written lesson must be a link. A planned lesson, or a planned section with no folder yet, passes. `scripts/test_validate_curriculer.py` tests both.
- Added a **Planned Lesson** entry to `CONTEXT.md`, and a Planned Lesson example to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version, and keep `_Course Scaffold/` at the workspace root. Replace steps 1 and 4 of "Creating A New Course" in the workspace's root `AGENTS.md` with this repo's. Courses that are already built need no change: every lesson in them is written. A course still being set up can be built the new way: the skill falls back to Planned Lessons in `_Course Scaffold/AGENTS.md` when the course's own `AGENTS.md` has none.

## v0.8.2

- The setup grill tells the tutor not to announce what it will ask next, and to skip "What's it for?" when the goal already says, such as a trip, a job, an exam or a project. In a live setup, one tutor opened with "I'll start with your experience level, then ask what it's for", and another asked what a trip to Madrid was for.

Upgrading an existing learning workspace: replace its `_Course Scaffold/` with this version. Courses that are already built need no change.

## v0.8.1

- The course check no longer flags a placeholder name inside a code example, such as `course: COURSE_NAME` in the frontmatter examples of a course's `AGENTS.md`, or the placeholder list in its copied `README.md`. Before, a course built from the scaffold failed on those two files even when everything else was renamed. A placeholder in frontmatter, in text or in a Dataview query still fails. `scripts/test_validate_curriculer.py` tests both.

Upgrading an existing learning workspace: nothing to do. The check is in this repo's `scripts/`.

## v0.8.0

This release replaces v0.6.1 and v0.7.0, which went out by mistake. v0.6.0's bridge lessons stay, now as offers, and the setup is shorter than in v0.7.0.

- **A short setup.** The tutor asks one short question at a time, and never numbers the questions or says how many are left. It asks the learner's starting level first, then what the course is for, and skips any question the goal already answers. After those two, the learner can ask to build right away, for example with "Just create the course". Otherwise the tutor asks about sources only when `_attachments/` is empty, proposes a section plan that names what's left out, and builds when the learner agrees.
- **Defaults instead of questions.** The tutor never asks about lesson size, practice shape, exercise, flashcard and quiz style, review cadence, completion standard, maintenance or the glossary. It gives each its recommended answer, writes it under Current Defaults in `00 Course Setup Grill.md` and in `CONTEXT.md`, ending with "(assumed by the tutor)", and mentions them in one sentence. The grill's headings have no numbers. `CONTEXT.md` keeps its Course Contract fields.
- **Bridge lessons are offered.** When no lesson teaches a missing prerequisite, the tutor offers a short bridge lesson and adds it only when the learner agrees. If the learner says no, nothing changes and the session close names the gap. The naming rules, `added_for` and the validator checks are v0.6.0's.
- Added a Course Setup example to `docs/examples.md`, and the offer to its Bridge Lesson example.

Upgrading an existing learning workspace: replace its `.agents/skills/course-study-coach/` and `_Course Scaffold/` with this version, and replace the setup-grill step in the workspace's root `AGENTS.md` with step 3 of "Creating A New Course" in this repo's `AGENTS.md`. Courses that are already built keep their own setup grill, and so can a course still being set up. From v0.5.x or v0.6.1, also copy the Bridge Lessons section from `_Course Scaffold/AGENTS.md` into each course's `AGENTS.md`, and the Bridge Lesson entry into each course's `CONTEXT.md`. From v0.6.0, replace the first paragraph of each course's Bridge Lessons section and its Bridge Lesson entry with this version's.

## v0.7.0

Superseded by v0.8.0.

- The setup grill is short and friendly. The learner gives the goal. Then the tutor asks one short question at a time: the learner's starting level, then the sources to follow, then anything to leave out. It never numbers the questions or says how many are left. Then it proposes a section plan and asks whether to build it.
- The tutor no longer asks about lesson size, practice shape, exercise, flashcard and quiz style, review cadence, completion standard, maintenance or the glossary. It gives each its recommended answer, fitted to the goal, and ends it with "(assumed by the tutor)" in `CONTEXT.md` and the grill. It lists them once, with the plan, so the learner can change any.
- Once the starting level and sources are answered, the learner can ask to build right away, for example with "Just create the course". The tutor then assumes every answer still open and builds.
- `00 Course Setup Grill.md` has unnumbered headings in three groups (Ask, Propose, Defaults) and an Answer line under each. `CONTEXT.md` keeps its Course Contract fields and says how assumed answers are marked. Added a setup example to `docs/examples.md`.

Upgrading an existing learning workspace: replace its `_Course Scaffold/` with this version, and replace the setup-grill step in the workspace's root `AGENTS.md` ("Use `00 Course Setup Grill.md` to clarify …") with step 3 of "Creating A New Course" in this repo's `AGENTS.md`. Courses that are already built need no change, and a course still being set up can keep its own copy of the grill. The skill is unchanged.

## v0.6.1

Superseded by v0.8.0, which keeps v0.6.0's bridge lessons as offers.

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
