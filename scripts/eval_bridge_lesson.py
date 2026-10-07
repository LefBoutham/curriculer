#!/usr/bin/env python3
"""Play a learner who can't follow a question, and check how the tutor repairs the course.

The tutor passes when it offers to add a bridge lesson before adding one, adds
it once the learner agrees, places and links it as Bridge Lessons in
`_Course Scaffold/AGENTS.md` says, and never renumbers, renames, moves, or
deletes a lesson.

It runs Claude Code in a temporary learning workspace with one short synthetic
course, with file tools only and the study skill in its context, as the app
runs it. Another Claude Code run plays the learner. It costs a few agent turns,
so it isn't a unit test: run it after changing Repairing The Course in the
skill or Bridge Lessons in `_Course Scaffold/AGENTS.md`.

    python3 scripts/eval_bridge_lesson.py
    python3 scripts/eval_bridge_lesson.py --model claude-opus-5-5 --keep
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path
from typing import Callable

import validate_curriculer as validate

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path(".agents/skills/course-study-coach")
COURSE = "Python Basics"
SECTION = "01 Lists"
NEEDED = "02 List Comprehensions"
# Lessons the course map lists as planned. The tutor may write them if the session gets that far.
PLANNED = {"02 Tuples/01 Making Tuples.md", "02 Tuples/02 Unpacking.md"}

OPENING = f"Quiz me on {NEEDED} in {COURSE}, one question at a time."
# The app's reply under a recall question (ILM-83).
UNSURE = "I don't understand the question or what it builds on"
AGREE = "Yes, please add it."

LEARNER = f"""You are playing a learner in a study session with a tutor, in a short Python course. You can make a list, read a value by its index, and append to it. You have never seen a for loop: you don't know what `for x in items` does and can't guess it. Once the tutor has taught you for loops, you understand them.

Reply to the tutor's last message as this learner, in one or two short sentences, with nothing else. Answer honestly, and say you don't know when you don't. If the tutor offers to add a lesson to the course, reply with exactly: {AGREE}

The conversation so far:

