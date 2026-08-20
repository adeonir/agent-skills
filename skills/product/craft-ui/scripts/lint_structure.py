#!/usr/bin/env python3
"""
Structure linter for the craft-ui skill.

Checks `structure.yaml` — the optional arrangement handoff the wireframe phase
writes and the mockup phase reads — for the defects a reading pass cannot
settle by eye: a shape outside the fixed vocabulary, a register outside its
two values, a flow edge pointing at a surface that does not exist, a surface
no flow path reaches, and a requirement ID the template forbids.

Everything perceptual stays with the structural self-check: whether the
arrangement matches its register, whether the primary action is obvious,
whether states and reflow are planned. This script settles form only.

Usage:
    python3 lint_structure.py [path]

`path` defaults to `.artifacts/design/structure.yaml`.

Exit codes:
    0  no error (warnings may still be printed)
    1  at least one error
    2  the file is missing or cannot be parsed
"""

import re
import sys

# PyYAML parses every valid document; the block-style reader below covers the
# template's own shape when PyYAML is not installed, so the linter never needs
# a dependency to run.
try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_PATH = ".artifacts/design/structure.yaml"

REGISTERS = ("brand", "product")

NAMED_SHAPES = ("full-width", "split", "stack", "sidebar", "modal", "overlay")

# grid-N names the column count, so a grid needs at least two columns; grid-1
# is a stack under another name and hides a shape that was never chosen.
GRID_SHAPE = re.compile(r"^grid-([2-9]|[1-9][0-9]+)$")

# Requirement IDs the structure template forbids: the upstream prefixes plus
# the bare m1 / j1 forms a PRD carries.
REQUIREMENT_ID = re.compile(r"\b(?:fr|br|ec|nfr|us|m|j)-?[0-9]+\b", re.IGNORECASE)


class ParseError(Exception):
    """The document is outside the block style the template defines."""


def strip_comment(line):
    """Drop a trailing `#` comment, leaving one inside a quoted scalar alone."""
    kept = []
    quote = None
    for index, char in enumerate(line):
        if quote:
            kept.append(char)
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            kept.append(char)
        elif char == "#" and (index == 0 or line[index - 1] in " \t"):
            break
        else:
            kept.append(char)
    return "".join(kept).rstrip()


def unquote(raw):
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    return raw


def parse_block_yaml(text):
    """Read the block-style subset the structure template uses.

    Mappings, sequences of mappings, sequences of scalars, and quoted or bare
    scalars. Flow style, anchors, and block scalars raise ParseError with the
    line that carries them.
    """
    lines = []
    for number, raw in enumerate(text.splitlines(), start=1):
        leading = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in leading:
            raise ParseError("line %d: tab in the indentation; use spaces" % number)
        body = strip_comment(raw)
        if not body.strip():
            continue
        lines.append((len(body) - len(body.lstrip(" ")), body.strip(), number))

    if not lines:
        return {}

    cursor = [0]

    def reject_unsupported(value, number):
        if value[:1] in "{[":
            raise ParseError(
                "line %d: flow style is not supported; write the value as an indented block" % number
            )
        if value in ("|", ">") or value[:1] in "&*":
            raise ParseError(
                "line %d: block scalars and anchors are not supported; write a plain value" % number
            )

    def parse_node():
        _, content, _ = lines[cursor[0]]
        indent = lines[cursor[0]][0]
        if content.startswith("- "):
            return parse_sequence(indent)
        return parse_mapping(indent)

    def parse_mapping(indent):
        result = {}
        while cursor[0] < len(lines):
            current_indent, content, number = lines[cursor[0]]
            if current_indent < indent or content.startswith("- "):
                break
            if current_indent > indent:
                raise ParseError("line %d: unexpected indentation" % number)
            if ":" not in content:
                raise ParseError("line %d: expected 'key:' or 'key: value'" % number)
            key, _, rest = content.partition(":")
            rest = rest.strip()
            cursor[0] += 1
            if rest:
                reject_unsupported(rest, number)
                result[unquote(key)] = unquote(rest)
            elif cursor[0] < len(lines) and lines[cursor[0]][0] > indent:
                result[unquote(key)] = parse_node()
            else:
                result[unquote(key)] = {}
        return result

    def parse_sequence(indent):
        items = []
        # The "- " marker takes two columns, so a mapping item's keys continue
        # at indent + 2 in the block style the template writes.
        key_indent = indent + 2
        while cursor[0] < len(lines):
            current_indent, content, number = lines[cursor[0]]
            if current_indent != indent or not content.startswith("- "):
                break
            rest = content[2:].strip()
            reject_unsupported(rest, number)
            if rest[:1] in "\"'" or ":" not in rest:
                items.append(unquote(rest))
                cursor[0] += 1
                continue
            # Re-seat the first key as a line at key_indent so parse_mapping
            # consumes it together with the item's remaining keys.
            lines[cursor[0]] = (key_indent, rest, number)
            items.append(parse_mapping(key_indent))
        return items

    document = parse_node()
    if cursor[0] < len(lines):
        raise ParseError("line %d: content outside the document's top level" % lines[cursor[0]][2])
    return document


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as error:
        return None, "cannot read %s: %s" % (path, error)

    if yaml is not None:
        try:
            document = yaml.safe_load(text)
        except yaml.YAMLError as error:
            return None, "%s is not valid YAML: %s" % (path, error)
    else:
        try:
            document = parse_block_yaml(text)
        except ParseError as error:
            return None, "%s: %s" % (path, error)

    if document is None:
        return None, "%s is empty" % path
    if not isinstance(document, dict):
        return None, "%s must be a mapping with a `surfaces:` key" % path
    return document, None


