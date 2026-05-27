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

## Principles

Curriculer is guided by a few learning-design principles:

- Learning should be active as soon as possible. Explanation matters, but the learner should quickly move into recall, problem solving, writing, building, or applying.
- Review should be scheduled, not left to vibes. Material that is not retrieved will fade, so courses track what needs review next.
- Retrieval should come before re-reading. Flashcards, quizzes, and study sessions should ask the learner to attempt recall before receiving hints or explanations.
- Practice should mix old and new material. Interleaving exposes weak understanding better than long runs of one familiar task.
- Lessons should stay small enough to fit working memory. Each lesson should teach one concept, operation, or skill with a concrete check for use.
- The course should adapt to mistakes. Missed questions, shaky explanations, and repeated confusion are signals for review, clarification, or curriculum repair.
- Learners need coherent paths, not content piles. `CONTEXT.md`, the curriculum index, and section structure keep the course language and scope stable as it grows.

These principles are influenced by cognitive psychology research on active learning, spaced repetition, retrieval practice, interleaving, deliberate practice, and prerequisite scaffolding. A quiet north star is Justin Skycak's summary of durable learning findings:

> "active learning beats passive learning."

See [Which Cognitive Psychology Findings are Solid, That Can Be Used to Help Students Learn Better?](https://www.justinmath.com/which-cognitive-psychology-findings-are-solid-that-can-be-used-to-help-students-learn-better/) for the broader argument.

The agent workflow conventions also take inspiration from Matt Pocock's [skills](https://github.com/mattpocock/skills) repo, especially the idea that useful agent behavior can be captured as small, composable workflows with shared project language, setup conventions, and explicit review loops.

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
