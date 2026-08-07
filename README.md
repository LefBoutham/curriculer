# Curriculer

**Learn anything. A curriculum builder & LLM tutor for any subject, using optimal learning methodologies.**

## Why

Knowledge is not a list of facts; it is a graph of connected ideas and skills.
Advanced concepts depend on simpler concepts, and if a prerequisite is weak,
later work becomes slow or confusing. A single AI lesson cannot provide a
complete path through a large subject.

Curriculer makes the curriculum the source of truth, helping an LLM turn a goal,
suggested topics, and source material into an ordered course. The course starts
with prerequisites and builds toward the goal; if the learner has a gap, the
agent can move back through the graph and reinforce it.

### Automaticity

Working memory is limited, so if a basic skill needs conscious effort, less
capacity remains for complex work. Automaticity is the fast and reliable use of
lower-level knowledge, freeing attention for higher-level reasoning.

### Mastery

Mastery means that a learner can use a prerequisite with enough accuracy and
fluency to continue, and Curriculer checks this before it adds more complexity.
A gap sends the learner back to the required knowledge or skill.

### Spaced Retrieval

Recall weakens without use, while rereading can feel familiar without producing
reliable recall. Curriculer uses questions, exercises, and quizzes for retrieval
practice, and it records each result and schedules the next review. Successful
reviews move farther apart, while difficult material returns sooner.

```mermaid
flowchart LR
    A["Goal and sources"] --> B["Map prerequisites"]
    B --> C["Learn at the knowledge frontier"]
    C --> D["Retrieve and apply"]
    D --> E["Schedule review"]
    D -->|Gap found| B
    E --> C
```

For more background, see Justin Skycak on
[prerequisite knowledge](https://www.justinmath.com/thoughts-about-prerequisite-knowledge/),
[automaticity](https://www.justinmath.com/cognitive-science-of-learning-developing-automaticity/),
[mastery learning](https://www.justinmath.com/a-brief-history-of-mastery-learning/), and
[spaced repetition](https://www.justinmath.com/cognitive-science-of-learning-spaced-repetition/).

## What

Curriculer is a Markdown-first scaffold for local course folders, and a course
can contain a curriculum map, lessons, sources, exercises, flashcards, quizzes,
a glossary, progress, and review dates.

An LLM can teach from these files, quiz the learner, record evidence, and choose
the next task, while the state stays visible and portable. No database, hosted
service, or application is required.

The repository contains `_Course Scaffold/`, the `course-study-coach` skill,
agent rules, and a scaffold validator.

The base repository does not contain real courses or learner history.

## How To Use It

Copy the scaffold into a separate learning workspace:

```sh
cp -R "_Course Scaffold" "/path/to/learning-workspace/My Course"
```

Then:

1. Open `00 Course Setup Grill.md` and define the goal, scope, and learner.
2. Add source material to `_attachments/` or give the agent suggested topics.
3. Ask the agent to map prerequisites and build the numbered course sections.
4. Use `course-study-coach` to learn, practice, review, and take quizzes.
5. Let the agent update progress and review dates from study evidence.

Example prompts:

```text
Build this course from my goal and source files.
Find where I left off and start the next useful task.
Quiz me on due material and update my review data.
```

Do not create real courses inside this base repository; copy the scaffold first.

Before you change the scaffold, run:

```sh
python3 scripts/validate_curriculer.py --mode scaffold
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules.

## License

MIT. See [LICENSE](LICENSE).
