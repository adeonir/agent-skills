#!/usr/bin/env python3
"""Static linter for a skill's trigger surface (name + description).

Flags the mechanical trigger problems before the reasoning pass in
references/trigger-eval.md — no model call, no eval run. Encodes this repo's
frontmatter conventions: kebab-case name, third-person inline-trigger
description. Dependency-free (no PyYAML); parses the frontmatter directly.
"""

import re
import sys
from pathlib import Path

DESC_HARD_CAP = 1024   # chars; descriptions over this are truncated in the listing
DESC_BRIEF_WORDS = 10  # below this, a description likely underspecifies triggers
CAPABILITY_MIN_WORDS = 5  # words of "what it does" expected before the first trigger phrase
RESERVED_TOKENS = ("claude", "anthropic")  # forbidden inside a skill name
BUILTIN_COLLISIONS = ("code-review", "review", "simplify", "security-review")
FILLER_OPENERS = ("helps with", "assists with", "supports", "tool for", "utility for")
TRIGGER_PHRASES = ("use when", "use this", "use for", "use to")
FOLD_INDICATORS = (">", ">-", ">+", "|", "|-", "|+")


def parse_frontmatter(text):
    """Return (name, description) from SKILL.md frontmatter, or (None, None)."""
    if not text.startswith("---"):
        return None, None
    end = text.find("\n---", 3)
    if end == -1:
        return None, None
    lines = text[3:end].splitlines()

    name = None
    description = None
    index = 0
    while index < len(lines):
        line = lines[index]
        name_match = re.match(r"^name:\s*(.*)$", line)
        if name_match:
            name = name_match.group(1).strip().strip("\"'")
        desc_match = re.match(r"^description:\s*(.*)$", line)
        if desc_match:
            head = desc_match.group(1).strip()
            if head in FOLD_INDICATORS:
                collected = []
                index += 1
                while index < len(lines):
                    nxt = lines[index]
                    if nxt.strip() and re.match(r"^\S", nxt):  # column 0 -> next key
                        break
                    collected.append(nxt.strip())
                    index += 1
                description = " ".join(part for part in collected if part).strip()
                continue
            description = head.strip("\"'")
        index += 1
    return name, description


def lint_name(name, findings):
    if not name:
        findings.append(("BLOCKER", "name", "frontmatter has no name"))
        return
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        findings.append(("MAJOR", "name", f"name must be kebab-case (lowercase, digits, single hyphens): {name}"))
    if len(name) > 64:
        findings.append(("MAJOR", "name", f"name exceeds 64 characters ({len(name)})"))
    lowered = name.lower()
    for token in RESERVED_TOKENS:
        if token in lowered:
            findings.append(("MAJOR", "name", f"name must not contain '{token}'"))
    if name in BUILTIN_COLLISIONS:
        findings.append(("MAJOR", "name", f"name collides with a built-in command: {name}"))


def lint_description(description, findings):
    if not description:
        findings.append(("BLOCKER", "description", "frontmatter has no description"))
        return
    chars = len(description)
    words = len(description.split())
    lowered = description.lower()

    if chars > DESC_HARD_CAP:
        findings.append(("MAJOR", "description", f"description exceeds {DESC_HARD_CAP} chars ({chars}) — it will be truncated"))
    if "<" in description or ">" in description:
        findings.append(("MINOR", "description", "description contains angle brackets (< or >)"))
    if words < DESC_BRIEF_WORDS:
        findings.append(("MINOR", "description", f"description is brief ({words} words) and may underspecify triggers"))
    if lowered.startswith(("i ", "i'", "we ", "you ")):
        findings.append(("MINOR", "description", "description should be third-person, not first/second person"))
    for opener in FILLER_OPENERS:
        if lowered.startswith(opener):
            findings.append(("MINOR", "description", f"description opens with filler '{opener}' — lead with the capability"))
    if re.search(r"\(1\).*\(2\)", description):
        findings.append(("MINOR", "description", "description uses a numbered (1)…(2) trigger list — weave triggers into prose instead"))
    trigger_positions = [lowered.find(phrase) for phrase in TRIGGER_PHRASES if phrase in lowered]
    if not trigger_positions:
        findings.append(("MINOR", "description", "description states no explicit trigger ('Use when …') — readers can't tell when it fires"))
    else:
        capability = description[: min(trigger_positions)]
        if len(capability.split()) < CAPABILITY_MIN_WORDS:
            findings.append(("MINOR", "description", "description states no capability before its first trigger — lead with what the skill does"))


def main():
    if len(sys.argv) != 2:
        print("usage: trigger_lint.py <skill-dir>", file=sys.stderr)
        return 2
    skill_dir = Path(sys.argv[1])
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        print(f"SKILL.md not found in {skill_dir}", file=sys.stderr)
        return 1
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        print(f"cannot read {skill_md}: {error}", file=sys.stderr)
        return 1

    name, description = parse_frontmatter(text)
    findings = []
    lint_name(name, findings)
    lint_description(description, findings)

    if not findings:
        print(f"PASS trigger_lint — name={name}, description ok ({len(description.split())} words)")
        return 0
    print(f"FAIL trigger_lint — {len(findings)} finding(s)")
    for severity, field, message in findings:
        print(f"- {severity} {field}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
