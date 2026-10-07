#!/usr/bin/env python3
"""Check a written handoff file against the save format.

Usage: python3 check_handoff.py <path>

Flags a missing required section, a section filled with "none", chat
phrasing, and lines that look like they carry a secret. Exit 0 when the
file is clean, 1 when a line is flagged, 2 when the file cannot be read.
Flagged secret values are masked in the output, never printed.
"""

import re
import sys

REQUIRED_SECTIONS = ["Focus", "Context", "Current state"]

SECTION = re.compile(r"^\*\*([A-Za-z ]+):\*\*\s*(.*)$")
NONE_VALUE = re.compile(r"^(?:-\s*)?(?:none|n/a|nothing)\.?$", re.IGNORECASE)

CHAT_PHRASES = re.compile(r"(?i)\b(?:as discussed|the user confirmed|we agreed|you chose)\b")

SECRET_PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    # sk- / pk- / rk- prefixes cover OpenAI, Anthropic, and Stripe style keys.
    ("API key", re.compile(r"\b(?:sk|pk|rk)[-_](?:live|test|ant|proj)?[-_]?[A-Za-z0-9_-]{6,}\b")),
    ("JWT", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    ("bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}")),
    ("credentials in URL", re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@")),
    # 8 characters: shorter values are almost always placeholders or examples.
    ("secret assignment", re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd|pwd)\b\s*[:=]\s*['\"]?[^\s'\"{}]{8,}")),
]

REDACTED = "{redacted}"


def mask(text):
    # Keep 4 characters so the user can locate the value without seeing it.
    return text[:4] + "…" if len(text) > 4 else "…"


def check_sections(lines):
    findings = []
    sections = {}
    current = None
    for number, line in enumerate(lines, start=1):
        match = SECTION.match(line)
        if match:
            current = match.group(1)
            sections[current] = {"line": number, "body": [match.group(2)] if match.group(2) else []}
        elif current and line.strip():
            sections[current]["body"].append(line.strip())

    for name in REQUIRED_SECTIONS:
        if name not in sections:
            findings.append((0, f"missing required section `{name}`. Add it from the template."))
    for name, section in sections.items():
        body = section["body"]
        if not body:
            findings.append((section["line"], f"section `{name}` is empty. Fill it, or remove an optional section."))
        elif all(NONE_VALUE.match(entry) for entry in body):
            findings.append((section["line"], f"section `{name}` says none. Remove the section; an absent section is the empty answer."))
    return findings


def check_lines(lines):
    findings = []
    for number, line in enumerate(lines, start=1):
        for match in CHAT_PHRASES.finditer(line):
            findings.append((number, f"chat phrasing \"{match.group(0)}\". State the fact about the work instead."))
        for kind, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                if REDACTED in match.group(0):
                    continue
                findings.append((number, f"{kind} ({mask(match.group(0))}). Replace the value with {REDACTED}."))
    return findings


def main():
    if len(sys.argv) != 2:
        print("usage: check_handoff.py <path>")
        return 2
    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            lines = handle.read().splitlines()
    except OSError as error:
        print(f"cannot read {path}: {error.strerror}. Write the handoff first, then check it.")
        return 2

    findings = sorted(check_sections(lines) + check_lines(lines))
    if not findings:
        print(f"clean: {path}")
        return 0
    for number, message in findings:
        print(f"{path}:{number}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
