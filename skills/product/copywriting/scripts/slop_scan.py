#!/usr/bin/env python3
"""Deterministic floor for the anti-patterns slop verdict.

Scans copy text (a file path or stdin) for the *deterministic-kind* tells from
references/anti-patterns.md — listed dead words, em-dash density, and known
stock phrases (openers, hooks, fillers) — and prints a line-numbered tally. It is an anchor, not
a verdict: the perceptual tells (empty antithesis, generic claim, robotic
parallelism) need a human read and are out of scope here on purpose.

Usage:
    python3 slop_scan.py path/to/copy.yaml
    python3 slop_scan.py < pasted_copy.txt
"""

import re
import sys

# Dead marketing words and hype verbs from the dead-marketing-words rule.
# Matched whole-word, case-insensitive.
DEAD_WORDS = [
    "passionate", "results-driven", "innovative", "cutting-edge", "world-class",
    "best-in-class", "seamless", "robust", "synergy", "holistic", "disruptive",
    "game-changing", "leverage", "unlock", "elevate", "supercharge", "empower",
    "revolutionize", "transform",
]

# Every literal-phrase tell from the catalog — borrowed-frame openers,
# reveal hooks, the whether-you're sweep, and the dead-phrases list. Kept in
# sync with anti-patterns.md so the floor mirrors the spec. Matched as
# substrings, case-insensitive.
OPENERS = [
    "imagine a world", "picture this", "in a world of", "we live in an age",
    "in today's fast-paced world", "welcome to our", "let's dive in",
    "but here's the thing", "the best part?", "here's the kicker",
    "and it gets better", "whether you're", "we are committed to excellence",
    "let's connect", "the fact of the matter is", "needless to say",
    "at this moment in time",
]

EM_DASH = "—"          # U+2014 em-dash; the over-used machine pause
EM_DASH_PER_LINE_MAX = 1    # em-dash-density rule: >1 in one unit is the tell


def read_input(argv):
    """Return (text, source-label), falling back to stdin. Never raises."""
    if len(argv) > 1:
        path = argv[1]
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read(), path
        except (OSError, UnicodeDecodeError) as err:
            print(f"slop_scan: cannot read {path}: {err}", file=sys.stderr)
            return "", path
    try:
        return sys.stdin.read(), "<stdin>"
    except (OSError, UnicodeDecodeError):
        return "", "<stdin>"


def scan(text):
    """Return the three tally lists; pure, deterministic over the input."""
    dead_hits, opener_hits, dash_hits = [], [], []
    word_patterns = [
        (word, re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE))
        for word in DEAD_WORDS
    ]
    for lineno, raw in enumerate(text.splitlines(), start=1):
        lowered = raw.lower()
        for word, pattern in word_patterns:
            if pattern.search(raw):
                dead_hits.append((lineno, word, raw.strip()))
        for opener in OPENERS:
            if opener in lowered:
                opener_hits.append((lineno, opener, raw.strip()))
        count = raw.count(EM_DASH)
        if count > EM_DASH_PER_LINE_MAX:
            dash_hits.append((lineno, count, raw.strip()))
    return dead_hits, opener_hits, dash_hits


def report(text, source):
    dead_hits, opener_hits, dash_hits = scan(text)
    total = len(dead_hits) + len(opener_hits) + len(dash_hits)
    print(f"slop_scan — {source}: {total} deterministic tell(s)\n")

    def section(title, hits, fmt):
        print(f"{title}: {len(hits)}")
        for hit in hits:
            print("  " + fmt(hit))
        print()

    section("Dead words", dead_hits,
            lambda h: f"L{h[0]}: '{h[1]}' — {h[2][:80]}")
    section("Borrowed-frame openers, reveal hooks, filler phrases", opener_hits,
            lambda h: f"L{h[0]}: '{h[1]}' — {h[2][:80]}")
    section(f"Em-dash density (>{EM_DASH_PER_LINE_MAX} per line)", dash_hits,
            lambda h: f"L{h[0]}: {h[1]} em-dashes — {h[2][:80]}")

    print("Note: perceptual tells (empty antithesis, generic claim, robotic "
          "parallelism) are NOT scanned here — read for those by eye.")
    return total


if __name__ == "__main__":
    text, source = read_input(sys.argv)
    report(text, source)
    # Exit 0 always: the tally is advisory input to a perceptual verdict,
    # not a pass/fail gate.
    sys.exit(0)
