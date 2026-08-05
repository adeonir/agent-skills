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

SPEC_SECTIONS = ["Overview", "Goals", "Non-Goals", "User Stories", "Edge Cases", "Open Questions",
                 "Divergences"]
DESIGN_SECTIONS = ["Scope", "Architecture Overview", "Components", "Decisions",
                   "Error Handling", "Risks & Concerns", "Requirements Traceability"]
TASKS_SECTIONS = ["Scope", "Task List", "Coverage Matrix"]

SPEC_FRONTMATTER = ["name", "scope", "sources", "user-facing", "status", "created", "branch"]
SCOPES = ["medium", "large", "complex"]
STATUSES = ["draft", "ready", "in-progress", "done"]

# Gherkin keywords that open a step group, and the ones that continue the open group.
STEP_OPENERS = ("Given", "When", "Then")
STEP_CONTINUATIONS = ("And", "But")

TASK_FIELDS = ["Story", "Gate", "Done when"]

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
DIVERGENCE_ID = re.compile(r"^DV-\d+$")
DIVERGENCE_STATUSES = ["open", "accepted"]
DIVERGENCE_DIRECTIONS = ["Added", "Dropped", "Loosened"]
GOAL_ID = re.compile(r"^G-\d+$")
STEP_KEYWORD = re.compile(r"^(Given|When|Then|And|But)\s+\S")
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
    """Return the `AC-N.M` ids the spec declares, in document order."""
    return [match.group(1) for line in spec_lines
            for match in [AC_DEFINITION.match(line)] if match]


def ac_sort_key(identifier):
    """Order ids numerically, so AC-1.10 follows AC-1.2 instead of preceding it."""
    story, position = identifier[len("AC-"):].split(".")
    return int(story), int(position)


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
                       "block": [], "serves": [], "satisfies": [], "fenced": False}
            criteria.append(current)
            continue
        match = STORY_HEADING.match(line)
        if match:
            story = match.group(1)
            current = None
            continue
        if line.startswith("## "):
            story = None
            current = None
            continue
        if current is None:
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
    for step in block[1:]:
        if step.startswith("Examples:") or step.startswith("|"):
            continue  # the Examples table binds placeholders; it carries no step keyword
        match = STEP_KEYWORD.match(step)
        if not match:
            findings.append("%s:%d: %s has a line that is not a Gherkin step: `%s`"
                            % (path, number, identifier, step))
            continue
        keyword = match.group(1)
        if keyword in STEP_CONTINUATIONS:
            continue
        if keyword == "When" and not seen["Given"]:
            findings.append("%s:%d: %s puts `When` before any `Given`" % (path, number, identifier))
        if keyword == "Then" and not seen["When"]:
            findings.append("%s:%d: %s puts `Then` before any `When`" % (path, number, identifier))
        seen[keyword] = True

    for keyword in STEP_OPENERS:
        if not seen[keyword]:
            findings.append("%s:%d: %s has no `%s` step" % (path, number, identifier, keyword))

    if outline and not any(step.startswith("Examples:") for step in block):
        findings.append("%s:%d: %s is a `Scenario Outline` with no `Examples` table"
                        % (path, number, identifier))


def check_criteria(path, lines, findings):
    """Check every criterion's form, identity, and upward links."""
    goals = spec_goal_ids(lines)
    seen_goals = set()
    for identifier in goals:
        if identifier in seen_goals:
            findings.append("%s:1: %s is declared more than once in `## Goals`" % (path, identifier))
        seen_goals.add(identifier)

    declared = set()
    highest = {}  # story id -> the highest M seen under it
    for criterion in spec_criteria(lines):
        identifier, number, story = criterion["id"], criterion["line"], criterion["story"]
        if identifier in declared:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        declared.add(identifier)

        story_number, position = identifier[len("AC-"):].split(".")
        if story is None:
            findings.append("%s:%d: %s sits under no story" % (path, number, identifier))
        elif story != "S-%s" % story_number:
            findings.append("%s:%d: %s sits under %s — the criterion number names story %s"
                            % (path, number, identifier, story, story_number))
        elif int(position) <= highest.get(story, 0):
            findings.append("%s:%d: %s does not ascend within %s" % (path, number, identifier, story))
        if story is not None:
            highest[story] = max(highest.get(story, 0), int(position))

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

        if len(criterion["satisfies"]) > 1:
            findings.append("%s:%d: %s carries %d `Satisfies` lines, expected one"
                            % (path, number, identifier, len(criterion["satisfies"])))
        for value in criterion["satisfies"]:
            if not SATISFIES_ID.match(value):
                findings.append("%s:%d: %s `Satisfies %s` is not exactly one `FR/BR/EC/NFR-N` id"
                                % (path, number, identifier, value))


