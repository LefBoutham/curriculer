# Course Scaffold

Copy this folder when starting a new course. Rename the copied folder to the course name, then update `CONTEXT.md`, `AGENTS.md`, and `00 Curriculum Index.md`.

## What This Scaffold Provides

- A repeatable Obsidian course structure.
- A `CONTEXT.md` for shared course language and boundaries.
- An `AGENTS.md` file that tells future LLMs how to work inside the course.
- An empty `Glossary/` folder for learner-facing term notes.
- A grill-with-docs prompt file for clarifying the course before building it.
- Exercise, flashcard, and quiz templates with spaced repetition frontmatter.
- A Dataview-friendly review dashboard.

## Suggested Setup Flow

1. Copy this folder.
2. Rename the copy to the course name.
3. Open `00 Course Setup Grill.md` with an LLM.
4. Answer the grill questions one at a time.
5. Update `CONTEXT.md` as terms and boundaries become clear.
6. Add glossary terms only when requested or when a term needs a stable learner-facing definition.
7. Replace `01 Section Template` with real numbered sections.
8. Add lessons, exercises, flashcards, and quizzes as the course develops.

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
