#!/usr/bin/env python3
"""Look up or add the project entry for the current repo in the registry.

Usage:
  python3 registry.py lookup
  python3 registry.py add --name <name> --path <obsidian-path> --tags <a,b>

The registry is ~/.config/wrap-up/projects.yml. The repo root is the main
worktree from `git worktree list --porcelain`, or the current directory
outside a git repo.

lookup prints the entry as JSON and exits 0; exits 1 when the registry or
the entry is missing, with a message naming which; exits 2 when the
registry cannot be read or parsed.

add appends the entry and exits 0. When the entry already exists, it
prints the existing entry and changes nothing. Exits 2 when the registry
cannot be parsed or the write does not read back.
"""

import argparse
import json
import os
import re
import subprocess
import sys

REGISTRY = os.path.expanduser("~/.config/wrap-up/projects.yml")

KEY_LINE = re.compile(r"^(\s*)(?:\"((?:[^\"\\]|\\.)*)\"|([^\s\"#][^:]*?))\s*:\s*(.*)$")
ITEM_LINE = re.compile(r"^(\s*)-\s+(.*)$")
PLAIN_SCALAR = re.compile(r"^[A-Za-z0-9_./~ +-]+$")


class RegistryError(Exception):
    pass


def repo_root():
    try:
        result = subprocess.run(
            ["git", "worktree", "list", "--porcelain"],
            capture_output=True, text=True, check=True,
        )
        first = result.stdout.splitlines()[0] if result.stdout else ""
        if first.startswith("worktree "):
            return first[len("worktree "):]
    except (OSError, subprocess.CalledProcessError, IndexError):
        pass
    return os.getcwd()


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return json.loads(value)
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def quote(value):
    return value if PLAIN_SCALAR.match(value) and ": " not in value else json.dumps(value)


def parse(text):
    """Parse the registry schema: projects -> root -> name, obsidian.path, tags."""
    projects = {}
    top_keys = []
    current = None
    section = None
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        item = ITEM_LINE.match(line)
        if item:
            if current is None or section != "tags":
                raise RegistryError(f"line {number}: list item outside `tags`")
            projects[current]["tags"].append(unquote(item.group(2)))
            continue
        match = KEY_LINE.match(line)
        if not match:
            raise RegistryError(f"line {number}: cannot parse `{line.strip()}`")
        indent = len(match.group(1))
        key = match.group(2) if match.group(2) is not None else match.group(3).strip()
        if match.group(2) is not None:
            key = json.loads(f'"{key}"')
        value = match.group(4).strip()
        if indent == 0:
            top_keys.append(key)
            current = None
        elif indent == 2:
            if key in projects:
                raise RegistryError(f"line {number}: duplicate entry `{key}`")
            current = key
            projects[key] = {"name": None, "obsidian_path": None, "tags": []}
            section = None
        elif current is not None:
            section = key
            if key == "name":
                projects[current]["name"] = unquote(value)
            elif key == "path":
                projects[current]["obsidian_path"] = unquote(value)
    if top_keys and top_keys != ["projects"]:
        raise RegistryError(f"top-level keys must be only `projects`, found {top_keys}")
    return projects


def read_registry():
    try:
        with open(REGISTRY, encoding="utf-8") as handle:
            return handle.read()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise RegistryError(f"cannot read {REGISTRY}: {error.strerror}")


def entry_block(root, name, path, tags):
    lines = [
        f"  {quote(root)}:",
        f"    name: {quote(name)}",
        "    obsidian:",
        f"      path: {quote(path)}",
        "    tags:" if tags else "    tags: []",
    ]
    lines += [f"      - {quote(tag)}" for tag in tags]
    return "\n".join(lines) + "\n"


def cmd_lookup():
    root = repo_root()
    text = read_registry()
    if text is None:
        print(f"no registry at {REGISTRY}. Run `registry.py add` to create it with this repo's entry.")
        return 1
    entry = parse(text).get(root)
    if entry is None:
        print(f"no entry for {root} in {REGISTRY}. Ask for the entry, then run `registry.py add`.")
        return 1
    print(json.dumps({"root": root, **entry}))
    return 0


def cmd_add(args):
    root = repo_root()
    text = read_registry()
    if text is None:
        os.makedirs(os.path.dirname(REGISTRY), exist_ok=True)
        text = "projects:\n"
    projects = parse(text)
    if root in projects:
        print(json.dumps({"root": root, **projects[root], "status": "exists"}))
        return 0
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    if not text.endswith("\n"):
        text += "\n"
    if not text.strip():
        text = "projects:\n"
    text += entry_block(root, args.name, args.path, tags)
    with open(REGISTRY, "w", encoding="utf-8") as handle:
        handle.write(text)
    written = parse(read_registry()).get(root)
    if written != {"name": args.name, "obsidian_path": args.path, "tags": tags}:
        raise RegistryError(f"the entry for {root} did not read back as written. Check {REGISTRY}.")
    print(json.dumps({"root": root, **written, "status": "added"}))
    return 0


def main():
    parser = argparse.ArgumentParser(description="Look up or add this repo's registry entry.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("lookup")
    add = sub.add_parser("add")
    add.add_argument("--name", required=True)
    add.add_argument("--path", required=True)
    add.add_argument("--tags", default="")
    args = parser.parse_args()
    try:
        return cmd_lookup() if args.command == "lookup" else cmd_add(args)
    except RegistryError as error:
        print(f"registry error: {error}. Fix {REGISTRY} by hand, then run the command again.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
