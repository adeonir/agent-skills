#!/usr/bin/env python3
"""PreToolUse gate: refuse Edit/Write when the target file was not read in full this session.

Reads the hook payload on stdin, walks the session transcript for Read calls on the
same file, and denies the edit when those reads do not cover every line of the file.

Fails open on every error it cannot attribute to a partial read: a gate that breaks
editing is worse than the habit it corrects.
"""

import json
import os
import sys

# Read tool defaults: reads start at line 1 and return at most 2000 lines when the
# call carries no offset/limit, so an omitted argument stands in for these.
DEFAULT_OFFSET = 1
DEFAULT_LIMIT = 2000

# 8192: enough of the head to spot a NUL byte in a binary or image file, which Read
# does not return as lines and this gate therefore cannot reason about.
BINARY_SNIFF_BYTES = 8192


def allow():
    sys.exit(0)


def deny(reason):
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )
    sys.exit(0)


def line_count(data):
    if not data:
        return 0
    return data.count(b"\n") + (0 if data.endswith(b"\n") else 1)


def read_ranges(transcript_path, target):
    """Every [start, end] line range the session already read for this file."""
    ranges = []
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line or '"Read"' not in line:
                    continue
                try:
                    entry = json.loads(line)
                except (json.JSONDecodeError, ValueError):
                    continue
                message = entry.get("message")
                if not isinstance(message, dict):
                    continue
                content = message.get("content")
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") != "tool_use" or block.get("name") != "Read":
                        continue
                    params = block.get("input")
                    if not isinstance(params, dict):
                        continue
                    path = params.get("file_path")
                    if not path or not same_file(path, target):
                        continue
                    offset = coerce_int(params.get("offset"), DEFAULT_OFFSET)
                    limit = coerce_int(params.get("limit"), DEFAULT_LIMIT)
                    if offset < 1:
                        offset = 1
                    if limit < 1:
                        continue
                    ranges.append((offset, offset + limit - 1))
    except OSError:
        return None
    return ranges


def coerce_int(value, fallback):
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def same_file(a, b):
    try:
        return os.path.realpath(a) == os.path.realpath(b)
    except OSError:
        return a == b


def first_gap(ranges, total):
    """Lowest line not covered by any range, or None when the file is fully covered."""
    cursor = 1
    for start, end in sorted(ranges):
        if start > cursor:
            return cursor
        if end >= cursor:
            cursor = end + 1
        if cursor > total:
            return None
    return None if cursor > total else cursor


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        allow()

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        allow()

    target = tool_input.get("file_path")
    transcript = payload.get("transcript_path")
    if not target or not transcript:
        allow()

    try:
        with open(target, "rb") as fh:
            data = fh.read()
    except OSError:
        # Missing file: this is a create, and there is nothing to have read.
        allow()

    if b"\0" in data[:BINARY_SNIFF_BYTES]:
        allow()

    total = line_count(data)
    if total == 0:
        allow()

    ranges = read_ranges(transcript, target)
    if ranges is None:
        # Transcript unreadable: cannot prove a partial read, so do not block on it.
        allow()

    gap = first_gap(ranges, total)
    if gap is None:
        allow()

    name = os.path.basename(target)
    if not ranges:
        detail = "it has not been read in this session"
    else:
        seen = ", ".join(f"{s}-{min(e, total)}" for s, e in sorted(ranges))
        detail = f"the session has only read lines {seen} of {total}; line {gap} onward is unread"

    deny(
        f"Read {name} in full before editing it — {detail}. "
        f"Editing from a window produces a patch that fits the window and contradicts "
        f"the rest of the file. Call Read on {target} with no offset/limit "
        f"(repeat with offset for files over {DEFAULT_LIMIT} lines), then edit."
    )


if __name__ == "__main__":
    main()
