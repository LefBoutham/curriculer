#!/usr/bin/env python3
"""Upgrade a learning workspace's Curriculer files to this release.

    python3 scripts/upgrade_workspace.py [--check] [--commit] WORKSPACE

It follows the CHANGELOG's upgrade steps, and changes only what Curriculer owns:

- the `course-study-coach` skill, its `.claude/skills/` link or copy, and the
  old `.codex/skills/` copy, which it removes;
- `_Course Scaffold/` at the workspace root;
- in the root `AGENTS.md`, the setup steps and study paragraphs that releases
  changed;
- in each course's `AGENTS.md`, the rule sections that releases asked you to
  copy in, and in its `CONTEXT.md`, the matching Language entries.

Lessons, flashcards, exercises, quizzes, glossaries and review metadata are
never read or written. Before it writes, it copies every file it will change to
`.curriculer/backups/<time>/` in the workspace. It records the release in
`.curriculer/version`. Run twice, the second run finds nothing to do.

--check reports what would change, changes nothing, and exits 1 when the
workspace isn't current. --commit commits the upgrade in the workspace's Git
repository, and only the files it changed.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = Path(".agents/skills/course-study-coach")
LINK = Path(".claude/skills/course-study-coach")
OLD_SKILL = Path(".codex/skills/course-study-coach")
SCAFFOLD = Path("_Course Scaffold")
VERSION = Path(".curriculer/version")
BACKUPS = Path(".curriculer/backups")
JUNK = {".DS_Store", "Thumbs.db", "desktop.ini"}

# Sections of `_Course Scaffold/AGENTS.md` a release asked you to copy into each
# course's `AGENTS.md` (v0.5.0, v0.3.0, v0.4.0, v0.10.0, and v0.6.0 then v0.8.0),
# in the scaffold's order.
COURSE_SECTIONS = ["Building Lessons", "Review Rules", "Prerequisite Check", "Section Opener", "Bridge Lessons"]
# Their entries in `_Course Scaffold/CONTEXT.md`, for each course's `CONTEXT.md`.
CONTEXT_ENTRIES = ["Prerequisite", "Section Opener", "Bridge Lesson", "Confidence", "Mastered"]

# Lines of the workspace's root `AGENTS.md` that releases changed. Each is the
# line of this repo's `AGENTS.md` that starts with the key. It replaces a line
# that starts with the key or with an older start. When the workspace has
# neither, it goes in as a paragraph after the line that starts with an anchor.
ROOT_LINES = [
    # v0.8.0: the short setup grill.
    ("3. Run `00 Course Setup Grill.md`", ["3. Use `00 Course Setup Grill.md`"], []),
    # v0.9.0: the map and lesson 1 first.
    ("4. Build the course map and lesson 1", ["4. Replace `01 Section Template/`"], []),
    # v0.6.0, then v0.8.0: bridge lessons, offered.
    ("When a learner lacks a prerequisite that no lesson teaches", [], ["Use the repo-scoped `course-study-coach`", "Use the workspace's `course-study-coach`"]),
    # v0.9.0: planned lessons.
    ("A lesson the course map lists as plain text is planned", [], ["Follow the course-level `AGENTS.md`"]),
    # v0.10.0: the section opener.
    ("Before the first lesson of a new section", [], ["A lesson the course map lists as plain text is planned"]),
]


def release() -> str:
    """This release, from the first version heading of the CHANGELOG."""
    match = re.search(r"^## (v\d+\.\d+\.\d+)\s*$", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise SystemExit("CHANGELOG.md has no version heading.")
    return match.group(1)


def version_key(version: str) -> tuple[int, ...] | None:
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", version.strip())
    return tuple(int(part) for part in match.groups()) if match else None


def tree(path: Path) -> dict[str, bytes]:
    return {
        file.relative_to(path).as_posix(): file.read_bytes()
        for file in sorted(path.rglob("*"))
        if file.is_file() and file.name not in JUNK
    }


def same_tree(a: Path, b: Path) -> bool:
    return a.is_dir() and tree(a) == tree(b)


def split_sections(text: str) -> list[list]:
    """[[title, text]] for each `## ` section, with the text before the first as title None."""
    parts: list[list] = [[None, ""]]
    fenced = False
    for line in text.splitlines(keepends=True):
        if line.startswith("```"):
            fenced = not fenced
        match = None if fenced else re.match(r"## (.+?)\s*$", line)
        if match:
            parts.append([match.group(1), ""])
        parts[-1][1] += line
    return parts


def ending(text: str) -> str:
    return text[len(text.rstrip("\n")):]


def upgrade_sections(text: str, scaffold: str, names: list[str]) -> tuple[str, list[str]]:
    """Puts each named scaffold section into a course's AGENTS.md, in the scaffold's order."""
    sections = split_sections(text)
    wanted = {title: body for title, body in split_sections(scaffold) if title}
    order = [title for title, _ in split_sections(scaffold) if title]
    done = []
    for name in names:
        new = wanted[name].rstrip("\n")
        titles = [title for title, _ in sections]
        if name in titles:
            index = titles.index(name)
            old = sections[index][1]
            if old.rstrip() == new.rstrip():
                continue
            sections[index][1] = new + (ending(old) or "\n")
            done.append(f"replaced {name}")
            continue
        index = insertion(titles, order, name)
        if index > 0 and not sections[index - 1][1].endswith("\n\n"):
            sections[index - 1][1] = sections[index - 1][1].rstrip("\n") + "\n\n"
        sections.insert(index, [name, new + ("\n\n" if index < len(sections) else "\n")])
        done.append(f"added {name}")
    return "".join(body for _, body in sections), done


def insertion(titles: list, order: list[str], name: str) -> int:
    """Just after the nearest section before it in the scaffold, or else just before the nearest after it."""
    position = order.index(name)
    for before in reversed(order[:position]):
        if before in titles:
            return titles.index(before) + 1
    for after in order[position + 1:]:
        if after in titles:
            return titles.index(after)
    return len(titles)


def entries(text: str) -> dict[str, str]:
    """`**Name**:` entries, each up to the next blank line."""
    found = {}
    for match in re.finditer(r"^\*\*(.+?)\*\*:[^\n]*(?:\n[^\n]+)*", text, re.MULTILINE):
        found.setdefault(match.group(1), match.group(0))
    return found


def upgrade_entries(text: str, scaffold: str, names: list[str]) -> tuple[str, list[str], list[str]]:
    """Puts each named Language entry into a course's CONTEXT.md, in the scaffold's order."""
    wanted = entries(scaffold)
    order = list(wanted)
    done, missing = [], []
    for name in names:
        have = entries(text)
        if name in have:
            if have[name] != wanted[name]:
                text = text.replace(have[name], wanted[name], 1)
                done.append(f"replaced {name}")
            continue
        position = order.index(name)
        before = next((have[other] for other in reversed(order[:position]) if other in have), None)
        after = next((have[other] for other in order[position + 1:] if other in have), None)
        if before:
            at = text.index(before) + len(before)
            text = text[:at] + "\n\n" + wanted[name] + text[at:]
        elif after:
            at = text.index(after)
            text = text[:at] + wanted[name] + "\n\n" + text[at:]
        else:
            language = re.search(r"^## (?:.*\s)?Language\s*\n", text, re.MULTILINE)
            if not language:
                missing.append(name)
                continue
            rest = re.search(r"^## ", text[language.end():], re.MULTILINE)
            at = language.end() + rest.start() if rest else len(text)
            head = text[:at].rstrip("\n")
            text = head + "\n\n" + wanted[name] + ("\n\n" if rest else "\n") + text[at:].lstrip("\n")
        done.append(f"added {name}")
    return text, done, missing


def upgrade_root(text: str, current: str) -> tuple[str, list[str], list[str]]:
    """The release's lines in a workspace's root AGENTS.md."""
    lines = text.split("\n")
    ours = current.split("\n")
    done, missing = [], []
    for key, older, anchors in ROOT_LINES:
        new = next(line for line in ours if line.startswith(key))
        index = next((i for i, line in enumerate(lines) if line.startswith((key, *older))), None)
        if index is not None:
            if lines[index] != new:
                lines[index] = new
                done.append(f"replaced the line “{key}…”")
            continue
        anchor = next((i for i, line in enumerate(lines) if anchors and line.startswith(tuple(anchors))), None)
        if anchor is None:
            missing.append(key)
            continue
        end = next((i for i in range(anchor, len(lines)) if not lines[i].strip()), len(lines))
        lines[end:end] = ["", new]
        done.append(f"added the paragraph “{key}…”")
    return "\n".join(lines), done, missing


def courses(workspace: Path) -> list[Path]:
    return sorted(
        path for path in workspace.iterdir()
        if path.is_dir() and not path.name.startswith((".", "_")) and (path / "AGENTS.md").is_file()
    )


def plan(workspace: Path, version: str) -> tuple[list[tuple], list[str]]:
    """The changes, as (kind, path, payload, note), and the steps left for a person."""
    changes: list[tuple] = []
    manual: list[str] = []

    if not same_tree(workspace / SKILL, ROOT / SKILL):
        changes.append(("tree", SKILL, ROOT / SKILL, f"replaced with {version}'s"))
    link = workspace / LINK
    target = Path("..", "..", SKILL)
    if link.is_symlink():
        if link.resolve() != (workspace / SKILL).resolve():
            changes.append(("link", LINK, target, "now links to .agents/skills/course-study-coach"))
    elif link.is_dir():
        if not same_tree(link, ROOT / SKILL):
            changes.append(("tree", LINK, ROOT / SKILL, f"the copy, replaced with {version}'s"))
    else:
        changes.append(("link", LINK, target, "added, linking to .agents/skills/course-study-coach"))
    if (workspace / OLD_SKILL).exists() or (workspace / OLD_SKILL).is_symlink():
        changes.append(("remove", OLD_SKILL, None, "removed: the skill moved to .agents/skills in v0.2.0"))
    if not same_tree(workspace / SCAFFOLD, ROOT / SCAFFOLD):
        changes.append(("tree", SCAFFOLD, ROOT / SCAFFOLD, f"replaced with {version}'s"))

    agents = workspace / "AGENTS.md"
    if agents.is_file():
        old = agents.read_text(encoding="utf-8")
        new, done, missing = upgrade_root(old, (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        if done:
            changes.append(("file", Path("AGENTS.md"), new, "; ".join(done)))
        manual += [f"AGENTS.md: add this release's line “{key}…” from Curriculer's AGENTS.md." for key in missing]

    scaffold_agents = (ROOT / SCAFFOLD / "AGENTS.md").read_text(encoding="utf-8")
    scaffold_context = (ROOT / SCAFFOLD / "CONTEXT.md").read_text(encoding="utf-8")
    for course in courses(workspace):
        name = course.name
        old = (course / "AGENTS.md").read_text(encoding="utf-8")
        new, done = upgrade_sections(old, scaffold_agents, COURSE_SECTIONS)
        if done:
            changes.append(("file", Path(name, "AGENTS.md"), new, "; ".join(done)))
        context = course / "CONTEXT.md"
        if not context.is_file():
            manual.append(f"{name}/: has no CONTEXT.md, so the entries {', '.join(CONTEXT_ENTRIES)} weren't added.")
            continue
        old = context.read_text(encoding="utf-8")
        new, done, missing = upgrade_entries(old, scaffold_context, CONTEXT_ENTRIES)
        if done:
            changes.append(("file", Path(name, "CONTEXT.md"), new, "; ".join(done)))
        if missing:
            manual.append(f"{name}/CONTEXT.md: has no Language section, so the entries {', '.join(missing)} weren't added.")

    if read_version(workspace) != version:
        changes.append(("file", VERSION, f"{version}\n", version))
    return changes, manual


def read_version(workspace: Path) -> str | None:
    path = workspace / VERSION
    return path.read_text(encoding="utf-8").strip() if path.is_file() else None


def back_up(workspace: Path, changes: list[tuple]) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    backup = workspace / BACKUPS / stamp
    backup.mkdir(parents=True)
    ignore = workspace / BACKUPS / ".gitignore"
    if not ignore.exists():
        ignore.write_text("*\n", encoding="utf-8")
    for _, path, _, _ in changes:
        source = workspace / path
        if source.is_symlink() or not source.exists():
            continue
        (backup / path).parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, backup / path, symlinks=True)
        else:
            shutil.copy2(source, backup / path)
    return backup


def remove(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def apply(workspace: Path, changes: list[tuple]) -> None:
    for kind, path, payload, _ in changes:
        target = workspace / path
        if kind == "file":
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(payload, encoding="utf-8")
        elif kind == "tree":
            remove(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(payload, target, ignore=shutil.ignore_patterns(*JUNK))
        elif kind == "link":
            remove(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                target.symlink_to(payload, target_is_directory=True)
            except OSError:
                shutil.copytree(workspace / SKILL, target)
        elif kind == "remove":
            remove(target)
            for parent in [target.parent, target.parent.parent]:
                if parent != workspace and parent.is_dir() and not any(parent.iterdir()):
                    parent.rmdir()


def commit(workspace: Path, changes: list[tuple], version: str) -> str:
    def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", str(workspace), *args], capture_output=True, text=True, check=check)

    if not (workspace / ".git").exists():
        return "Not committed: the workspace isn't a Git repository."
    paths = [path.as_posix() for _, path, _, _ in changes]
    tracked = set(git("ls-files", "-z", "--", *paths).stdout.split("\0"))
    paths = [path for path in paths if (workspace / path).exists() or (workspace / path).is_symlink() or any(t == path or t.startswith(path + "/") for t in tracked)]
    git("add", "-A", "--", *paths)
    if git("diff", "--cached", "--quiet", "--", *paths, check=False).returncode == 0:
        return "Nothing to commit."
    try:
        git("commit", "-q", "-m", f"Upgrade Curriculer to {version}", "--", *paths)
    except subprocess.CalledProcessError:
        git("reset", "-q", "--", *paths, check=False)
        raise
    return f"Committed as {git('rev-parse', '--short', 'HEAD').stdout.strip()}."


def main() -> int:
    parser = argparse.ArgumentParser(description="Upgrade a learning workspace's Curriculer files to this release.")
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--check", action="store_true", help="report what would change, and change nothing")
    parser.add_argument("--commit", action="store_true", help="commit the upgrade in the workspace's Git repository")
    args = parser.parse_args()

    workspace = args.workspace.expanduser().resolve()
    if not workspace.is_dir():
        print(f"{workspace} is not a folder.", file=sys.stderr)
        return 2
    if workspace == ROOT:
        print("That is Curriculer itself. Give the path of a learning workspace.", file=sys.stderr)
        return 2
    if not any((workspace / path).exists() for path in [SKILL, OLD_SKILL, SCAFFOLD, Path("AGENTS.md")]):
        print(f"{workspace} doesn't look like a learning workspace: it has no skill, scaffold or AGENTS.md.", file=sys.stderr)
        return 2

    version = release()
    found = read_version(workspace)
    if found and (version_key(found) or ()) > (version_key(version) or ()):
        print(f"{workspace} is at {found}, newer than this {version}. Nothing changed.")
        return 0

    changes, manual = plan(workspace, version)
    if not changes:
        print(f"{workspace} is at {version}. Nothing to do.")
    else:
        verb = "would change" if args.check else "changed"
        print(f"{workspace}: from {found or 'a version before v0.11.0'} to {version}, this {verb}:")
        for _, path, _, note in changes:
            print(f"- {path.as_posix()}: {note}")
    if manual:
        print("Left for you:")
        for line in manual:
            print(f"- {line}")
    sys.stdout.flush()
    if args.check or not changes:
        return 1 if args.check and changes else 0

    backup = back_up(workspace, changes)
    apply(workspace, changes)
    print(f"The files it changed are backed up in {backup.relative_to(workspace).as_posix()}/.")
    if args.commit:
        try:
            print(commit(workspace, changes, version))
        except subprocess.CalledProcessError as error:
            reason = (error.stderr or "").strip().splitlines() or [str(error)]
            print(f"Not committed: {reason[-1]}", file=sys.stderr, flush=True)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
