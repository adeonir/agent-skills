#!/usr/bin/env python3
"""Inspect or apply tracker settings and their instruction block using local Git config."""

import json
from pathlib import Path
import re
import subprocess
import sys

PREFIX = "tracker."
KEYS = {"kind", "team", "team-name", "project", "project-name", "repository", "project-owner", "channel", "fallback"}


def git(root, *args, allowed=(0,)):
    result = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if result.returncode not in allowed:
        raise ValueError(result.stderr.strip() or "Git command failed: " + " ".join(args))
    return result.stdout


def read_settings(root):
    raw = git(root, "config", "--local", "--null", "--get-regexp", r"^tracker\.", allowed=(0, 1))
    settings = {}
    for item in raw.split("\0"):
        if item:
            key, value = item.split("\n", 1)
            key = key[len(PREFIX):]
            if key in settings:
                raise ValueError("Duplicate owned key: " + key)
            settings[key] = value
    return settings


def validate(settings):
    if not isinstance(settings, dict):
        raise ValueError("Settings must be a JSON object.")
    if set(settings) - KEYS:
        raise ValueError("Unknown settings: " + ", ".join(sorted(set(settings) - KEYS)))
    for key, value in settings.items():
        if not isinstance(value, str) or not value.strip() or any(c in value for c in "\r\n\0"):
            raise ValueError(key + " must be a nonempty single-line string.")
    kind = settings.get("kind")
    if kind == "linear":
        if set(settings) != {"kind", "team", "team-name", "project", "project-name"}:
            raise ValueError("Linear requires kind, team, team-name, project, and project-name.")
    elif kind == "github":
        required = {"kind", "repository", "channel", "fallback"}
        if not required <= set(settings) or {"team", "team-name", "project-name"} & set(settings):
            raise ValueError("GitHub requires kind, repository, channel, and fallback, without Linear settings.")
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", settings["repository"]):
            raise ValueError("repository must be owner/name.")
        primary, fallback = settings["channel"], settings["fallback"]
        if primary not in {"mcp", "cli"} or fallback not in {"mcp", "cli", "none"} or primary == fallback:
            raise ValueError("Choose mcp or cli as primary, and a different fallback or none.")
        if ("project" in settings) != ("project-owner" in settings):
            raise ValueError("GitHub project and project-owner must be supplied together.")
        if "project" in settings and (not settings["project"].isdigit() or int(settings["project"]) <= 0):
            raise ValueError("GitHub project must be a positive project number.")
    else:
        raise ValueError("kind must be linear or github.")


def instruction_path(root):
    candidates = [root / "CLAUDE.md", root / ".claude" / "CLAUDE.md"]
    target = next((p for p in candidates if p.is_file()), root / "AGENTS.md")
    if target.name == "CLAUDE.md":
        imported = re.search(r"(?m)^[ \t]*@((?:\./|\.\./)?AGENTS\.md)[ \t]*$", target.read_text())
        if imported:
            target = target.parent / imported.group(1)
    target = target.resolve()
    try:
        target.relative_to(root)
    except ValueError as error:
        raise ValueError("Instruction file resolves outside the repository.") from error
    return target


def block(settings):
    if settings["kind"] == "linear":
        destination = "Linear; team " + settings["team-name"] + "; project " + settings["project-name"]
    else:
        destination = "GitHub Issues; repository " + settings["repository"]
        if "project" in settings:
            destination += "; project " + settings["project-owner"] + "/" + settings["project"]
    return "## Issue tracker\n\nTracker: " + destination + ". Configuration: repository-local `tracker.*`; inspect with `git config --local --get-regexp '^tracker\\.'`. Change with \"configure tracker\".\n"


def tracker_sections(text):
    """Locate real level-two tracker headings, excluding fenced code examples."""
    headings = []
    fence = None
    offset = 0
    for line in text.splitlines(keepends=True):
        # CommonMark fences allow up to three leading spaces and at least three markers.
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line.rstrip("\r\n"))
        if fence:
            if marker and marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence) and not marker.group(2).strip():
                fence = None
        elif marker:
            fence = marker.group(1)
        else:
            heading = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*$", line.rstrip("\r\n"))
            if heading:
                title = re.sub(r"[ \t]+#+$", "", (heading.group(2) or "")).strip()
                headings.append((offset, len(heading.group(1)), title))
        offset += len(line)
    if fence:
        raise ValueError("Unclosed Markdown fence; repair it before maintaining the tracker block.")
    result = []
    for index, (start, level, title) in enumerate(headings):
        if level == 2 and title == "Issue tracker":
            end = next((pos for pos, depth, _ in headings[index + 1:] if depth <= level), len(text))
            result.append((start, end))
    return result


def replace_block(text, new_block):
    if "\r\n" in text:
        new_block = new_block.replace("\n", "\r\n")
    separator = "\r\n" if "\r\n" in text else "\n"
    matches = tracker_sections(text)
    if len(matches) > 1:
        raise ValueError("Duplicate Issue tracker sections; resolve them before applying settings.")
    if matches:
        start, end = matches[0]
        body = text[start:end].splitlines()[1:]
        if len([line for line in body if line.strip()]) > 1:
            raise ValueError("Issue tracker section contains extra or ambiguous content; preserve it and resolve manually.")
        return text[:start] + new_block + (separator if text[end:] else "") + text[end:]
    return text.rstrip("\r\n") + (separator * 2 if text else "") + new_block


def write_settings(root, settings):
    current = read_settings(root)
    for key in current:
        if key not in settings:
            git(root, "config", "--local", "--unset-all", PREFIX + key)
    for key, value in settings.items():
        git(root, "config", "--local", "--replace-all", PREFIX + key, value)


def main():
    if len(sys.argv) not in (2, 3) or sys.argv[1] not in {"show", "apply"}:
        raise ValueError("Usage: config.py show | apply <settings.json>")
    if len(sys.argv) != (3 if sys.argv[1] == "apply" else 2):
        raise ValueError("apply requires one settings file; show takes no settings file.")
    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
    previous = read_settings(root)
    target = instruction_path(root)
    text = target.read_bytes().decode("utf-8") if target.exists() else ""
    if sys.argv[1] == "show":
        error = None
        try:
            validate(previous)
        except ValueError as problem:
            error = str(problem)
        matches = tracker_sections(text)
        consistent = error is None and len(matches) == 1 and text[matches[0][0]:matches[0][1]].replace("\r\n", "\n").rstrip() == block(previous).rstrip()
        print(json.dumps(dict(settings=previous, error=error, instruction_file=str(target), block_consistent=consistent)))
        return
    settings = json.loads(Path(sys.argv[2]).read_text())
    validate(settings)
    updated = replace_block(text, block(settings))
    try:
        write_settings(root, settings)
        target.write_bytes(updated.encode("utf-8"))
        if read_settings(root) != settings:
            raise ValueError("Saved settings did not match selected settings.")
    except (OSError, ValueError) as error:
        rollback_errors = []
        try:
            write_settings(root, previous)
        except (OSError, ValueError) as rollback:
            rollback_errors.append(str(rollback))
        try:
            if target.exists() and target.read_bytes().decode("utf-8") != text:
                target.write_bytes(text.encode("utf-8"))
        except OSError as rollback:
            rollback_errors.append(str(rollback))
        raise ValueError(str(error) + "; rollback: " + ("; ".join(rollback_errors) or "prior contents restored")) from error
    print(json.dumps(dict(settings=settings, instruction_file=str(target), block_consistent=True)))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print("tracker-config: " + str(error), file=sys.stderr)
        sys.exit(1)
