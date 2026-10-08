#!/usr/bin/env python3
"""Check an edited draft for literals, protected blocks, and conditions it lost.

Usage:
  python3 check_preserved.py --source <file> --draft <file> [--accept <word> ...]

Every fenced code block and frontmatter block in the source must appear
verbatim in the draft. Every code span, URL, link target, path, and number in
the source must appear verbatim in the draft. Each condition word (only,
unless, never, ...) must appear at least as often, and each modal verb (must,
should, may, can, ...) exactly as often. Pass --accept <word> for a condition
or modal the draft states another way. Chat-tool citation markers such as
[cite: 1] or turn0search0 are dropped from the source first, since the edit
removes them.

Exit 0 when clean, 1 when a line is flagged, 2 when a file cannot be read.
"""

import argparse
import re
import sys
from collections import Counter

# Markers chat tools leave in pasted answers; the edit removes them, so their digits are not literals.
CITATION_MARKER = re.compile(
    r":?contentReference\[oaicite:\d+\](?:\{index=\d+\})?"
    r"|\[?oaicite:\d+\]?"
    r"|\[cite(?::\s*[\d,\s]+)?\]"
    r"|\bturn\d+(?:search|news|view|fetch)\d+\b"
    r"|【[^】\n]*】"
)
FENCE = re.compile(r"^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$", re.M | re.S)
FRONTMATTER = re.compile(r"\A---\n.*?\n---[ \t]*$", re.M | re.S)
CODE_SPAN = re.compile(r"`([^`\n]+)`")
URL = re.compile(r"\bhttps?://[^\s)>\]]+")
LINK_TARGET = re.compile(r"\]\(([^)\s]+)")
PATH = re.compile(r"(?<![\w/.])(?:~|\.{1,2})?/?[\w.-]+(?:/[\w.-]+)+/?")
# Any digit run counts: an edit may reword a number's sentence but never its value.
NUMBER = re.compile(r"(?<![\w.])\d+(?:[.,:]\d+)*%?")
CONDITION_WORDS = ["only", "unless", "until", "while", "never", "except", "if",
                   "somente", "apenas", "exceto", "nunca", "enquanto"]
# A modal sets how strongly a sentence binds; swapping "should" for "must" changes the norm.
MODAL_WORDS = ["must", "should", "may", "might", "can", "cannot", "can't", "will", "won't", "shall",
               "deve", "devem", "deveria", "pode", "podem", "poderia"]


def read(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def is_path(token):
    # "and/or" and "1/2" are not paths: require a root, a dot in the last segment, or two slashes.
    return token.startswith(("/", "~", ".")) or "." in token.rsplit("/", 1)[-1] or token.count("/") >= 2


def blocks(text):
    found = [match.group(0) for match in FENCE.finditer(text)]
    frontmatter = FRONTMATTER.match(text)
    if frontmatter:
        found.append(frontmatter.group(0))
    return found


def literals(text):
    prose = FENCE.sub("", text)
    found = set(CODE_SPAN.findall(prose)) | set(URL.findall(prose)) | set(LINK_TARGET.findall(prose))
    found |= set(NUMBER.findall(prose))
    found |= {p for p in PATH.findall(prose) if is_path(p) and not p.startswith("http")}
    return found


def count(text, vocabulary):
    words = re.findall(r"\b\w+(?:'\w+)?\b", FENCE.sub("", text).lower())
    return Counter(w for w in words if w in vocabulary)


def check(source, draft, accepted):
    findings = []
    source = CITATION_MARKER.sub("", source)
    for block in blocks(source):
        if block not in draft:
            first = block.splitlines()[0]
            findings.append(f"protected block starting {first!r} changed or missing. Restore it verbatim.")
    for item in sorted(literals(source)):
        if item not in draft:
            findings.append(f"missing literal `{item}`. Keep it verbatim from the source.")
    before, after = count(source, CONDITION_WORDS), count(draft, CONDITION_WORDS)
    for word in sorted(before):
        if after[word] < before[word] and word not in accepted:
            findings.append(f"condition word `{word}` appears {before[word]} times in the source and "
                            f"{after[word]} in the draft. Restore the condition, or pass --accept {word} "
                            f"when the draft states it another way.")
    before, after = count(source, MODAL_WORDS), count(draft, MODAL_WORDS)
    for word in sorted(set(before) | set(after)):
        if after[word] != before[word] and word not in accepted:
            findings.append(f"modal `{word}` appears {before[word]} times in the source and {after[word]} "
                            f"in the draft. Keep each modal's strength, or pass --accept {word} when the "
                            f"draft states the same obligation another way.")
    return findings


def main():
    parser = argparse.ArgumentParser(description="Check an edited draft against its source.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--draft", required=True)
    parser.add_argument("--accept", action="append", default=[])
    args = parser.parse_args()
    try:
        source = read(args.source)
        draft = read(args.draft)
    except OSError as error:
        print(f"cannot read {error.filename}: {error.strerror}.")
        return 2
    findings = check(source, draft, {word.lower() for word in args.accept})
    if not findings:
        print(f"clean: {args.draft}")
        return 0
    for message in findings:
        print(f"{args.draft}: {message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
