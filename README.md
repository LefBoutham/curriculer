# Curriculer

Curriculer is a Markdown-first base for building personalized, progressive learning curricula with an LLM as the study partner.

The core idea is that a course should start from a reusable scaffold, then grow from the learner's goals, source material, notes, exercises, mistakes, and review history. The curriculum is not a static content dump. It is a living workspace that adapts as the learner studies.

## What This Repository Provides

- `_Course Scaffold/`: a reusable course template.
- Course-level `CONTEXT.md` for shared language, scope, and decisions.
- `00 Curriculum Index.md` as the course map.
- Section folders for lessons, flashcards, quizzes, and review metadata.
- `_attachments/` for source material such as PDFs, screenshots, notes, datasets, and examples.
- LLM-facing conventions for active recall, spaced review, quizzes, glossary terms, and incremental curriculum growth.

## How To Start A Course

1. Copy `_Course Scaffold/` to a new folder named after the course.
2. Open `00 Course Setup Grill.md` with an LLM.
3. Define the outcome, learner, boundaries, section plan, and source policy.
4. Update `CONTEXT.md` as the course language becomes clear.
5. Replace `01 Section Template/` with real numbered sections.
6. Add lessons, flashcards, quizzes, glossary notes, and source attachments as the course develops.

## Learning Model

Curriculer is designed around:

- active recall before explanation
- spaced review
- interleaved practice
- short lessons with concrete exercises
- mistake-driven refinement
- course-specific language and boundaries
- progressive expansion from real learner material

The goal is an optimal workspace for learning: a curriculum that stays coherent while adapting to what the learner actually needs next.