"""

Talk = list[tuple[str, str]]


class AgentError(Exception):
    """The agent couldn't answer: not installed, signed out, or a usage limit. It says nothing about the tutor."""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", help="the tutor's model; Claude Code's default when left out")
    parser.add_argument("--learner-model", default="haiku", help="the model that plays the learner (default: haiku)")
    parser.add_argument("--turns", type=int, default=10, help="tutor replies before the eval gives up (default: 10)")
    parser.add_argument("--keep", action="store_true", help="keep the workspace, to read what the tutor wrote")
    args = parser.parse_args()

    root = Path(tempfile.mkdtemp(prefix="curriculer-eval-"))
    talk: Talk = []
    try:
        course, start = make_workspace(root / "workspace")
        (root / "learner").mkdir()
        tutor = claude_tutor(root / "workspace", args.model)
        learner = claude_learner(root / "learner", args.learner_model)
        failures = converse(tutor, learner, course, start, talk, args.turns)
    except AgentError as error:
        failures = None
        problem = str(error)
    finally:
        for who, text in talk:
            print(f"{who}: {text}\n", flush=True)
        if args.keep:
            print(f"Workspace: {root / 'workspace'}")
        else:
            shutil.rmtree(root)

    if failures is None:
        print(f"Could not run the eval: {problem}", file=sys.stderr)
        return 2
    if failures:
        print("Bridge lesson eval failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    print("Bridge lesson eval passed: the tutor offered a bridge lesson, added it when the learner agreed, and kept every lesson.")
    return 0


def converse(tutor: Callable[[str], str], learner: Callable[[Talk], str], course: Path, start: str, talk: Talk, turns: int) -> list[str]:
    """Play the session and return what the tutor got wrong: nothing when it passed."""
    before = lessons(course)
    message = OPENING
    agreed = False
    for turn in range(turns):
        talk.append(("Learner", message))
        talk.append(("Tutor", tutor(message)))
        now = lessons(course)
        if before - now:
            return [f"the tutor renumbered, renamed, moved or deleted {', '.join(sorted(before - now))}"]
        added = sorted(now - before - PLANNED)
        if added and not agreed:
            return [f"the tutor added {', '.join(added)} before the learner agreed to it"]
        if added:
            return check_bridge(course, start, added)
        # The learner first taps the reply the app shows under a question.
        message = UNSURE if turn == 0 else learner(talk)
        agreed = agreed or AGREE.lower() in message.lower()
    if agreed:
        return ["the learner agreed, but the tutor added no lesson"]
    return [f"the tutor didn't offer a lesson for the missing prerequisite in {turns} replies"]


def check_bridge(course: Path, start: str, added: list[str]) -> list[str]:
    """One bridge lesson, just before the lesson that needed it, and the course check passes."""
    errors: list[str] = []
    expected = f"{SECTION}/01a "
    if len(added) != 1 or not added[0].startswith(expected):
        errors.append(f"expected one bridge lesson {expected}…, just before {NEEDED}; the tutor added {', '.join(added)}")
    elif NEEDED not in (validate.parse_frontmatter(course / added[0]) or {}).get("added_for", ""):
        errors.append(f'{added[0]}: added_for should be "[[{NEEDED}]]"')
    errors.extend(validate.check_course_placeholders(course))
    errors.extend(validate.check_course_lessons(course))
    errors.extend(validate.check_course_map(course))
    errors.extend(validate.check_lessons_kept(course, start))
    return errors


def lessons(course: Path) -> set[str]:
    """The course's lesson files, such as `01 Lists/02 List Comprehensions.md`."""
    return {
        f"{path.parent.name}/{path.name}"
        for path in course.glob("*/*.md")
        if validate.SECTION_RE.match(path.parent.name) and path.name != validate.SECTION_INDEX and validate.LESSON_RE.match(path.name)
    }


def claude(args: list[str], prompt: str, cwd: Path) -> dict:
    try:
        done = subprocess.run(["claude", "-p", "--output-format", "json", *args], input=prompt, cwd=cwd, capture_output=True, text=True, timeout=900)
        out = json.loads(done.stdout)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise AgentError(f"claude: {error}") from error
    except json.JSONDecodeError as error:
        raise AgentError(f"claude: {(done.stderr or done.stdout).strip()}") from error
    if out.get("is_error"):
        raise AgentError(f"claude: {out.get('result')}")
    return out


def claude_tutor(workspace: Path, model: str | None) -> Callable[[str], str]:
    """One Claude Code conversation in the workspace, resumed each turn."""
    context = "You have file tools only: no shell and no web access. Follow this study skill.\n\n" + (workspace / SKILL / "SKILL.md").read_text(encoding="utf-8")
    args = ["--restricted", "--strict-mcp-config", "--tools", "Read,Write,Edit,Glob,Grep", "--permission-mode", "acceptEdits", "--append-system-prompt", context]
    if model:
        args += ["--model", model]
    session: list[str] = []

    def reply(message: str) -> str:
        out = claude(args + ["--resume", session[-1]] if session else args, message, workspace)
        session.append(out["session_id"])
        return str(out.get("result", ""))

    return reply


def claude_learner(folder: Path, model: str) -> Callable[[Talk], str]:
    """A Claude Code run with no tools, in an empty folder, given the whole conversation each turn."""
    args = ["--restricted", "--strict-mcp-config", "--tools", "", "--no-session-persistence", "--model", model]
    return lambda talk: str(claude(args, LEARNER + "\n\n".join(f"{who}: {text}" for who, text in talk), folder).get("result", "")).strip()


def make_workspace(workspace: Path) -> tuple[Path, str]:
    """A learning workspace as How To Use It in the README makes one, with a short synthetic course, committed to git.

    The learner has studied both lessons of section 1. The second builds on for loops, which no lesson teaches.
    Returns the course folder and the commit.
    """
    shutil.copytree(ROOT / SKILL, workspace / SKILL)
    (workspace / ".claude" / "skills").mkdir(parents=True)
    (workspace / ".claude" / "skills" / SKILL.name).symlink_to(Path("..", "..", SKILL))
    shutil.copytree(ROOT / "_Course Scaffold", workspace / "_Course Scaffold")
    course = workspace / COURSE
    shutil.copytree(ROOT / "_Course Scaffold", course)
    shutil.rmtree(course / "01 Section Template")
    for path in course.rglob("*.md"):
        path.write_text(path.read_text(encoding="utf-8").replace("COURSE_NAME", COURSE), encoding="utf-8")
    dashboard = course / "00 Review Dashboard.md"
    rows = [line for line in dashboard.read_text(encoding="utf-8").splitlines() if "/exercises/" not in line and "/quizes/" not in line]
    dashboard.write_text("\n".join(rows).replace("01 Section Template", SECTION) + "\n", encoding="utf-8")
    studied = (date.today() - timedelta(days=7)).isoformat()
    for rel, text in course_files(studied).items():
        (course / rel).parent.mkdir(parents=True, exist_ok=True)
        (course / rel).write_text(text, encoding="utf-8")
    (workspace / "00 Courses Index.md").write_text(f"# Courses Index\n\n## Courses\n\n- [[{COURSE}/00 Curriculum Index|{COURSE}]]\n", encoding="utf-8")

    def git(*args: str) -> str:
        return subprocess.run(["git", *args], cwd=workspace, check=True, capture_output=True, text=True).stdout.strip()

    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=eval", "-c", "user.email=eval@example.com", "commit", "-q", "-m", "A short course")
    return course, git("rev-parse", "HEAD")


def course_files(studied: str) -> dict[str, str]:
    lesson = """---
type: lesson
title: "{title}"
section: "01 Lists"
source:
order: {order}
study_status: studied
last_studied: {studied}
study_count: 1
prerequisites: {prerequisites}
depends_on:
mastery_evidence:
---
# {title}

## Core Idea

{idea}

## Worked Example

{example}

## Study Notes
"""
    return {
        "00 Curriculum Index.md": """# Python Basics

Build and change lists and tuples in short Python programs.

## Course Contract

- **Outcome**: Write short Python programs that build and change lists and tuples.
- **Target Learner**: A beginner who has written a few lines of Python.
- **Boundary**: Lists and tuples only.
- **Source Policy**: The Python tutorial.
- **Practice Shape**: Short code questions.
- **Quiz Style**: Short answers.
- **Completion Standard**: Writes each lesson's kind of code without hints.
- **Maintenance Rule**: Keep lessons short.

## Sections

Every section, and under it every lesson, in the order they are taught. A section or lesson that isn't written yet is plain text, such as `- 02 Left Join`, not a link: the tutor writes it when the learner reaches it, then links it here.

- [[01 Lists/00 Section Index|01 Lists]]
  - [[01 Lists/01 Making Lists|01 Making Lists]]
  - [[01 Lists/02 List Comprehensions|02 List Comprehensions]]
- 02 Tuples
  - 01 Making Tuples
  - 02 Unpacking

## Curriculum Graph

| Section | Outcome | Prerequisites | Depends On | Mastery Evidence |
| --- | --- | --- | --- | --- |
| 01 Lists | Build lists and change them | None | None | Study set |
| 02 Tuples | Build tuples and unpack them | 01 Lists | 01 Lists | Study set |

## Study Tools

- [[00 Review Dashboard|Review Dashboard]]
- [[00 Course Setup Grill|Course Setup Grill]]
- [[Glossary/00 Glossary Index|Glossary]]
- [[CONTEXT|Course Context]]
""",
        "01 Lists/00 Section Index.md": """# 01 Lists

Build lists and change them.

## Prerequisites

- None yet.

## Depends On

- None yet.

## Lessons

A lesson that isn't written yet is plain text, not a link, until the learner reaches it.

- [[01 Making Lists|Making Lists]]
- [[02 List Comprehensions|List Comprehensions]]

## Study

Each set is listed here once it is written: flashcards as lessons are studied, exercises and the quiz once every lesson is.

- [[flashcards/Flashcards|Flashcards]]

## Repair Notes
""",
        "01 Lists/01 Making Lists.md": lesson.format(
            title="Making Lists",
            order="1.1",
            studied=studied,
            prerequisites="",
            idea="A list holds values in order. `nums[0]` reads the first value, and `nums.append(4)` adds a value at the end.",
            example="1. `nums = [3, 1]` makes a list of two values.\n2. `nums.append(4)` makes it `[3, 1, 4]`.\n3. `nums[2]` is `4`.",
        ),
        f"01 Lists/{NEEDED}.md": lesson.format(
            title="List Comprehensions",
            order="1.2",
            studied=studied,
            prerequisites='"[[01 Making Lists]]"',
            idea="A list comprehension builds a new list from another: `[x * 2 for x in nums]` doubles each value of `nums`.",
            example="1. `nums = [1, 2, 3]`.\n2. `[x * 2 for x in nums]` gives `[2, 4, 6]`.\n3. `[x for x in nums if x > 1]` gives `[2, 3]`.",
        ),
        "01 Lists/flashcards/Flashcards.md": f"""---
type: study-set
course: {COURSE}
section: "01 Lists"
status: needs review
last_reviewed: {studied}
next_review: {date.today().isoformat()}
review_count: 1
confidence: 3
notes:
---
# 01 Lists Flashcards

<details>
<summary>How do you add a value at the end of a list?</summary>

`nums.append(value)`.

Source lesson: [[../01 Making Lists|Making Lists]]

</details>

<details>
<summary>What does `[x + 1 for x in [1, 2]]` give?</summary>

`[2, 3]`.

Source lesson: [[../{NEEDED}|List Comprehensions]]

</details>
""",
    }


if __name__ == "__main__":
    raise SystemExit(main())
