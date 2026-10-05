"""Tests for the validator's course checks: python3 -m unittest discover -s scripts"""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import validate_curriculer as validate

BRIDGE = """---
type: lesson
title: "NULL Values"
section: "03 Joins"
source:
order: 3.1a
added_for: "[[02 Left Join]]"
study_status: studied
last_studied: 2026-05-25
study_count: 1
prerequisites:
depends_on:
mastery_evidence:
---
# NULL Values
"""

LESSON = """---
type: lesson
title: "{title}"
study_status: not started
---
# {title}
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class CourseLessons(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.course = Path(self.tmp.name) / "SQL"
        joins = self.course / "03 Joins"
        write(self.course / "00 Curriculum Index.md", "# SQL\n\n## Curriculum Graph\n\n| Section | Prerequisites |\n| --- | --- |\n| 03 Joins | 01a NULL Values |\n")
        write(joins / "00 Section Index.md", "# 03 Joins\n\n## Prerequisites\n\n- [[01a NULL Values]]\n\n## Lessons\n\n- [[01 Inner Join]]\n- [[01a NULL Values|NULL Values]]\n- [[02 Left Join]]\n")
        write(joins / "01 Inner Join.md", LESSON.format(title="Inner Join"))
        write(joins / "01a NULL Values.md", BRIDGE)
        write(joins / "02 Left Join.md", LESSON.format(title="Left Join"))
        write(joins / "flashcards" / "Flashcards.md", "<details>\n<summary>What is NULL?</summary>\n\nNo value.\n\nSource lesson: [[../01a NULL Values|NULL Values]]\n\n</details>\n")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def errors(self) -> str:
        return "\n".join(validate.check_course_lessons(self.course))

    def test_a_linked_bridge_lesson_passes(self) -> None:
        self.assertEqual(self.errors(), "")

    def test_a_course_without_bridge_lessons_passes(self) -> None:
        (self.course / "03 Joins" / "01a NULL Values.md").unlink()
        self.assertEqual(self.errors(), "")

    def test_a_bridge_lesson_needs_its_origin(self) -> None:
        write(self.course / "03 Joins" / "01a NULL Values.md", BRIDGE.replace('added_for: "[[02 Left Join]]"', "added_for:"))
        self.assertIn("added_for must link the lesson that needed it", self.errors())
        write(self.course / "03 Joins" / "01a NULL Values.md", BRIDGE.replace("02 Left Join", "09 Outer Join"))
        self.assertIn("not a lesson in this section", self.errors())

    def test_a_bridge_lesson_needs_its_links(self) -> None:
        write(self.course / "00 Curriculum Index.md", "# SQL\n\n## Curriculum Graph\n\n| Section | Prerequisites |\n| --- | --- |\n| 03 Joins | None |\n")
        write(self.course / "03 Joins" / "00 Section Index.md", "# 03 Joins\n")
        write(self.course / "03 Joins" / "flashcards" / "Flashcards.md", "# Flashcards\n")
        errors = self.errors()
        self.assertIn("list bridge lesson '01a NULL Values' under Lessons", errors)
        self.assertIn("add 2 to 4 cards", errors)
        self.assertIn("Curriculum Graph", errors)

    def test_a_bridge_lesson_follows_a_lesson_of_its_number(self) -> None:
        (self.course / "03 Joins" / "01a NULL Values.md").rename(self.course / "03 Joins" / "05a NULL Values.md")
        self.assertIn("no lesson 05 in this section", self.errors())

    def test_00a_comes_before_the_first_lesson(self) -> None:
        (self.course / "03 Joins" / "01a NULL Values.md").rename(self.course / "03 Joins" / "00a NULL Values.md")
        for name in ["00 Section Index.md", "flashcards/Flashcards.md"]:
            path = self.course / "03 Joins" / name
            write(path, path.read_text(encoding="utf-8").replace("01a NULL", "00a NULL"))
        write(self.course / "00 Curriculum Index.md", (self.course / "00 Curriculum Index.md").read_text(encoding="utf-8").replace("01a", "00a"))
        self.assertEqual(self.errors(), "")

    def test_since_finds_a_renamed_lesson(self) -> None:
        git = lambda *args: subprocess.run(["git", *args], cwd=self.tmp.name, check=True, capture_output=True)
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "course")
        self.assertEqual(validate.check_lessons_kept(self.course, "HEAD"), [])
        write(self.course / "03 Joins" / "01b Outer Rows.md", BRIDGE)
        self.assertEqual(validate.check_lessons_kept(self.course, "HEAD"), [])
        (self.course / "03 Joins" / "02 Left Join.md").rename(self.course / "03 Joins" / "03 Left Join.md")
        errors = validate.check_lessons_kept(self.course, "HEAD")
        self.assertEqual(len(errors), 1)
        self.assertIn("02 Left Join.md: this lesson was in the course at HEAD and is gone", errors[0])

    def test_since_needs_git_history(self) -> None:
        self.assertIn("cannot read the course", validate.check_lessons_kept(self.course, "HEAD")[0])


MAP = """# SQL

