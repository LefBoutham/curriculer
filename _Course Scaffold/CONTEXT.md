# Course Scaffold Context

This context defines the shared language for building repeatable Obsidian courses that can be studied with an LLM.

## Course Contract

**Outcome**:
What the learner should be able to do after finishing this course.

**Target Learner**:
Who the course is for, including assumed prerequisites and existing fluency.

**Boundary**:
What belongs outside the course even when related.

**Source Policy**:
Which sources the course should trust. Generated explanations are secondary to canonical sources.

**Practice Shape**:
The kind of performance the course should ask for: recall, coding, writing, problem solving, artifact creation, or a mix.

**Quiz Style**:
The kind of self-checks the course should use: multiple choice, short answer, scenario-based, or artifact-based.

**Completion Standard**:
What counts as finishing a section or the whole course.

**Maintenance Rule**:
When the course should be revised.

## Language

**Course**:
A self-contained learning path for one subject.
_Avoid_: Vault, repo, knowledge base

**Section**:
A numbered group of lessons within a course.
_Avoid_: Module, chapter, unit

**Lesson**:
A single focused note that teaches one concept, operation, or skill.
_Avoid_: Page, article, content item

**Prerequisite**:
A section whose material a later section builds on. A section names its prerequisites in its section index or its Curriculum Graph row. When it names no other section, every earlier section is a prerequisite.
_Avoid_: Requirement

**Bridge Lesson**:
A short lesson the LLM adds during study, just before the lesson that needed it, when the learner lacks a prerequisite that no lesson teaches. A letter follows its number, such as `01a`, and its `added_for` links the lesson that needed it.
_Avoid_: Remedial lesson, extra lesson

**Exercise Set**:
A reviewable collection of applied practice for one section.
_Avoid_: Worksheet, homework, assignment

**Study Set**:
A reviewable collection of flashcards for one section.
_Avoid_: Deck, card pile

**Quiz**:
A self-check artifact that tests recall or application for one section.
_Avoid_: Test, exam

**Glossary**:
A learner-facing collection of course subject terms and definitions.
_Avoid_: Context, dictionary

**Glossary Term**:
A single subject term with its own note and a concise definition.
_Avoid_: Context term, tag

**Glossary Index**:
The note that lists glossary terms with one-line meanings.
_Avoid_: Table of contents, glossary home

**Review State**:
The frontmatter fields that describe when and how well an exercise set, study set, or quiz has been reviewed.
_Avoid_: Progress, grade

**Confidence**:
A score from 0 to 5 for how well the learner recalled the material, set from evidence the LLM checked. With the previous interval, it determines the next review interval. The learner's own report alone supports at most 4.
_Avoid_: Ease, difficulty, mastery score

**Mastered**:
A review status meaning the learner recalled the material cleanly, fluently, and without help, in an attempt the LLM checked or in a quiz.
_Avoid_: Done, completed, finished

**Needs Review**:
A review status meaning the learner mostly understood the material but should revisit it soon.
_Avoid_: Okay, shaky

**Needs Practice**:
A review status meaning the learner missed important ideas or needed substantial hints.
_Avoid_: Failed, bad

## Relationships

- A **Course** contains one or more **Sections**.
- A **Section** contains one or more **Lessons**.
- A **Section** builds on its **Prerequisites**. Before the first **Lesson** of a new **Section**, a weak **Review State** in a **Prerequisite** is reviewed first.
- A **Bridge Lesson** is added to a **Section** during study. Adding one never renumbers, renames, moves, or deletes a **Lesson**.
- A **Section** has one **Exercise Set** by default.
- A **Section** has one **Study Set** by default.
- A **Section** has one **Quiz** by default.
- A **Course** has one **Glossary**.
- A **Glossary** has one **Glossary Index**.
- A **Glossary Index** links to zero or more **Glossary Terms**.
- An **Exercise Set**, **Study Set**, and **Quiz** each have one **Review State**.
- **Confidence** and the previous review interval set `next_review`.
- **Mastered**, **Needs Review**, and **Needs Practice** are values of **Review State**.

## Example dialogue

> **Learner:** "I finished section one, but I missed the examples about constraints."
> **LLM:** "I'll update the section **Study Set** as **Needs Review**, set **Confidence** to 3, and schedule the next review in three days."

## Flagged ambiguities

- "Module" should usually be resolved to **Section**.
- "Deck" should usually be resolved to **Study Set**.
- "Progress" should usually be resolved to **Review State** when discussing spaced repetition metadata.
- "Glossary" should mean learner-facing subject definitions; use `CONTEXT.md` for course-building language and boundaries.
