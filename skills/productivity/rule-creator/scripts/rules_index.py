#!/usr/bin/env python3
"""Index the rules at user and project level, under .claude/rules and .agents/rules.

Usage:
  python3 rules_index.py [--user <dir>] [--project <dir>]
                         [--user-agents <dir>] [--project-agents <dir>]

Walks four rules directories recursively, following symlinks once: the user
directories (default ~/.claude/rules and ~/.agents/rules) and the project
directories (default .claude/rules and .agents/rules under the project root).
Prints a table, then each file expanded with its rule titles and Impact, then
the notes: a topic present in more than one directory, a symlink and its
target, a dangling link, and a file that departs from the rule template. Topic
identity is the path relative to its rules directory. The project root is the
nearest directory at or above the current one that holds .claude/rules,
.agents/rules, or .git, stopping below the home directory, so the index is the
same from any subdirectory.

Exit 0 when the index was printed, 2 when an argument is invalid.
"""

import os
import re
import sys

H1 = re.compile(r"^#\s+\S")
H2 = re.compile(r"^##\s+(.+?)\s*#*\s*$")
IMPACT = re.compile(r"^\*\*Impact:\s*(HIGH|MEDIUM|LOW)\*\*\s*$")
FENCE = re.compile(r"^(`{3,}|~{3,})")  # 3: shortest code fence CommonMark accepts
ITEM = re.compile(r"^\s*-\s*(.+?)\s*$")


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(lines):
    """Return (paths, body_start, problem). paths is None when the rule is unconditional."""
    if not lines or lines[0].strip() != "---":
        return None, 0, None
    for end in range(1, len(lines)):
        if lines[end].strip() == "---":
            break
    else:
        return None, 0, "frontmatter never closes, so Claude Code loads it as an unconditional rule"
    paths = None
    index = 1
    while index < end:
        line = lines[index]
        if line.startswith("paths:"):
            inline = line[len("paths:"):].strip()
            if inline:
                paths = [unquote(part) for part in inline.strip("[]").split(",") if part.strip()]
            else:
                paths = []
                index += 1
                while index < end and ITEM.match(lines[index]):
                    paths.append(unquote(ITEM.match(lines[index]).group(1)))
                    index += 1
                continue
        index += 1
    if paths is not None and not paths:
        return None, end + 1, "paths: is empty, so the rule loads unconditionally"
    return paths, end + 1, None


def parse_rules(lines, start):
    """Return ([(title, impact)] for every H2, whether an H1 stands) outside fenced blocks."""
    rules = []
    heading_one = False
    fence = None
    for line in lines[start:]:
        opening = FENCE.match(line.strip())
        if opening:
            marker = opening.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and line.strip() == marker:
                fence = None
            continue
        if fence is not None:
            continue
        if H1.match(line):
            heading_one = True
            continue
        heading = H2.match(line)
        if heading:
            rules.append([heading.group(1), None])
            continue
        impact = IMPACT.match(line.strip())
        if impact and rules and rules[-1][1] is None:
            rules[-1][1] = impact.group(1)
    return [tuple(rule) for rule in rules], heading_one