## Sections

Every section, and under it every lesson. A section or lesson that isn't written yet is plain text, such as `- 02 Left Join`.

- [[01 Basics/00 Section Index|01 Basics]]
  - [[01 Basics/01 Tables And Rows|01 Tables And Rows]]
  - 02 Selecting Columns
- 02 Joins
  - 01 Inner Join
  - 02 Left Join

## Study Tools

- [[00 Review Dashboard|Review Dashboard]]
"""

SECTION = """# 01 Basics

## Lessons

- [[01 Tables And Rows|Tables And Rows]]
- 02 Selecting Columns

## Study

- None yet.
"""


class CourseMap(unittest.TestCase):
    """Planned lessons: listed in the map as plain text, written when the learner reaches them."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.course = Path(self.tmp.name) / "SQL"
        write(self.course / "00 Curriculum Index.md", MAP)
        write(self.course / "01 Basics" / "00 Section Index.md", SECTION)
        write(self.course / "01 Basics" / "01 Tables And Rows.md", LESSON.format(title="Tables And Rows"))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def errors(self) -> str:
        return "\n".join(validate.check_course_map(self.course) + validate.check_course_lessons(self.course))

    def test_planned_lessons_and_sections_pass(self) -> None:
        self.assertEqual(self.errors(), "")

    def test_a_link_to_an_unwritten_lesson_fails(self) -> None:
        index = self.course / "00 Curriculum Index.md"
        write(index, MAP.replace("  - 02 Selecting Columns", "  - [[01 Basics/02 Selecting Columns|02 Selecting Columns]]"))
        self.assertIn("links a lesson that isn't written", self.errors())
        write(index, MAP.replace("- 02 Joins", "- [[02 Joins/00 Section Index|02 Joins]]"))
        self.assertIn("links a lesson that isn't written", self.errors())

    def test_a_written_lesson_is_a_link(self) -> None:
        write(self.course / "01 Basics" / "02 Selecting Columns.md", LESSON.format(title="Selecting Columns"))
        errors = self.errors()
        self.assertIn("00 Curriculum Index.md: '02 Selecting Columns' is written; make it a link", errors)
        self.assertIn("00 Section Index.md: '02 Selecting Columns' is written; make it a link", errors)
        for name, old, new in [
            ("00 Curriculum Index.md", "  - 02 Selecting Columns", "  - [[01 Basics/02 Selecting Columns|02 Selecting Columns]]"),
            ("01 Basics/00 Section Index.md", "- 02 Selecting Columns", "- [[02 Selecting Columns|Selecting Columns]]"),
        ]:
            path = self.course / name
            write(path, path.read_text(encoding="utf-8").replace(old, new))
        self.assertEqual(self.errors(), "")

    def test_a_written_section_is_a_link(self) -> None:
        write(self.course / "02 Joins" / "00 Section Index.md", "# 02 Joins\n\n## Lessons\n\n- 01 Inner Join\n- 02 Left Join\n")
        self.assertIn("'02 Joins' is written; make it a link", self.errors())


class CoursePlaceholders(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.course = Path(self.tmp.name) / "SQL"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def errors(self, name: str, text: str) -> list[str]:
        write(self.course / name, text)
        return validate.check_course_placeholders(self.course)

    def test_placeholders_in_code_examples_pass(self) -> None:
        text = "Replace `01 Section Template` with real sections.\n\n```yaml\ncourse: COURSE_NAME\n```\n\n```sh\nrg \"Lesson Template\"\n```\n"
        self.assertEqual(self.errors("AGENTS.md", text), [])

    def test_a_placeholder_in_frontmatter_fails(self) -> None:
        self.assertTrue(self.errors("01 Basics/flashcards/Flashcards.md", "---\ntype: flashcards\ncourse: COURSE_NAME\n---\n"))

    def test_a_placeholder_in_text_fails(self) -> None:
        self.assertTrue(self.errors("00 Curriculum Index.md", "# COURSE_NAME\n"))

    def test_a_placeholder_in_a_dataview_query_fails(self) -> None:
        self.assertTrue(self.errors("00 Review Dashboard.md", "```dataview\nTABLE status\nFROM \"COURSE_NAME\"\n```\n"))


if __name__ == "__main__":
    unittest.main()
