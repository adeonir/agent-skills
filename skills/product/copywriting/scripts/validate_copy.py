#!/usr/bin/env python3
"""Deterministic floor for the copy.yaml self-check.

Every mutating operation (write, extract, refresh, revoice, reconcile) ends by
checking the same two things by eye: is the content tree well-formed, and is it
free of design decisions? This scans for both so the check is reproducible
instead of re-derived each run.

It is advisory, not a gate: a product legitimately named "Grid" or a CTA that
mentions "Blue" is a false positive the human judges — same contract as
slop_scan.py. Content-only is the invariant; this just surfaces candidates.

Usage:
    python3 validate_copy.py docs/design/copy.yaml
    python3 validate_copy.py < copy.yaml
"""

import re
import sys

# copy.yaml carries content only — these patterns are design decisions that do
# not belong in it. Each is (label, compiled-regex), matched case-insensitive.
LEAKAGE = [
    ("hex color",
     re.compile(r"#[0-9a-f]{3}(?:[0-9a-f]{3}(?:[0-9a-f]{2})?)?\b", re.I)),
    ("color function",
     re.compile(r"\b(?:rgba?|hsla?|oklch|oklab|lab|lch)\s*\(", re.I)),
    ("css length unit",
     re.compile(r"\b\d+(?:\.\d+)?(?:px|rem|em|vh|vw|vmin|vmax|pt)\b", re.I)),
    # Tailwind color-scale utility, e.g. bg-blue-500, text-slate-900, ring-red-200.
    ("tailwind color class",
     re.compile(
         r"\b(?:bg|text|border|ring|from|via|to|fill|stroke|divide)-"
         r"(?:slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|"
         r"green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|"
         r"pink|rose)-\d{2,3}\b", re.I)),
    # Tailwind spacing/sizing utility, e.g. p-4, mt-2, gap-6, space-x-3.
    ("tailwind spacing class",
     re.compile(r"\b(?:p|m|px|py|pt|pb|pl|pr|mx|my|mt|mb|ml|mr|gap|"
                r"space-[xy]|w|h)-\d+(?:\.5)?\b")),
    # Decorative tailwind utilities with an explicit value.
    ("tailwind decoration class",
     re.compile(r"\b(?:rounded|shadow)-(?:sm|md|lg|xl|2xl|3xl|full|inner|none)\b"
                r"|\bgrid-cols-\d+\b|\bflex-(?:row|col|wrap|nowrap)\b")),
    # Literal CSS property declarations.
    ("css property",
     re.compile(r"\b(?:font-family|font-size|font-weight|line-height|z-index|"
                r"display|position)\s*:", re.I)),
    # Icon picks — iconify-style namespace:name, or an icon key. The skill's
    # design-leakage definition names icons; copy.yaml carries content, not them.
    ("icon reference",
     re.compile(r"\b(?:lucide|heroicons|mdi|tabler|ph|bi|fa[brs]?|"
                r"material-symbols|carbon|ri|feather|octicon):[a-z0-9-]+"
                r"|^\s*icon(?:_name)?\s*:", re.I)),
]

# Top-level keys the extract template establishes. Missing ones are flagged only
# when a YAML parser is available, since the check needs real structure.
REQUIRED_TOP_KEYS = ("metadata", "project", "content")


def read_input(argv):
    """Return (text, source-label), falling back to stdin. Never raises."""
    if len(argv) > 1:
        path = argv[1]
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read(), path
        except (OSError, UnicodeDecodeError) as err:
            print(f"validate_copy: cannot read {path}: {err}", file=sys.stderr)
            return "", path
    try:
        return sys.stdin.read(), "<stdin>"
    except (OSError, UnicodeDecodeError):
        return "", "<stdin>"


def scan_leakage(text):
    """Return [(lineno, label, snippet)] for every design-token candidate."""
    hits = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
        for label, pattern in LEAKAGE:
            if pattern.search(raw):
                hits.append((lineno, label, raw.strip()))
    return hits


def check_structure(text):
    """Return (ran, problems). Degrades gracefully when no YAML parser exists."""
    try:
        import yaml  # PyYAML is common but not guaranteed; absence is not fatal.
    except ImportError:
        return False, []
    try:
        tree = yaml.safe_load(text)
    except yaml.YAMLError as err:
        return True, [f"YAML does not parse: {err}"]
    if not isinstance(tree, dict):
        return True, ["top level is not a mapping (expected metadata/project/content)"]
    missing = [key for key in REQUIRED_TOP_KEYS if key not in tree]
    return True, ([f"missing top-level key: {key}" for key in missing])


def report(text, source):
    if not text.strip():
        print(f"validate_copy — {source}: no content to validate")
        return 0
    leakage = scan_leakage(text)
    ran_structure, problems = check_structure(text)
    total = len(leakage) + len(problems)
    print(f"validate_copy — {source}: {total} candidate(s)\n")

    print(f"Structure: {'checked' if ran_structure else 'skipped (no YAML parser)'}")
    for problem in problems:
        print(f"  {problem}")
    print()

    print(f"Design leakage: {len(leakage)}")
    for lineno, label, snippet in leakage:
        print(f"  L{lineno}: {label} — {snippet[:80]}")
    print()

    print("Note: leakage hits are candidates, not verdicts — a product named "
          "'Grid' or copy mentioning 'Blue' is a false positive to judge by eye.")
    return total


if __name__ == "__main__":
    text, source = read_input(sys.argv)
    report(text, source)
    # Exit 0 always: the report is advisory input to the human self-check,
    # not a pass/fail gate.
    sys.exit(0)
