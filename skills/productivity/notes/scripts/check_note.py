#!/usr/bin/env python3
"""Check a written note against its type's template.

Usage:
  python3 check_note.py <type> <note-path> [--source <file>] [--vault <dir>]
  python3 check_note.py brag <note-path> --entry <text> --category <name>

<type> is project, brag, challenge, company, or transcription. <note-path>
is the note's path relative to the vault root. The vault is --vault, or the
vault in Obsidian's obsidian.json that holds <note-path>.

Flags a missing frontmatter key, a missing required heading, a template
slot left unfilled, chat phrasing, and a brag H1 that does not match the
filename. With --source, the transcription body must contain the source
file exactly. With --entry and --category, a brag entry must appear once,
inside that category's section. Exit 0 when clean, 1 when a line is flagged, 2 when the note or
the vault cannot be found.
"""

import argparse
import json
import os
import re
import sys

COMMON_KEYS = ["created", "updated", "status", "tags"]

TYPES = {
    "project": {"keys": ["stack"], "headings": ["## Goals"]},
    "brag": {"keys": [], "headings": []},
    "challenge": {"keys": ["company", "stack"], "headings": ["## Approach", "## Solution", "## Learnings"]},
    "company": {"keys": ["company", "role", "stack"], "headings": ["## Timeline"]},
    "transcription": {"keys": ["date", "context"], "headings": []},
}

OBSIDIAN_CONFIGS = [
    "~/Library/Application Support/obsidian/obsidian.json",
    "~/.config/obsidian/obsidian.json",
    "~/.var/app/md.obsidian.Obsidian/config/obsidian/obsidian.json",
    os.path.join(os.environ.get("APPDATA", ""), "obsidian", "obsidian.json"),
]

# A [slot] that is neither a [[wikilink]], a markdown link, nor a "- [ ]" checkbox.
SLOT = re.compile(r"(?<!\[)\[(?!\[)(?! \]|x\])[^\[\]\n]+\](?!\]|\()")
CHAT_PHRASES = re.compile(r"(?i)\b(?:as discussed|the user confirmed|we agreed|you chose)\b")
FRONTMATTER_KEY = re.compile(r"^([A-Za-z_][\w-]*):")
BODY_END = re.compile(r"^## (?:Observations|Relations)\b")


def known_vaults():
    for config in OBSIDIAN_CONFIGS:
        try:
            with open(os.path.expanduser(config), encoding="utf-8") as handle:
                vaults = list(json.load(handle).get("vaults", {}).values())
        except (OSError, ValueError, AttributeError):
            continue
        if vaults:
            return vaults
    return []


def find_vault(note_path, vault):
    if vault:
        return vault if os.path.isfile(os.path.join(vault, note_path)) else None
    matches = [v["path"] for v in known_vaults() if os.path.isfile(os.path.join(v.get("path", ""), note_path))]
    return matches[0] if matches else None


def default_vault(vault):
    """The vault a new note goes to: --vault, the only vault, or the open one."""
    if vault:
        return vault if os.path.isdir(vault) else None
    vaults = known_vaults()
    if len(vaults) == 1:
        return vaults[0].get("path")
    open_vaults = [v.get("path") for v in vaults if v.get("open")]
    return open_vaults[0] if len(open_vaults) == 1 else None


def split(lines):
    if not lines or lines[0].strip() != "---":
        return [], lines, 0
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], lines[index + 1:], index + 1
    return lines[1:], [], len(lines)


def body_of(body):
    start = next((i + 1 for i, line in enumerate(body) if line.startswith("# ")), 0)
    end = next((i for i in range(start, len(body)) if BODY_END.match(body[i])), len(body))
    return "\n".join(body[start:end]).strip("\n")


