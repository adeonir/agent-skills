#!/usr/bin/env python3
"""Annotate every added line of a unified diff with its post-image line number.

Usage:
  git diff <range> | python3 annotate_diff.py

Reads a unified diff on stdin and prints it with each added line rewritten
from `+code` to `+[L<n>] code`, where <n> is the line number in the new file.
Context lines advance the counter; removed lines and "\\ No newline" markers
do not. File headers (`+++`, `---`) pass through unchanged.

After the diff, prints `CHANGED_FILES:` followed by one post-image path per
line (deleted files are listed by their old path).

Exit 0 on success, 1 when stdin holds no diff hunk.
"""

import re
import sys

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def annotate(lines):
    out, files = [], []
    line = None
    old_path = None
    for raw in lines:
        text = raw.rstrip("\n")
        if text.startswith("--- "):
            old_path = text[4:].removeprefix("a/")
            line = None
            out.append(text)
            continue
        if text.startswith("+++ "):
            new_path = text[4:].removeprefix("b/")
            files.append(old_path if new_path == "/dev/null" else new_path)
            line = None
            out.append(text)
            continue
        match = HUNK.match(text)
        if match:
            line = int(match.group(1))
            out.append(text)
            continue
        if line is None:
            out.append(text)
            continue
        if text.startswith("+"):
            out.append(f"+[L{line}] {text[1:]}")
            line += 1
        elif text.startswith(" ") or text == "":
            out.append(text)
            line += 1
        else:
            out.append(text)
    return out, files


def main():
    try:
        lines = sys.stdin.readlines()
    except (OSError, UnicodeDecodeError) as error:
        print(f"Could not read the diff from stdin: {error}", file=sys.stderr)
        return 1
    if not any(HUNK.match(raw) for raw in lines):
        print("No diff hunk on stdin. Pipe `git diff <range>` into this script.", file=sys.stderr)
        return 1
    out, files = annotate(lines)
    print("\n".join(out))
    print("\nCHANGED_FILES:")
    print("\n".join(files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
