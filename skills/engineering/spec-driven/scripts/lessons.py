#!/usr/bin/env python3
"""Manage the spec-driven lessons layer.

Owns .artifacts/LESSONS.json, the canonical machine-owned store. A lesson
enters as a `candidate` grounded in a validation.md signal, becomes
`confirmed` once it recurs across two distinct features, and is
`quarantined` once it was loaded as guidance and the same failure recurred
anyway. Only `confirmed` lessons load into specify and design.

Subcommands: add, list, promote, penalize, normalize.

Exit codes:
  0  success
  2  argument/usage error (argparse default)
  3  target not found (e.g. promote --id on a missing lesson)
  4  data/store error that could not be recovered
"""

import argparse
import datetime
import json
import os
import sys

# A lesson is confirmed once it is seen on this many distinct features.
CONFIRM_FEATURE_THRESHOLD = 2
# A confirmed lesson is quarantined once it fails this many times as guidance.
QUARANTINE_PENALTY_THRESHOLD = 2
# Zero-pad width for the L-NNN identifier (L-001..L-999 before it widens).
ID_PAD_WIDTH = 3

# The validation.md sections that ground a lesson. A lesson with no signal is
# an opinion, so `add` refuses one outside this set.
SIGNALS = ["goal_unmet", "ac_fail", "surviving_mutant", "spec_defect", "suite_red"]
STATUSES = ["candidate", "confirmed", "quarantined"]

DEFAULT_STORE = os.path.join(".artifacts", "LESSONS.json")


def _today():
    """Return today's date as YYYY-MM-DD (UTC-naive local date)."""
    return datetime.date.today().isoformat()


def load_store(path):
    """Load the lesson store, returning a dict with a `lessons` list.

    Missing or corrupt files degrade to an empty store rather than raising,
    so callers always receive a usable structure.
    """
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {"lessons": []}
    except (OSError, json.JSONDecodeError):
        # Corrupt or unreadable store: start clean rather than crash.
        sys.stderr.write("warning: could not read %s; starting empty\n" % path)
        _backup_corrupt(path)
        return {"lessons": []}
    if not isinstance(data, dict) or not isinstance(data.get("lessons"), list):
        sys.stderr.write("warning: malformed store %s; starting empty\n" % path)
        _backup_corrupt(path)
        return {"lessons": []}
    return data


def _backup_corrupt(path):
    """Preserve an unreadable store as .bak so a later save never destroys it."""
    try:
        os.replace(path, path + ".bak")
        sys.stderr.write("warning: preserved unreadable store as %s.bak\n" % path)
    except OSError:
        pass  # backup is best-effort; never block the caller


