#!/usr/bin/env python3
"""Lint a spec-driven artifact against its template contract.

Checks structure, presence, and cross-file references only — never style or
prose. Every violation it reports is resolvable without judgment, so the reading
that precedes it spends itself on what needs a reader.

Two severities. An error is a contract violation and blocks `ready`. A warning
names what is usually wrong and can be deliberate; it never blocks, and the
phase says at its gate whether it acted on the warning or kept what it names.

Usage:
  lint_artifact.py spec     .artifacts/specs/{slug}
  lint_artifact.py design   .artifacts/specs/{slug}
  lint_artifact.py tasks    .artifacts/specs/{slug}
  lint_artifact.py validate .artifacts/specs/{slug}
  lint_artifact.py audit    .artifacts/specs/{slug}

Exit codes:
  0  no error (warnings may still be printed)
  1  errors found (one line each on stdout)
  2  argument/usage error (argparse default)
  3  target artifact not found
  4  read error that could not be recovered
"""

import argparse
import os
import re
import sys

SPEC_SECTIONS = ["Overview", "Goals", "Non-Goals", "User Stories", "Edge Cases", "Assumptions", "Open Questions"]
DESIGN_SECTIONS = ["Scope", "Architecture Overview", "Components", "Decisions", "Error Handling",
                   "Risks & Concerns", "Requirements Traceability"]
TASKS_SECTIONS = ["Scope", "Sequence", "Task List"]
VALIDATE_SECTIONS = ["Summary", "Criteria", "Accessibility", "Responsiveness", "Out of Scope", "Findings"]
AUDIT_SECTIONS = ["Summary", "Goals", "Acceptance Criteria", "Discrimination Sensor", "Re-run", "Gaps"]

VALIDATE_SUMMARY = ["Status", "Feature", "Date", "Application", "Criteria"]
AUDIT_SUMMARY = ["Status", "Feature", "Commit range", "Failed audits in a row", "Auditor", "Date", "Disproof"]
REPORT_STATUSES = ["PASS", "FAIL", "BLOCKED"]
VALIDATE_VERDICTS = ["met", "unmet", "blocked"]
AUDIT_AC_STATUSES = ["PASS", "FAIL", "UNSETTLED"]

SPEC_FRONTMATTER = ["name", "sources", "user-facing", "status", "created", "branch"]
SPEC_STATUSES = ["draft", "ready"]
DESIGN_STATUSES = ["draft", "ready"]
TASK_STATUSES = ["draft", "ready", "in-progress", "done"]
# Gherkin keywords that open a step group, and the ones that continue the open group.
STEP_OPENERS = ("Given", "When", "Then")
STEP_CONTINUATIONS = ("And", "But")

TASK_FIELDS = ["Slice", "Builds", "Depends on", "Gate", "Done when"]


# Source-file extensions barred from spec.md prose: naming one is a HOW leak.
# Backtick-quoted only, so a bare domain term with a dot never trips it.
CODE_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".py", ".rb", ".go", ".rs",
                   ".java", ".kt", ".php", ".c", ".cpp", ".h", ".hpp", ".cs", ".swift",
                   ".sql", ".sh", ".vue", ".svelte", ".scala", ".ex", ".exs")

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
AC_PATTERN = re.compile(r"\bAC-\d+\.\d+\b")
AC_DEFINITION = re.compile(r"^####\s+(AC-\d+\.\d+)\b")
GOAL_DEFINITION = re.compile(r"^\s*-\s*(?:\[[ x]\]\s*)?\*\*(G-\d+)\*\*")
SERVES = re.compile(r"^\*\*Serves\*\*\s*(.*)$", re.IGNORECASE)
SATISFIES = re.compile(r"^\*\*Satisfies\*\*\s*(.*)$", re.IGNORECASE)
SATISFIES_ID = re.compile(r"^(?:FR|BR|EC|NFR)-\d+$")
ASSUMPTION_ID = re.compile(r"^ASM-[1-9]\d*$")
ASSUMPTION_STATUSES = ["open", "confirmed", "invalidated"]
OPEN_QUESTION_ID = re.compile(r"^OQ-[1-9]\d*$")
OPEN_QUESTION_STATUSES = ["open", "answered"]
GOAL_ID = re.compile(r"^G-\d+$")
STEP_KEYWORD = re.compile(r"^(Given|When|Then|And|But)\s+\S")
GHERKIN_PLACEHOLDER = re.compile(r"<([^<>]+)>")
STORY_HEADING = re.compile(r"^###\s+(S-\d+):")
TASK_HEADING = re.compile(r"^###\s+\[([ x-])\]\s+(T-\d+):\s*(.*)$")
AC_REMOVED = re.compile(r"^####\s+AC-\d+\.\d+:\s*~~.+~~\s+removed\s*$")
STORY_REMOVED = re.compile(r"^###\s+S-\d+:\s*~~.+~~\s+removed\s*$")
REMOVED_TITLE = re.compile(r"^~~.+~~\s+removed\s*$")
REASON_LINE = re.compile(r"^Reason:\s*\S")
SLICE_REF = re.compile(r"\bS-\d+\b")
TASK_REF = re.compile(r"\bT-\d+\b")
TASK_COVERS = re.compile(r"^\s*-\s*\*\*Covers:\*\*\s*(.*)$", re.IGNORECASE)
TASK_TEST = re.compile(r"^\s*-\s*\*\*Test:\*\*\s*(.*)$", re.IGNORECASE)
TASK_TEST_NONE = re.compile(r"^none\b\s*[—–:-]*\s*(.*)$", re.IGNORECASE)
TASKS_RUNNER = re.compile(r"^\*\*Runner:\*\*\s*(.*)$", re.IGNORECASE)
TASK_SLICE = re.compile(r"^\s*-\s*\*\*Slice:\*\*\s*(.*)$", re.IGNORECASE)
TASK_BUILDS = re.compile(r"^\s*-\s*\*\*Builds:\*\*\s*(.*)$", re.IGNORECASE)
TASK_DEPENDS = re.compile(r"^\s*-\s*\*\*Depends on:\*\*\s*(.*)$", re.IGNORECASE)
WAVE_ID = re.compile(r"^W-(\d+)$")
BACKTICKED = re.compile(r"`([^`]+)`")
BLOCK_ITEM = re.compile(r"^\s*-\s+(.*)$")