def walk_blocks(blocks, trail):
    """Yield (path, block) for every block, descending into `children`."""
    if not isinstance(blocks, list):
        return
    for index, block in enumerate(blocks):
        path = "%s[%d]" % (trail, index)
        yield path, block
        if isinstance(block, dict):
            for nested in walk_blocks(block.get("children"), path + ".children"):
                yield nested


def check_surfaces(document, findings):
    surfaces = document.get("surfaces")
    if not isinstance(surfaces, dict) or not surfaces:
        findings.append(("ERROR", "surfaces", "missing or empty; the contract needs at least one surface"))
        return {}

    for name, surface in surfaces.items():
        trail = "surfaces.%s" % name
        if not isinstance(surface, dict):
            findings.append(("ERROR", trail, "must be a mapping with `register:` and `blocks:`"))
            continue

        register = surface.get("register")
        if register not in REGISTERS:
            findings.append((
                "ERROR",
                trail + ".register",
                "%r is not a register; use one of %s" % (register, ", ".join(REGISTERS)),
            ))

        blocks = surface.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            findings.append(("ERROR", trail + ".blocks", "missing or empty; a surface is an ordered list of blocks"))
            continue

        for path, block in walk_blocks(blocks, trail + ".blocks"):
            if not isinstance(block, dict):
                findings.append(("ERROR", path, "must be a mapping with `block:` and `shape:`"))
                continue
            if not block.get("block"):
                findings.append(("ERROR", path + ".block", "missing; every block carries a label"))
            shape = block.get("shape")
            if not shape:
                findings.append(("ERROR", path + ".shape", "missing; every block carries a shape"))
            elif shape not in NAMED_SHAPES and not GRID_SHAPE.match(str(shape)):
                findings.append((
                    "ERROR",
                    path + ".shape",
                    "%r is not in the shape vocabulary; use %s, or grid-N with N of 2 or more"
                    % (shape, ", ".join(NAMED_SHAPES)),
                ))

    return surfaces


def check_flow(document, surfaces, findings):
    flow = document.get("flow")
    # A single-surface contract has nowhere to travel, so `flow:` only carries
    # a claim worth checking once a second surface exists.
    multi_surface = len(surfaces) > 1

    if flow in (None, {}, []):
        if multi_surface:
            findings.append(("WARN", "flow", "%d surfaces and no path between them" % len(surfaces)))
        return
    if not isinstance(flow, list):
        findings.append(("ERROR", "flow", "must be a list of `source -> target` paths"))
        return

    connected = set()
    for index, edge in enumerate(flow):
        path = "flow[%d]" % index
        if not isinstance(edge, str) or "->" not in edge:
            findings.append(("ERROR", path, "%r is not a `source -> target` path" % edge))
            continue
        source, _, target = edge.partition("->")
        source, target = source.strip(), target.strip()
        for role, name in (("source", source), ("target", target)):
            if name not in surfaces:
                findings.append(("ERROR", path, "%s %r is not a surface in this contract" % (role, name)))
        connected.update((source, target))

    # An entry surface is a source and never a target, so a surface counts as
    # connected from either end; one that appears on neither end is dangling.
    if not multi_surface:
        return
    for name in surfaces:
        if name not in connected:
            findings.append(("WARN", "surfaces.%s" % name, "no flow path connects this surface"))


def check_forbidden_ids(document, surfaces, findings):
    for name, surface in surfaces.items():
        if not isinstance(surface, dict):
            continue
        for path, block in walk_blocks(surface.get("blocks"), "surfaces.%s.blocks" % name):
            if not isinstance(block, dict):
                continue
            for field in ("block", "note"):
                value = block.get(field)
                if not isinstance(value, str):
                    continue
                found = REQUIREMENT_ID.search(value)
                if found:
                    findings.append((
                        "ERROR",
                        "%s.%s" % (path, field),
                        "carries the requirement ID %r; the plan holds structure only" % found.group(0),
                    ))


def main(argv):
    path = argv[1] if len(argv) > 1 else DEFAULT_PATH

    document, failure = load(path)
    if failure:
        print("ERROR %s" % failure)
        return 2

    findings = []
    surfaces = check_surfaces(document, findings)
    if surfaces:
        check_flow(document, surfaces, findings)
        check_forbidden_ids(document, surfaces, findings)

    for level, location, message in findings:
        print("%-5s %s: %s" % (level, location, message))

    errors = sum(1 for level, _, _ in findings if level == "ERROR")
    warnings = len(findings) - errors
    if not findings:
        print("clean: %s" % path)
    else:
        print("%d error(s), %d warning(s) in %s" % (errors, warnings, path))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
