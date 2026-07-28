#!/usr/bin/env python3
"""Lint a spec-driven artifact against its template contract.

Checks structure, presence, and cross-file references only — never style or
prose. Every violation it reports is resolvable without judgment, so the peer
check that follows spends its reading on what needs a reader.

Usage:
  lint_artifact.py spec   .artifacts/specs/{slug}
  lint_artifact.py design .artifacts/specs/{slug}
  lint_artifact.py tasks  .artifacts/specs/{slug}

Exit codes:
  0  clean
  1  violations found (one line each on stdout)
  2  argument/usage error (argparse default)
  3  target artifact not found
  4  read error that could not be recovered
"""

import argparse
import os
import re
import sys

SPEC_SECTIONS = ["Overview", "Goals", "Non-Goals", "User Stories", "Edge Cases", "Open Questions"]
DESIGN_SECTIONS = ["Scope", "Architecture Overview", "Components", "Decisions",
                   "Error Handling", "Risks & Concerns", "Requirements Traceability"]
TASKS_SECTIONS = ["Scope", "Task List", "Coverage Matrix"]

SPEC_FRONTMATTER = ["name", "scope", "sources", "user-facing", "status", "created", "branch"]
SCOPES = ["medium", "large", "complex"]
STATUSES = ["draft", "in-progress", "done"]

TASK_FIELDS = ["Story", "Gate", "Done when"]

# Source-file extensions barred from spec.md prose: naming one is a HOW leak.
# Backtick-quoted only, so a bare domain term with a dot never trips it.
CODE_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".rb", ".go", ".rs",
                   ".java", ".kt", ".php", ".c", ".cpp", ".h", ".hpp", ".cs", ".swift",
                   ".sql", ".sh", ".vue", ".svelte", ".scala", ".ex", ".exs")

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AC_PATTERN = re.compile(r"\bAC-(\d+)\b")
AC_DEFINITION = re.compile(r"^\s*-\s+AC-(\d+):")
AC_TOMBSTONE = re.compile(r"\bAC-(\d+)\s+removed\b")
STORY_HEADING = re.compile(r"^###\s+(S-\d+):")
TASK_HEADING = re.compile(r"^###\s+\[[ x]\]\s+(T-\d+):")
STORY_REF = re.compile(r"\bS-\d+\b")
TASK_REF = re.compile(r"\bT-\d+\b")
BACKTICKED = re.compile(r"`([^`]+)`")
DESIGN_TAG = re.compile(r"\((?:verify|confirm) @ design\)")


def read_lines(path):
    """Return the file's lines without trailing newlines, or None if unreadable."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        sys.stderr.write("error: could not read %s: %s\n" % (path, error))
        return None


def parse_frontmatter(lines):
    """Return (fields, body_start). An absent fence yields ({}, 0)."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fields = {}
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return fields, index + 1
        raw = lines[index].split("#", 1)[0]  # strip trailing YAML comment
        if ":" in raw:
            key, value = raw.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, 0  # unterminated fence: treat the whole file as body


def section_bounds(lines, title):
    """Return (start, end) line indices for a `## title` section, or None."""
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and line[3:].strip().split("<!--")[0].strip() == title:
            start = index
            continue
        if start is not None and line.startswith("## "):
            return start, index
    if start is not None:
        return start, len(lines)
    return None


def table_rows(lines, start, end):
    """Yield (line_number, header, cells) for each body row of the first table found."""
    header = None
    for index in range(start, end):
        stripped = lines[index].strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(set(cell) <= set("-: ") for cell in cells) and cells:
            continue  # separator row
        yield index + 1, header, cells


def cell(header, cells, name):
    """Return the named column's value, or '' when the column is absent."""
    try:
        position = header.index(name)
    except ValueError:
        return ""
    return cells[position] if position < len(cells) else ""


def spec_ac_ids(spec_lines):
    """Return (live ids, tombstoned ids) declared by the spec."""
    live = []
    for line in spec_lines:
        match = AC_DEFINITION.match(line)
        if match:
            live.append(int(match.group(1)))
    tombstoned = {int(m.group(1)) for line in spec_lines for m in [AC_TOMBSTONE.search(line)] if m}
    return live, tombstoned


def check_sections(path, lines, titles, findings):
    for title in titles:
        if section_bounds(lines, title) is None:
            findings.append("%s:1: missing required section `## %s`" % (path, title))


