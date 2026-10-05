# Course Setup Grill

Use this note with an LLM to set up a course before building it. Keep it short and friendly: ask only what shapes the course, give everything else its recommended answer, and build.

## Protocol

- Ask one short question at a time, in plain words, and wait for the answer.
- Never number the questions, never say how many there are or how many are left, and don't announce what you'll ask next: just ask.
- Skip any question that the goal or an earlier answer already settles.
- Ask the Starting Level first, then the Purpose.
- After those two, offer to build right away, for example with the reply "Just create the course". If the learner takes it, ask nothing more: assume every answer still open, and build.
- Otherwise, ask about Sources only when `_attachments/` holds no source files yet. Then propose the Section Plan, and build when the learner agrees.
- To build, follow Planned Lessons in the course's `AGENTS.md`: write the map and lesson 1, then start lesson 1 and ask its first question in the same reply. Write the other lessons when the learner reaches them.
- Never ask the Defaults. Give each one its recommended answer, fitted to the goal and the answers so far.
- Write every answer under Current Defaults at the end of this note, and in its `CONTEXT.md` Course Contract field when it has one. End each answer the learner didn't give with "(assumed by the tutor)".
- Mention the assumed answers in one sentence, for example: "I used the usual choices for lesson size, quizzes and reviews; say if you'd like any changed."
- Add the sources the learner names to `_attachments/00 Source Index.md`. Resolve terminology conflicts against `CONTEXT.md`. Create an ADR only when a decision is hard to reverse, surprising, and trade-off-driven.

## Questions

### Goal

The learner gives the goal when they start the course. Ask for it only when it is missing or unclear: "What do you want to be able to do when you finish?"

Recommended answer: one practical outcome, not a topic list. Record it as the Outcome.

### Starting Level

Ask first, for example: "Let's build it. Are you new to this and want the prerequisites first, or shall we start at the basics?" The likeliest answers are "I'm new to this" and "Start at the basics", but any answer is fine, such as "I know the basics".

Recommended answer: start with the prerequisites the goal needs. A few diagnostic questions during study confirm the starting point. Record it as the Target Learner.

### Purpose

Ask next, for example: "What's it for: something at work, a project, or just curiosity?" Skip it when the goal already says what the course is for, such as a trip, a job, an exam or a project.

Recommended answer: fit the outcome, the practice, the quizzes and what's left out to it. Record it in the Outcome.

### Sources

Ask only when `_attachments/` holds no source files yet: "Anything you want me to follow, like a book, a course or your notes?" The likeliest answer is "You pick".

Recommended answer: pick canonical sources for the subject and list them in `_attachments/00 Source Index.md`. Generated explanations are secondary. Record it as the Source Policy.

### Section Plan

Don't ask for it. Propose 3 to 6 sections, and name what's left out: "Here's the plan: 1. … 2. … 3. … I'll leave out … Shall I build it?"

Recommended answer: order sections by learning dependency, not source order. Keep concepts that are easy to confuse apart: put at least one other lesson between them, and give the later one's section a flashcard or exercise that tells them apart. Leave out what the goal doesn't need, so the course doesn't sprawl, and record that as the Boundary.

## Defaults

Never ask these.

### Lesson Size

Recommended answer: one concept, operation, or skill per lesson, small enough for one worked example and one practice task.

### Practice Shape

Recommended answer: match practice to the goal: recall, coding, writing, problem solving, or a mix.

### Exercise Style

Recommended answer: ask for a concrete answer, command, explanation, artifact, or solution that proves the learner can apply the lesson material.

### Flashcard Style

Recommended answer: prefer distinctions, procedures, and mistake correction over bare definitions.

### Quiz Style

Recommended answer: scenario-based questions when the course teaches applied skills; short answer otherwise.

### Review Cadence

Recommended answer: keep the default schedule unless the material is especially dense or high stakes.

### Completion Standard

Recommended answer: the learner can explain the key ideas, complete the exercises, and pass the quiz without substantial hints.

### Maintenance Rule

Recommended answer: revise when a source changes, the learner repeatedly misses the same idea, or the course language becomes ambiguous. During study, when the learner lacks a prerequisite that no lesson teaches, the tutor offers a short bridge lesson and adds it when the learner agrees; it never renumbers or renames lessons.

### Glossary Rule

Recommended answer: add a glossary note when the learner asks for a term, when a term is central to several lessons, or when confusing it with nearby terms would cause real misunderstanding.

## Current Defaults

The course's answers, filled in during setup. An answer the learner didn't give ends with "(assumed by the tutor)".

- **Outcome**:
- **Target Learner**:
- **Source Policy**:
- **Boundary**:
- **Section Plan**:
- **Lesson Size**:
- **Practice Shape**:
- **Exercise Style**:
- **Flashcard Style**:
- **Quiz Style**:
- **Review Cadence**:
- **Completion Standard**:
- **Maintenance Rule**:
- **Glossary Rule**:
