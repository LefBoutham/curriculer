#!/usr/bin/env python3
"""Validate Curriculer scaffold conventions without third-party dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAFFOLD = ROOT / "_Course Scaffold"

ALLOWED_TOP_LEVEL = {
    ".codex",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["scaffold", "course"], default="scaffold")
    parser.add_argument("--course", type=Path, help="Copied course folder for --mode course")
    args = parser.parse_args()

    errors: list[str] = []
    errors.extend(check_repo_shape())
    errors.extend(check_scaffold_structure())
    errors.extend(check_frontmatter(SCAFFOLD))
    errors.extend(check_markdown_sanity(ROOT))
    errors.extend(check_wiki_links(SCAFFOLD))
    errors.extend(check_quiz_html(SCAFFOLD))

    if args.mode == "scaffold":
        errors.extend(check_scaffold_placeholders())
    else:
        if not args.course:
            errors.append("--course is required with --mode course")
        else:
            errors.extend(check_course_placeholders(args.course))

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
            if PLACEHOLDER_RE.search(text):
                errors.append(f"{path}: copied course still contains scaffold placeholder")
    return errors


if __name__ == "__main__":
    raise SystemExit(main())
