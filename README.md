# Curriculer

**Learn anything. A curriculum builder and LLM tutor for any subject, built on
prerequisites, mastery, automaticity and spaced retrieval.**

The course is plain files, so you can read it and correct it.

## Why

Knowledge is not a list of facts. It is a graph of connected ideas and skills.
Advanced concepts depend on simpler concepts, so a weak prerequisite can make
later work unnecessarily hard. A single AI lesson cannot provide a complete path
through a large subject.

The curriculum holds the course plan in one place. Curriculer helps an LLM turn
a goal, suggested topics, and source material into an ordered course. The course
starts with prerequisites and builds toward the goal. If the learner has a gap,
the agent will automatically move back through the graph and reinforce it.

### Automaticity

Working memory is limited. If a basic skill needs conscious effort, less capacity
remains for complex work. Automaticity is the fast and reliable use of
lower-level knowledge. It frees attention for higher-level reasoning. Curriculer
gives its top score only to recall that is both quick and correct.

### Mastery

Mastery means that a learner can use a prerequisite with enough accuracy and
fluency to continue. Curriculer checks this before it adds more complexity. A
gap sends the learner back to the required knowledge or skill. Before a new
section, the tutor looks at the review state of the sections it builds on and
reviews any weak or overdue one first.

### Spaced Retrieval

Recall weakens without use. Rereading can feel familiar, but it does not always
produce reliable recall. Curriculer uses questions, exercises, and quizzes for
retrieval practice. It records each result and schedules the next review.
Successful reviews move farther apart: each clean review about doubles the gap,
up to six months. Difficult material returns sooner.

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

Curriculer is a Markdown-first scaffold for local course folders. A course can
contain a curriculum map, lessons, sources, exercises, flashcards, quizzes, a
glossary, progress, and review dates.

An LLM can teach from these files, quiz the learner, record evidence, and choose
the next task. The state stays visible and portable. No database, hosted service,
or application is required.

The repository contains `_Course Scaffold/`, the `course-study-coach` skill,
agent rules, and a scaffold validator.

The skill lives in `.agents/skills/course-study-coach/`, where Codex finds it.
Claude Code finds the same skill through the `.claude/skills/course-study-coach`
symlink. On Windows, Git may check out that symlink as a small text file. Clone
with `git clone -c core.symlinks=true` (needs Developer Mode or an administrator
shell), or copy the skill folder into `.claude/skills/`.

The base repository does not contain real courses or learner history.

## How To Use It

A learning workspace is a separate folder for your courses. From the root of
this repository, copy the `course-study-coach` skill into it, where Codex and
Claude Code look for it, and copy the scaffold into it as a course:

```sh
mkdir -p "/path/to/learning-workspace/.agents/skills" "/path/to/learning-workspace/.claude/skills"
cp -R .agents/skills/course-study-coach "/path/to/learning-workspace/.agents/skills/"
ln -s ../../.agents/skills/course-study-coach "/path/to/learning-workspace/.claude/skills/course-study-coach"
cp -R "_Course Scaffold" "/path/to/learning-workspace/My Course"
```

On Windows, a link needs Developer Mode or an administrator shell. Instead of
the `ln -s` line, copy the skill folder into `.claude/skills/` as well, and
replace both copies when you upgrade.

Open your agent at the workspace root, the folder that holds `.agents/`,
`.claude/` and your course folders, so it finds the skill and sees every course.
For another course, run only the last `cp` line again with a new name.

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

Do not create real courses inside this base repository. Copy the scaffold first.

Before you change the scaffold, run:

```sh
python3 scripts/validate_curriculer.py --mode scaffold
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution rules.

## License

MIT. See [LICENSE](LICENSE).
