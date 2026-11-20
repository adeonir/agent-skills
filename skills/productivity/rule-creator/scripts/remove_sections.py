#!/usr/bin/env python3
"""Remove sections from a memory file by heading.

Usage:
  python3 remove_sections.py <memory-file> <heading>...

A heading is its text (Testing conventions) or its text with the hashes
(## Testing conventions); with the hashes the level must match too. A section
runs from its heading to the line before the next heading of the same or a
higher level, so nested headings leave with their parent. A heading inside a
fenced block never counts. A heading that is already gone is reported as
absent, and a run that removes nothing leaves the file untouched.

Prints one line per heading: removed with its line range, or absent.
Exit 0 when the file was processed, 2 when it cannot be read or written or when
a heading matches more than one section (nothing is written then).
"""

import re
import sys

from resolve_memory import outside_code, read_lines

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")  # 6: deepest Markdown heading level
ARGUMENT = re.compile(r"^(#{1,6})\s+(.+?)\s*$")  # 6: deepest Markdown heading level
USAGE = "Usage: remove_sections.py <memory-file> <heading>..."


def headings(lines):
    """Return (line number, level, title) for every heading outside a fenced block."""
    found = []
    for number, line, is_code in outside_code(lines):
        match = None if is_code else HEADING.match(line)
        if match:
            found.append((number, len(match.group(1)), match.group(2)))
    return found


def section_end(found, index, total):
    """Return the last line of the section that starts at found[index]."""
    level = found[index][1]
    for number, other, _ in found[index + 1:]:
        if other <= level:
            return number - 1
    return total


def main(argv):
    if len(argv) < 2:
        print(f"expected a memory file and at least one heading. {USAGE}")
        return 2
    path = argv[0]
    lines, error = read_lines(path)
    if lines is None:
        print(f"cannot read {path}: {error}.")
        return 2

    found = headings(lines)
    drop = set()
    report = []
    for raw in argv[1:]:
        title, level = raw.strip(), None
        given = ARGUMENT.match(title)
        if given:
            level, title = len(given.group(1)), given.group(2)
        hits = [i for i, (_, other, text) in enumerate(found) if text == title and level in (None, other)]
        if len(hits) > 1:
            print(f"ambiguous: {raw!r} matches {len(hits)} sections; pass the hashes to pick one. Nothing written.")
            return 2
        if not hits:
            report.append(f"absent: {raw}")
            continue
        start = found[hits[0]][0]
        end = section_end(found, hits[0], len(lines))
        drop.update(range(start, end + 1))
        report.append(f"removed: {raw} (lines {start}-{end})")

    if drop:
        kept = [line for number, line in enumerate(lines, start=1) if number not in drop]
        while kept and not kept[-1].strip():
            kept.pop()
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("\n".join(kept) + "\n" if kept else "")
        except OSError as failure:
            print(f"cannot write {path}: {failure.strerror or 'unwritable'}.")
            return 2
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
