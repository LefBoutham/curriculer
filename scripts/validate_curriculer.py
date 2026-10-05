#!/usr/bin/env python3
"""Validate Curriculer scaffold conventions without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "_Course Scaffold"
SKILLS = ROOT / ".agents" / "skills"
CLAUDE_SKILLS = ROOT / ".claude" / "skills"

ALLOWED_TOP_LEVEL = {
    ".agents",
    ".claude",
    ".git",
    ".github",
    ".gitignore",
    "00 Courses Index.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "_Course Scaffold",
    "docs",
    "scripts",
}

REQUIRED_FILES = [
    "AGENTS.md",
    "CONTEXT.md",
    "README.md",
    "00 Course Setup Grill.md",
    "00 Curriculum Index.md",
    "00 Review Dashboard.md",
    "Glossary/00 Glossary Index.md",
    "_attachments/README.md",
    "_attachments/00 Source Index.md",
    "docs/adr/README.md",
    "01 Section Template/00 Section Index.md",
    "01 Section Template/01 Lesson Template.md",
    "01 Section Template/exercises/Exercises.md",
    "01 Section Template/flashcards/Flashcards.md",
    "01 Section Template/quizes/Quiz.md",
    "01 Section Template/quizes/Quiz.html",
]

REVIEW_STATUS = {"not started", "needs practice", "needs review", "mastered"}
STUDY_STATUS = {"not started", "studied"}
DATE_FIELDS = {"last_reviewed", "next_review", "last_studied"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_RE = re.compile(r"COURSE_NAME|01 Section Template|Lesson Template|FROM \"COURSE_NAME\"")
WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
SECTION_RE = re.compile(r"^\d{2} ")
# A lesson is `01 Title.md`. A letter after the number marks a bridge lesson added during study: `01a Title.md`.
LESSON_RE = re.compile(r"^(\d{2})([a-z])? .+\.md$")
SECTION_INDEX = "00 Section Index.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["scaffold", "course"], default="scaffold")
    parser.add_argument("--course", type=Path, help="Copied course folder for --mode course")
    parser.add_argument("--since", help="With --mode course: a git commit; fail if a lesson the course had then is gone")
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(check_repo_shape())
    errors.extend(check_skills())
    errors.extend(check_scaffold_structure())
    errors.extend(check_frontmatter(SCAFFOLD))
    errors.extend(check_markdown_sanity(ROOT))
    errors.extend(check_wiki_links(SCAFFOLD))
    errors.extend(check_quiz_html(SCAFFOLD))

    if args.mode == "scaffold":
        errors.extend(check_scaffold_placeholders())
        if args.since:
            errors.append("--since works only with --mode course")
    else:
        if not args.course:
            errors.append("--course is required with --mode course")
        else:
            errors.extend(check_course_placeholders(args.course))
            errors.extend(check_course_lessons(args.course))
            errors.extend(check_course_map(args.course))
            if args.since:
                errors.extend(check_lessons_kept(args.course, args.since))

    if errors:
        print("Curriculer validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Curriculer validation passed.")
    return 0


def check_repo_shape() -> list[str]:
    errors: list[str] = []
    for path in ROOT.iterdir():
        if path.name not in ALLOWED_TOP_LEVEL:
            errors.append(f"unexpected top-level item {path.name!r}; do not add real courses to this repo")
    return errors


def check_skills() -> list[str]:
    errors: list[str] = []
    names = {"course-study-coach"}
    for folder in [SKILLS, CLAUDE_SKILLS]:
        if folder.is_dir():
            names.update(path.name for path in folder.iterdir() if not path.name.startswith("."))
    for name in sorted(names):
        skill = SKILLS / name
        link = CLAUDE_SKILLS / name
        if not (skill / "SKILL.md").is_file():
            errors.append(f"missing skill file: .agents/skills/{name}/SKILL.md")
        elif not link.is_symlink() or link.resolve() != skill.resolve():
            errors.append(f".claude/skills/{name} must be a symlink to ../../.agents/skills/{name} so Claude Code finds the skill")
    return errors


def check_scaffold_structure() -> list[str]:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (SCAFFOLD / rel).exists():
            errors.append(f"missing scaffold file: _Course Scaffold/{rel}")
    for path in SCAFFOLD.rglob("*"):
        if path.is_dir() and path.name == "quizzes":
            errors.append(f"use canonical 'quizes' folder spelling, not {path}")
    return errors


def check_frontmatter(root: Path) -> list[str]:
    errors: list[str] = []
    files = [
        root / "Glossary/00 Glossary Index.md",
        root / "01 Section Template/01 Lesson Template.md",
        root / "01 Section Template/exercises/Exercises.md",
        root / "01 Section Template/flashcards/Flashcards.md",
        root / "01 Section Template/quizes/Quiz.md",
    ]
    for path in files:
        data = parse_frontmatter(path)
        if data is None:
            errors.append(f"missing frontmatter: {path.relative_to(ROOT)}")
            continue
        errors.extend(validate_frontmatter(path, data))
    return errors


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip().strip('"')
    return None


def validate_frontmatter(path: Path, data: dict[str, str]) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    is_lesson = path.name == "01 Lesson Template.md"
    is_reviewable = path.name in {"Exercises.md", "Flashcards.md", "Quiz.md"}

    if is_lesson:
        required = {
            "type",
            "title",
            "section",
            "source",
            "order",
            "study_status",
            "last_studied",
            "study_count",
            "prerequisites",
            "depends_on",
            "mastery_evidence",
        }
        errors.extend(missing_keys(rel, data, required))
        if data.get("type") != "lesson":
            errors.append(f"{rel}: lesson type must be 'lesson'")
        if data.get("study_status") not in STUDY_STATUS:
            errors.append(f"{rel}: invalid study_status {data.get('study_status')!r}")
        errors.extend(validate_int(rel, "study_count", data.get("study_count")))

    if is_reviewable:
        required = {
            "type",
            "course",
            "section",
            "status",
            "last_reviewed",
            "next_review",
            "review_count",
            "confidence",
            "notes",
        }
        if path.name == "Quiz.md":
            required.update({"last_score", "best_score"})
        errors.extend(missing_keys(rel, data, required))
        expected_type = {"Exercises.md": "exercises", "Flashcards.md": "study-set", "Quiz.md": "quiz"}[path.name]
        if data.get("type") != expected_type:
            errors.append(f"{rel}: type must be {expected_type!r}")
        if data.get("status") not in REVIEW_STATUS:
            errors.append(f"{rel}: invalid status {data.get('status')!r}")
        errors.extend(validate_int(rel, "review_count", data.get("review_count")))
        errors.extend(validate_confidence(rel, data.get("confidence", "")))

    for field in DATE_FIELDS:
        value = data.get(field, "")
        if value and not DATE_RE.match(value):
            errors.append(f"{rel}: {field} must be blank or YYYY-MM-DD")

    return errors


def missing_keys(rel: Path, data: dict[str, str], required: set[str]) -> list[str]:
    return [f"{rel}: missing frontmatter field {key!r}" for key in sorted(required - set(data))]


def validate_int(rel: Path, field: str, value: str | None) -> list[str]:
    if value is None:
        return []
    if not re.match(r"^\d+$", value):
        return [f"{rel}: {field} must be a non-negative integer"]
    return []


def validate_confidence(rel: Path, value: str) -> list[str]:
    if value == "":
        return []
    if not re.match(r"^\d+$", value):
        return [f"{rel}: confidence must be blank or an integer from 0 to 5"]
    if int(value) > 5:
        return [f"{rel}: confidence must be blank or an integer from 0 to 5"]
    return []


def check_markdown_sanity(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        fence_count = sum(1 for line in text.splitlines() if line.startswith("```"))
        if fence_count % 2:
            errors.append(f"{path.relative_to(ROOT)}: unbalanced fenced code block")
    return errors


def check_wiki_links(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("*.md"):
        if path.name == "README.md":
            continue
        text = strip_code_fences(path.read_text(encoding="utf-8"))
        for raw in WIKI_LINK_RE.findall(text):
            target = raw.split("|", 1)[0].split("#", 1)[0].strip()
            if target == "Term Name":
                continue
            if not resolves_wiki_target(path.parent, target):
                errors.append(f"{path.relative_to(ROOT)}: unresolved wiki link [[{raw}]]")
    return errors


def strip_code_fences(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def resolves_wiki_target(base: Path, target: str) -> bool:
    candidates = [
        base / target,
        base / f"{target}.md",
        base / f"{target}.html",
        SCAFFOLD / target,
        SCAFFOLD / f"{target}.md",
        SCAFFOLD / f"{target}.html",
    ]
    return any(path.exists() for path in candidates)


def check_quiz_html(root: Path) -> list[str]:
    errors: list[str] = []
    for path in root.rglob("quizes/Quiz.html"):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        required = ['id="quiz"', 'id="grade"', 'id="result"', "const questions", "<fieldset", "<legend"]
        for marker in required:
            if marker not in text:
                errors.append(f"{rel}: missing {marker}")
        forbidden = [r"<script[^>]+src=", r"<link[^>]+href=", r"https?://", r"fetch\(", r"XMLHttpRequest"]
        for pattern in forbidden:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{rel}: quiz HTML must be self-contained; found {pattern}")
    return errors


def check_scaffold_placeholders() -> list[str]:
    text = "\n".join(path.read_text(encoding="utf-8") for path in SCAFFOLD.rglob("*.md"))
    errors: list[str] = []
    for placeholder in ["COURSE_NAME", "01 Section Template", "Lesson Template"]:
        if placeholder not in text:
            errors.append(f"scaffold mode expects placeholder {placeholder!r}")
    dashboard = SCAFFOLD / "00 Review Dashboard.md"
    if 'FROM "COURSE_NAME"' not in dashboard.read_text(encoding="utf-8"):
        errors.append('scaffold dashboard should retain FROM "COURSE_NAME" placeholder')
    return errors


def check_course_placeholders(course: Path) -> list[str]:
    errors: list[str] = []
    if not course.exists():
        return [f"course path does not exist: {course}"]
    for path in course.rglob("*"):
        if path.is_file() and path.suffix in {".md", ".html"}:
            text = path.read_text(encoding="utf-8")
            if path.suffix == ".md":
                text = without_code_examples(text)
            if PLACEHOLDER_RE.search(text):
                errors.append(f"{path}: copied course still contains scaffold placeholder")
    return errors


INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def without_code_examples(text: str) -> str:
    """Markdown without its code blocks and inline code, which may name a placeholder as an example. Dataview blocks run, so they stay."""
    lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        if line.startswith("```"):
            fence = line[3:].strip() if fence is None else None
            continue
        if fence is None:
            lines.append(INLINE_CODE_RE.sub("", line))
        elif fence == "dataview":
            lines.append(line)
    return "\n".join(lines)


def check_course_lessons(course: Path) -> list[str]:
    """Check that each bridge lesson is placed, marked, and linked as Bridge Lessons in AGENTS.md says."""
    errors: list[str] = []
    if not course.is_dir():
        return errors
    index = course / "00 Curriculum Index.md"
    course_index = index.read_text(encoding="utf-8") if index.is_file() else ""
    for section in sorted(path for path in course.iterdir() if path.is_dir() and SECTION_RE.match(path.name)):
        lessons = [(path, LESSON_RE.match(path.name)) for path in sorted(section.glob("*.md")) if path.name != SECTION_INDEX]
        numbers = {match.group(1) for path, match in lessons if match and not match.group(2)}
        seen: set[str] = set()
        for path, match in lessons:
            if not match or not match.group(2):
                continue
            number, letter = match.groups()
            stem = path.stem
            if number + letter in seen:
                errors.append(f"{path}: another bridge lesson is numbered {number}{letter}; use the next free letter")
            seen.add(number + letter)
            if number != "00" and number not in numbers:
                errors.append(f"{path}: no lesson {number} in this section; a bridge lesson takes the number of the lesson before it")
            data = parse_frontmatter(path)
            if data is None:
                errors.append(f"{path}: missing frontmatter")
                continue
            if data.get("type") != "lesson":
                errors.append(f"{path}: lesson type must be 'lesson'")
            if data.get("study_status") not in STUDY_STATUS:
                errors.append(f"{path}: invalid study_status {data.get('study_status')!r}")
            needed_by = [link_stem(raw) for raw in WIKI_LINK_RE.findall(data.get("added_for", ""))]
            if not needed_by:
                errors.append(f'{path}: added_for must link the lesson that needed it, such as "[[02 Left Join]]"')
            elif not (section / f"{needed_by[0]}.md").is_file():
                errors.append(f"{path}: added_for links {needed_by[0]!r}, which is not a lesson in this section")
            if not links_to(section / SECTION_INDEX, stem):
                errors.append(f"{section / SECTION_INDEX}: list bridge lesson {stem!r} under Lessons and Prerequisites")
            if not links_to(section / "flashcards" / "Flashcards.md", stem):
                errors.append(f"{section / 'flashcards' / 'Flashcards.md'}: add 2 to 4 cards whose Source lesson links bridge lesson {stem!r}")
            if "## Curriculum Graph" in course_index and stem not in course_index:
                errors.append(f"{index}: add bridge lesson {stem!r} to the Prerequisites cell of the {section.name!r} row in the Curriculum Graph")
    return errors


# A list item and its indent: `- 02 Left Join`, or `  - [[01 Basics/01 Tables And Rows|…]]` under a section.
LIST_ITEM_RE = re.compile(r"^(\s*)[-*+]\s+(.+?)\s*$")
# A section or lesson named in plain text, as a planned one is: `02 Left Join`.
PLANNED_RE = re.compile(r"^\d{2}[a-z]? [^\[\]]+$")


def check_course_map(course: Path) -> list[str]:
    """In the course map and the section indexes, a written lesson is a link and a planned one is plain text (Planned Lessons in AGENTS.md)."""
    errors: list[str] = []
    index = course / "00 Curriculum Index.md"
    if not course.is_dir() or not index.is_file():
        return errors
    files = {path.relative_to(course).as_posix() for path in course.rglob("*") if path.is_file()}
    pages = [(index, "Sections")]
    pages += [(section / SECTION_INDEX, "Lessons") for section in sorted(course.iterdir()) if section.is_dir() and SECTION_RE.match(section.name)]
    for page, heading in pages:
        if not page.is_file():
            continue
        # A lesson in the map is listed under its section; one in a section index, in that section.
        folder = page.parent
        for depth, item in list_items(strip_code_fences(page.read_text(encoding="utf-8")), heading):
            target = link_target(item)
            if heading == "Sections" and depth == 0:
                folder = course / (target.split("/", 1)[0] if target else item)
            if target is not None:
                if LESSON_RE.match(f"{target.rsplit('/', 1)[-1]}.md") and not in_course(files, course, page.parent, target):
                    errors.append(f"{page}: {item} links a lesson that isn't written; write it, or list it as plain text while it's planned")
            elif PLANNED_RE.match(item) and (folder / (SECTION_INDEX if heading == "Sections" and depth == 0 else f"{item}.md")).is_file():
                errors.append(f"{page}: {item!r} is written; make it a link")
    return errors


def list_items(text: str, heading: str) -> list[tuple[int, str]]:
    """The list items under `## heading`, up to the next heading, with 0 for a top-level item."""
    items: list[tuple[int, str]] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("#"):
            inside = line.strip() == f"## {heading}"
            continue
        match = LIST_ITEM_RE.match(line) if inside else None
        if match:
            items.append((0 if not match.group(1) else 1, match.group(2)))
    return items


def link_target(item: str) -> str | None:
    """The note an item's first wiki link points to, without alias, heading or `.md`."""
    match = WIKI_LINK_RE.search(item)
    return match.group(1).split("|", 1)[0].split("#", 1)[0].strip().removesuffix(".md") if match else None