def read_lines(path):
    """Return the file's lines without trailing newlines, or None if unreadable."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        sys.stderr.write("error: could not read %s: %s\n" % (path, error))
        return None


def parse_frontmatter(lines):
    """Return (fields, body_start). A block sequence joins into one comma-separated
    value under its key. An absent fence yields ({}, 0)."""
    if not lines or lines[0].strip() != "---":
        return {}, 0
    fields = {}
    key = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return fields, index + 1
        raw = lines[index].split("#", 1)[0]  # strip trailing YAML comment
        item = BLOCK_ITEM.match(raw)
        if item and key is not None:
            value = item.group(1).strip()
            if value:
                fields[key] = ", ".join(part for part in (fields[key], value) if part)
            continue
        if ":" in raw:
            key, value = raw.split(":", 1)
            key = key.strip()
            fields[key] = value.strip()
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
    """Return the live `AC-N.M` ids the spec declares, in document order.

    A removed criterion, or one under a removed slice, is not live.
    """
    return [criterion["id"] for criterion in spec_criteria(spec_lines)
            if not criterion["removed"] and not criterion["under_removed"]]


def spec_live_stories(spec_lines):
    """Return the `S-N` ids the spec declares and has not removed."""
    return {match.group(1) for line in spec_lines
            for match in [STORY_HEADING.match(line)]
            if match and not STORY_REMOVED.match(line)}


def implementation_started(base):
    """Return True once `tasks.md` carries a ticked task; ids are frozen from then on."""
    lines = read_lines(os.path.join(base, "tasks.md"))
    return any(match and match.group(1) == "x"
               for line in (lines or []) for match in [TASK_HEADING.match(line)])


def ac_sort_key(identifier):
    """Order ids numerically, so AC-1.10 follows AC-1.2 instead of preceding it."""
    story, position = identifier[len("AC-"):].split(".")
    return int(story), int(position)


def spec_user_facing(spec_lines):
    """Return True when the spec frontmatter declares `user-facing: true`."""
    for line in spec_lines:
        match = re.match(r"^user-facing:\s*(\S+)", line)
        if match:
            return match.group(1).strip().lower() == "true"
    return False


def spec_goal_ids(spec_lines):
    """Return the `G-N` ids declared under `## Goals`, in document order."""
    bounds = section_bounds(spec_lines, "Goals")
    if bounds is None:
        return []
    start, end = bounds
    return [match.group(1) for index in range(start, end)
            for match in [GOAL_DEFINITION.match(spec_lines[index])] if match]


def spec_criteria(lines):
    """Return one record per `#### AC-N.M` block.

    Each is {id, line, story, block, serves, satisfies}: the enclosing story id,
    the fenced gherkin block's step lines, and the two bold sub-lines it carries.
    """
    criteria = []
    story = None
    story_removed = False
    current = None
    in_block = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if in_block:
            if stripped.startswith("```"):
                in_block = False
            elif current is not None and stripped:
                current["block"].append(stripped)
            continue
        heading = AC_DEFINITION.match(line)
        if heading:
            current = {"id": heading.group(1), "line": index + 1, "story": story,
                       "block": [], "serves": [], "satisfies": [], "fenced": False,
                       "removed": bool(AC_REMOVED.match(line)), "under_removed": story_removed,
                       "reason": False}
            criteria.append(current)
            continue
        match = STORY_HEADING.match(line)
        if match:
            story = match.group(1)
            story_removed = bool(STORY_REMOVED.match(line))
            current = None
            continue
        if line.startswith("## "):
            story = None
            story_removed = False
            current = None
            continue
        if current is None:
            continue
        if REASON_LINE.match(stripped):
            current["reason"] = True
            continue
        if stripped.startswith("```gherkin"):
            in_block = True
            current["fenced"] = True
            continue
        found = SERVES.match(stripped)
        if found:
            current["serves"].append(found.group(1).strip())
            continue
        found = SATISFIES.match(stripped)
        if found:
            current["satisfies"].append(found.group(1).strip())
    return criteria


def validate_gherkin(path, criterion, findings):
    """Check one criterion's fenced block against the Gherkin form."""
    identifier, number, block = criterion["id"], criterion["line"], criterion["block"]
    if not criterion["fenced"] or not block:
        findings.append("%s:%d: %s carries no fenced ```gherkin block" % (path, number, identifier))
        return

    opening = block[0]
    outline = opening.startswith("Scenario Outline:")
    if not outline and not opening.startswith("Scenario:"):
        findings.append("%s:%d: %s does not open with `Scenario:` or `Scenario Outline:`"
                        % (path, number, identifier))
        return

    seen = {"Given": False, "When": False, "Then": False}
    current_group = None
    examples_at = [index for index, line in enumerate(block) if line.startswith("Examples:")]
    steps_end = examples_at[0] if examples_at else len(block)
    for step in block[1:steps_end]:
        match = STEP_KEYWORD.match(step)
        if not match:
            findings.append("%s:%d: %s has a line that is not a Gherkin step: `%s`"
                            % (path, number, identifier, step))
            continue
        keyword = match.group(1)
        if keyword in STEP_CONTINUATIONS:
            if current_group is None:
                findings.append("%s:%d: %s puts `%s` before any step group"
                                % (path, number, identifier, keyword))
            continue
        if keyword == "When" and not seen["Given"]:
            findings.append("%s:%d: %s puts `When` before any `Given`" % (path, number, identifier))
        if keyword == "Then" and not seen["When"]:
            findings.append("%s:%d: %s puts `Then` before any `When`" % (path, number, identifier))
        current_group = keyword
        seen[keyword] = True

    for keyword in STEP_OPENERS:
        if not seen[keyword]:
            findings.append("%s:%d: %s has no `%s` step" % (path, number, identifier, keyword))

    if not outline and examples_at:
        findings.append("%s:%d: %s is a `Scenario` but carries an `Examples` table"
                        % (path, number, identifier))
    if not outline:
        return
    if len(examples_at) != 1:
        findings.append("%s:%d: %s is a `Scenario Outline` with %d `Examples` tables, expected one"
                        % (path, number, identifier, len(examples_at)))
        return

    table = block[examples_at[0] + 1:]
    if len(table) < 2 or any(not row.startswith("|") for row in table):
        findings.append("%s:%d: %s `Examples` needs one header and at least one data row"
                        % (path, number, identifier))
        return
    rows = [[value.strip() for value in row.strip("|").split("|")] for row in table]
    header = rows[0]
    if any(not value for value in header) or len(set(header)) != len(header):
        findings.append("%s:%d: %s `Examples` header has an empty or duplicate column"
                        % (path, number, identifier))
    for row in rows[1:]:
        if len(row) != len(header):
            findings.append("%s:%d: %s `Examples` row has %d cells, expected %d"
                            % (path, number, identifier, len(row), len(header)))

    placeholders = set(GHERKIN_PLACEHOLDER.findall("\n".join(block[:steps_end])))
    columns = set(header)
    for missing in sorted(placeholders - columns):
        findings.append("%s:%d: %s placeholder <%s> has no `Examples` column"
                        % (path, number, identifier, missing))
    for unused in sorted(columns - placeholders):
        findings.append("%s:%d: %s `Examples` column `%s` binds no placeholder"
                        % (path, number, identifier, unused))


def check_criteria(path, lines, findings, warnings):
    """Check every criterion's form, identity, and upward links."""
    goals = spec_goal_ids(lines)
    seen_goals = set()
    served_goals = set()
    for identifier in goals:
        if identifier in seen_goals:
            findings.append("%s:1: %s is declared more than once in `## Goals`" % (path, identifier))
        seen_goals.add(identifier)

    seen_stories = set()
    for index, line in enumerate(lines):
        match = STORY_HEADING.match(line)
        if not match:
            continue
        if match.group(1) in seen_stories:
            findings.append("%s:%d: %s is declared more than once"
                            % (path, index + 1, match.group(1)))
        seen_stories.add(match.group(1))
        if STORY_REMOVED.match(line):
            following = next((other.strip() for other in lines[index + 1:] if other.strip()), "")
            if not REASON_LINE.match(following):
                findings.append("%s:%d: %s is removed but carries no `Reason:` line"
                                % (path, index + 1, match.group(1)))

    declared = set()
    for criterion in spec_criteria(lines):
        identifier, number, story = criterion["id"], criterion["line"], criterion["story"]
        if identifier in declared:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        declared.add(identifier)

        story_number = identifier[len("AC-"):].split(".")[0]
        if story is None:
            findings.append("%s:%d: %s sits under no story" % (path, number, identifier))
        elif story != "S-%s" % story_number:
            findings.append("%s:%d: %s sits under %s — the criterion number names story %s"
                            % (path, number, identifier, story, story_number))
        if criterion["under_removed"]:
            findings.append("%s:%d: %s sits under removed %s — a removed slice takes its criteria with it"
                            % (path, number, identifier, story))
            continue
        if criterion["removed"]:
            if not criterion["reason"]:
                findings.append("%s:%d: %s is removed but carries no `Reason:` line"
                                % (path, number, identifier))
            continue

        validate_gherkin(path, criterion, findings)

        if len(criterion["serves"]) > 1:
            findings.append("%s:%d: %s carries %d `Serves` lines, expected one"
                            % (path, number, identifier, len(criterion["serves"])))
        for value in criterion["serves"]:
            if not GOAL_ID.match(value):
                findings.append("%s:%d: %s `Serves %s` is not exactly one `G-N` id"
                                % (path, number, identifier, value))
            elif value not in seen_goals:
                findings.append("%s:%d: %s serves %s, which `## Goals` does not declare"
                                % (path, number, identifier, value))
            else:
                served_goals.add(value)

        if len(criterion["satisfies"]) > 1:
            findings.append("%s:%d: %s carries %d `Satisfies` lines, expected one"
                            % (path, number, identifier, len(criterion["satisfies"])))
        for value in criterion["satisfies"]:
            if not SATISFIES_ID.match(value):
                findings.append("%s:%d: %s `Satisfies %s` is not exactly one `FR/BR/EC/NFR-N` id"
                                % (path, number, identifier, value))

    for identifier in dict.fromkeys(goals):
        if identifier not in served_goals:
            findings.append("%s:1: %s is declared in `## Goals` but no acceptance criterion serves it"
                            % (path, identifier))


def check_frozen_ids(path, lines, started, warnings):
    """Before any task is done, ask for renumbering instead of a removal or a gap."""
    if started:
        return
    for index, line in enumerate(lines):
        if STORY_REMOVED.match(line) or AC_REMOVED.match(line):
            warnings.append("%s:%d: warning: a removal before any task is done — renumber instead"
                            % (path, index + 1))
    stories = [int(identifier[len("S-"):]) for line in lines
               for match in [STORY_HEADING.match(line)] if match and not STORY_REMOVED.match(line)
               for identifier in [match.group(1)]]
    if stories != list(range(1, len(stories) + 1)):
        warnings.append("%s:1: warning: slices are not numbered S-1 onward without gaps — renumber before any task is done"
                        % path)
    per_story = {}
    for criterion in spec_criteria(lines):
        if criterion["removed"] or criterion["under_removed"]:
            continue
        story, position = ac_sort_key(criterion["id"])
        per_story.setdefault(story, []).append(position)
    for story, positions in sorted(per_story.items()):
        if positions != list(range(1, len(positions) + 1)):
            warnings.append("%s:1: warning: S-%d criteria are not numbered AC-%d.1 onward without gaps — renumber before any task is done"
                            % (path, story, story))


def check_pending_table(path, lines, title, identifier_pattern, statuses, expected_header, seen_ids, findings):
    """Check an ASM/OQ table and return the identifiers it declares."""
    bounds = section_bounds(lines, title)
    if bounds is None:
        return set()
    start, end = bounds
    content = [line.strip().lower() for line in lines[start + 1:end] if line.strip()]
    if content == ["none"]:
        return set()

    rows = list(table_rows(lines, start, end))
    if not rows:
        findings.append("%s:1: `## %s` carries no table or `none`" % (path, title))
        return set()
    header = rows[0][1]
    if header != expected_header:
        findings.append("%s:%d: `## %s` header is `%s`, expected `%s`"
                        % (path, rows[0][0], title, " | ".join(header), " | ".join(expected_header)))
        return set()

    declared = set()
    for number, _, cells in rows:
        if len(cells) != len(expected_header):
            findings.append("%s:%d: `## %s` row has %d cells, expected %d"
                            % (path, number, title, len(cells), len(expected_header)))
            continue
        identifier = cells[0]
        if not identifier_pattern.match(identifier):
            findings.append("%s:%d: `%s` is not a well-formed identifier for `## %s`"
                            % (path, number, identifier, title))
        elif identifier in seen_ids:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        else:
            seen_ids.add(identifier)
            declared.add(identifier)

        status = cells[expected_header.index("Status")].lower()
        if status not in statuses:
            findings.append("%s:%d: %s carries status `%s`, not one of %s"
                            % (path, number, identifier, status, "/".join(statuses)))
    return declared


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


def check_frontmatter_status(path, fields, allowed, findings):
    """Require an artifact status and validate it against its phase contract."""
    status = fields.get("status", "")
    if not status:
        findings.append("%s:1: frontmatter `status:` is missing" % path)
    elif status not in allowed:
        findings.append("%s:1: `status` is `%s`, not one of %s"
                        % (path, status, "/".join(allowed)))


def resolve_linked_file(base, target):
    """Resolve a frontmatter path from the repository root or feature directory."""
    if not target:
        return None
    candidates = [target, os.path.join(base, os.path.basename(target))]
    return next((candidate for candidate in candidates if os.path.isfile(candidate)), None)


def read_design_components(base, target, findings=None):
    """Return component names from the linked design blocks, or None if unavailable."""
    design_path = resolve_linked_file(base, target)
    if design_path is None:
        return None
    lines = read_lines(design_path)
    if lines is None:
        return None
    bounds = section_bounds(lines, "Components")
    if bounds is None:
        return None
    components = []
    first_lines = {}
    for index, line in enumerate(lines[bounds[0] + 1:bounds[1]], start=bounds[0] + 2):
        if line.startswith("### "):
            name = line[4:].strip()
            if name:
                if findings is not None and "," in name:
                    findings.append("%s:%d: component name `%s` cannot contain a comma" %
                                    (design_path, index, name))
                if findings is not None and name.lower() == "none":
                    findings.append("%s:%d: component name `none` is reserved by the `Builds` field" %
                                    (design_path, index))
                if findings is not None and name in first_lines:
                    findings.append("%s:%d: component `%s` duplicates the component at line %d" %
                                    (design_path, index, name, first_lines[name]))
                else:
                    first_lines[name] = index
                components.append(name)
    return components


def split_field_list(value):
    """Split a comma-separated task field, treating `none` as an empty list."""
    if value is None or not value.strip() or value.strip().lower() == "none":
        return []
    return [entry.strip() for entry in value.split(",") if entry.strip()]


def lint_spec(path, lines, base, findings, warnings):
    fields, body_start = parse_frontmatter(lines)
    for key in SPEC_FRONTMATTER:
        if key not in fields:
            findings.append("%s:1: frontmatter is missing `%s`" % (path, key))
    if fields.get("status") and fields["status"] not in SPEC_STATUSES:
        findings.append("%s:1: `status` is `%s`, not one of %s" % (path, fields["status"], "/".join(SPEC_STATUSES)))
    if fields.get("created") and not DATE_PATTERN.match(fields["created"]):
        findings.append("%s:1: `created` is not YYYY-MM-DD" % path)

    check_sections(path, lines, SPEC_SECTIONS, findings)

    check_criteria(path, lines, findings, warnings)

    seen_ids = set()
    assumption_ids = check_pending_table(
        path, lines, "Assumptions", ASSUMPTION_ID, ASSUMPTION_STATUSES,
        ["ID", "Assumption", "Rationale", "Status"], seen_ids, findings)
    check_pending_table(
        path, lines, "Open Questions", OPEN_QUESTION_ID, OPEN_QUESTION_STATUSES,
        ["ID", "Question", "Answer", "Status"], seen_ids, findings)
    check_frozen_ids(path, lines, implementation_started(base), warnings)

    for index in range(body_start, len(lines)):
        line = lines[index]
        number = index + 1
        for reference in re.findall(r"\bASM-[1-9]\d*\b", line):
            if reference not in assumption_ids:
                findings.append("%s:%d: %s is referenced but not declared in `## Assumptions`" % (path, number, reference))
        for quoted in BACKTICKED.findall(line):
            if quoted.endswith(CODE_EXTENSIONS):
                findings.append("%s:%d: `%s` names a source file — that is HOW" % (path, number, quoted))


def lint_design(path, lines, base, spec_path, spec_lines, findings):
    fields, _ = parse_frontmatter(lines)
    check_frontmatter_status(path, fields, DESIGN_STATUSES, findings)
    check_frontmatter_path(path, base, fields, "spec", findings)
    check_sections(path, lines, DESIGN_SECTIONS, findings)
    design_components = read_design_components(base, path, findings)

    bounds = section_bounds(lines, "Decisions")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            if not cell(header, cells, "Rejected") and not cell(header, cells, "Source"):
                findings.append("%s:%d: Decisions row has neither `Rejected` nor `Source` — a fork closed silently" % (path, number))

    inventory_columns = ["Candidate", "Existing declarations/usages", "Established meaning",
                         "Renderer/token mapping", "Conflict", "Source"]
    bounds = section_bounds(lines, "Semantic Contract Inventory")
    inventory_rows = list(table_rows(lines, *bounds)) if bounds else []
    if bounds and not inventory_rows:
        findings.append("%s:1: `Semantic Contract Inventory` needs a table with at least one row" % path)
    elif inventory_rows:
        _, header, _ = inventory_rows[0]
        for column in inventory_columns:
            if column not in header:
                findings.append("%s:1: `Semantic Contract Inventory` is missing `%s`" % (path, column))
        for number, row_header, cells in inventory_rows[1:]:
            candidate = cell(row_header, cells, "Candidate").strip().strip("`").lower()
            if not candidate:
                findings.append("%s:%d: semantic inventory row has an empty `Candidate`" % (path, number))
                continue
            if candidate == "none":
                continue
            for column in inventory_columns[1:]:
                if not cell(row_header, cells, column).strip():
                    findings.append("%s:%d: semantic inventory row for `%s` has an empty `%s`" %
                                    (path, number, cell(row_header, cells, "Candidate"), column))

    bounds = section_bounds(lines, "Risks & Concerns")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            if not cell(header, cells, "Mitigation"):
                findings.append("%s:%d: Risks row has an empty `Mitigation`" % (path, number))

    if spec_lines is None:
        return
    live = spec_ac_ids(spec_lines)
    traced = set()
    bounds = section_bounds(lines, "Requirements Traceability")
    if bounds:
        traceability_rows = list(table_rows(lines, *bounds))
        if traceability_rows:
            _, header, _ = traceability_rows[0]
            for column in ("AC", "Component"):
                if column not in header:
                    findings.append("%s:1: `Requirements Traceability` is missing `%s`" % (path, column))
        for number, header, cells in traceability_rows:
            component = cell(header, cells, "Component").strip()
            if not component:
                findings.append("%s:%d: traceability row has an empty `Component`" % (path, number))
            elif design_components is not None and component not in design_components:
                findings.append("%s:%d: traceability names unknown component `%s`" %
                                (path, number, component))
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                identifier = match.group(0)
                traced.add(identifier)
                if identifier not in live:
                    findings.append("%s:%d: traceability names %s, which the spec does not declare" % (path, number, identifier))
    for identifier in sorted(set(live), key=ac_sort_key):
        if identifier not in traced:
            findings.append("%s:1: %s reaches no row in Requirements Traceability" % (path, identifier))

def derive_task_waves(tasks, path, findings):
    """Return the graph level for each task, or an empty map on a cycle."""
    by_id = {task["id"]: task for task in tasks}
    waves = {}
    visiting = set()
    cycle_reported = set()

    def visit(identifier, trail):
        if identifier in waves:
            return waves[identifier]
        if identifier in visiting:
            cycle = tuple(trail[trail.index(identifier):] + [identifier])
            if cycle not in cycle_reported:
                findings.append("%s:1: task dependency cycle: %s" % (path, " -> ".join(cycle)))
                cycle_reported.add(cycle)
            return None
        task = by_id.get(identifier)
        if task is None:
            return None
        visiting.add(identifier)
        dependency_waves = []
        for dependency in task["depends"]:
            result = visit(dependency, trail + [identifier])
            if result is not None:
                dependency_waves.append(result)
        visiting.remove(identifier)
        if any(dependency in visiting for dependency in task["depends"]):
            return None
        if len(dependency_waves) != len(task["depends"]):
            return None
        waves[identifier] = max(dependency_waves, default=0) + 1
        return waves[identifier]

    for task in tasks:
        visit(task["id"], [])
    return waves


def lint_sequence(path, lines, tasks, expected_waves, findings):
    """Validate the Sequence table against the dependency-derived waves."""
    bounds = section_bounds(lines, "Sequence")
    if bounds is None:
        return
    rows = list(table_rows(lines, *bounds))
    if not rows:
        findings.append("%s:1: `Sequence` needs a `Wave` / `Tasks` table" % path)
        return
    _, header, _ = rows[0]
    if "Wave" not in header or "Tasks" not in header:
        findings.append("%s:%d: `Sequence` table must have `Wave` and `Tasks` columns" % (path, rows[0][0]))
        return

    known = {task["id"] for task in tasks}
    listed = {}
    wave_numbers = []
    for number, row_header, cells in rows:
        wave = cell(row_header, cells, "Wave")
        match = WAVE_ID.match(wave)
        if not match:
            findings.append("%s:%d: Sequence row has invalid wave `%s`" % (path, number, wave))
            continue
        wave_number = int(match.group(1))
        wave_numbers.append(wave_number)
        task_refs = TASK_REF.findall(cell(row_header, cells, "Tasks"))
        if not task_refs:
            findings.append("%s:%d: %s lists no tasks" % (path, number, wave))
        for identifier in task_refs:
            if identifier not in known:
                findings.append("%s:%d: %s names unknown task %s" % (path, number, wave, identifier))
            elif identifier in listed:
                findings.append("%s:%d: %s appears more than once in Sequence" % (path, number, identifier))
            else:
                listed[identifier] = wave_number

    if wave_numbers and wave_numbers != list(range(1, max(wave_numbers) + 1)):
        findings.append("%s:1: Sequence waves must start at W-1 and have no gaps" % path)
    for task in tasks:
        identifier = task["id"]
        if identifier not in listed:
            findings.append("%s:1: %s is missing from Sequence" % (path, identifier))
    for identifier, expected in expected_waves.items():
        actual = listed.get(identifier)
        if actual is not None and actual != expected:
            findings.append("%s:1: %s is in W-%d but the dependency graph derives W-%d" %
                            (path, identifier, actual, expected))
    if listed and expected_waves and any(listed.get(identifier) != expected
                                         for identifier, expected in expected_waves.items()):
        canonical = {}
        for identifier, wave in sorted(expected_waves.items(), key=lambda item: (item[1], item[0])):
            canonical.setdefault(wave, []).append(identifier)
        rendered = "; ".join("W-%d: %s" % (wave, ", ".join(identifiers))
                             for wave, identifiers in sorted(canonical.items()))
        findings.append("%s:1: Sequence canonical waves: %s" % (path, rendered))


