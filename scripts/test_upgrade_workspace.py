"""Tests for the workspace upgrade: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import upgrade_workspace as upgrade

ROOT = upgrade.ROOT
SCRIPT = ROOT / "scripts" / "upgrade_workspace.py"
GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "test",
    "GIT_AUTHOR_EMAIL": "test@localhost",
    "GIT_COMMITTER_NAME": "test",
    "GIT_COMMITTER_EMAIL": "test@localhost",
}

OLD_STEP_3 = "3. Use `00 Course Setup Grill.md` to clarify the course goal, audience, scope, and section plan."
OLD_STEP_4 = "4. Replace `01 Section Template/` with real numbered course sections."
OLD_BRIDGE = (
    "When a learner lacks a prerequisite that no lesson teaches, the skill adds one short bridge lesson, "
    "such as `01a NULL Values.md`, with a few flashcards. Repairs only add: they never renumber, rename, "
    "move, or delete a lesson. The rules are under Bridge Lessons in `_Course Scaffold/AGENTS.md`."
)

COURSE_AGENTS = """# Stats Agent Instructions

## Mission

Teach descriptive statistics for a data analyst.

## Course Structure

Sections are numbered folders.

## Review Rules

- `confidence: 5`: `status: mastered`, review in 14 to 30 days

## Flashcards

Keep cards short.
"""

COURSE_CONTEXT = """# Stats Context

## Language

**Course**:
A self-contained learning path for one subject.

**Lesson**:
A note on descriptive statistics.

**Confidence**:
An old definition.

## Relationships

