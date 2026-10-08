#!/usr/bin/env python3
"""Validate a grill-me decision ledger and read the frontier or the close from it.

Usage:
  python3 ledger.py frontier <ledger.json>
  python3 ledger.py close <ledger.json>

frontier prints every open decision whose depends_on entries are all settled,
split into fact and preference. close prints every settled decision with its
answer, the terms, and the decisions whose three adr flags are all true; it
flags a settled decision whose adr is not three booleans. Both validate the
ledger first: the JSON, the fields, duplicate ids, unknown dependencies, and
dependency cycles.

Exit 0 when the ledger is valid, 1 when it has a problem, 2 when it cannot be read.
"""

import json
import sys

FIELDS = ["id", "question", "depends_on", "kind", "status", "answer", "adr", "term"]
KINDS = {"fact", "preference"}
STATUSES = {"open", "settled"}


def load(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle), None
    except OSError as error:
        return None, f"cannot read {path}: {error.strerror}."
    except json.JSONDecodeError as error:
        return [], f"invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}. Fix the file."


def validate(entries):
    problems = []
    if not isinstance(entries, list):
        return ["the ledger must be a JSON list of decision entries."]
    ids = {}
    for index, entry in enumerate(entries):
        label = entry.get("id", f"entry {index + 1}") if isinstance(entry, dict) else f"entry {index + 1}"
        if not isinstance(entry, dict):
            problems.append(f"{label}: not a JSON object.")
            continue
        missing = [field for field in FIELDS if field not in entry]
        if missing:
            problems.append(f"{label}: missing {', '.join(missing)}.")
        if entry.get("kind") not in KINDS:
            problems.append(f"{label}: kind must be fact or preference, not {entry.get('kind')!r}.")
        if entry.get("status") not in STATUSES:
            problems.append(f"{label}: status must be open or settled, not {entry.get('status')!r}.")
        if entry.get("status") == "settled" and entry.get("answer") in (None, ""):
            problems.append(f"{label}: settled without an answer.")
        if not isinstance(entry.get("depends_on", []), list):
            problems.append(f"{label}: depends_on must be a list of ids.")
        if label in ids:
            problems.append(f"{label}: duplicate id.")
        ids[label] = entry
    for label, entry in ids.items():
        for dep in entry.get("depends_on") or []:
            if dep not in ids:
                problems.append(f"{label}: depends_on {dep!r}, which is not an id in the ledger.")
    problems += cycles(ids)
    return problems


def cycles(ids):
    state = {}
    found = []

    def visit(node, path):
        state[node] = "visiting"
        for dep in ids[node].get("depends_on") or []:
            if dep not in ids:
                continue
            if state.get(dep) == "visiting":
                found.append(f"dependency cycle: {' -> '.join(path + [node, dep])}. Break one depends_on.")
            elif dep not in state:
                visit(dep, path + [node])
        state[node] = "done"

    for node in ids:
        if node not in state:
            visit(node, [])
    return found[:1]


def frontier(entries):
    by_id = {entry["id"]: entry for entry in entries}
    ready = [e for e in entries if e["status"] == "open"
             and all(by_id[d]["status"] == "settled" for d in e["depends_on"])]
    open_count = sum(1 for e in entries if e["status"] == "open")
    for kind in ("fact", "preference"):
        print(f"{kind}:")
        for entry in (e for e in ready if e["kind"] == kind):
            print(f"  {entry['id']}: {entry['question']}")
    print(f"open: {open_count}")
    return 0


def close(entries):
    problems = []
    settled = [e for e in entries if e["status"] == "settled"]
    for entry in settled:
        adr = entry["adr"]
        if not (isinstance(adr, list) and len(adr) == 3 and all(isinstance(flag, bool) for flag in adr)):
            problems.append(f"{entry['id']}: adr is {adr!r}; record three booleans: hard to reverse, surprising without context, real trade-off.")
    still_open = [e["id"] for e in entries if e["status"] == "open"]
    if still_open:
        problems.append(f"open decisions remain: {', '.join(still_open)}. Return to Step 1.")
    if problems:
        for message in problems:
            print(message)
        return 1
    print("settled:")
    for entry in settled:
        print(f"  {entry['id']}: {entry['question']} -> {entry['answer']}")
    print("terms:")
    for entry in (e for e in settled if e["term"]):
        print(f"  {entry['term']}")
    print("adr:")
    for entry in (e for e in settled if all(e["adr"])):
        print(f"  {entry['id']}: {entry['question']}")
    return 0


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("frontier", "close"):
        print("usage: ledger.py frontier|close <ledger.json>")
        return 2
    entries, error = load(sys.argv[2])
    if entries is None:
        print(error)
        return 2
    problems = [error] if error else validate(entries)
    if problems:
        for message in problems:
            print(message)
        return 1
    return frontier(entries) if sys.argv[1] == "frontier" else close(entries)


if __name__ == "__main__":
    sys.exit(main())
