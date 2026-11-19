#!/usr/bin/env python3
"""Check a storytelling document against the mechanical rules of its template.

Usage: python3 check_storytelling.py <path-to-storytelling.md>

Prints one line per finding, ERROR or WARN, then a summary line.
Exit code: 0 when no ERROR was found, 1 when at least one ERROR was found,
2 when the document cannot be read.
"""

import re
import sys
from pathlib import Path

REQUIRED_HEADINGS = [
    "## Concept",
    "## Arc",
    "## Experience",
    "## Current Experience",
    "## Recommendations",
    "## Open Questions",
    "## References",
]

ARC_HEADER = ["Moment", "Visitor should feel or understand", "Pace", "Leads to next"]
PACE_VALUES = {"peak", "breather"}

METADATA_LIST = [
    re.compile(r"^- Created: \d{4}-\d{2}-\d{2}$"),
    re.compile(r"^- Updated: \d{4}-\d{2}-\d{2}$"),
]

# A square-bracket slot left from the template; a markdown link [text](url) is not a slot.
SLOT = re.compile(r"\[[^\]\n]+\](?!\()")

FORBIDDEN = [
    (re.compile(r"\b\d+(\.\d+)?\s?(px|vh|vw|rem|em|ms|fps)\b", re.I), "a measurement or timing value"),
    # 1-3 digits: a duration such as 2s or 1.5s; four digits would catch a decade such as 1990s.
    (re.compile(r"\b\d{1,3}(\.\d+)?s\b"), "a duration in seconds"),
    (re.compile(r"(?<![\w#])#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?(?:[0-9a-fA-F]{2})?\b"), "a color value"),
    (re.compile(r"\b(rgb|rgba|hsl|hsla)\(", re.I), "a color value"),
    (re.compile(r"\b(easing|ease-in|ease-out|cubic-bezier|frame rate)\b", re.I), "an easing or frame-rate specification"),
    (
        re.compile(r"\b(as discussed|as agreed|we agreed|we decided|the user (accepted|agreed|asked|said|wants))\b", re.I),
        "a trace of the conversation",
    ),
]


def find_document(arg):
    path = Path(arg)
    if path.is_file():
        return path
    if not path.is_absolute():
        # Walk up to the project root so a project-relative path resolves from a subdirectory.
        for parent in [Path.cwd(), *Path.cwd().parents]:
            candidate = parent / path
            if candidate.is_file():
                return candidate
            if (parent / ".git").exists():
                break
    return None


def split_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section_lines(lines, heading):
    start = None
    for i, line in enumerate(lines):
        if line.strip() == heading:
            start = i + 1
        elif start is not None and line.startswith("## "):
            return lines[start:i], start
    return (lines[start:], start) if start is not None else ([], None)


def check(text):
    errors, warns = [], []
    lines = text.splitlines()

    if not lines or lines[0].strip() != "# Storytelling":
        errors.append("line 1: the document must open with '# Storytelling'")

    created = [i for i, line in enumerate(lines) if line.startswith("- Created:")]
    if not created:
        errors.append("no '- Created:' item under the title")
    else:
        block = [line.strip() for line in lines[created[0]:created[0] + len(METADATA_LIST)]]
        if len(block) < len(METADATA_LIST) or not all(p.match(line) for p, line in zip(METADATA_LIST, block)):
            errors.append(
                f"line {created[0] + 1}: the metadata list must read "
                "'- Created: YYYY-MM-DD', '- Updated: YYYY-MM-DD', one item per line"
            )

    positions = []
    for heading in REQUIRED_HEADINGS:
        found = [i for i, line in enumerate(lines) if line.strip() == heading]
        if not found:
            errors.append(f"missing section '{heading}'")
        else:
            positions.append(found[0])
    if positions != sorted(positions):
        errors.append("the sections are out of the template order")

    for i, line in enumerate(lines, 1):
        if "<!--" in line:
            errors.append(f"line {i}: a template comment is left in the document")
        for match in SLOT.finditer(line):
            errors.append(f"line {i}: a template slot is left unfilled: {match.group(0)}")
        for pattern, label in FORBIDDEN:
            match = pattern.search(line)
            if match:
                errors.append(f"line {i}: {label} is out of scope: '{match.group(0)}'")

    arc, arc_start = section_lines(lines, "## Arc")
    if arc_start is not None:
        check_arc(arc, arc_start, errors, warns)

    for heading in ("## Current Experience", "## Recommendations", "## Open Questions"):
        body, _ = section_lines(lines, heading)
        if not any(line.strip() for line in body):
            errors.append(f"section '{heading}' is empty; write None when it does not apply")

    return errors, warns


def check_arc(arc, offset, errors, warns):
    pages, tables, current = [], [], None
    page_of_table = []
    i = 0
    while i < len(arc):
        line = arc[i].strip()
        number = offset + i + 1
        if line.startswith("### "):
            current = {"name": line[4:], "entry": False, "line": number}
            pages.append(current)
        elif line.startswith("Entry:"):
            if current is None:
                errors.append(f"line {number}: an Entry line sits outside a page heading")
            else:
                current["entry"] = True
        elif line.startswith("|"):
            table = []
            while i < len(arc) and arc[i].strip().startswith("|"):
                table.append((offset + i + 1, arc[i]))
                i += 1
            tables.append(table)
            page_of_table.append(current)
            continue
        i += 1

    if not tables:
        errors.append("the Arc carries no table of moments")
        return
    if len(tables) == 1 and pages:
        errors.append("a single-page arc carries no page heading and no Entry line")
    if len(tables) > 1 and any(page is None for page in page_of_table):
        errors.append("an arc that spans pages puts every table under its page heading")
    if len(tables) > 1 and pages:
        if pages[0]["entry"]:
            errors.append(f"line {pages[0]['line']}: the first page opens the arc and carries no Entry line")
        for page in pages[1:]:
            if not page["entry"]:
                errors.append(f"line {page['line']}: page '{page['name']}' comes after the first and needs an Entry line")

    for table in tables:
        check_table(table, errors, warns)


def check_table(table, errors, warns):
    # Pace alternates within a page only; a page boundary resets the comparison.
    header_line, header = table[0]
    if split_row(header) != ARC_HEADER:
        errors.append(f"line {header_line}: the Arc columns must be {' | '.join(ARC_HEADER)}")
        return
    moments = []
    for number, row in table[2:]:
        cells = split_row(row)
        if len(cells) != len(ARC_HEADER) or not all(cells):
            errors.append(f"line {number}: every moment fills all four columns")
            continue
        pace = cells[2].lower()
        if pace not in PACE_VALUES:
            errors.append(f"line {number}: Pace is '{cells[2]}'; use peak or breather")
        moments.append((number, cells[0], pace))

    for (_, prev_name, prev_pace), (number, name, pace) in zip(moments, moments[1:]):
        if pace == prev_pace and pace in PACE_VALUES:
            warns.append(
                f"line {number}: '{prev_name}' and '{name}' are neighbors with the same pace ({pace}); "
                "make the intent of the second say why, or alternate"
            )


def main():
    if len(sys.argv) != 2:
        print("usage: check_storytelling.py <path-to-storytelling.md>")
        return 2
    path = find_document(sys.argv[1])
    if path is None:
        print(f"ERROR: document not found: {sys.argv[1]}. Pass the path of the written storytelling document.")
        return 2
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: cannot read {path}: {exc}")
        return 2

    errors, warns = check(text)
    for message in errors:
        print(f"ERROR {message}")
    for message in warns:
        print(f"WARN {message}")
    print(f"{path}: {len(errors)} error(s), {len(warns)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
