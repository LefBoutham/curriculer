# Curriculer

Curriculer is a Markdown-first template for local course folders.

Use it to make a course that an LLM reads, updates, and uses for study.

A course folder includes:

- a curriculum index
- lessons
- exercises
- flashcards
- quizzes
- glossary terms
- source files
- review data

## What This Repository Contains

- `_Course Scaffold/`: the template for a new course.
- `.codex/skills/course-study-coach/`: the Codex study coach skill.
- `AGENTS.md`: repository rules for agents.
- `00 Courses Index.md`: a small index for course libraries.
- `scripts/validate_curriculer.py`: a validator for scaffold files.

## What This Repository Does Not Contain

- Real courses.
- Learner review history.
- A database.
- A hosted service.
- A required app.

Copy the scaffold into your own learning workspace before you make a real course.

## Why Curriculer Exists

AI tools can make lessons fast.

But a set of one-off lessons is not a course.

Those lessons can use different terms.

They can miss prerequisites.

They can skip review.

They can give a useful answer without a stable path through the subject.

Curriculer keeps the course structure visible. It gives the learner and the agent one place to find:

- the course goal
- the section order
- the next lesson
- the trusted source files
- the glossary terms
- the exercises and quizzes
- the due reviews
- the weak spots

The main unit is the curriculum, not the prompt.

## Learning Model

Curriculer uses a small set of learning rules.

**Keep The Map Visible**

The curriculum index shows the course goal, section order, and next work.

**Use Stable Terms**

The glossary gives important terms one clear meaning inside the course.

**Retrieve Before Explanation**

The study coach asks the learner to answer first.

It gives hints only after the learner makes an attempt.

**Review On A Schedule**

Review metadata lives in Markdown frontmatter. The agent can find due work without chat memory.

**Repair Weak Prerequisites**

If a learner misses a concept, the course can move back to the prerequisite.

The fix can be a clearer lesson, a new exercise, a glossary note, or another review.

**Keep The Learner In Control**

The learner can use their own files, set their own goal, and choose their own pace.

## Start A Course

Copy the scaffold into a downstream or local learning workspace.

```sh
cp -R "_Course Scaffold" "/path/to/learning-workspace/My Course"
```

Then update the copied course.

1. Rename `COURSE_NAME` placeholders.
2. Rename `01 Section Template`.
3. Rename lesson, exercise, flashcard, and quiz placeholders.
4. Update dashboard queries that refer to `COURSE_NAME`.
5. Open `00 Course Setup Grill.md`.
6. Define the goal, learner, scope, sources, practice, quiz style, and finish criteria.
7. Replace the template section with real numbered sections.

Do not create real courses inside this base repository.

## Course Folder Shape

A mature copied course usually has this shape:

```text
My Course/
|-- AGENTS.md
|-- CONTEXT.md
|-- 00 Course Setup Grill.md
|-- 00 Curriculum Index.md
|-- 00 Review Dashboard.md
|-- 01 Foundations/
|   |-- 00 Section Index.md
|   |-- 01 Lesson.md
|   |-- exercises/
|   |   `-- Exercises.md
|   |-- flashcards/
|   |   `-- Flashcards.md
|   `-- quizes/
|       |-- Quiz.md
|       `-- Quiz.html
|-- Glossary/
|   `-- 00 Glossary Index.md
`-- _attachments/
    `-- 00 Source Index.md
```

The folder name `quizes` is kept for compatibility with existing course folders.

## Study With Codex

Curriculer includes the `course-study-coach` skill.

Use it when you want to:

- study
- review
- take a quiz
- continue a course
- find your last checkpoint
- practice weak material

Example prompts:

```text
Use course-study-coach. I want to study this course.
```

```text
Quiz me on the next due review and update the review metadata.
```

```text
Find where I left off and start with overdue reviews.
```

The study coach should:

- read the course instructions
- inspect the curriculum index
- find due reviews
- ask one question at a time
- wait for a learner attempt
- give hints before full answers
- update progress and review metadata when there is enough evidence

## Review Metadata

Exercises, flashcards, quizzes, and lessons can use review metadata.

```yaml
last_reviewed:
next_review:
review_count: 0
confidence:
status: not started
notes:
```

The default review states are:

- `not started`
- `needs practice`
- `needs review`
- `mastered`

These states are routing labels. They tell the agent what to show next. They are not grades.

## Repository Rules

Keep this repository as a public base.

- Do not add real courses.
- Do not add learner review history.
- Keep files plain and editable.
- Prefer Markdown and simple embedded HTML.
- Keep quiz HTML self-contained.
- Preserve the `quizes` folder name unless the repository standard changes.
- Store important state in files, not only in chat history.

Before you change the scaffold, run:

```sh
python3 scripts/validate_curriculer.py --mode scaffold
```

## Design Principles

- Markdown first.
- Local first.
- Human editable.
- Agent readable.
- Curriculum before content.
- Review as course data.
- Mistakes improve the course.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

Use short, direct prose in public documentation.

Prefer active voice. Use the same term for the same thing each time.

## License

MIT. See [LICENSE](LICENSE).
