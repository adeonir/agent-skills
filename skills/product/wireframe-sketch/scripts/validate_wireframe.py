#!/usr/bin/env python3
"""validate_wireframe.py — deterministic structural gate for WIREFRAME.md.

Execute this script; never read it as reference.

Checks only what is mechanically decidable about the region tree — schema
well-formedness, screen-flow connectivity, and whether the committed
`wireframe.html` still matches its source. Usability judgement (the Nielsen
checklist) stays with the model in validate.md; this script never opines on it.

Usage:
    python3 validate_wireframe.py <path-to-WIREFRAME.md>

Reuses the parser and renderer from render_wireframe.py so the drift check
compares against the exact bytes a re-render would produce.

Exit codes: 0 = no errors (warnings/info allowed), 1 = at least one error,
2 = usage / IO / parse error.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_wireframe as rw  # noqa: E402  (path set above so the sibling resolves)

ERROR, WARN, INFO = "ERROR", "WARN", "INFO"


def valid_shape(shape):
    return shape in rw.SHAPES or rw.GRID.match(shape) is not None


def check_schema(surfaces, findings):
    if not surfaces:
        findings.append((ERROR, "region tree has no surfaces"))
        return

    def walk(blocks, surface_name):
        for block in blocks:
            if not isinstance(block, dict):
                continue
            label = block.get("block") or "(unnamed block)"
            shape = rw.shape_of(block)
            if not shape:
                findings.append((ERROR, f"{surface_name}: block '{label}' has no shape"))
            elif not valid_shape(shape):
                findings.append(
                    (ERROR, f"{surface_name}: block '{label}' has shape '{shape}' "
                            "outside the fixed vocabulary "
                            "(full-width | split | grid-N | stack | sidebar | modal | overlay)")
                )
            children = block.get("children")
            if isinstance(children, list):
                walk(children, surface_name)

    for name, surface in surfaces.items():
        blocks = rw.blocks_of(surface)
        if not blocks:
            findings.append((WARN, f"{name}: surface has no blocks"))
        walk(blocks, name)


def parse_flow_edges(flow):
    # Each `flow:` entry may chain multiple hops ("a -> b -> c"); expand to edges.
    edges = []
    for step in flow:
        ends = [end.strip() for end in re.split(r"\s*-+>\s*", step) if end.strip()]
        for src, dst in zip(ends, ends[1:]):
            edges.append((src, dst))
    return edges


def check_flow(surfaces, flow, findings):
    if not flow:
        return  # a single-surface page needs no flow; absence is not a defect
    names = set(surfaces.keys())
    edges = parse_flow_edges(flow)
    referenced = set()
    for src, dst in edges:
        referenced.update((src, dst))
        for endpoint in (src, dst):
            if endpoint not in names:
                findings.append(
                    (WARN, f"flow references '{endpoint}', which is not a defined surface")
                )
    for name in names:
        if name not in referenced:
            findings.append(
                (INFO, f"surface '{name}' never appears in the flow — disconnected?")
            )


def check_drift(path, surfaces, findings):
    out_path = os.path.join(os.path.dirname(os.path.abspath(path)), "wireframe.html")
    if not os.path.exists(out_path):
        findings.append((INFO, "no wireframe.html yet — run render_wireframe.py to create it"))
        return
    try:
        with open(out_path, "r", encoding="utf8") as handle:
            committed = handle.read()
    except OSError:
        findings.append((WARN, f"cannot read {out_path} to check for drift"))
        return
    fresh = rw.render_html(surfaces)
    if committed != fresh:
        findings.append(
            (ERROR, "wireframe.html is stale — it no longer matches WIREFRAME.md; "
                    "re-run render_wireframe.py")
        )


def main(argv):
    args = argv[1:]
    if not args or args[0].startswith("--"):
        print("Usage: validate_wireframe.py <path-to-WIREFRAME.md>", file=sys.stderr)
        return 2
    path = args[0]
    parsed = rw.load(path)
    if parsed is None:
        return 2  # load already explained the IO/parse failure
    surfaces, flow = parsed

    findings = []
    check_schema(surfaces, findings)
    check_flow(surfaces, flow, findings)
    check_drift(path, surfaces, findings)

    errors = sum(1 for status, _ in findings if status == ERROR)
    warns = sum(1 for status, _ in findings if status == WARN)
    for status, message in findings:
        print(f"{status.ljust(5)} {message}")
    if not findings:
        print("OK — region tree is well-formed, flow connects, render is current")
    else:
        print(f"\n{errors} error(s), {warns} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