def check_runner(path, lines, findings):
    """Check the `**Runner:**` line in `## Scope`; return its line number and whether it is `none`."""
    bounds = section_bounds(lines, "Scope")
    if bounds is None:
        return 1, False
    entries = []
    for index in range(*bounds):
        match = TASKS_RUNNER.match(lines[index].strip())
        if match:
            value = re.sub(r"<!--.*?-->", "", match.group(1)).strip().strip("`").strip()
            entries.append((index + 1, value))
    if not entries:
        findings.append("%s:%d: `## Scope` carries no `**Runner:**` line" % (path, bounds[0] + 1))
        return bounds[0] + 1, False
    if len(entries) > 1:
        findings.append("%s:%d: `## Scope` carries more than one `**Runner:**` line" % (path, entries[1][0]))
    number, value = entries[0]
    if not value:
        findings.append("%s:%d: `Runner` must name the test command or `none — [why the project has none]`" %
                        (path, number))
        return number, False
    marker = TASK_TEST_NONE.match(value)
    if marker is not None and not marker.group(1).strip():
        findings.append("%s:%d: `Runner: none` must name why the project has no test runner" % (path, number))
    return number, marker is not None


def lint_tasks(path, lines, base, spec_lines, findings, warnings):
    fields, _ = parse_frontmatter(lines)
    check_frontmatter_status(path, fields, TASK_STATUSES, findings)
    check_frontmatter_path(path, base, fields, "spec", findings)
    check_frontmatter_path(path, base, fields, "design", findings)
    design_components = read_design_components(base, fields.get("design"), findings)
    check_sections(path, lines, TASKS_SECTIONS, findings)
    runner_line, runner_none = check_runner(path, lines, findings)
    unreached_total = 0
    tasks = []
    current = None
    for index, line in enumerate(lines):
        match = TASK_HEADING.match(line)
        if match:
            current = {"id": match.group(2), "line": index + 1, "slice": "", "depends": [], "block": [],
                       "state": match.group(1), "title": match.group(3).strip(), "builds": []}
            tasks.append(current)
        elif current is not None and line.startswith("### "):
            current = None
        elif current is not None:
            current["block"].append(line)

    declared = set()
    covered = {}
    highest = 0
    for task in tasks:
        identifier, number, block = task["id"], task["line"], task["block"]
        value = int(identifier.split("-")[1])
        if identifier in declared:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        elif value < highest:
            findings.append("%s:%d: %s breaks the monotonic sequence" % (path, number, identifier))
        declared.add(identifier)
        highest = max(highest, value)
        removed_title = REMOVED_TITLE.match(task["title"])
        if task["state"] == "-":
            if not removed_title:
                findings.append("%s:%d: %s is marked `[-]` but its title is not `~~title~~ removed`"
                                % (path, number, identifier))
            if not any(REASON_LINE.match(line.strip()) for line in block):
                findings.append("%s:%d: %s is removed but carries no `Reason:` line" % (path, number, identifier))
            continue
        if removed_title:
            findings.append("%s:%d: %s has a removed title but is not marked `[-]`" % (path, number, identifier))
        body = "\n".join(block)
        for field in TASK_FIELDS:
            if "**%s:**" % field not in body:
                findings.append("%s:%d: %s carries no `**%s:**`" % (path, number, identifier, field))
        builds_values = [match.group(1).strip() for line in block
                         for match in [TASK_BUILDS.match(line)] if match]
        if len(builds_values) != 1 or not builds_values[0]:
            findings.append("%s:%d: %s must carry one non-empty `Builds` field" %
                            (path, number, identifier))
        builds_value = builds_values[0] if builds_values else ""
        task["builds"] = split_field_list(builds_value)
        task["builds_none"] = builds_value.lower() == "none"
        if not task["builds_none"]:
            if any(not component.strip() for component in builds_value.split(",")):
                findings.append("%s:%d: %s `Builds` contains an empty component name" %
                                (path, number, identifier))
            normalized_builds = [component.lower() for component in task["builds"]]
            if "none" in normalized_builds:
                findings.append("%s:%d: %s `Builds` cannot combine `none` with component names" %
                                (path, number, identifier))
            duplicate_components = sorted({component for component in task["builds"]
                                           if task["builds"].count(component) > 1})
            if duplicate_components:
                findings.append("%s:%d: %s `Builds` repeats component(s): %s" %
                                (path, number, identifier, ", ".join(duplicate_components)))
        if design_components is not None and not task["builds_none"]:
            unknown_components = [component for component in task["builds"]
                                  if component not in design_components]
            if unknown_components:
                findings.append("%s:%d: %s `Builds` names unknown design component(s): %s" %
                                (path, number, identifier, ", ".join(unknown_components)))

        slice_values = [match.group(1).strip() for line in block
                        for match in [TASK_SLICE.match(line)] if match]
        if len(slice_values) != 1 or not slice_values[0]:
            findings.append("%s:%d: %s must carry one non-empty `Slice` field" %
                            (path, number, identifier))
        else:
            slice_refs = SLICE_REF.findall(slice_values[0])
            if slice_values[0].lower() == "none":
                task["slice"] = "none"
            elif len(slice_refs) == 1:
                task["slice"] = slice_refs[0]
            else:
                findings.append("%s:%d: %s `Slice` must name one `S-N` or `none`" %
                                (path, number, identifier))
        if task["builds_none"] and task["slice"] != "none":
            findings.append("%s:%d: %s may use `Builds: none` only for groundwork (`Slice: none`)" %
                            (path, number, identifier))
        depends_values = [match.group(1).strip() for line in block
                          for match in [TASK_DEPENDS.match(line)] if match]
        if len(depends_values) != 1 or not depends_values[0]:
            findings.append("%s:%d: %s must carry one non-empty `Depends on` field" %
                            (path, number, identifier))
        elif depends_values[0].lower() != "none":
            task["depends"] = TASK_REF.findall(depends_values[0])
            if "none" in depends_values[0].lower() or not task["depends"]:
                findings.append("%s:%d: %s `Depends on` must name tasks or `none`" %
                                (path, number, identifier))
        covers_values = [match.group(1).strip() for line in block
                         for match in [TASK_COVERS.match(line)] if match]
        test_values = [match.group(1).strip() for line in block
                       for match in [TASK_TEST.match(line)] if match]
        covers = [reference for value in covers_values for reference in AC_PATTERN.findall(value)]
        if covers_values and not covers:
            findings.append("%s:%d: %s `Covers` must name at least one `AC-N.M`" %
                            (path, number, identifier))
        if len(covers) != len(set(covers)):
            findings.append("%s:%d: %s `Covers` names the same criterion more than once" %
                            (path, number, identifier))
        for criterion in covers:
            if task["slice"] and task["slice"] != "none" and \
                    "S-%s" % criterion[len("AC-"):].split(".")[0] != task["slice"]:
                findings.append("%s:%d: %s covers %s, which sits under another slice than %s" %
                                (path, number, identifier, criterion, task["slice"]))
            if spec_lines is not None and criterion not in spec_ac_ids(spec_lines):
                findings.append("%s:%d: %s `Covers` names %s, which the spec does not declare" %
                                (path, number, identifier, criterion))
            elif criterion in covered and covered[criterion] != identifier:
                findings.append("%s:%d: %s and %s both cover %s; each AC needs exactly one task" %
                                (path, number, covered[criterion], identifier, criterion))
            else:
                covered[criterion] = identifier
        if covers and runner_none:
            if test_values:
                findings.append("%s:%d: %s carries `Test` under `Runner: none`; drop it" %
                                (path, number, identifier))
            unreached_total += len(covers)
        elif covers:
            named_tests = [value for value in test_values if value]
            if len(named_tests) != len(covers):
                findings.append("%s:%d: each covered AC needs its own `Test`: %s covers %d, "
                                "with %d non-empty `Test`" %
                                (path, number, identifier, len(covers), len(named_tests)))
            unreached = 0
            for value in named_tests:
                marker = TASK_TEST_NONE.match(value)
                if marker is not None and not marker.group(1).strip():
                    findings.append("%s:%d: %s `Test: none` must name what the runner does not reach" %
                                    (path, number, identifier))
                elif marker is not None:
                    unreached += 1
            if unreached and spec_lines is not None and not spec_user_facing(spec_lines):
                warnings.append("%s:%d: warning: %s has no runner-level test for %d covered %s on a feature that is not user-facing; route to specify" %
                                (path, number, identifier, unreached,
                                 "criterion" if unreached == 1 else "criteria"))

    if unreached_total and spec_lines is not None and not spec_user_facing(spec_lines):
        warnings.append("%s:%d: warning: `Runner: none` leaves %d covered %s without a runner-level test on a feature that is not user-facing; route to specify" %
                        (path, runner_line, unreached_total,
                         "criterion" if unreached_total == 1 else "criteria"))

    removed_ids = {task["id"] for task in tasks if task["state"] == "-"}
    started = any(task["state"] == "x" for task in tasks)
    if not started:
        for task in tasks:
            if task["state"] == "-":
                warnings.append("%s:%d: warning: %s is removed before any task is done — renumber instead"
                                % (path, task["line"], task["id"]))
        numbers = [int(task["id"].split("-")[1]) for task in tasks if task["state"] != "-"]
        if numbers != list(range(1, len(numbers) + 1)):
            warnings.append("%s:1: warning: tasks are not numbered T-1 onward without gaps — renumber before any task is done"
                            % path)
    live_tasks = [task for task in tasks if task["state"] != "-"]

    slices = spec_live_stories(spec_lines or [])
    slice_task_ids = {task["id"] for task in live_tasks if task["slice"] and task["slice"] != "none"}
    slice_order = []
    declared_before = set()
    slice_task_seen = False
    for task in tasks:
        identifier, number = task["id"], task["line"]
        if task["state"] == "-":
            declared_before.add(identifier)
            continue
        if task["slice"] == "none":
            if slice_task_seen and not any(dependency in slice_task_ids for dependency in task["depends"]):
                findings.append("%s:%d: %s is groundwork listed after a slice task it does not depend on — move it before the slice tasks" %
                                (path, number, identifier))
        elif task["slice"]:
            slice_task_seen = True
            slice_order.append(task["slice"])
            if spec_lines is not None and task["slice"] not in slices:
                findings.append("%s:%d: %s names %s, which the spec does not declare" %
                                (path, number, identifier, task["slice"]))
        elif spec_lines is not None:
            findings.append("%s:%d: %s names no slice" % (path, number, identifier))
        for dependency in task["depends"]:
            if dependency in removed_ids:
                findings.append("%s:%d: %s depends on %s, which was removed" %
                                (path, number, identifier, dependency))
                continue
            if dependency not in declared_before:
                if dependency in declared:
                    warnings.append("%s:%d: warning: %s depends on %s, which is declared later" %
                                    (path, number, identifier, dependency))
                else:
                    findings.append("%s:%d: %s depends on %s, which is not declared" %
                                    (path, number, identifier, dependency))
            if dependency == identifier:
                findings.append("%s:%d: %s cannot depend on itself" % (path, number, identifier))
        declared_before.add(identifier)

    seen_slices = []
    for slice_id in slice_order:
        if slice_id in seen_slices and seen_slices[-1] != slice_id:
            findings.append("%s:1: %s's tasks are not contiguous" % (path, slice_id))
        if not seen_slices or seen_slices[-1] != slice_id:
            seen_slices.append(slice_id)

    expected_waves = derive_task_waves(live_tasks, path, findings)
    lint_sequence(path, lines, live_tasks, expected_waves, findings)

    if design_components:
        built_components = {component for task in live_tasks for component in task["builds"]}
        for component in design_components:
            if component not in built_components:
                warnings.append("%s:1: warning: component `%s` from the design reaches no task `Builds` field" %
                                (path, component))

    if spec_lines is None:
        return
    live = spec_ac_ids(spec_lines)
    for identifier in sorted(set(live), key=ac_sort_key):
        if identifier not in covered:
            findings.append("%s:1: %s reaches no task `Covers` field" % (path, identifier))


