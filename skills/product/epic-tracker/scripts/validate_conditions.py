#!/usr/bin/env python3
"""Parse an artifact body from stdin and enforce the condition contract (V1-V4)."""
import argparse
import re
import sys

HEADINGS = {"task": "Acceptance Criteria", "bug": "Acceptance Criteria", "spike": "Exit Criteria"}
MARKER = re.compile(r"^\s*[-*]\s+\\?\[\s*[xX]?\s*\\?\]\s*(.*)$")
SPACED_DASH = re.compile(r"\s[—–-]\s")
LINK_START = re.compile(r"N?FR(?![A-Za-z])")
LINK = re.compile(r"N?FR-\d+")


def section_lines(body, heading):
    lines = body.splitlines()
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$")
    for index, line in enumerate(lines):
        if pattern.match(line):
            rest = lines[index + 1 :]
            for offset, candidate in enumerate(rest):
                if candidate.startswith("## "):
                    return rest[:offset]
            return rest
    return []


def parse(lines):
    conditions = []
    stray = False
    for line in lines:
        match = MARKER.match(line)
        if match:
            conditions.append(match.group(1).strip())
        elif line.strip():
            if conditions:
                conditions[-1] = f"{conditions[-1]} {line.strip()}".strip()
            else:
                stray = True
    return conditions, stray


def split_link(condition):
    dashes = list(SPACED_DASH.finditer(condition))
    if dashes:
        tail = condition[dashes[-1].end() :].strip()
        if LINK_START.match(tail):
            return condition[: dashes[-1].start()].strip(), tail
    return condition, None


def normalize(text):
    return " ".join(text.lower().split())


def validate(body, artifact_type):
    conditions, stray = parse(section_lines(body, HEADINGS[artifact_type]))
    errors = []
    if not conditions:
        errors.append("Artifact fails V1: no checklist lines under the criteria heading. Add at least one `- [ ]` condition.")
    if stray:
        errors.append("Artifact fails V2: text under the heading before the first checklist line. Move it into a condition, or remove it.")

    parsed = []
    seen = {}
    for number, condition in enumerate(conditions, start=1):
        text, link = split_link(condition)
        parsed.append((number, text, link))
        if not text:
            errors.append(f"Condition {number} fails V2: empty condition. Write the condition after the marker, or remove the line.")
        else:
            key = normalize(text)
            if key in seen:
                errors.append(f"Condition {number} fails V3: duplicate of condition {seen[key]}. Remove or differentiate one of them.")
            seen.setdefault(key, number)
        if link is not None:
            if artifact_type != "task":
                errors.append(f'Condition {number} fails V4: a {artifact_type} condition carries the link "{link}". Remove the requirement link.')
            elif not LINK.fullmatch(link):
                errors.append(f'Condition {number} fails V4: link "{link}" is not exactly one id. Name exactly one requirement per condition; split the condition if it operationalizes two.')
    return parsed, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", required=True, choices=sorted(HEADINGS), help="artifact type, which selects the criteria heading and the link rule")
    args = parser.parse_args()
    parsed, errors = validate(sys.stdin.read(), args.type)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(parsed)} conditions")
    for number, _, link in parsed:
        print(f"{number}: {link or 'no link'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
