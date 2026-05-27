# Course Setup Grill

Use this note with an LLM before generating or expanding a course. Ask one question at a time. After each answer, update `CONTEXT.md` if a term, relationship, or boundary becomes clear.

## Protocol

For each question:

1. Ask the question.
2. Provide the recommended answer.
3. Wait for the learner's response.
4. Resolve terminology conflicts against `CONTEXT.md`.
5. Update `CONTEXT.md` immediately when a course-specific term is clarified.
6. Create an ADR only when the decision is hard to reverse, surprising, and trade-off-driven.

## Questions

### 1. Course Outcome

What should the learner be able to do after finishing this course?

Recommended answer: define one practical outcome, not a topic list.

### 2. Target Learner

Who is this course for, and what can they already do?

Recommended answer: specify prerequisites and assumed fluency.

### 3. Course Boundary

What belongs outside this course even if it is related?

Recommended answer: name explicit exclusions so the course does not sprawl.

### 4. Section Model

What are the first 3 to 6 sections?

Recommended answer: organize sections by learning dependency, not source order.

### 5. Lesson Granularity

How small should each lesson be?

Recommended answer: one concept, operation, or skill per lesson.

### 6. Practice Shape

Should practice be recall, coding, writing, problem solving, or mixed?

Recommended answer: match practice to the final course outcome.

### 7. Exercise Style

What should section exercises ask the learner to produce?

Recommended answer: require a concrete answer, command, explanation, artifact, or solution that proves the learner can apply the lesson material.

### 8. Flashcard Style

Should flashcards test definitions, distinctions, procedures, examples, or mistakes?

Recommended answer: prefer distinctions, procedures, and mistake correction over bare definitions.

### 9. Quiz Style

Should quizzes be multiple choice, short answer, scenario-based, or artifact-based?

Recommended answer: use scenario-based questions when the course teaches applied skills.

### 10. Review Cadence

Should the default spaced repetition schedule be changed?

Recommended answer: keep the default unless the material is especially dense or high stakes.

### 11. Source Policy

What source material should the course trust?

Recommended answer: list canonical sources and mark generated explanations as secondary.

### 12. Completion Standard

What counts as finishing a section?

Recommended answer: the learner can explain the key ideas, complete the exercises, and pass the quiz without substantial hints.

### 13. Maintenance Rule

When should the course be revised?

Recommended answer: revise when a source changes, the learner repeatedly misses the same idea, or the course language becomes ambiguous.

### 14. Glossary Rule

Which terms deserve glossary notes?

Recommended answer: add a glossary note when the learner explicitly asks for a term, when a term is central to several lessons, or when confusing it with nearby terms would cause real misunderstanding.