def summary_fields(lines):
    """Return the `- **Name:** value` pairs of a report's `## Summary` section."""
    bounds = section_bounds(lines, "Summary")
    if bounds is None:
        return {}
    values = {}
    for index in range(*bounds):
        match = re.match(r"^- \*\*([^:*]+):\*\*\s*(.*)$", lines[index])
        if match:
            values[match.group(1).strip()] = match.group(2).strip()
    return values


def check_report_summary(path, lines, expected, findings):
    """Check a report's Summary block: every field present, `Status` in vocabulary."""
    values = summary_fields(lines)
    if not values:
        findings.append("%s:1: `## Summary` carries no `- **Field:**` lines" % path)
        return
    for field in expected:
        if field not in values:
            findings.append("%s:1: `## Summary` is missing `- **%s:**`" % (path, field))
    status = values.get("Status", "")
    if status and status not in REPORT_STATUSES:
        findings.append("%s:1: `Status` is `%s`, not one of %s"
                        % (path, status, "/".join(REPORT_STATUSES)))


def check_report_coverage(path, section_ids, spec_lines, findings, extra=None):
    """Check a report's criteria against the spec: every AC once, and no unknown id."""
    if spec_lines is None:
        return
    live = spec_ac_ids(spec_lines)
    seen = {}
    for identifier, number, origin in section_ids + (extra or []):
        if identifier not in live:
            findings.append("%s:%d: %s names %s, which the spec does not declare"
                            % (path, number, origin, identifier))
        elif identifier in seen:
            findings.append("%s:%d: %s appears twice in the report, first at line %d"
                            % (path, number, identifier, seen[identifier]))
        else:
            seen[identifier] = number
    for identifier in sorted(set(live), key=ac_sort_key):
        if identifier not in seen:
            findings.append("%s:1: %s reaches no row of the report" % (path, identifier))


