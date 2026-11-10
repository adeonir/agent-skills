#!/usr/bin/env python3
"""Record the repository's pull request merge rule in its instruction file."""

import subprocess
import sys
from pathlib import Path
import re

RULES = {
    "squash": "Pull requests merge as a single squashed commit.",
    "merge": "Pull requests merge with a merge commit, preserving branch commits.",
    "rebase": "Pull requests merge by rebasing branch commits onto the base.",
}
HEADING = "Merge method"


def git(*args, allowed=(0,)):
    result = subprocess.run(args, text=True, capture_output=True)
    if result.returncode not in allowed:
        raise ValueError(result.stderr.strip() or "Shell command failed: " + " ".join(args))
    return result.stdout


def instruction_path(root):
    candidates = [root / "CLAUDE.md", root / ".claude" / "CLAUDE.md"]
    target = next((p for p in candidates if p.is_file()), root / "AGENTS.md")
    if target.name == "CLAUDE.md":
        imported = re.search(r"(?m)^[ \t]*@((?:\./|\.\./)?AGENTS\.md)[ \t]*$", target.read_text())
        if imported:
            target = target.parent / imported.group(1)
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise ValueError("Instruction file resolves outside the repository.") from error
    return target


def rule_sections(text):
    """Locate real level-two rule headings, excluding fenced code examples."""
    headings = []
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        # CommonMark fences allow up to three leading spaces and at least three markers.
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
                fence = None
        elif marker:
            fence = marker.group(1)
        else:
            heading = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$", line.rstrip("\r\n"))
            if heading:
                title = re.sub(r"[ \t]+#+$", "", (heading.group(2) or "")).strip()
                headings.append((offset, len(heading.group(1)), title))
        offset += len(line)
    if fence:
        raise ValueError("Unclosed Markdown fence; repair it before maintaining the rule section.")
    result = []
    for index, (start, level, title) in enumerate(headings):
        if level == 2 and title == HEADING:
            end = next((pos for pos, depth, _ in headings[index + 1:] if depth <= level), len(text))
            result.append((start, end))
    return result


def replace_section(text, block):
    if "\r\n" in text:
        block = block.replace("\n", "\r\n")
    separator = "\r\n" if "\r\n" in text else "\n"
    matches = rule_sections(text)
    if len(matches) > 1:
        raise ValueError("Duplicate " + HEADING + " sections; resolve them before applying the rule.")
    if matches:
        start, end = matches[0]
        body = text[start:end].splitlines()[1:]
        if len([line for line in body if line.strip()]) > 1:
            raise ValueError("The " + HEADING + " section contains extra or ambiguous content; preserve it and resolve manually.")
        return text[:start] + block + (separator if text[end:] else "") + text[end:]
    return text.rstrip("\r\n") + (separator * 2 if text else "") + block


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in RULES:
        raise ValueError("Usage: merge-method.py squash | merge | rebase")
    root = Path(git("git", "-C", str(Path.cwd()), "rev-parse", "--show-toplevel").strip()).resolve()
    target = instruction_path(root)
    text = target.read_bytes().decode("utf-8") if target.exists() else ""
    updated = replace_section(text, "## " + HEADING + "\n\n" + RULES[sys.argv[1]] + "\n")
    if updated != text:
        target.write_bytes(updated.encode("utf-8"))
    print(str(target))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print("git-helpers: " + str(error), file=sys.stderr)
        sys.exit(1)
