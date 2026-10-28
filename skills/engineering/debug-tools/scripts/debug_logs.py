#!/usr/bin/env python3
"""Find and remove [DEBUG] log statements, each with its full line span.

Usage:
  python3 debug_logs.py find [<root>]
  python3 debug_logs.py remove [<root>]

Walks <root> (default: the current directory) for source files and finds every
candidate that carries the exact [DEBUG] prefix. A statement spans from the
line where its brackets open to the line where they close, so a call a
formatter split across lines is found and removed whole. Brackets inside
strings and comments are ignored. Dependency, build, and VCS directories are
skipped: generated output is rebuilt, never edited.

find prints one entry per statement as <file>:<start>-<end>, then the spans
held back for review (shared lines, non-log data, unsupported calls, comments,
or brackets that never close), then near-miss prefixes such as [debug] or
[DEBUG ] for the user to confirm. remove deletes every safe span and prints
the same report for what is left.

Exit 0 when no [DEBUG] candidate is left after the command, 1 when one is
left (including non-log markers held for review), 2 when an argument is invalid.
"""

import os
import re
import sys

EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte",
    ".py", ".go", ".rs", ".rb", ".java", ".kt", ".kts", ".scala", ".swift",
    ".cs", ".php", ".c", ".cc", ".cpp", ".h", ".hpp", ".dart", ".ex", ".exs", ".lua",
}
HASH_COMMENT = {".py", ".rb", ".ex", ".exs"}
DASH_COMMENT = {".lua"}
SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "out",
    "target", ".next", ".nuxt", ".svelte-kit", "__pycache__", ".venv", "venv",
    "coverage", ".turbo", ".cache",
}
MAX_SPAN = 50  # 50: a log call longer than this is not a log call; hold it back for a person
PREFIX = "[DEBUG]"
NEAR_MISS = re.compile(r"\[\s*debug\s*\]", re.IGNORECASE)
LOG_CALLS = {
    **dict.fromkeys((".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"), r"console\.(?:log|debug|info|warn|error|trace)"),
    ".py": r"print",
    ".go": r"fmt\.(?:Print|Printf|Println)",
    ".rs": r"(?:println|eprintln)!",
    ".rb": r"puts",
}


def standalone_log(text, ext):
    """Accept only a recognized log call with no code outside its parentheses."""
    name = LOG_CALLS.get(ext)
    if name is None:
        return False
    match = re.match(r"\s*(?:" + name + r")\s*\(", text)
    if not match:
        return False
    stack = ["("]
    marker = False
    i = match.end()
    while i < len(text):
        ch = text[i]
        if ch in "'\"`":
            quote = ch * 3 if text.startswith(ch * 3, i) else ch
            begin = i
            i += len(quote)
            while i < len(text) and not text.startswith(quote, i):
                i += 2 if text[i] == "\\" else 1
            if i >= len(text):
                return False
            marker |= PREFIX in text[begin:i]
            i += len(quote)
            continue
        if text.startswith("/*", i) and ext not in HASH_COMMENT:
            end = text.find("*/", i + 2)
            if end == -1:
                return False
            i = end + 2
            continue
        if (ch == "#" and ext in HASH_COMMENT) or (text.startswith("//", i) and ext not in HASH_COMMENT):
            i = skip_to_eol(text, i)
            continue
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != {")": "(", "]": "[", "}": "{"}[ch]:
                return False
            if not stack:
                suffix = text[i + 1:].strip()
                return marker and re.fullmatch(r";?\s*(?:(?://|\#)[^\n]*)?", suffix) is not None
        i += 1
    return False


def skip_to_eol(text, i):
    j = text.find("\n", i)
    return len(text) if j == -1 else j