def check_entry(body, offset, entry, category):
    first = entry.strip().splitlines()[0].strip() if entry.strip() else ""
    hits = [i for i, line in enumerate(body) if line.strip() == first]
    if len(hits) != 1:
        return [(0, f"entry `{first}` appears {len(hits)} times; it must appear once.")]
    section = next((body[i][3:].strip() for i in range(hits[0], -1, -1) if body[i].startswith("## ")), None)
    if section != category:
        return [(offset + hits[0] + 1, f"entry sits under `{section}`, not `{category}`. Move it into `## {category}`.")]
    return []


def check(note_type, note_path, lines, source, entry=None, category=None):
    findings = []
    front, body, offset = split(lines)
    keys = {m.group(1) for m in map(FRONTMATTER_KEY.match, front) if m}
    for key in COMMON_KEYS + TYPES[note_type]["keys"]:
        if key not in keys:
            findings.append((1, f"frontmatter has no `{key}`. Add it from the template."))

    h1 = next((line[2:].strip() for line in body if line.startswith("# ")), None)
    if h1 is None:
        findings.append((offset + 1, "no H1 heading. Add the template's H1."))
    elif note_type == "project" and not h1.endswith(" Overview"):
        findings.append((offset + 1, f"H1 `{h1}` does not end in ` Overview`."))
    elif note_type == "brag":
        stem = os.path.splitext(os.path.basename(note_path))[0]
        if h1 != stem:
            findings.append((offset + 1, f"H1 `{h1}` does not match the filename `{stem}`."))
    for heading in TYPES[note_type]["headings"]:
        if heading not in (line.strip() for line in body):
            findings.append((offset + 1, f"missing `{heading}`. Add it from the template."))

    skip = set()
    if note_type == "transcription":
        start = next((i for i, line in enumerate(body) if line.startswith("# ")), -1) + 1
        end = next((i for i in range(start, len(body)) if BODY_END.match(body[i])), len(body))
        skip = set(range(start, end))
    for index, line in enumerate(front + [""] + body):
        number = index + 1
        body_index = index - len(front) - 1
        if body_index in skip:
            continue
        for match in SLOT.finditer(line):
            findings.append((number, f"unfilled slot `{match.group(0)}`. Fill it or remove the line."))
        for match in CHAT_PHRASES.finditer(line):
            findings.append((number, f"chat phrasing \"{match.group(0)}\". State the fact about the work instead."))

    if source is not None:
        expected = source.strip("\n")
        actual = body_of(body)
        if expected not in actual:
            want, got = expected.splitlines(), actual.splitlines()
            line = next((i for i, (a, b) in enumerate(zip(want, got)) if a != b), min(len(want), len(got)))
            findings.append((0, f"body differs from the source at body line {line + 1} "
                                f"(source has {len(want)} lines, note has {len(got)}). Rewrite the body from the source."))
    if entry is not None:
        findings += check_entry(body, offset, entry, category)
    return findings


def main():
    parser = argparse.ArgumentParser(description="Check a written note against its template.")
    parser.add_argument("type", choices=sorted(TYPES))
    parser.add_argument("note_path")
    parser.add_argument("--source")
    parser.add_argument("--vault")
    parser.add_argument("--entry")
    parser.add_argument("--category", choices=["Impact", "Technical", "Growth"])
    args = parser.parse_args()
    if (args.entry is None) != (args.category is None):
        parser.error("--entry and --category go together")

    vault = find_vault(args.note_path, args.vault)
    if vault is None:
        print(f"cannot find {args.note_path} in any Obsidian vault. Pass the vault directory with --vault.")
        return 2
    path = os.path.join(vault, args.note_path)
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
        source = None
        if args.source:
            with open(args.source, encoding="utf-8", errors="replace") as handle:
                source = handle.read()
    except OSError as error:
        print(f"cannot read {error.filename}: {error.strerror}.")
        return 2

    findings = sorted(check(args.type, args.note_path, lines, source, args.entry, args.category))
    if not findings:
        print(f"clean: {args.note_path}")
        return 0
    for number, message in findings:
        print(f"{args.note_path}:{number}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
