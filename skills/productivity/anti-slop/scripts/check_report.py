#!/usr/bin/env python3
"""Check a detect report against the catalog and the draft it reports on.

Usage:
  python3 check_report.py --catalog <slop-catalog.md> --draft <file> --report <file>

Every finding line in the report has the shape
  - **<catalog name>** — "<quoted line from the draft>" — <fix>
The name must match a bold entry name in the catalog verbatim, and the quote
must appear verbatim in the draft. An ellipsis (... or …) inside a quote marks
an elision: each part must appear in the draft, in order.

Exit 0 when clean, 1 when a finding is flagged, 2 when a file cannot be read.
"""

import argparse
import re
import sys

# Catalog entries open a line with a bold name ending in a period or a colon.
CATALOG_NAME = re.compile(r"^\*\*([^*]+?)[.:]\*\*", re.M)
FINDING = re.compile(r"^\s*[-*]\s+\*\*([^*]+?)\*\*(.*)$")
QUOTE = re.compile(r"[\"“]([^\"”]+)[\"”]")
ELLIPSIS = re.compile(r"\s*(?:\.\.\.|…)\s*")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def squash(text):
    return re.sub(r"\s+", " ", text).strip()


def quoted_in_draft(quote, draft):
    position = 0
    for part in (p for p in ELLIPSIS.split(squash(quote)) if p):
        found = draft.find(part, position)
        if found < 0:
            return False
        position = found + len(part)
    return True


def check(catalog, draft, report):
    names = {name.strip() for name in CATALOG_NAME.findall(catalog)}
    flat_draft = squash(draft)
    findings = []
    for number, line in enumerate(report.splitlines(), start=1):
        match = FINDING.match(line)
        if not match:
            continue
        name, rest = match.group(1).strip(), match.group(2)
        if name not in names:
            findings.append(f"line {number}: `{name}` is not a catalog entry name. Use the catalog name verbatim.")
        quote = QUOTE.search(rest)
        if not quote:
            findings.append(f"line {number}: no quoted line from the draft. Quote the shortest useful excerpt.")
        elif not quoted_in_draft(quote.group(1), flat_draft):
            findings.append(f"line {number}: the quote \"{quote.group(1)}\" is not in the draft. Quote it verbatim.")
    return findings


def main():
    parser = argparse.ArgumentParser(description="Check a detect report against the catalog and the draft.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--draft", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    try:
        catalog, draft, report = read(args.catalog), read(args.draft), read(args.report)
    except OSError as error:
        print(f"cannot read {error.filename}: {error.strerror}.")
        return 2
    findings = check(catalog, draft, report)
    if not findings:
        print(f"clean: {args.report}")
        return 0
    for message in findings:
        print(f"{args.report}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
