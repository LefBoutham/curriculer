# Course Scaffold

Scaffold version: 0.1.0

Copy this folder when starting a new course. Rename the copied folder to the course name, then update `CONTEXT.md`, `AGENTS.md`, and `00 Curriculum Index.md`.

## What This Scaffold Provides

- A repeatable Obsidian course structure.
- A `CONTEXT.md` for shared course language and boundaries.
- An `AGENTS.md` file that tells future LLMs how to work inside the course.
- An empty `Glossary/` folder for learner-facing term notes.
- A short course setup grill: what to ask before building a course, and recommended answers for the rest.
- Exercise, flashcard, and quiz templates with spaced repetition frontmatter.
- A Dataview-friendly review dashboard.

## Suggested Setup Flow

1. Copy this folder into a downstream/local learning workspace. Keep a copy of it at the workspace root as `_Course Scaffold/` too: the LLM makes later sections' flashcards, exercises and quizzes from its templates. The workspace root also needs the `course-study-coach` skill in `.agents/skills/` and `.claude/skills/`, as "How To Use It" in the Curriculer README shows. Open the agent at the workspace root.
2. Rename the copy to the course name.
3. Tell the LLM the course goal. It runs `00 Course Setup Grill.md` with you, one short question at a time, starting with your level and what the course is for.
4. After those two, you can ask it to build right away. Otherwise it asks about sources when `_attachments/` is empty, and proposes a section plan. It gives every other answer its recommended value, marked as assumed, so you can change any of them later.
5. The LLM builds the course: the full course map, then section 1 and its first lesson in place of `01 Section Template`, and it asks lesson 1's first question in the same reply.
6. It writes each later lesson when you reach it, the lesson's flashcards when you've studied it, and a section's exercises and quiz once you've studied all its lessons (Planned Lessons in `AGENTS.md`). Ask it to write the rest now if you want the whole course at once.
7. Update `CONTEXT.md` as terms and boundaries become clear.
8. Add glossary terms only when requested or when a term needs a stable learner-facing definition.

## Post-Copy Placeholder Sweep

After copying the scaffold, replace these placeholders everywhere they appear:

- `COURSE_NAME`
- `01 Section Template`
- `Lesson Template`
- `FROM "COURSE_NAME"` in `00 Review Dashboard.md`
- section names in lesson, exercise, flashcard, and quiz frontmatter

Use a text search before studying the course:

```sh
rg "COURSE_NAME|Section Template|Lesson Template" "COURSE_FOLDER"
```

## Naming Convention

Use numbered course sections:

```text
01 Foundations
02 Core Concepts
03 Practice
04 Advanced Topics
```

Inside each numbered section, number the lessons in order:

```text
00 Section Index.md
01 Inner Join.md
01a NULL Values.md
02 Left Join.md
```

The course map lists every lesson from the start. A lesson that isn't written yet is plain text there, not a link, and gets its file when the learner reaches it, under the same number and title.

A letter after the number marks a bridge lesson, which the tutor offers during study when the learner lacks a prerequisite, and adds when the learner agrees (Bridge Lessons in `AGENTS.md`). Lessons are never renumbered to make room.

Also keep:

```text
exercises/Exercises.md
flashcards/Flashcards.md
quizes/Quiz.md
quizes/Quiz.html
```

The folder name `quizes` is intentionally preserved for compatibility with existing course libraries that already use that spelling.

## Glossary Convention

The glossary starts empty. Add terms on request.

Use `Glossary/00 Glossary Index.md` as the glossary table of contents. Each term gets its own note in `Glossary/`.

Index entries use this format:

```md
- [[Term Name]] — one-line meaning.
```

When a term has a glossary note, link meaningful mentions in course files to that note:

```md
[[Glossary/Term Name|Term Name]]
```

Do not link every repeated occurrence mechanically. Link the first meaningful occurrence in a section or any occurrence where the learner is likely to want the definition.

## Source Convention

Use `_attachments/00 Source Index.md` for canonical source material when the course depends on trusted external material. Each source entry should include:

- source id
- local file path or URL
- trust level
- access date when relevant
- affected sections

Lessons can refer to source ids in their `source:` frontmatter.
