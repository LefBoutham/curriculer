# Course Scaffold

Scaffold version: 0.1.0

Copy this folder when starting a new course. Rename the copied folder to the course name, then update `CONTEXT.md`, `AGENTS.md`, and `00 Curriculum Index.md`.

## What This Scaffold Provides

- A repeatable Obsidian course structure.
- A `CONTEXT.md` for shared course language and boundaries.
- An `AGENTS.md` file that tells future LLMs how to work inside the course.
- An empty `Glossary/` folder for learner-facing term notes.
- A course setup grill prompt file for clarifying the course before building it.
- Exercise, flashcard, and quiz templates with spaced repetition frontmatter.
- A Dataview-friendly review dashboard.

## Suggested Setup Flow

1. Copy this folder into a downstream/local learning workspace.
2. Rename the copy to the course name.
3. Open `00 Course Setup Grill.md` with an LLM.
4. Answer the grill questions one at a time.
5. Update `CONTEXT.md` as terms and boundaries become clear.
6. Add glossary terms only when requested or when a term needs a stable learner-facing definition.
7. Replace `01 Section Template` with real numbered sections.
8. Add lessons, exercises, flashcards, and quizzes as the course develops.

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

Inside each numbered section, keep:

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
