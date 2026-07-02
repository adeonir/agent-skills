#!/usr/bin/env python3
"""Manage the spec-driven lessons layer.

Owns .artifacts/lessons.json (canonical, machine-owned) and renders
.artifacts/LESSONS.md for humans. A lesson starts as a `candidate` and
becomes `confirmed` once it recurs across two distinct features.

Subcommands: add, list, promote, normalize, render.

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
# Zero-pad width for the L-NNN identifier (L-001..L-999 before it widens).
ID_PAD_WIDTH = 3

DEFAULT_STORE = os.path.join(".artifacts", "lessons.json")
DEFAULT_RENDER = os.path.join(".artifacts", "LESSONS.md")


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
        return {"lessons": []}
    if not isinstance(data, dict) or not isinstance(data.get("lessons"), list):
        sys.stderr.write("warning: malformed store %s; starting empty\n" % path)
        return {"lessons": []}
    return data


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


def _confirm_if_recurring(lesson):
    """Promote a lesson to confirmed once it spans the feature threshold."""
    features = lesson.get("features", [])
    if len(set(features)) >= CONFIRM_FEATURE_THRESHOLD and lesson.get("status") != "confirmed":
        lesson["status"] = "confirmed"
        lesson.setdefault("confirmed_at", _today())


def cmd_add(args):
    """Add a candidate lesson; auto-confirm if it recurs on a new feature."""
    store = load_store(args.store)
    lessons = store["lessons"]
    existing = find_by_text(lessons, args.text)
    if existing is not None:
        # Same lesson seen again: attach the feature and re-evaluate status.
        if args.feature and args.feature not in existing.get("features", []):
            existing.setdefault("features", []).append(args.feature)
        _confirm_if_recurring(existing)
        target = existing
    else:
        target = {
            "id": next_id(lessons),
            "text": args.text.strip(),
            "origin": args.origin or "",
            "status": "candidate",
            "features": [args.feature] if args.feature else [],
            "created": _today(),
            "confirmed_at": None,
        }
        _confirm_if_recurring(target)
        lessons.append(target)
    if not save_store(args.store, store):
        return 4
    render_store(store, args.render)
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
        print("%s [%s] %s (features: %s)" % (
            lesson.get("id", "?"), lesson.get("status", "?"),
            lesson.get("text", ""), features))
    return 0


def cmd_promote(args):
    """Force a lesson to confirmed, optionally attaching a feature."""
    store = load_store(args.store)
    lessons = store["lessons"]
    target = None
    for lesson in lessons:
        if lesson.get("id") == args.id:
            target = lesson
            break
    if target is None:
        sys.stderr.write("error: no lesson with id %s\n" % args.id)
        return 3
    if args.feature and args.feature not in target.get("features", []):
        target.setdefault("features", []).append(args.feature)
    target["status"] = "confirmed"
    target.setdefault("confirmed_at", _today())
    if not save_store(args.store, store):
        return 4
    render_store(store, args.render)
    print("%s confirmed" % target["id"])
    return 0


def cmd_normalize(args):
    """Dedupe by text, sort by id, backfill ids/fields, then re-render."""
    store = load_store(args.store)
    merged = {}
    order = []
    for lesson in store["lessons"]:
        key = lesson.get("text", "").strip()
        if not key:
            continue
        if key in merged:
            # Merge duplicate texts: union features, keep earliest created.
            base = merged[key]
            base["features"] = sorted(set(base.get("features", []) + lesson.get("features", [])))
            _confirm_if_recurring(base)
        else:
            lesson["features"] = sorted(set(lesson.get("features", [])))
            lesson.setdefault("status", "candidate")
            lesson.setdefault("origin", "")
            lesson.setdefault("created", _today())
            lesson.setdefault("confirmed_at", None)
            _confirm_if_recurring(lesson)
            merged[key] = lesson
            order.append(key)
    normalized = [merged[key] for key in order]
    # Backfill ids for any lesson missing one, keeping existing ids stable.
    for lesson in normalized:
        if not lesson.get("id"):
            lesson["id"] = next_id(normalized)
    normalized.sort(key=lambda l: l.get("id", ""))
    store["lessons"] = normalized
    if not save_store(args.store, store):
        return 4
    render_store(store, args.render)
    print("normalized %d lessons" % len(normalized))
    return 0


def cmd_render(args):
    """Render lessons.json to LESSONS.md."""
    store = load_store(args.store)
    if render_store(store, args.render):
        print("rendered %s" % args.render)
        return 0
    return 4


def render_store(store, path):
    """Write LESSONS.md grouped by status. Returns True/False."""
    confirmed = [l for l in store["lessons"] if l.get("status") == "confirmed"]
    candidates = [l for l in store["lessons"] if l.get("status") != "confirmed"]
    lines = ["# Lessons", "",
             "Rendered from `lessons.json` — do not hand-edit.", ""]

    def section(title, rows):
        lines.append("## %s" % title)
        lines.append("")
        if not rows:
            lines.append("(none)")
            lines.append("")
            return
        for lesson in rows:
            features = ", ".join(lesson.get("features", [])) or "-"
            lines.append("- **%s** — %s" % (lesson.get("id", "?"), lesson.get("text", "")))
            lines.append("  - origin: %s" % (lesson.get("origin") or "-"))
            lines.append("  - features: %s" % features)
        lines.append("")

    section("Confirmed", confirmed)
    section("Candidates", candidates)
    directory = os.path.dirname(path) or "."
    try:
        os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))
    except OSError as error:
        sys.stderr.write("error: could not render %s: %s\n" % (path, error))
        return False
    return True


def build_parser():
    parser = argparse.ArgumentParser(description="Manage the spec-driven lessons layer.")
    parser.add_argument("--store", default=DEFAULT_STORE, help="path to lessons.json")
    parser.add_argument("--render", default=DEFAULT_RENDER, help="path to LESSONS.md")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a candidate lesson")
    add.add_argument("--text", required=True)
    add.add_argument("--origin", default="")
    add.add_argument("--feature", default="")
    add.set_defaults(func=cmd_add)

    listing = sub.add_parser("list", help="list lessons")
    listing.add_argument("--status", choices=["candidate", "confirmed"], default="")
    listing.set_defaults(func=cmd_list)

    promote = sub.add_parser("promote", help="force a lesson to confirmed")
    promote.add_argument("--id", required=True)
    promote.add_argument("--feature", default="")
    promote.set_defaults(func=cmd_promote)

    normalize = sub.add_parser("normalize", help="dedupe, sort, backfill, re-render")
    normalize.set_defaults(func=cmd_normalize)

    render = sub.add_parser("render", help="render LESSONS.md from lessons.json")
    render.set_defaults(func=cmd_render)
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