def check_frontmatter_path(path, base, fields, key, findings):
    """Confirm a frontmatter path field is present and resolves to a file."""
    target = fields.get(key, "")
    if not target:
        findings.append("%s:1: frontmatter `%s:` is missing" % (path, key))
        return
    candidates = [target, os.path.join(base, os.path.basename(target))]
    if not any(os.path.isfile(candidate) for candidate in candidates):
        findings.append("%s:1: frontmatter `%s:` points at a missing file (%s)" % (path, key, target))


def lint_spec(path, lines, base, findings):
    fields, body_start = parse_frontmatter(lines)
    for key in SPEC_FRONTMATTER:
        if key not in fields:
            findings.append("%s:1: frontmatter is missing `%s`" % (path, key))
    if fields.get("scope") and fields["scope"] not in SCOPES:
        findings.append("%s:1: `scope` is `%s`, not one of %s" % (path, fields["scope"], "/".join(SCOPES)))
    if fields.get("status") and fields["status"] not in STATUSES:
        findings.append("%s:1: `status` is `%s`, not one of %s" % (path, fields["status"], "/".join(STATUSES)))
    if fields.get("created") and not DATE_PATTERN.match(fields["created"]):
        findings.append("%s:1: `created` is not YYYY-MM-DD" % path)

    check_sections(path, lines, SPEC_SECTIONS, findings)

    live, _ = spec_ac_ids(lines)
    seen = set()
    highest = 0
    for number in live:
        if number in seen:
            findings.append("%s:1: AC-%d is declared more than once" % (path, number))
        elif number < highest:
            findings.append("%s:1: AC-%d breaks the monotonic sequence" % (path, number))
        seen.add(number)
        highest = max(highest, number)

    prompt_seeded = fields.get("sources", "").strip() in ("[]", "")
    downstream = any(os.path.isfile(os.path.join(base, name)) for name in ("design.md", "tasks.md"))

    for index in range(body_start, len(lines)):
        line = lines[index]
        number = index + 1
        if "[needs-clarification" in line:
            findings.append("%s:%d: `[needs-clarification]` survives in the saved spec" % (path, number))
        if "[assumption]" in line:
            if not DESIGN_TAG.search(line):
                findings.append("%s:%d: `[assumption]` carries no `(confirm @ design)` or `(verify @ design)`" % (path, number))
            elif "(verify @ design)" in line and "verify:" not in line:
                findings.append("%s:%d: `(verify @ design)` carries no `verify:` check" % (path, number))
        if "[seed-gap]" in line:
            if "(reconcile seed)" not in line:
                findings.append("%s:%d: `[seed-gap]` closes without `(reconcile seed)`" % (path, number))
            if prompt_seeded:
                findings.append("%s:%d: `[seed-gap]` on a prompt-seeded spec (`sources: []`)" % (path, number))
            if not downstream:
                findings.append("%s:%d: `[seed-gap]` without `design.md` or `tasks.md` — not a re-entry" % (path, number))
        for quoted in BACKTICKED.findall(line):
            if quoted.endswith(CODE_EXTENSIONS):
                findings.append("%s:%d: `%s` names a source file — that is HOW" % (path, number, quoted))


def lint_design(path, lines, base, spec_path, spec_lines, findings):
    fields, _ = parse_frontmatter(lines)
    check_frontmatter_path(path, base, fields, "spec", findings)
    check_sections(path, lines, DESIGN_SECTIONS, findings)

    bounds = section_bounds(lines, "Decisions")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            if not cell(header, cells, "Rejected") and not cell(header, cells, "Source"):
                findings.append("%s:%d: Decisions row has neither `Rejected` nor `Source` — a fork closed silently" % (path, number))

    bounds = section_bounds(lines, "Risks & Concerns")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            if not cell(header, cells, "Mitigation"):
                findings.append("%s:%d: Risks row has an empty `Mitigation`" % (path, number))

    if spec_lines is None:
        return
    live, tombstoned = spec_ac_ids(spec_lines)
    traced = set()
    bounds = section_bounds(lines, "Requirements Traceability")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                identifier = int(match.group(1))
                traced.add(identifier)
                if identifier not in live:
                    findings.append("%s:%d: traceability names AC-%d, which the spec does not declare" % (path, number, identifier))
    for identifier in sorted(set(live)):
        if identifier not in traced and identifier not in tombstoned:
            findings.append("%s:1: AC-%d reaches no row in Requirements Traceability" % (path, identifier))

    for index, line in enumerate(spec_lines):
        if DESIGN_TAG.search(line):
            findings.append("%s:%d: `@ design` line survives in the spec while `design.md` exists" % (spec_path, index + 1))


