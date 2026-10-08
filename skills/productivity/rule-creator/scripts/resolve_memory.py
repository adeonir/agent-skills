#!/usr/bin/env python3
"""Resolve the @path imports of a memory file and map its sections to the file that holds them.

Usage:
  python3 resolve_memory.py <memory-file>

Follows each @path import the way Claude Code loads it: relative to the file
that contains it, absolute, or under ~; a backslash before a space keeps the
space in the path; an @path inside a code span or a fenced block is literal
text and never loads; imports stop after four hops. Prints every loaded file
with its hop and line count, the resolved line count, each H2 and H3 with the
file and line that hold it, and the notes: a missing import, an import cycle,
and an import past the hop limit.

Exit 0 when the file was resolved, 2 when it cannot be read.
"""

import os
import re
import sys

MAX_HOPS = 4  # 4: import depth Claude Code follows, per its memory documentation
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")  # 3: shortest code fence CommonMark accepts
CODE_SPAN = re.compile(r"(`+).*?\1")
IMPORT = re.compile(r"(?:^|(?<=\s))@((?:\\ |[^\s\\])+)")
HEADING = re.compile(r"^(##|###)\s+(.+?)\s*#*\s*$")


def read_lines(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().splitlines(), None
    except UnicodeDecodeError:
        return None, "not UTF-8 text"
    except OSError as error:
        return None, error.strerror or "unreadable"


def outside_code(lines):
    """Yield (number, line, is_code) with fenced blocks marked as code."""
    fence = None
    for number, line in enumerate(lines, start=1):
        opening = FENCE.match(line)
        if opening:
            marker = opening.group(1)
            if fence is None:
                fence = marker
                yield number, line, True
                continue
            if marker[0] == fence[0] and len(marker) >= len(fence) and line.strip() == marker:
                fence = None
                yield number, line, True
                continue
        yield number, line, fence is not None


def target_of(raw, base):
    path = raw.replace("\\ ", " ")
    path = os.path.expanduser(path)
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(base), path)
    return os.path.normpath(path)


def resolve(path, hop, chain, loaded, sections, notes, display):
    lines, error = read_lines(path)
    if lines is None:
        notes.append(f"{display(path)}: {error}")
        return 0
    loaded.append((hop, path, len(lines)))
    total = len(lines)
    for number, line, is_code in outside_code(lines):
        if is_code:
            continue
        heading = HEADING.match(line)
        if heading:
            sections.append((heading.group(1), heading.group(2), path, number))
        for match in IMPORT.finditer(CODE_SPAN.sub("", line)):
            target = target_of(match.group(1), path)
            where = f"{display(path)}:{number}"
            if not os.path.isfile(target):
                notes.append(f"{where}: @{match.group(1)} does not resolve to a file, so nothing loads")
            elif target in chain:
                notes.append(f"{where}: @{match.group(1)} closes an import cycle and is not loaded again")
            elif hop + 1 > MAX_HOPS:
                notes.append(f"{where}: @{match.group(1)} is past the {MAX_HOPS}-hop limit and does not load")
            else:
                total += resolve(target, hop + 1, chain + [target], loaded, sections, notes, display)
    return total


def main(argv):
    if len(argv) != 1:
        print("expected one memory file. Usage: resolve_memory.py <memory-file>")
        return 2
    root = os.path.normpath(os.path.abspath(os.path.expanduser(argv[0])))
    if not os.path.isfile(root):
        print(f"cannot read {argv[0]}: no such file.")
        return 2
    base = os.path.dirname(root)

    def display(path):
        relative = os.path.relpath(path, base)
        return path if relative.startswith("..") else relative

    loaded, sections, notes = [], [], []
    total = resolve(root, 0, [root], loaded, sections, notes, display)

    print("LOADED FILES")
    for hop, path, count in loaded:
        print(f"  hop {hop}  {display(path)}  {count} lines")
    print(f"RESOLVED LINES: {total}")
    holders = sorted({path for _, _, path, _ in sections})
    if holders:
        print("CONTENT HELD IN: " + ", ".join(display(path) for path in holders))
    print()
    print("SECTIONS")
    if not sections:
        print("  none")
    for level, title, path, number in sections:
        indent = "  " if level == "##" else "    "
        print(f"{indent}{level} {title}  ({display(path)}:{number})")
    if notes:
        print()
        print("NOTES")
        for note in notes:
            print(f"  - {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