def scan(text, ext):
    """Return per-line bracket depths, innermost bracket, and code-at-start state.

    Brackets inside strings and comments are ignored.
    """
    line_comment = "#" if ext in HASH_COMMENT else "--" if ext in DASH_COMMENT else "//"
    block_comments = ext not in HASH_COMMENT | DASH_COMMENT
    stack = []
    starts, ends, inner, active = [0], [], [None], [True]
    quote = None
    block = False
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "\n":
            ends.append(len(stack))
            starts.append(len(stack))
            inner.append(stack[-1] if stack else None)
            if quote in ("'", '"'):
                quote = None
            active.append(not block and quote is None)
            i += 1
            continue
        if block:
            if text.startswith("*/", i):
                block = False
                i += 1
        elif quote:
            if ch == "\\":
                i += 1
            elif text.startswith(quote, i):
                i += len(quote) - 1
                quote = None
        elif ch in "'\"`":
            quote = ch * 3 if ext == ".py" and text.startswith(ch * 3, i) else ch
            i += len(quote) - 1
        elif text.startswith(line_comment, i):
            i = skip_to_eol(text, i)
            continue
        elif block_comments and text.startswith("/*", i):
            block = True
            i += 1
        elif ch in "([{":
            stack.append(ch)
        elif ch in ")]}" and stack:
            stack.pop()
        i += 1
    ends.append(len(stack))
    return starts, ends, inner, active


def find_in_file(path):
    ext = os.path.splitext(path)[1]
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError):
        return [], [], []
    if PREFIX not in text and not NEAR_MISS.search(text):
        return [], [], []
    lines = text.split("\n")
    starts, ends, inner, active = scan(text, ext)
    spans, held, near = [], [], []
    seen = set()
    for idx, line in enumerate(lines):
        if PREFIX in line:
            if idx in seen:
                continue
            # A line that opens inside ( or [ continues a call or list begun above it.
            start = idx
            while start > 0 and inner[start] in ("(", "[") and idx - start < MAX_SPAN:
                start -= 1
            base = starts[start]
            end = idx
            while end < len(lines) - 1 and ends[end] > base and end - start < MAX_SPAN:
                end += 1
            seen.update(range(start, end + 1))
            if ends[end] != base or inner[start] in ("(", "["):
                held.append((start, end, "brackets never close"))
            elif not active[start] or not standalone_log("\n".join(lines[start:end + 1]), ext):
                held.append((start, end, "not a standalone recognized log call; preserve and review"))
            else:
                spans.append((start, end))
        elif NEAR_MISS.search(line):
            near.append(idx)
    return spans, held, near


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if os.path.splitext(name)[1] in EXTENSIONS:
                yield os.path.join(dirpath, name)


def collect(root):
    found = {}
    for path in walk(root):
        spans, held, near = find_in_file(path)
        if spans or held or near:
            found[path] = (spans, held, near)
    return found


def report(found, root, removed=None):
    rel = lambda p: os.path.relpath(p, root)
    if removed is not None:
        total = sum(len(s) for s in removed.values())
        print(f"removed: {total} statement(s) in {len(removed)} file(s)")
        for path, spans in sorted(removed.items()):
            print(f"  {rel(path)}: {len(spans)}")
    spans = [(p, s) for p, (ss, _, _) in sorted(found.items()) for s in ss]
    held = [(p, h) for p, (_, hh, _) in sorted(found.items()) for h in hh]
    near = [(p, n) for p, (_, _, nn) in sorted(found.items()) for n in nn]
    print(f"[DEBUG] statements: {len(spans)}")
    for p, (a, b) in spans:
        print(f"  {rel(p)}:{a + 1}-{b + 1}")
    print(f"held back for manual removal: {len(held)}")
    for p, (a, b, why) in held:
        print(f"  {rel(p)}:{a + 1}-{b + 1} ({why})")
    print(f"near-miss prefixes to confirm: {len(near)}")
    for p, n in near:
        print(f"  {rel(p)}:{n + 1}")
    return len(spans) + len(held)


def remove(found):
    removed = {}
    for path, (spans, _, _) in found.items():
        if not spans:
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                lines = fh.read().split("\n")
        except (OSError, UnicodeDecodeError):
            continue
        drop = set()
        for a, b in spans:
            drop.update(range(a, b + 1))
        kept = [line for i, line in enumerate(lines) if i not in drop]
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(kept))
        except OSError as err:
            print(f"could not write {path}: {err}", file=sys.stderr)
            continue
        removed[path] = spans
    return removed


def main(argv):
    if not argv or argv[0] not in ("find", "remove") or len(argv) > 2:
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    root = argv[1] if len(argv) == 2 else "."
    if not os.path.isdir(root):
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    found = collect(root)
    if argv[0] == "find":
        return 1 if report(found, root) else 0
    removed = remove(found)
    left = report(collect(root), root, removed)
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