def save_store(path, data):
    """Write the store atomically-ish (temp then replace). Returns True/False."""
    directory = os.path.dirname(path) or "."
    try:
        os.makedirs(directory, exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
        return True
    except OSError as error:
        sys.stderr.write("error: could not write %s: %s\n" % (path, error))
        return False


def next_id(lessons):
    """Return the next monotonic L-NNN id, one past the current maximum."""
    highest = 0
    for lesson in lessons:
        raw = str(lesson.get("id", "")).replace("L-", "")
        try:
            highest = max(highest, int(raw))
        except ValueError:
            # Non-numeric id: ignore for the purpose of computing the next one.
            continue
    return "L-%0*d" % (ID_PAD_WIDTH, highest + 1)


def find_by_text(lessons, text):
    """Return the first lesson whose text matches exactly, or None."""
    normalized = text.strip()
    for lesson in lessons:
        if lesson.get("text", "").strip() == normalized:
            return lesson
    return None


def find_by_id(lessons, lesson_id):
    """Return the lesson with this id, or None."""
    for lesson in lessons:
        if lesson.get("id") == lesson_id:
            return lesson
    return None


def _id_sort_key(lesson):
    """Sort on the numeric part of L-NNN, so L-1000 follows L-999 rather than L-100."""
    raw = str(lesson.get("id", "")).replace("L-", "")
    try:
        return (0, int(raw))
    except ValueError:
        # Non-numeric ids sort last; they never collide with the generated ones.
        return (1, 0)


def _confirm_if_recurring(lesson):
    """Promote a lesson to confirmed once it spans the feature threshold.

    A quarantined lesson already failed as guidance, so recurrence never
    revives it — that would reinstate the exact lesson the penalty retired.
    """
    if lesson.get("status") in ("confirmed", "quarantined"):
        return
    features = lesson.get("features", [])
    if len(set(features)) >= CONFIRM_FEATURE_THRESHOLD:
        lesson["status"] = "confirmed"
        lesson.setdefault("confirmed_at", _today())


def cmd_add(args):
    """Add a candidate lesson; auto-confirm if it recurs on a new feature."""
    # `required=True` accepts an empty string, which would slip an ungrounded
    # lesson past the gate; reject it here so the gate actually holds.
    for flag in ("text", "origin", "feature"):
        if not getattr(args, flag).strip():
            sys.stderr.write("error: --%s must not be empty\n" % flag)
            return 2
    store = load_store(args.store)
    lessons = store["lessons"]
    existing = find_by_text(lessons, args.text)
    if existing is not None:
        # Same lesson seen again: attach the feature and re-evaluate status.
        if args.feature not in existing.get("features", []):
            existing.setdefault("features", []).append(args.feature)
        _confirm_if_recurring(existing)
        target = existing
    else:
        target = {
            "id": next_id(lessons),
            "text": args.text.strip(),
            "signal": args.signal,
            "origin": args.origin.strip(),
            "status": "candidate",
            "features": [args.feature],
            "penalties": 0,
            "created": _today(),
            "confirmed_at": None,
        }
        _confirm_if_recurring(target)
        lessons.append(target)
    if not save_store(args.store, store):
        return 4
    print("%s %s: %s" % (target["id"], target["status"], target["text"]))
    return 0


def cmd_list(args):
    """List lessons, optionally filtered by status."""
    store = load_store(args.store)
    rows = [l for l in store["lessons"] if not args.status or l.get("status") == args.status]
    if not rows:
        print("(no lessons)")
        return 0
    for lesson in rows:
        features = ", ".join(lesson.get("features", [])) or "-"
        print("%s [%s] %s (signal: %s; features: %s)" % (
            lesson.get("id", "?"), lesson.get("status", "?"),
            lesson.get("text", ""), lesson.get("signal", "-"), features))
    return 0


def cmd_promote(args):
    """Force a lesson to confirmed, optionally attaching a feature."""
    store = load_store(args.store)
    target = find_by_id(store["lessons"], args.id)
    if target is None:
        sys.stderr.write("error: no lesson with id %s\n" % args.id)
        return 3
    if args.feature and args.feature not in target.get("features", []):
        target.setdefault("features", []).append(args.feature)
    target["status"] = "confirmed"
    target.setdefault("confirmed_at", _today())
    if not save_store(args.store, store):
        return 4
    print("%s confirmed" % target["id"])
    return 0


def cmd_penalize(args):
    """Record that a lesson failed as guidance; quarantine it at the threshold."""
    store = load_store(args.store)
    target = find_by_id(store["lessons"], args.id)
    if target is None:
        sys.stderr.write("error: no lesson with id %s\n" % args.id)
        return 3
    target["penalties"] = int(target.get("penalties", 0)) + 1
    if target["penalties"] >= QUARANTINE_PENALTY_THRESHOLD:
        target["status"] = "quarantined"
    if not save_store(args.store, store):
        return 4
    print("%s %s (penalties: %d)" % (target["id"], target["status"], target["penalties"]))
    return 0


def cmd_normalize(args):
    """Dedupe by text, sort by id, backfill ids and fields."""
    store = load_store(args.store)
    merged = {}
    order = []
    for lesson in store["lessons"]:
        key = lesson.get("text", "").strip()
        if not key:
            continue
        if key in merged:
            # Merge duplicate texts: union features, keep the earliest created date,
            # and carry the strongest status forward. `promote` can confirm on a single
            # feature, which the recurrence rule alone would silently demote back;
            # a quarantine outranks both, since reviving it undoes the penalty.
            base = merged[key]
            # Identifiers are never renumbered, so a merge keeps the lower id
            # rather than whichever duplicate happened to come first in the store.
            if lesson.get("id") and _id_sort_key(lesson) < _id_sort_key(base):
                base["id"] = lesson["id"]
            base["features"] = sorted(set(base.get("features", []) + lesson.get("features", [])))
            base["penalties"] = max(int(base.get("penalties", 0)), int(lesson.get("penalties", 0)))
            dates = [d for d in (base.get("created"), lesson.get("created")) if d]
            base["created"] = min(dates) if dates else _today()
            if not base.get("origin"):
                base["origin"] = lesson.get("origin", "")
            if not base.get("signal"):
                base["signal"] = lesson.get("signal", "")
            if lesson.get("status") == "confirmed":
                base["status"] = "confirmed"
                stamps = [s for s in (base.get("confirmed_at"), lesson.get("confirmed_at")) if s]
                base["confirmed_at"] = min(stamps) if stamps else _today()
            if "quarantined" in (base.get("status"), lesson.get("status")):
                base["status"] = "quarantined"
            _confirm_if_recurring(base)
        else:
            lesson["features"] = sorted(set(lesson.get("features", [])))
            lesson.setdefault("status", "candidate")
            lesson.setdefault("signal", "")
            lesson.setdefault("origin", "")
            lesson.setdefault("penalties", 0)
            lesson.setdefault("created", _today())
            lesson.setdefault("confirmed_at", None)
            if lesson["penalties"] >= QUARANTINE_PENALTY_THRESHOLD:
                lesson["status"] = "quarantined"
            _confirm_if_recurring(lesson)
            merged[key] = lesson
            order.append(key)
    normalized = [merged[key] for key in order]
    # Backfill ids for any lesson missing one, keeping existing ids stable.
    for lesson in normalized:
        if not lesson.get("id"):
            lesson["id"] = next_id(normalized)
    normalized.sort(key=_id_sort_key)
    store["lessons"] = normalized
    if not save_store(args.store, store):
        return 4
    print("normalized %d lessons" % len(normalized))
    return 0


def build_parser():
    # The store flag lives on both the top parser and every subcommand, so it works on
    # either side of the subcommand. SUPPRESS on the child keeps an absent flag from
    # clobbering a value the top parser already resolved.
    paths = argparse.ArgumentParser(add_help=False)
    paths.add_argument("--store", default=argparse.SUPPRESS, help="path to LESSONS.json")

    parser = argparse.ArgumentParser(description="Manage the spec-driven lessons layer.")
    parser.add_argument("--store", default=DEFAULT_STORE, help="path to LESSONS.json")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", parents=[paths], help="add a candidate lesson")
    add.add_argument("--text", required=True)
    # signal, origin and feature are all required: the first two ground the lesson in a
    # validation.md row, and without the third recurrence cannot be counted, so the
    # lesson would sit as a candidate forever and never load.
    add.add_argument("--signal", required=True, choices=SIGNALS)
    add.add_argument("--origin", required=True)
    add.add_argument("--feature", required=True)
    add.set_defaults(func=cmd_add)

    listing = sub.add_parser("list", parents=[paths], help="list lessons")
    listing.add_argument("--status", choices=STATUSES, default="")
    listing.set_defaults(func=cmd_list)

    promote = sub.add_parser("promote", parents=[paths], help="force a lesson to confirmed")
    promote.add_argument("--id", required=True)
    promote.add_argument("--feature", default="")
    promote.set_defaults(func=cmd_promote)

    penalize = sub.add_parser("penalize", parents=[paths], help="record that a lesson failed as guidance")
    penalize.add_argument("--id", required=True)
    penalize.set_defaults(func=cmd_penalize)

    normalize = sub.add_parser("normalize", parents=[paths], help="dedupe, sort, backfill")
    normalize.set_defaults(func=cmd_normalize)
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as error:  # last-resort guard: never surface a raw traceback
        sys.stderr.write("error: %s\n" % error)
        return 4


if __name__ == "__main__":
    sys.exit(main())
