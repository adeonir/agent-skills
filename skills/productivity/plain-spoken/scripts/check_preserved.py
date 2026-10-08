#!/usr/bin/env python3
"""Check a draft for lost literals, dropped conditions, and leaked credentials.

Usage:
  python3 check_preserved.py --draft <file> [--source <file>] [--accept <word> ...]

With --source, every code span, URL, path, and number with a unit or a
decimal in the source must appear verbatim in the draft, each condition
word (only, unless, never, ...) must appear at least as often, and each modal
verb (must, should, may, can, ...) must appear exactly as often. Pass
--accept <word> for a condition or modal the draft states another way. Without
--source, only the credential check runs. A credential value found in the
draft is masked in the output, never printed.

Exit 0 when clean, 1 when a line is flagged, 2 when a file cannot be read.
"""

import argparse
import re
import sys
from collections import Counter

CODE_SPAN = re.compile(r"`([^`\n]+)`")
URL = re.compile(r"\bhttps?://[^\s)>\]]+")
PATH = re.compile(r"(?<![\w/.])(?:~|\.{1,2})?/?[\w.-]+(?:/[\w.-]+)+/?")
# A number carries meaning when it has a decimal, a unit, or a percent sign.
NUMBER = re.compile(r"\b\d+(?:\.\d+)?\s?(?:%|ms|s|min|h|d|KB|MB|GB|TB|px|rem|em)(?![\w])|\b\d+\.\d+\b")
CONDITION_WORDS = ["only", "unless", "until", "while", "never", "except", "if",
                   "somente", "apenas", "exceto", "nunca", "enquanto"]
# A modal sets how strongly a sentence binds; swapping "should" for "must" changes the norm.
MODAL_WORDS = ["must", "should", "may", "might", "can", "cannot", "can't", "will", "won't", "shall",
               "deve", "devem", "deveria", "pode", "podem", "poderia"]

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
    ("secret assignment", re.compile(r"(?i)\b\w*(?:api[_-]?key|secret|token|password|passwd|pwd)\w*\s*[:=]\s*['\"]?(?![$<{])[^\s'\"{}`]{8,}")),
]


def mask(text):
    # Keep 4 characters so the user can locate the value without seeing it.
    return text[:4] + "…" if len(text) > 4 else "…"


def read(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def is_path(token):
    # "and/or" and "1/2" are not paths: require a root, a dot in the last segment, or two slashes.
    return token.startswith(("/", "~", ".")) or "." in token.rsplit("/", 1)[-1] or token.count("/") >= 2


def is_secret(token):
    return any(pattern.search(token) for _, pattern in SECRET_PATTERNS)


def literals(text):
    found = set(CODE_SPAN.findall(text)) | set(URL.findall(text)) | set(NUMBER.findall(text))
    found |= {p for p in PATH.findall(text) if is_path(p) and not p.startswith("http")}
    return {item for item in found if not is_secret(item)}


def count(text, vocabulary):
    words = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())
    return Counter(w for w in words if w in vocabulary)


def check(source, draft, accepted):
    findings = []
    if source is not None:
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
    for number, line in enumerate(draft.splitlines(), start=1):
        for kind, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(line):
                findings.append(f"line {number}: {kind} ({mask(match.group(0))}). Replace the value with a placeholder such as $API_KEY.")
    return findings


def main():
    parser = argparse.ArgumentParser(description="Check a draft against its source.")
    parser.add_argument("--draft", required=True)
    parser.add_argument("--source")
    parser.add_argument("--accept", action="append", default=[])
    args = parser.parse_args()
    try:
        draft = read(args.draft)
        source = read(args.source) if args.source else None
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