def check_downstream_ac_refs(base, live, findings):
    """Report a downstream table row citing a criterion the spec no longer declares.

    A specify re-entry may renumber while the spec is `draft`, and `design.md` and
    `tasks.md` are read by their own phases only — without this, a row left behind
    reaches no reader until the audit.
    """
    for name, section in (("design.md", "Requirements Traceability"),
                          ("tasks.md", "Coverage Matrix")):
        target = os.path.join(base, name)
        if not os.path.isfile(target):
            continue
        lines = read_lines(target)
        if lines is None:
            continue
        bounds = section_bounds(lines, section)
        if bounds is None:
            continue
        for number, header, cells in table_rows(lines, *bounds):
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                if match.group(0) not in live:
                    findings.append("%s:%d: %s names %s, which the spec no longer declares"
                                    % (target, number, section, match.group(0)))


def check_divergences(path, lines, prompt_seeded, findings):
    """Check the `## Divergences` table: identity, status, direction, and the AC it names."""
    bounds = section_bounds(lines, "Divergences")
    if bounds is None:
        return  # check_sections already reports the missing section
    live = set(spec_ac_ids(lines))
    declared = set()
    rows = 0
    for number, header, cells in table_rows(lines, *bounds):
        rows += 1
        identifier = cell(header, cells, "ID")
        if not DIVERGENCE_ID.match(identifier):
            findings.append("%s:%d: `%s` is not a well-formed `DV-N` id" % (path, number, identifier))
        elif identifier in declared:
            findings.append("%s:%d: %s is declared more than once" % (path, number, identifier))
        declared.add(identifier)

        status = cell(header, cells, "Status")
        if status not in DIVERGENCE_STATUSES:
            findings.append("%s:%d: %s carries status `%s`, not one of %s"
                            % (path, number, identifier, status, "/".join(DIVERGENCE_STATUSES)))

        divergence = cell(header, cells, "Divergence")
        direction = divergence.split(":", 1)[0].strip()
        if direction not in DIVERGENCE_DIRECTIONS:
            findings.append("%s:%d: %s opens with `%s`, not one of %s"
                            % (path, number, identifier, direction, "/".join(DIVERGENCE_DIRECTIONS)))
            continue

        named = cell(header, cells, "AC").strip("— -")
        if direction == "Dropped":
            if named:
                findings.append("%s:%d: %s is `Dropped` and names %s — no criterion carries a dropped obligation"
                                % (path, number, identifier, named))
        elif not named:
            findings.append("%s:%d: %s is `%s` and names no criterion" % (path, number, identifier, direction))
        elif named not in live:
            findings.append("%s:%d: %s names %s, which the spec does not declare" % (path, number, identifier, named))

    if prompt_seeded and rows:
        findings.append("%s:1: Divergences carries %d row(s) on a prompt-seeded spec (`sources: []`)"
                        % (path, rows))


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

    check_criteria(path, lines, findings)

    prompt_seeded = fields.get("sources", "").strip() in ("[]", "")
    check_divergences(path, lines, prompt_seeded, findings)
    check_downstream_ac_refs(base, set(spec_ac_ids(lines)), findings)

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
    live = spec_ac_ids(spec_lines)
    traced = set()
    bounds = section_bounds(lines, "Requirements Traceability")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                identifier = match.group(0)
                traced.add(identifier)
                if identifier not in live:
                    findings.append("%s:%d: traceability names %s, which the spec does not declare" % (path, number, identifier))
    for identifier in sorted(set(live), key=ac_sort_key):
        if identifier not in traced:
            findings.append("%s:1: %s reaches no row in Requirements Traceability" % (path, identifier))

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
    live = spec_ac_ids(spec_lines)
    covered = set()
    bounds = section_bounds(lines, "Coverage Matrix")
    if bounds:
        for number, header, cells in table_rows(lines, *bounds):
            for match in AC_PATTERN.finditer(cell(header, cells, "AC") or " ".join(cells)):
                identifier = match.group(0)
                covered.add(identifier)
                if identifier not in live:
                    findings.append("%s:%d: Coverage Matrix names %s, which the spec does not declare" % (path, number, identifier))
            for reference in TASK_REF.findall(cell(header, cells, "Task")):
                if reference not in declared:
                    findings.append("%s:%d: Coverage Matrix names %s, which the Task List does not declare" % (path, number, reference))
    for identifier in sorted(set(live), key=ac_sort_key):
        if identifier not in covered:
            findings.append("%s:1: %s reaches no row in the Coverage Matrix" % (path, identifier))


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