def read_lines(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read().splitlines(), None
    except UnicodeDecodeError:
        return None, "not UTF-8 text"
    except OSError as error:
        return None, error.strerror or "unreadable"


def label(entry):
    return entry["level"] if entry["home"] == "claude" else f"{entry['level']}-agents"


def walk(level, home, root):
    """Yield one entry per .md file under root, following each linked directory once."""
    entries = []
    if not os.path.isdir(root):
        return entries
    seen = set()
    for current, dirs, files in os.walk(root, followlinks=True):
        real = os.path.realpath(current)
        if real in seen:
            dirs[:] = []
            continue
        seen.add(real)
        dirs.sort()
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = os.path.join(current, name)
            entry = {
                "level": level,
                "home": home,
                "file": os.path.relpath(path, root),
                "path": path,
                "link": None,
                "paths": None,
                "rules": [],
                "problems": [],
            }
            if not os.path.exists(path):
                entry["problems"].append(f"dangling link to {os.readlink(path)}")
                entries.append(entry)
                continue
            lines, error = read_lines(path)
            if lines is None:
                entry["problems"].append(error)
                entries.append(entry)
                continue
            paths, start, problem = parse_frontmatter(lines)
            entry["paths"] = paths
            if os.path.islink(path):
                entry["link"] = os.path.realpath(path)
            if problem:
                entry["problems"].append(problem)
            if level == "user" and paths:
                entry["problems"].append("user-level rule carries paths:, which is reported to be ignored")
            if home == "agents" and paths:
                entry["problems"].append("rule under an .agents directory carries paths:, which only .claude rules directories use")
            entry["rules"], heading_one = parse_rules(lines, start)
            if heading_one:
                entry["problems"].append("H1 heading; a rule file carries none")
            if not entry["rules"]:
                entry["problems"].append("no H2 rule title")
            missing = [title for title, impact in entry["rules"] if impact is None]
            if missing:
                entry["problems"].append("no Impact line under: " + ", ".join(missing))
            entries.append(entry)
    return entries


def find_project_root(start):
    """Return the nearest ancestor of start holding .claude/rules, .agents/rules, or .git, or None."""
    home = os.path.realpath(os.path.expanduser("~"))
    current = os.path.realpath(start)
    while True:
        if current == home:
            return None
        markers = (os.path.join(".claude", "rules"), os.path.join(".agents", "rules"), ".git")
        if any(os.path.exists(os.path.join(current, marker)) for marker in markers):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def summary(rules):
    counts = {}
    for _, impact in rules:
        key = {"HIGH": "HIGH", "MEDIUM": "MED", "LOW": "LOW"}.get(impact, "no Impact")
        counts[key] = counts.get(key, 0) + 1
    order = ["HIGH", "MED", "LOW", "no Impact"]
    detail = ", ".join(f"{counts[key]} {key}" for key in order if key in counts)
    return f"{len(rules)} ({detail})" if rules else "0"


def scope(entry):
    return ", ".join(entry["paths"]) if entry["paths"] else "unconditional"


FLAGS = {"--user": "user", "--project": "project", "--user-agents": "user_agents", "--project-agents": "project_agents"}
USAGE = "Usage: rules_index.py [--user <dir>] [--project <dir>] [--user-agents <dir>] [--project-agents <dir>]"


def main(argv):
    dirs = {
        "user": os.path.expanduser("~/.claude/rules"),
        "user_agents": os.path.expanduser("~/.agents/rules"),
        "project": None,
        "project_agents": None,
    }
    args = list(argv)
    while args:
        flag = args.pop(0)
        if flag in FLAGS and args:
            dirs[FLAGS[flag]] = os.path.expanduser(args.pop(0))
        else:
            print(f"unknown or incomplete argument {flag!r}. {USAGE}")
            return 2

    root = find_project_root(os.getcwd())
    if root is not None:
        if dirs["project"] is None:
            dirs["project"] = os.path.join(root, ".claude", "rules")
        if dirs["project_agents"] is None:
            dirs["project_agents"] = os.path.join(root, ".agents", "rules")
    absent = "none, no .claude/rules, .agents/rules or .git at or above the current directory"
    print(f"USER RULES: {dirs['user']}")
    print(f"USER AGENTS RULES: {dirs['user_agents']}")
    print(f"PROJECT RULES: {dirs['project'] or absent}")
    print(f"PROJECT AGENTS RULES: {dirs['project_agents'] or absent}")
    print()

    entries = []
    walked = set()
    for level, home, key in (("user", "claude", "user"), ("user", "agents", "user_agents"), ("project", "claude", "project"), ("project", "agents", "project_agents")):
        root_dir = dirs[key]
        if not root_dir or os.path.realpath(root_dir) in walked:
            continue
        walked.add(os.path.realpath(root_dir))
        entries += walk(level, home, root_dir)
    if not entries:
        print("No rules defined.")
        return 0

    width = max(len(entry["file"]) for entry in entries) + 2
    label_width = max(len("LEVEL"), max(len(label(entry)) for entry in entries)) + 2
    scope_width = max(len(scope(entry)) for entry in entries) + 2
    print(f"{'LEVEL':<{label_width}}{'FILE':<{width}}{'SCOPE':<{scope_width}}RULES")
    for entry in entries:
        print(f"{label(entry):<{label_width}}{entry['file']:<{width}}{scope(entry):<{scope_width}}{summary(entry['rules'])}")

    print()
    for entry in entries:
        print(f"{entry['file']} ({label(entry)}, {scope(entry)})")
        for title, impact in entry["rules"]:
            print(f"  - {title} ({impact or 'no Impact'})")

    notes = []
    by_file = {}
    for entry in entries:
        by_file.setdefault(entry["file"], set()).add(label(entry))
    for name, labels in sorted(by_file.items()):
        if labels == {"user", "project"}:
            notes.append(f"{name}: present at both levels; the project rule prevails")
        elif len(labels) > 1:
            notes.append(f"{name}: present in {', '.join(sorted(labels))}")
    for entry in entries:
        if entry["link"]:
            notes.append(f"{entry['file']} ({label(entry)}): symlink to {entry['link']}; an edit writes through to every project linked to it")
        for problem in entry["problems"]:
            notes.append(f"{entry['file']} ({label(entry)}): {problem}")
    if notes:
        print()
        print("NOTES")
        for note in notes:
            print(f"  - {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