- A **Course** has sections.
"""

LESSON = """---
type: lesson
title: "Mean"
study_status: studied
last_studied: 2026-05-25
---
# Mean
"""

CARDS = """---
type: study-set
status: needs review
last_reviewed: 2026-05-25
next_review: 2026-05-28
review_count: 2
confidence: 3
---
# Flashcards
"""


def old_root_agents() -> str:
    lines = []
    for line in (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n"):
        if line.startswith("3. Run `00 Course Setup Grill.md`"):
            line = OLD_STEP_3
        elif line.startswith("4. Build the course map and lesson 1"):
            line = OLD_STEP_4
        elif line.startswith("When a learner lacks a prerequisite"):
            line = OLD_BRIDGE
        elif line.startswith(("A lesson the course map lists as plain text", "Before the first lesson of a new section")):
            continue
        lines.append(line)
    return "\n".join(lines).replace("\n\n\n", "\n\n").replace("\n\n\n", "\n\n")


def make_workspace(at: Path) -> Path:
    """A workspace as an old release left it, with one course and its review history."""
    shutil.copytree(ROOT / upgrade.SKILL, at / upgrade.SKILL)
    (at / upgrade.SKILL / "SKILL.md").write_text("an older skill\n", encoding="utf-8")
    shutil.copytree(ROOT / upgrade.SKILL, at / upgrade.OLD_SKILL)
    shutil.copytree(ROOT / upgrade.SCAFFOLD, at / upgrade.SCAFFOLD)
    (at / upgrade.SCAFFOLD / "AGENTS.md").write_text("an older scaffold\n", encoding="utf-8")
    (at / "AGENTS.md").write_text(old_root_agents(), encoding="utf-8")
    course = at / "Stats"
    (course / "01 Basics" / "flashcards").mkdir(parents=True)
    (course / "AGENTS.md").write_text(COURSE_AGENTS, encoding="utf-8")
    (course / "CONTEXT.md").write_text(COURSE_CONTEXT, encoding="utf-8")
    (course / "01 Basics" / "01 Mean.md").write_text(LESSON, encoding="utf-8")
    (course / "01 Basics" / "flashcards" / "Flashcards.md").write_text(CARDS, encoding="utf-8")
    (at / "Notes").mkdir()
    (at / "Notes" / "AGENTS.md").write_text("# Notes\n\n## Mission\n\nShort notes.\n", encoding="utf-8")
    return at


def snapshot(path: Path) -> dict[str, bytes]:
    return {
        file.relative_to(path).as_posix(): file.read_bytes()
        for file in sorted(path.rglob("*"))
        if file.is_file() and ".git" not in file.relative_to(path).parts
    }


def run(*args: str, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env)


class UpgradeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = make_workspace(Path(self.tmp.name) / "workspace")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_upgrade_brings_the_workspace_to_this_release(self) -> None:
        before = snapshot(self.workspace)
        result = run(str(self.workspace))
        self.assertEqual(result.returncode, 0, result.stderr)
        ws = self.workspace

        self.assertEqual(upgrade.tree(ws / upgrade.SKILL), upgrade.tree(ROOT / upgrade.SKILL))
        self.assertTrue((ws / upgrade.LINK).is_symlink())
        self.assertEqual((ws / upgrade.LINK).resolve(), (ws / upgrade.SKILL).resolve())
        self.assertFalse((ws / ".codex").exists())
        self.assertEqual(upgrade.tree(ws / upgrade.SCAFFOLD), upgrade.tree(ROOT / upgrade.SCAFFOLD))

        root = (ws / "AGENTS.md").read_text(encoding="utf-8")
        ours = (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n")
        for key, _, _ in upgrade.ROOT_LINES:
            line = next(line for line in ours if line.startswith(key))
            self.assertEqual(root.count(line), 1, key)
        for old in [OLD_STEP_3, OLD_STEP_4, OLD_BRIDGE]:
            self.assertNotIn(old, root)
        self.assertNotIn("\n\n\n", root)

        agents = (ws / "Stats" / "AGENTS.md").read_text(encoding="utf-8")
        scaffold = dict((title, body) for title, body in upgrade.split_sections((ROOT / upgrade.SCAFFOLD / "AGENTS.md").read_text(encoding="utf-8")))
        sections = dict((title, body) for title, body in upgrade.split_sections(agents))
        for name in upgrade.COURSE_SECTIONS:
            self.assertEqual(sections[name].rstrip(), scaffold[name].rstrip(), name)
        self.assertIn("Teach descriptive statistics for a data analyst.", agents)
        self.assertNotIn("14 to 30 days", agents)
        titles = [title for title, _ in upgrade.split_sections(agents) if title]
        self.assertEqual(titles, ["Mission", "Course Structure", "Building Lessons", "Review Rules", "Prerequisite Check", "Section Opener", "Bridge Lessons", "Flashcards"])

        context = (ws / "Stats" / "CONTEXT.md").read_text(encoding="utf-8")
        entries = upgrade.entries(context)
        wanted = upgrade.entries((ROOT / upgrade.SCAFFOLD / "CONTEXT.md").read_text(encoding="utf-8"))
        for name in upgrade.CONTEXT_ENTRIES:
            self.assertEqual(entries[name], wanted[name], name)
        self.assertEqual(entries["Lesson"], "**Lesson**:\nA note on descriptive statistics.")
        self.assertEqual(list(entries), ["Course", "Lesson", "Prerequisite", "Section Opener", "Bridge Lesson", "Confidence", "Mastered"])
        self.assertIn("## Relationships\n\n- A **Course** has sections.\n", context)

        after = snapshot(ws)
        for path in ["Stats/01 Basics/01 Mean.md", "Stats/01 Basics/flashcards/Flashcards.md"]:
            self.assertEqual(after[path], before[path], path)
        self.assertEqual((ws / upgrade.VERSION).read_text(encoding="utf-8"), f"{upgrade.release()}\n")
        self.assertIn("Notes/: has no CONTEXT.md", result.stdout)

        backups = [path for path in (ws / upgrade.BACKUPS).iterdir() if path.is_dir()]
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / upgrade.SKILL / "SKILL.md").read_text(encoding="utf-8"), "an older skill\n")
        self.assertEqual((backups[0] / "Stats" / "AGENTS.md").read_text(encoding="utf-8"), COURSE_AGENTS)
        self.assertTrue((backups[0] / upgrade.OLD_SKILL / "SKILL.md").is_file())
        self.assertFalse((backups[0] / "Stats" / "01 Basics").exists())

    def test_a_second_run_changes_nothing(self) -> None:
        self.assertEqual(run(str(self.workspace)).returncode, 0)
        before = snapshot(self.workspace)
        result = run(str(self.workspace))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Nothing to do.", result.stdout)
        self.assertEqual(snapshot(self.workspace), before)

    def test_check_reports_and_changes_nothing(self) -> None:
        before = snapshot(self.workspace)
        result = run("--check", str(self.workspace))
        self.assertEqual(result.returncode, 1)
        self.assertIn("would change", result.stdout)
        self.assertIn("- Stats/AGENTS.md: added Building Lessons; replaced Review Rules", result.stdout)
        self.assertEqual(snapshot(self.workspace), before)
        self.assertFalse((self.workspace / ".curriculer").exists())
        run(str(self.workspace))
        self.assertEqual(run("--check", str(self.workspace)).returncode, 0)

    def test_a_newer_workspace_is_left_alone(self) -> None:
        (self.workspace / upgrade.VERSION).parent.mkdir()
        (self.workspace / upgrade.VERSION).write_text("v99.0.0\n", encoding="utf-8")
        before = snapshot(self.workspace)
        result = run(str(self.workspace))
        self.assertEqual(result.returncode, 0)
        self.assertIn("newer than this", result.stdout)
        self.assertEqual(snapshot(self.workspace), before)

    def test_it_refuses_a_folder_that_is_not_a_workspace(self) -> None:
        empty = Path(self.tmp.name) / "empty"
        empty.mkdir()
        self.assertEqual(run(str(empty)).returncode, 2)
        self.assertEqual(run(str(ROOT)).returncode, 2)
        self.assertEqual(list(empty.iterdir()), [])

    def test_a_copied_skill_for_claude_code_stays_a_copy(self) -> None:
        link = self.workspace / upgrade.LINK
        shutil.copytree(self.workspace / upgrade.SKILL, link)
        self.assertEqual(run(str(self.workspace)).returncode, 0)
        self.assertFalse(link.is_symlink())
        self.assertEqual(upgrade.tree(link), upgrade.tree(ROOT / upgrade.SKILL))

    def test_commit_takes_only_the_upgrade(self) -> None:
        ws = self.workspace
        git = lambda *args: subprocess.run(["git", "-C", str(ws), *args], capture_output=True, text=True, check=True, env=GIT_ENV)
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "old")
        lesson = ws / "Stats" / "01 Basics" / "01 Mean.md"
        lesson.write_text(LESSON + "A note the learner hasn't committed.\n", encoding="utf-8")

        result = run("--commit", str(ws), env=GIT_ENV)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(git("log", "-1", "--format=%s").stdout.strip(), f"Upgrade Curriculer to {upgrade.release()}")
        self.assertEqual(git("status", "--short").stdout.strip(), 'M "Stats/01 Basics/01 Mean.md"')
        changed = git("show", "--name-only", "--format=", "HEAD").stdout
        self.assertIn(".codex/skills/course-study-coach/SKILL.md", changed)
        self.assertIn(".curriculer/version", changed)
        self.assertNotIn("backups", changed)

    def test_commit_failure_leaves_nothing_staged(self) -> None:
        ws = self.workspace
        git = lambda *args: subprocess.run(["git", "-C", str(ws), *args], capture_output=True, text=True, check=True, env=GIT_ENV)
        git("init", "-q")
        git("add", "-A")
        git("commit", "-q", "-m", "old")
        hook = ws / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\necho refused >&2\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        result = run("--commit", str(ws), env=GIT_ENV)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Not committed: refused", result.stderr)
        self.assertEqual(git("diff", "--cached", "--name-only").stdout, "")


class ReleaseTest(unittest.TestCase):
    def test_the_release_is_the_changelogs_first_version(self) -> None:
        self.assertIsNotNone(upgrade.version_key(upgrade.release()))

    def test_every_step_finds_its_text_in_this_release(self) -> None:
        root = (ROOT / "AGENTS.md").read_text(encoding="utf-8").split("\n")
        for key, _, anchors in upgrade.ROOT_LINES:
            self.assertEqual(sum(line.startswith(key) for line in root), 1, key)
        scaffold = [title for title, _ in upgrade.split_sections((ROOT / upgrade.SCAFFOLD / "AGENTS.md").read_text(encoding="utf-8"))]
        self.assertEqual([name for name in scaffold if name in upgrade.COURSE_SECTIONS], upgrade.COURSE_SECTIONS)
        entries = list(upgrade.entries((ROOT / upgrade.SCAFFOLD / "CONTEXT.md").read_text(encoding="utf-8")))
        self.assertEqual([name for name in entries if name in upgrade.CONTEXT_ENTRIES], upgrade.CONTEXT_ENTRIES)

    def test_entries_without_a_language_section_are_left_for_a_person(self) -> None:
        scaffold = (ROOT / upgrade.SCAFFOLD / "CONTEXT.md").read_text(encoding="utf-8")
        text = "# Context\n\n## Outcome\n\nA job.\n"
        new, done, missing = upgrade.upgrade_entries(text, scaffold, ["Confidence"])
        self.assertEqual((new, done, missing), (text, [], ["Confidence"]))


if __name__ == "__main__":
    unittest.main()
