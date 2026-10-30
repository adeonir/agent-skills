#!/usr/bin/env python3
"""Validate, dedup, and sort review findings against the annotated diff.

Usage:
  python3 merge_findings.py <annotated_diff_path> < findings.md

stdin holds findings grouped under `## Findings`, `## Guidelines Compliance`,
and `## Spec Compliance`. Each item starts with
`- **[severity] [file:line]** title` (a spec gap may omit `[file:line]`) and
carries a `- confidence: N` sub-line.

An item is dropped when its severity is unknown, its confidence is missing or
below the report gate, or its `file:line` has no `[L<n>]` marker in the
annotated diff. Surviving items are deduplicated per section on `file:line`
plus a similar title (the highest severity wins), sorted by severity, and
printed without the confidence line. After the sections, prints
`COUNTS:` and one `DROPPED:` line per rejected item.

Exit 0 on success, 1 when the diff file cannot be read or stdin holds no item.
"""

import difflib
import re
import sys

SECTIONS = {
    "Findings": "findings",
    "Guidelines Compliance": "guideline_violations",
    "Spec Compliance": "spec_gaps",
}
SEVERITY_RANK = {"critical": 0, "warning": 1, "suggestion": 2, "nit": 3}
CONFIDENCE_GATE = 80  # 80: report gate from the confidence rubric; below it a finding is speculation
TITLE_SIMILARITY = 0.8  # 0.8: ratio above which two titles on one line read as the same finding

ITEM = re.compile(r"^- \*\*\[(\w+)\](?: \[([^\]]+):(\d+)\])?\*\* (.+)$")
CONFIDENCE = re.compile(r"^\s*-\s*confidence:\s*(\d+)\s*$", re.IGNORECASE)
FILE_HEADER = re.compile(r"^\+\+\+ (?:b/)?(.+)$")
MARKER = re.compile(r"^\+\[L(\d+)\] ")
HEADING = re.compile(r"^## (.+?)\s*$")


def load_markers(path):
    """Map each file to the set of line numbers that carry an [L<n>] marker."""
    markers, current = {}, None
    with open(path, encoding="utf-8") as handle:
        for text in handle:
            header = FILE_HEADER.match(text.rstrip("\n"))
            if header:
                current = header.group(1)
                markers.setdefault(current, set())
                continue
            marker = MARKER.match(text)
            if marker and current is not None:
                markers[current].add(int(marker.group(1)))
    return markers


def parse_items(lines):
    """Split stdin into (section, item) pairs; an item is a header match plus its body."""
    items, section, current = [], None, None
    for raw in lines:
        text = raw.rstrip("\n")
        heading = HEADING.match(text)
        if heading:
            section = SECTIONS.get(heading.group(1))
            current = None
            continue
        match = ITEM.match(text)
        if match:
            current = {
                "section": section,
                "severity": match.group(1).lower(),
                "file": match.group(2),
                "line": int(match.group(3)) if match.group(3) else None,
                "title": match.group(4),
                "confidence": None,
                "body": [],
            }
            items.append(current)
            continue
        if current is not None:
            confidence = CONFIDENCE.match(text)
            if confidence:
                current["confidence"] = int(confidence.group(1))
            else:
                current["body"].append(text)
    return items


def reject_reason(item, markers):
    if item["section"] is None:
        return "outside a known section"
    if item["severity"] not in SEVERITY_RANK:
        return f"unknown severity '{item['severity']}'"
    if item["confidence"] is None:
        return "missing confidence"
    if item["confidence"] < CONFIDENCE_GATE:
        return f"confidence {item['confidence']} below {CONFIDENCE_GATE}"
    if item["file"] is None:
        if item["section"] != "spec_gaps":
            return "missing file:line"
        return None
    if item["line"] not in markers.get(item["file"], set()):
        return "line has no [L<n>] marker"
    return None


def same_finding(a, b):
    if (a["file"], a["line"]) != (b["file"], b["line"]):
        return False
    ratio = difflib.SequenceMatcher(None, a["title"].lower(), b["title"].lower()).ratio()
    return ratio >= TITLE_SIMILARITY


def dedup(items):
    kept = []
    for item in items:
        twin = next((k for k in kept if same_finding(k, item)), None)
        if twin is None:
            kept.append(item)
        elif SEVERITY_RANK[item["severity"]] < SEVERITY_RANK[twin["severity"]]:
            kept[kept.index(twin)] = item
    return kept


def render(item):
    where = f" [{item['file']}:{item['line']}]" if item["file"] else ""
    lines = [f"- **[{item['severity']}]{where}** {item['title']}"]
    lines.extend(item["body"])
    return "\n".join(lines).rstrip()


def main():
    if len(sys.argv) != 2:
        print("Usage: merge_findings.py <annotated_diff_path> < findings.md", file=sys.stderr)
        return 1
    try:
        markers = load_markers(sys.argv[1])
    except (OSError, UnicodeDecodeError) as error:
        print(f"Could not read the annotated diff: {error}", file=sys.stderr)
        return 1
    try:
        items = parse_items(sys.stdin.readlines())
    except (OSError, UnicodeDecodeError) as error:
        print(f"Could not read the findings from stdin: {error}", file=sys.stderr)
        return 1
    if not items:
        print("No finding item on stdin.", file=sys.stderr)
        return 1

    dropped, valid = [], []
    for item in items:
        reason = reject_reason(item, markers)
        if reason:
            where = f"{item['file']}:{item['line']}" if item["file"] else "no line"
            dropped.append(f"DROPPED: [{item['severity']}] {where} {item['title']} ({reason})")
        else:
            valid.append(item)

    counts = {}
    for heading, key in SECTIONS.items():
        merged = dedup([i for i in valid if i["section"] == key])
        merged.sort(key=lambda i: SEVERITY_RANK[i["severity"]])  # stable: ties keep arrival order
        counts[key] = len(merged)
        print(f"## {heading}\n")
        print("\n".join(render(i) for i in merged) if merged else "(none)")
        print()
    print(
        f"COUNTS: findings={counts['findings']} "
        f"guideline_violations={counts['guideline_violations']} "
        f"spec_gaps={counts['spec_gaps']}"
    )
    print("\n".join(dropped))
    return 0


if __name__ == "__main__":
    sys.exit(main())