def report_criteria_rows(lines, title, column):
    """Yield (ac_id, line, title) for each row of a report table keyed by `AC`."""
    bounds = section_bounds(lines, title)
    if bounds is None:
        return []
    rows = []
    for number, header, cells in table_rows(lines, *bounds):
        for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
            rows.append((match.group(0), number, title))
            break
    return rows


def check_report_verdicts(path, lines, title, column, allowed, findings):
    """Check the verdict column of a report's criteria table against its vocabulary."""
    bounds = section_bounds(lines, title)
    if bounds is None:
        return
    for number, header, cells in table_rows(lines, *bounds):
        if column not in header:
            findings.append("%s:%d: `## %s` table has no `%s` column" % (path, number, title, column))
            return
        value = cell(header, cells, column)
        if value not in allowed:
            findings.append("%s:%d: verdict `%s` is not one of %s"
                            % (path, number, value, "/".join(allowed)))


def lint_validate(path, lines, spec_lines, findings):
    """Check the validate report: sections, summary, per-criterion verdicts, coverage."""
    check_sections(path, lines, VALIDATE_SECTIONS, findings)
    check_report_summary(path, lines, VALIDATE_SUMMARY, findings)
    check_report_verdicts(path, lines, "Criteria", "Verdict", VALIDATE_VERDICTS, findings)
    check_report_coverage(path, report_criteria_rows(lines, "Criteria", "AC"), spec_lines, findings,
                          report_criteria_rows(lines, "Out of Scope", "AC"))


def lint_audit(path, lines, spec_lines, findings):
    """Check the audit report: sections, summary, per-criterion status, coverage."""
    check_sections(path, lines, AUDIT_SECTIONS, findings)
    check_report_summary(path, lines, AUDIT_SUMMARY, findings)
    check_report_verdicts(path, lines, "Acceptance Criteria", "Status", AUDIT_AC_STATUSES, findings)
    check_report_coverage(path, report_criteria_rows(lines, "Acceptance Criteria", "AC"), spec_lines, findings)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lint a spec-driven artifact against its template contract.")
    parser.add_argument("phase", choices=["spec", "design", "tasks", "validate", "audit"])
    parser.add_argument("feature_dir", help="the feature folder, e.g. .artifacts/specs/{slug}")
    args = parser.parse_args(argv)

    base = args.feature_dir
    filename = "%s.md" % args.phase
    path = os.path.join(base, filename)
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
    warnings = []
    try:
        if args.phase == "spec":
            lint_spec(path, lines, base, findings, warnings)
        elif args.phase == "design":
            lint_design(path, lines, base, spec_path, spec_lines, findings)
        elif args.phase == "validate":
            lint_validate(path, lines, spec_lines, findings)
        elif args.phase == "audit":
            lint_audit(path, lines, spec_lines, findings)
        else:
            lint_tasks(path, lines, base, spec_lines, findings, warnings)
    except Exception as error:  # last-resort guard: never surface a raw traceback
        sys.stderr.write("error: %s\n" % error)
        return 4

    for finding in findings:
        print(finding)
    for warning in warnings:
        print(warning)
    if findings:
        return 1
    if not warnings:
        print("%s: clean" % path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