def lint_tasks(path, lines, base, spec_lines, findings):
    fields, _ = parse_frontmatter(lines)
    check_frontmatter_path(path, base, fields, "spec", findings)
    check_frontmatter_path(path, base, fields, "design", findings)
    check_sections(path, lines, TASKS_SECTIONS, findings)

    tasks = []           # (id, line number, story, block lines)
    current = None
    for index, line in enumerate(lines):
        match = TASK_HEADING.match(line)
        if match:
            current = [match.group(1), index + 1, "", []]
            tasks.append(current)
        elif current is not None and line.startswith("### "):
            current = None
        elif current is not None:
            current[3].append(line)

    declared = set()
    highest = 0
    for identifier, number, _, block in tasks:
        value = int(identifier.split("-")[1])
        if identifier in declared:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        elif value < highest:
            findings.append("%s:%d: %s breaks the monotonic sequence" % (path, number, identifier))
        declared.add(identifier)
        highest = max(highest, value)
        body = "\n".join(block)
        for field in TASK_FIELDS:
            if "**%s:**" % field not in body:
                findings.append("%s:%d: %s carries no `**%s:**`" % (path, number, identifier, field))

    stories = {match.group(1) for line in (spec_lines or []) for match in [STORY_HEADING.match(line)] if match}
    order = []
    for entry in tasks:
        identifier, number, _, block = entry
        for line in block:
            if line.strip().startswith("- **Story:**"):
                found = STORY_REF.search(line)
                entry[2] = found.group(0) if found else ""
                break
        if entry[2]:
            order.append(entry[2])
            if spec_lines is not None and entry[2] not in stories:
                findings.append("%s:%d: %s names %s, which the spec does not declare" % (path, number, identifier, entry[2]))
        if entry[2] == "" and spec_lines is not None:
            findings.append("%s:%d: %s names no story" % (path, number, identifier))
        for line in block:
            if line.strip().startswith("- **Depends on:**"):
                for reference in TASK_REF.findall(line):
                    if reference not in declared:
                        findings.append("%s:%d: %s depends on %s, which is not declared above it" % (path, number, identifier, reference))

    seen_stories = []
    for story in order:
        if story in seen_stories and seen_stories[-1] != story:
            findings.append("%s:1: %s's tasks are not contiguous" % (path, story))
        if not seen_stories or seen_stories[-1] != story:
            seen_stories.append(story)

    if spec_lines is None:
        return
    live, tombstoned = spec_ac_ids(spec_lines)
    covered = set()
    bounds = section_bounds(lines, "Coverage Matrix")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                covered.add(int(match.group(1)))
            for reference in TASK_REF.findall(cell(header, cells, "Task")):
                if reference not in declared:
                    findings.append("%s:%d: Coverage Matrix names %s, which the Task List does not declare" % (path, number, reference))
    for identifier in sorted(set(live)):
        if identifier not in covered and identifier not in tombstoned:
            findings.append("%s:1: AC-%d reaches no row in the Coverage Matrix" % (path, identifier))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lint a spec-driven artifact against its template contract.")
    parser.add_argument("phase", choices=["spec", "design", "tasks"])
    parser.add_argument("feature_dir", help="the feature folder, e.g. .artifacts/specs/{slug}")
    args = parser.parse_args(argv)

    base = args.feature_dir
    path = os.path.join(base, "%s.md" % args.phase)
    if not os.path.isfile(path):
        sys.stderr.write("error: no %s at %s\n" % (args.phase, path))
        return 3
    lines = read_lines(path)
    if lines is None:
        return 4

    spec_path = os.path.join(base, "spec.md")
    spec_lines = lines if args.phase == "spec" else None
    if args.phase != "spec":
        if os.path.isfile(spec_path):
            spec_lines = read_lines(spec_path)
        else:
            sys.stderr.write("warning: no spec.md at %s; skipping cross-file checks\n" % spec_path)

    findings = []
    try:
        if args.phase == "spec":
            lint_spec(path, lines, base, findings)
        elif args.phase == "design":
            lint_design(path, lines, base, spec_path, spec_lines, findings)
        else:
            lint_tasks(path, lines, base, spec_lines, findings)
    except Exception as error:  # last-resort guard: never surface a raw traceback
        sys.stderr.write("error: %s\n" % error)
        return 4

    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("%s: clean" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