def in_course(files: set[str], course: Path, base: Path, target: str) -> bool:
    """Whether a link resolves as Obsidian would: next to the page, or anywhere in the course by its path (`02 Joins/01 Inner Join`) or, without a folder, by its name."""
    rel = base.relative_to(course).as_posix()
    near = f"{rel}/{target}.md" if rel != "." else f"{target}.md"
    return near in files or any(file == f"{target}.md" or file.endswith(f"/{target}.md") for file in files)


def link_stem(raw: str) -> str:
    """The note a wiki link points to, without folders, alias, heading, or `.md`."""
    target = raw.split("|", 1)[0].split("#", 1)[0].strip()
    return target.rsplit("/", 1)[-1].removesuffix(".md")


def links_to(path: Path, stem: str) -> bool:
    if not path.is_file():
        return False
    return any(link_stem(raw) == stem for raw in WIKI_LINK_RE.findall(path.read_text(encoding="utf-8")))


def check_lessons_kept(course: Path, since: str) -> list[str]:
    """Repairs only add lessons, so every lesson the course had at `since` must still be there."""
    if since.startswith("-"):
        return [f"--since {since!r} must name a commit"]
    try:
        listed = subprocess.run(
            ["git", "ls-tree", "-r", "-z", "--name-only", since, "--", "."],
            cwd=course,
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as error:
        detail = (getattr(error, "stderr", None) or str(error)).strip()
        return [f"--since {since}: cannot read the course at that commit: {detail}"]
    errors: list[str] = []
    for rel in listed.split("\0"):
        parts = rel.split("/")
        if len(parts) != 2 or not SECTION_RE.match(parts[0]) or parts[1] == SECTION_INDEX or not LESSON_RE.match(parts[1]):
            continue
        if not (course / rel).is_file():
            errors.append(f"{course / rel}: this lesson was in the course at {since} and is gone; repairs only add lessons, never renumber, rename, move, or delete one")
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
