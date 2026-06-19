# Contributing

Curriculer is a public base for Markdown-first, LLM-assisted course workspaces. Keep changes focused on the scaffold, documentation, validation, and agent instructions.

## Boundaries

- Do not add real courses or learner review history to this repository.
- Do not add an app framework, database, hosted service, LMS layer, or required build step.
- Preserve the `quizes` folder spelling unless the whole convention is intentionally migrated.
- Prefer Markdown, YAML frontmatter, Obsidian-compatible links, collapsible `<details>` blocks, and unminified self-contained HTML.
- Keep quiz HTML local and dependency-free. Do not add CDNs, remote scripts, hidden persistence, analytics, or network calls.
- Update related convention files together when behavior changes: `README.md`, `AGENTS.md`, `_Course Scaffold/README.md`, `_Course Scaffold/AGENTS.md`, `_Course Scaffold/CONTEXT.md`, and `.codex/skills/course-study-coach/SKILL.md`.

## Checks

Run:

```sh
python3 scripts/validate_curriculer.py --mode scaffold
```

Before opening a change, also inspect `_Course Scaffold/01 Section Template/quizes/Quiz.html` in a browser when quiz behavior changes.

## ADRs

Use `_Course Scaffold/docs/adr/` only for decisions that are hard to reverse, surprising without context, and the result of a real trade-off.
