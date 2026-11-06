#!/usr/bin/env python3
"""Remove topic blocks from a handoff file and leave the rest unchanged.

Usage: python3 drop_blocks.py <path> <topic> [<topic> ...]

A topic is the text of a `## <topic>` heading. Each named block is removed from
its heading to the next heading; every other byte of the file stays as it was.
When no block remains, the file is emptied. Exit 0 when the blocks were removed,
1 when a topic names no block (nothing is written), 2 when the file cannot be
read or written.
"""

import re
import sys

HEADING = re.compile(r"^## +(.+?)\s*$")


def split_blocks(text):
    preamble = []
    blocks = []
    for line in text.splitlines(keepends=True):
        match = HEADING.match(line.rstrip("\r\n"))
        if match:
            blocks.append((match.group(1), [line]))
        elif blocks:
            blocks[-1][1].append(line)
        else:
            preamble.append(line)
    return preamble, blocks


def main():
    if len(sys.argv) < 3:
        print("usage: drop_blocks.py <path> <topic> [<topic> ...]")
        return 2
    path, topics = sys.argv[1], sys.argv[2:]
    try:
        with open(path, encoding="utf-8", newline="") as handle:
            text = handle.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"cannot read {path}: {getattr(error, 'strerror', None) or error}. Leave the handoff as it is and report it.")
        return 2

    preamble, blocks = split_blocks(text)
    known = [topic for topic, _ in blocks]
    missing = [topic for topic in topics if topic not in known]
    if missing:
        listed = ", ".join(f"`{topic}`" for topic in missing)
        present = ", ".join(f"`{topic}`" for topic in known) or "none"
        print(f"no block named {listed}; blocks in the file: {present}. Pass each heading exactly as written. Nothing was written.")
        return 1

    kept = [(topic, lines) for topic, lines in blocks if topic not in topics]
    result = "".join(preamble) + "".join("".join(lines) for _, lines in kept) if kept else ""
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(result)
    except OSError as error:
        print(f"cannot write {path}: {error.strerror}. Leave the handoff as it is and report it.")
        return 2

    dropped = ", ".join(f"`{topic}`" for topic in topics)
    if kept:
        left = ", ".join(f"`{topic}`" for topic, _ in kept)
        print(f"removed {dropped}; left in the file: {left}")
    else:
        print(f"removed {dropped}; no block left, file emptied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
