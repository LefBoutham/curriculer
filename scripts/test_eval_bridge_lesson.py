"""Tests for the bridge lesson eval's checks, with a scripted tutor: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Callable

import eval_bridge_lesson as bridge
import validate_curriculer as validate

ROOT = Path(__file__).resolve().parents[1]

BRIDGE = """---
type: lesson
title: "For Loops"
section: "01 Lists"
source:
order: 1.1a
added_for: "[[02 List Comprehensions]]"
study_status: studied
last_studied: 2026-05-25
study_count: 1
prerequisites:
depends_on:
mastery_evidence:
---
# For Loops
"""

CARD = """
<details>
<summary>What does `for x in [1, 2]: print(x)` print?</summary>

1, then 2.

Source lesson: [[../01a For Loops|For Loops]]

</details>
"""


def edit(path: Path, old: str, new: str) -> None:
    path.write_text(path.read_text(encoding="utf-8").replace(old, new, 1), encoding="utf-8")


def add_bridge(course: Path) -> None:
    """What the tutor writes for a bridge lesson, as Bridge Lessons in `_Course Scaffold/AGENTS.md` says."""
    section = course / "01 Lists"
    (section / "01a For Loops.md").write_text(BRIDGE, encoding="utf-8")
    edit(section / "00 Section Index.md", "## Prerequisites\n\n- None yet.", "## Prerequisites\n\n- [[01a For Loops|For Loops]]")
    edit(section / "00 Section Index.md", "- [[02 List", "- [[01a For Loops|For Loops]]\n- [[02 List")
    edit(section / "flashcards" / "Flashcards.md", "\n<details>", CARD + "\n<details>")
    edit(course / "00 Curriculum Index.md", "| 01 Lists | Build lists and change them | None |", "| 01 Lists | Build lists and change them | 01a For Loops |")
    edit(course / "00 Curriculum Index.md", "  - [[01 Lists/02 List", "  - [[01 Lists/01a For Loops|01a For Loops]]\n  - [[01 Lists/02 List")


def renumber(course: Path) -> None:
    """A repair that makes room by renumbering instead of adding `01a`."""
    section = course / "01 Lists"
    (section / "02 List Comprehensions.md").rename(section / "03 List Comprehensions.md")
    (section / "02 For Loops.md").write_text(BRIDGE.replace("02 List Comprehensions", "03 List Comprehensions"), encoding="utf-8")


def tutor(*turns: tuple[str, Callable[[Path], None] | None], course: Path) -> Callable[[str], str]:
    """A tutor that gives these replies in turn, making each one's change to the course first."""
    replies = iter(turns)

    def reply(message: str) -> str:
        text, change = next(replies, ("Let's keep going.", None))
        if change:
            change(course)
        return text

    return reply


def learner(*replies: str) -> Callable[[bridge.Talk], str]:
    answers = iter(replies)
    return lambda talk: next(answers, "I don't know.")


QUESTION = ("What does [x * 2 for x in [1, 2]] give?", None)
DIAGNOSE = ("What does `for x in [1, 2]: print(x)` print?", None)
OFFER = ("Shall I add a short lesson on for loops before this one, with a few flashcards?", None)


class Eval(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.course, self.start = bridge.make_workspace(Path(self.tmp.name) / "workspace")
        self.talk: bridge.Talk = []

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def converse(self, tutor: Callable[[str], str], learner: Callable[[bridge.Talk], str], turns: int = 6) -> str:
        return "\n".join(bridge.converse(tutor, learner, self.course, self.start, self.talk, turns))

    def test_the_course_passes_the_course_check(self) -> None:
        errors = validate.check_course_placeholders(self.course) + validate.check_course_lessons(self.course) + validate.check_course_map(self.course)
        self.assertEqual(errors, [])
        self.assertEqual(len(bridge.lessons(self.course)), 2)

    def test_offering_then_adding_passes(self) -> None:
        added = ("I've added a short lesson on for loops before this one, with one flashcard.", add_bridge)
        result = self.converse(tutor(QUESTION, DIAGNOSE, OFFER, added, course=self.course), learner("I've never seen `for`.", bridge.AGREE))
        self.assertEqual(result, "")
        self.assertEqual(self.talk[2], ("Learner", bridge.UNSURE))

    def test_adding_before_the_learner_agrees_fails(self) -> None:
        added = ("I've added a short lesson on for loops before this one.", add_bridge)
        result = self.converse(tutor(QUESTION, DIAGNOSE, added, course=self.course), learner("I've never seen `for`."))
        self.assertIn("added 01 Lists/01a For Loops.md before the learner agreed", result)

    def test_renumbering_fails(self) -> None:
        added = ("I've added a lesson on for loops.", renumber)
        result = self.converse(tutor(QUESTION, DIAGNOSE, OFFER, added, course=self.course), learner("I've never seen `for`.", bridge.AGREE))
        self.assertIn("renumbered, renamed, moved or deleted 01 Lists/02 List Comprehensions.md", result)

    def test_a_bridge_lesson_that_breaks_the_course_check_fails(self) -> None:
        unlinked = ("I've added a lesson on for loops.", lambda course: (course / "01 Lists" / "01a For Loops.md").write_text(BRIDGE, encoding="utf-8"))
        result = self.converse(tutor(QUESTION, DIAGNOSE, OFFER, unlinked, course=self.course), learner("I've never seen `for`.", bridge.AGREE))
        self.assertIn("list bridge lesson '01a For Loops' under Lessons and Prerequisites", result)

    def test_never_offering_fails(self) -> None:
        result = self.converse(tutor(QUESTION, DIAGNOSE, course=self.course), learner(), turns=4)
        self.assertIn("didn't offer a lesson for the missing prerequisite in 4 replies", result)

    def test_writing_a_planned_lesson_is_not_a_repair(self) -> None:
        def write_planned(course: Path) -> None:
            (course / "02 Tuples").mkdir()
            (course / "02 Tuples" / "01 Making Tuples.md").write_text("---\ntype: lesson\nstudy_status: not started\n---\n# Making Tuples\n", encoding="utf-8")

        result = self.converse(tutor(QUESTION, ("On to tuples.", write_planned), course=self.course), learner(), turns=3)
        self.assertIn("didn't offer a lesson", result)
        self.assertNotIn("before the learner agreed", result)


class Rules(unittest.TestCase):
    def test_the_rules_offer_before_adding_and_only_add(self) -> None:
        skill = (ROOT / ".agents/skills/course-study-coach/SKILL.md").read_text(encoding="utf-8")
        scaffold = (ROOT / "_Course Scaffold/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Add it only when the learner agrees", skill)
        self.assertIn("adds it only when the learner agrees", scaffold)
        for text in [skill, scaffold]:
            self.assertIn("Never renumber, rename, move, or delete a lesson", text)


if __name__ == "__main__":
    unittest.main()
