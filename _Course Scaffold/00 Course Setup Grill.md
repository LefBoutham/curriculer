# Course Setup Grill

Use this note with an LLM to set up a course before building it. Keep it short and friendly: ask only what changes what gets built, give everything else its recommended answer, and build.

## Protocol

- Ask one short question at a time, in plain words, and wait for the answer.
- Never number the questions, and never say how many there are or how many are left.
- Ask in the order below: Starting Level, then Sources, then Boundary. Then propose the Section Plan. Don't ask the Defaults.
- Once the learner has answered Starting Level and Sources, they can ask you to build right away, for example with "Just create the course". Then ask nothing more: assume every answer still open, and build. If they ask sooner, ask only what is still open of those two first.
- To assume an answer, take its recommended answer, fit it to the goal and the answers so far, and end it with "(assumed by the tutor)".
- List the assumed answers once, in one short message, a few words each, so the learner can change any of them. Put the list in the same message as the Section Plan.
- Record every answer, given or assumed, on the Answer line under its heading below, and in its `CONTEXT.md` Course Contract field when it has one. Add the sources the learner names to `_attachments/00 Source Index.md`.
- Resolve terminology conflicts against `CONTEXT.md`. Create an ADR only when a decision is hard to reverse, surprising, and trade-off-driven.

## Ask

### Goal

The learner gives the goal when they start the course. Ask for it only when it is missing or unclear: "What do you want to be able to do when you finish?"

Recommended answer: one practical outcome, not a topic list.

Course Contract: **Outcome**.

Answer:

### Starting Level

Ask first, for example: "Let's build it. Are you new to this, so we start with the prerequisites, or do you already know the basics?" Any answer is fine, such as "I know the basics".

Recommended answer: start with the prerequisites the goal needs. A few diagnostic questions during study confirm the starting point.

Course Contract: **Target Learner**.

Answer:

### Sources

Ask next, for example: "Got a book, course or notes you want me to follow, or shall I pick the sources?"

Recommended answer: pick canonical sources for the subject and list them in `_attachments/00 Source Index.md`. Generated explanations are secondary.

Course Contract: **Source Policy**.

Answer:

### Boundary

Ask next: "Anything you want to leave out?"

Recommended answer: leave out what the goal doesn't need, and name it, so the course does not sprawl.

Course Contract: **Boundary**.

Answer:

## Propose

### Section Plan

Don't ask for it. Propose 3 to 6 sections, with the assumed answers in the same short message: "Here's the plan: 1. … 2. … 3. … I've assumed the rest, and you can change any of it: … Shall I build it?"

Recommended answer: order sections by learning dependency, not source order. Keep concepts that are easy to confuse apart: put at least one other lesson between them, and give the later one's section a flashcard or exercise that tells them apart.

Answer:

## Defaults

Don't ask these. Assume each one, and list them with the Section Plan.

### Lesson Size

Recommended answer: one concept, operation, or skill per lesson, small enough for one worked example and one practice task.

Answer:

### Practice Shape

Recommended answer: match practice to the goal: recall, coding, writing, problem solving, or a mix.

Course Contract: **Practice Shape**.

Answer:

### Exercise Style

Recommended answer: ask for a concrete answer, command, explanation, artifact, or solution that proves the learner can apply the lesson material.

Answer:

### Flashcard Style

Recommended answer: prefer distinctions, procedures, and mistake correction over bare definitions.

Answer:

### Quiz Style

Recommended answer: scenario-based questions when the course teaches applied skills; short answer otherwise.

Course Contract: **Quiz Style**.

Answer:

### Review Cadence

Recommended answer: keep the default schedule unless the material is especially dense or high stakes.

Answer:

### Completion Standard

Recommended answer: the learner can explain the key ideas, complete the exercises, and pass the quiz without substantial hints.

Course Contract: **Completion Standard**.

Answer:

### Maintenance Rule

Recommended answer: revise when a source changes, the learner repeatedly misses the same idea, or the course language becomes ambiguous.

Course Contract: **Maintenance Rule**.

Answer:

### Glossary Rule

Recommended answer: add a glossary note when the learner asks for a term, when a term is central to several lessons, or when confusing it with nearby terms would cause real misunderstanding.

Answer:
