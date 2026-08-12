#!/usr/bin/env python3
"""Manage the machine-owned signal history for one active feature.

Signals live in .artifacts/specs/{slug}/SIGNALS.md. An open signal is unique by
Code + Reference. Resolving a signal closes that occurrence; a later add then
records a new occurrence instead of hiding a recurrence.
"""

import argparse
import os
import re
import sys


CODES = [
    "agreed-behavior",
    "test-case",
    "test-suite",
    "planned-task",
    "source-code",
    "spec-defect",
    "open-question",
]
PHASES = ["implement", "validate", "audit"]
STATUSES = ["open", "resolved"]
HEADER = "# Signals: {slug}"
TABLE_HEADER = "| Code | Phase | Reference | Report | Status |"
TABLE_SEPARATOR = "|------|-------|-----------|--------|--------|"
ROW_PATTERN = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(open|resolved)\s*\|$")


def signal_path(spec_dir):
    return os.path.join(spec_dir, "SIGNALS.md")


def read_rows(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except FileNotFoundError:
        return []
    except (OSError, UnicodeDecodeError) as error:
        raise ValueError("could not read %s: %s" % (path, error)) from error

    rows = []
    for line_number, line in enumerate(lines, 1):
        match = ROW_PATTERN.match(line)
        if not match:
            continue
        code, phase, reference, report, status = (value.strip() for value in match.groups())
        rows.append({
            "code": code,
            "phase": phase,
            "reference": reference,
            "report": report,
            "status": status,
            "line": line_number,
        })
    return rows


def render(slug, rows):
    lines = [HEADER.format(slug=slug), "", TABLE_HEADER, TABLE_SEPARATOR]
    for row in rows:
        lines.append(
            "| %s | %s | %s | %s | %s |"
            % (row["code"], row["phase"], row["reference"], row["report"], row["status"])
        )
    return "\n".join(lines) + "\n"


def write_rows(path, slug, rows):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    temporary_path = path + ".tmp"
    with open(temporary_path, "w", encoding="utf-8") as handle:
        handle.write(render(slug, rows))
    os.replace(temporary_path, path)


def validate_signal(code, phase, reference, report):
    if code not in CODES:
        raise ValueError("--code must be one of %s" % ", ".join(CODES))
    if phase not in PHASES:
        raise ValueError("--phase must be one of %s" % ", ".join(PHASES))
    if not reference.strip():
        raise ValueError("--reference must not be empty")
    if not report.strip():
        raise ValueError("--report must not be empty")


def cmd_add(args):
    validate_signal(args.code, args.phase, args.reference, args.report)
    path = signal_path(args.spec_dir)
    rows = read_rows(path)
    for row in rows:
        if row["status"] == "open" and row["code"] == args.code and row["reference"] == args.reference:
            print("DUPLICATE %s %s" % (args.code, args.reference))
            return 0

    rows.append({
        "code": args.code,
        "phase": args.phase,
        "reference": args.reference,
        "report": args.report,
        "status": "open",
    })
    write_rows(path, os.path.basename(os.path.normpath(args.spec_dir)), rows)
    print("ADDED %s %s" % (args.code, args.reference))
    return 0


def cmd_resolve(args):
    if args.code not in CODES:
        raise ValueError("--code must be one of %s" % ", ".join(CODES))
    if not args.reference.strip():
        raise ValueError("--reference must not be empty")
    path = signal_path(args.spec_dir)
    rows = read_rows(path)
    for row in reversed(rows):
        if row["status"] == "open" and row["code"] == args.code and row["reference"] == args.reference:
            row["status"] = "resolved"
            write_rows(path, os.path.basename(os.path.normpath(args.spec_dir)), rows)
            print("RESOLVED %s %s" % (args.code, args.reference))
            return 0
    print("NOT FOUND %s %s" % (args.code, args.reference))
    return 0


def cmd_list(args):
    path = signal_path(args.spec_dir)
    rows = read_rows(path)
    for row in rows:
        if not args.status or row["status"] == args.status:
            print(
                "%s | %s | %s | %s | %s"
                % (row["code"], row["phase"], row["reference"], row["report"], row["status"])
            )
    return 0


def cmd_normalize(args):
    path = signal_path(args.spec_dir)
    rows = read_rows(path)
    normalized = []
    open_keys = set()
    for row in rows:
        key = (row["code"], row["reference"])
        if row["status"] == "open" and key in open_keys:
            continue
        if row["status"] == "open":
            open_keys.add(key)
        normalized.append({key: value for key, value in row.items() if key != "line"})
    write_rows(path, os.path.basename(os.path.normpath(args.spec_dir)), normalized)
    print("NORMALIZED %d signals" % len(normalized))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Manage feature-local signals.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    add = subcommands.add_parser("add")
    add.add_argument("--spec-dir", required=True)
    add.add_argument("--code", required=True)
    add.add_argument("--phase", required=True)
    add.add_argument("--reference", required=True)
    add.add_argument("--report", required=True)
    add.set_defaults(func=cmd_add)

    resolve = subcommands.add_parser("resolve")
    resolve.add_argument("--spec-dir", required=True)
    resolve.add_argument("--code", required=True)
    resolve.add_argument("--reference", required=True)
    resolve.set_defaults(func=cmd_resolve)

    listing = subcommands.add_parser("list")
    listing.add_argument("--spec-dir", required=True)
    listing.add_argument("--status", choices=STATUSES, default="")
    listing.set_defaults(func=cmd_list)

    normalize = subcommands.add_parser("normalize")
    normalize.add_argument("--spec-dir", required=True)
    normalize.set_defaults(func=cmd_normalize)
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
        return args.func(args)
    except (OSError, ValueError) as error:
        sys.stderr.write("error: %s\n" % error)
        return 2


if __name__ == "__main__":
    sys.exit(main())
