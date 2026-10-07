# Contributing

Curriculer is a public base for Markdown-first, LLM-assisted course workspaces. Keep changes focused on the scaffold, documentation, validation, and agent instructions.

## Boundaries

- Do not add real courses or learner review history to this repository.
- Do not add an app framework, database, hosted service, LMS layer, or required build step.
- Preserve the `quizes` folder spelling unless the whole convention is intentionally migrated.
- Prefer Markdown, YAML frontmatter, Obsidian-compatible links, collapsible `<details>` blocks, and unminified self-contained HTML.
- Keep quiz HTML local and dependency-free. Do not add CDNs, remote scripts, hidden persistence, analytics, or network calls.
- Update related convention files together when behavior changes: `README.md`, `AGENTS.md`, `_Course Scaffold/README.md`, `_Course Scaffold/AGENTS.md`, `_Course Scaffold/CONTEXT.md`, and `.agents/skills/course-study-coach/SKILL.md`.
- Keep agent skills in `.agents/skills/`. `.claude/skills/<name>` must stay a symlink to `../../.agents/skills/<name>` so Claude Code loads the same skill. On Windows, clone with `git clone -c core.symlinks=true`; the validator fails when Git checks out the link as a plain file.

## Checks

Run:

```sh
python3 scripts/validate_curriculer.py --mode scaffold
python3 -m unittest discover -s scripts
```

Before opening a change, also inspect `_Course Scaffold/01 Section Template/quizes/Quiz.html` in a browser when quiz behavior changes.

When you change Repairing The Course in the skill or Bridge Lessons in `_Course Scaffold/AGENTS.md`, also run:

```sh
python3 scripts/eval_bridge_lesson.py
```

It needs Claude Code, signed in. It plays a learner who can't follow a question on a short synthetic course, and passes when the tutor offers a bridge lesson, adds it only once the learner agrees, and never renumbers, renames, moves, or deletes a lesson. It costs a few agent turns, so the unit tests only check its checks, with a scripted tutor.

## ADRs

Use `_Course Scaffold/docs/adr/` only for decisions that are hard to reverse, surprising without context, and the result of a real trade-off.
