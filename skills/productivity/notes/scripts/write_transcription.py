#!/usr/bin/env python3
"""Write a transcription note with its body read straight from the source file.

Usage:
  python3 write_transcription.py --source <file> --meta <json-file> --note <note-path> [--append] [--vault <dir>]

<note-path> is relative to the vault root. The vault is --vault, the only
vault in Obsidian's obsidian.json, or the open one.

The meta file is JSON:
  {"frontmatter": {"created": "...", "updated": "...", "status": "active",
                   "date": "...", "context": "...", "tags": ["..."]},
   "title": "...", "observations": ["#category text"],
   "relations": ["[[Note]]"], "source_link": "https://..." or null}

Without --append, creates the note and refuses to overwrite one that
exists. With --append, inserts the source body at the end of the existing
note's body, before its Observations; the meta file is then ignored. After
writing, the note is checked as `check_note.py transcription --source`
does. Exit 0 when the note is written and clean, 1 when the check flags a
line, 2 when an input is missing or the write is refused.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_note import BODY_END, check, default_vault  # noqa: E402

FRONTMATTER_ORDER = ["created", "updated", "status", "date", "context", "tags"]


def scalar(value):
    text = str(value)
    # "1:1" quoted: YAML 1.1 readers parse digits joined by colons as a base-60 number.
    plain = (text and text[0] not in "[]{}&*!|>'\"%@`#-?:," and ": " not in text and " #" not in text
             and not re.fullmatch(r"[\d:]*:[\d:]*", text))
    return text if plain else json.dumps(text)


def frontmatter(fields):
    lines = ["---"]
    for key in FRONTMATTER_ORDER + [k for k in fields if k not in FRONTMATTER_ORDER]:
        if key not in fields:
            continue
        value = fields[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines += [f"  - {scalar(item)}" for item in value]
        else:
            lines.append(f"{key}: {scalar(value)}")
    lines.append("---")
    return lines


def compose(meta, body):
    lines = frontmatter(meta["frontmatter"]) + [f"# {meta['title']}", "", body.strip("\n"), ""]
    if meta.get("observations"):
        lines += ["## Observations", ""] + [f"- {item}" for item in meta["observations"]] + [""]
    if meta.get("relations"):
        lines += ["## Relations", ""] + [f"- {item}" for item in meta["relations"]] + [""]
    if meta.get("source_link"):
        lines += [f"Source: {meta['source_link']}", ""]
    return "\n".join(lines)


def append(existing, body):
    lines = existing.splitlines()
    end = next((i for i, line in enumerate(lines) if BODY_END.match(line)), len(lines))
    head = end
    while head > 0 and not lines[head - 1].strip():
        head -= 1
    return "\n".join(lines[:head] + ["", body.strip("\n"), ""] + lines[end:]) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Write a transcription note from its source file.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--meta")
    parser.add_argument("--note", required=True)
    parser.add_argument("--append", action="store_true")
    parser.add_argument("--vault")
    args = parser.parse_args()
    if not args.append and not args.meta:
        parser.error("--meta is required unless --append")

    vault = default_vault(args.vault)
    if vault is None:
        print("cannot pick the vault from obsidian.json. Pass the vault directory with --vault.")
        return 2
    path = os.path.join(vault, args.note)
    try:
        with open(args.source, encoding="utf-8") as handle:
            body = handle.read()
        meta = None
        if args.meta:
            with open(args.meta, encoding="utf-8") as handle:
                meta = json.load(handle)
    except (OSError, ValueError) as error:
        print(f"cannot read an input: {error}. Fix the file and run again.")
        return 2
    if not body.strip():
        print(f"{args.source} is empty. Write the transcription to it first.")
        return 2

    if args.append:
        if not os.path.isfile(path):
            print(f"{args.note} does not exist. Run without --append to create it.")
            return 2
        with open(path, encoding="utf-8") as handle:
            content = append(handle.read(), body)
    else:
        if os.path.exists(path):
            print(f"{args.note} already exists. Choose another name, or pass --append.")
            return 2
        try:
            content = compose(meta, body)
        except (KeyError, TypeError) as error:
            print(f"meta file is missing {error}. Add it and run again.")
            return 2

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)

    findings = sorted(check("transcription", args.note, content.splitlines(), body))
    if not findings:
        print(f"clean: {args.note}")
        return 0
    for number, message in findings:
        print(f"{args.note}:{number}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
