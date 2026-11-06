#!/usr/bin/env python3
"""Check a requirement assignment read from stdin for orphan, duplicate, and unknown IDs."""
import argparse
import json
import re
import sys

REQUIREMENT_ID = re.compile(r"\bN?FR-\d+\b")


def source_ids(args):
    if args.ids is not None:
        return set(args.ids.split())
    with open(args.source, encoding="utf-8") as source:
        return set(REQUIREMENT_ID.findall(source.read()))


def check(ids, assignments, omitted, allow_repeat):
    owners = {}
    for candidate, assigned in assignments.items():
        for requirement in assigned:
            owners.setdefault(requirement, []).append(candidate)

    errors = []
    for requirement in sorted(ids - owners.keys() - omitted):
        errors.append(f"ORPHAN {requirement}: no candidate carries it. Assign it, or confirm its omission with the user and list it under omitted.")
    for requirement in sorted(owners.keys() - ids):
        errors.append(f"UNKNOWN {requirement}: assigned to {', '.join(owners[requirement])}, but the source does not declare it. Remove the id.")
    if not allow_repeat:
        for requirement in sorted(owners):
            if len(owners[requirement]) > 1:
                errors.append(f"DUPLICATE {requirement}: assigned to {', '.join(owners[requirement])}. Move the boundary so one candidate owns it.")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--source", help="file to extract the FR/NFR ids from")
    source.add_argument("--ids", help="space-separated FR/NFR ids")
    parser.add_argument("--allow-repeat", action="store_true", help="accept an id on more than one candidate")
    args = parser.parse_args()

    try:
        ids = source_ids(args)
    except OSError as error:
        print(f"Cannot read the source: {error}. Pass the path of the requirements file.")
        return 2
    try:
        data = json.load(sys.stdin)
        assignments = {str(candidate): list(assigned) for candidate, assigned in data["assignments"].items()}
        omitted = set(data.get("omitted", []))
    except (json.JSONDecodeError, KeyError, AttributeError, TypeError) as error:
        print(f'Invalid input: {error}. Pass JSON on stdin: {{"assignments": {{"candidate": ["FR-1"]}}, "omitted": ["FR-2"]}}.')
        return 2

    errors = check(ids, assignments, omitted, args.allow_repeat)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"PASS: {len(ids) - len(ids & omitted)} ids assigned, {len(ids & omitted)} omitted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
