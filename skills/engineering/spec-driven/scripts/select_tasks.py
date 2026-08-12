#!/usr/bin/env python3
"""Select incomplete spec-driven tasks by task, slice, or derived wave.

Usage:
  select_tasks.py .artifacts/specs/{slug} [T-N | T-N..T-M | S-N | S-N..S-M | W-N | W-N..W-M]
"""

import argparse
import os
import re
import sys


TASK_HEADING = re.compile(r"^###\s+\[([ x])\]\s+(T-\d+):\s*(.*)$")
TASK_REF = re.compile(r"\bT-\d+\b")
SLICE_REF = re.compile(r"\bS-\d+\b")
WAVE_REF = re.compile(r"\bW-\d+\b")
TASK_SLICE = re.compile(r"^\s*-\s*\*\*Slice:\*\*\s*(.*)$", re.IGNORECASE)
TASK_DEPENDS = re.compile(r"^\s*-\s*\*\*Depends on:\*\*\s*(.*)$", re.IGNORECASE)


def read_lines(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise RuntimeError("could not read %s: %s" % (path, error)) from error


def section_bounds(lines, title):
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip().split("<!--")[0].strip() == title:
            start = index
            continue
        if start is not None and line.startswith("## "):
            return start, index
    return (start, len(lines)) if start is not None else None


def table_rows(lines, bounds):
    header = None
    for index in range(bounds[0], bounds[1]):
        stripped = lines[index].strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set("-: ") for cell in cells) and cells:
            continue
        yield header, cells


def cell(header, cells, name):
    try:
        position = header.index(name)
    except ValueError:
        return ""
    return cells[position] if position < len(cells) else ""


def parse_tasks(lines):
    tasks = []
    current = None
    for line in lines:
        match = TASK_HEADING.match(line)
        if match:
            current = {
                "id": match.group(2),
                "title": match.group(3),
                "done": match.group(1).lower() == "x",
                "slice": "none",
                "depends": [],
                "block": [],
            }
            tasks.append(current)
        elif current is not None and line.startswith("### "):
            current = None
        elif current is not None:
            current["block"].append(line)

    for task in tasks:
        for line in task["block"]:
            slice_match = TASK_SLICE.match(line)
            if slice_match:
                value = slice_match.group(1).strip()
                if value.lower() != "none":
                    refs = SLICE_REF.findall(value)
                    task["slice"] = refs[0] if refs else value
            dependency_match = TASK_DEPENDS.match(line)
            if dependency_match and dependency_match.group(1).strip().lower() != "none":
                task["depends"] = TASK_REF.findall(dependency_match.group(1))
    return tasks


def parse_sequence(lines):
    bounds = section_bounds(lines, "Sequence")
    if bounds is None:
        raise RuntimeError("tasks.md has no `Sequence` section")
    sequence = {}
    for header, cells in table_rows(lines, bounds):
        wave = cell(header, cells, "Wave")
        refs = TASK_REF.findall(cell(header, cells, "Tasks"))
        if not WAVE_REF.fullmatch(wave) or not refs:
            continue
        sequence[wave] = refs
    if not sequence:
        raise RuntimeError("`Sequence` has no valid wave rows")
    return sequence


def parse_selector(selector):
    if selector is None:
        return None, None, None
    match = re.fullmatch(r"([TSW])-(\d+)(?:\.\.([TSW])-(\d+))?", selector)
    if not match or (match.group(3) and match.group(1) != match.group(3)):
        raise RuntimeError("invalid selector `%s`; use T, S, or W with an optional same-kind range" % selector)
    kind = match.group(1)
    start = int(match.group(2))
    end = int(match.group(4) or match.group(2))
    if end < start:
        raise RuntimeError("selector range must ascend: `%s`" % selector)
    return kind, start, end


def selected_ids(tasks, sequence, selector):
    kind, start, end = parse_selector(selector)
    if kind is None:
        return {task["id"] for task in tasks}
    if kind == "T":
        return {"T-%d" % value for value in range(start, end + 1)}
    if kind == "S":
        selected = set()
        for task in tasks:
            match = re.fullmatch(r"S-(\d+)", task["slice"])
            if match and start <= int(match.group(1)) <= end:
                selected.add(task["id"])
        return selected
    selected = set()
    for wave, refs in sequence.items():
        wave_number = int(wave.split("-")[1])
        if start <= wave_number <= end:
            selected.update(refs)
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description="Select incomplete spec-driven tasks.")
    parser.add_argument("feature_dir")
    parser.add_argument("selector", nargs="?")
    args = parser.parse_args(argv)

    try:
        task_path = os.path.join(args.feature_dir, "tasks.md")
        lines = read_lines(task_path)
        tasks = parse_tasks(lines)
        sequence = parse_sequence(lines)
        by_id = {task["id"]: task for task in tasks}
        if len(by_id) != len(tasks):
            raise RuntimeError("tasks.md declares a task more than once")
        requested = selected_ids(tasks, sequence, args.selector)
        unknown = sorted(requested - set(by_id), key=lambda value: int(value.split("-")[1]))
        if unknown:
            raise RuntimeError("selector names unknown task(s): %s" % ", ".join(unknown))
        incomplete = {identifier for identifier in requested if not by_id[identifier]["done"]}
        ordered = [task for wave in sorted(sequence, key=lambda value: int(value.split("-")[1]))
                   for identifier in sequence[wave]
                   if identifier in incomplete
                   for task in [by_id[identifier]]]
        selected_set = {task["id"] for task in ordered}
        print("Selection: %s" % (args.selector or "whole feature"))
        print("Tasks:")
        if not ordered:
            print("- none (all selected tasks are complete)")
        for task in ordered:
            waiting = [dependency for dependency in task["depends"]
                       if dependency not in selected_set and dependency in by_id and not by_id[dependency]["done"]]
            status = "blocked by %s" % ", ".join(waiting) if waiting else "ready"
            print("- %s [%s] %s" % (task["id"], status, task["title"]))
        skipped = sorted(requested - incomplete, key=lambda value: int(value.split("-")[1]))
        if skipped:
            print("Skipped complete: %s" % ", ".join(skipped))
        return 0
    except RuntimeError as error:
        print("error: %s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
