#!/usr/bin/env python3
"""render_wireframe.py — project WIREFRAME.md into a low-fi, design-blind view.

Execute this script; never read it as reference.

Reads the YAML frontmatter region tree of a WIREFRAME.md (the `surfaces:` map
and optional `flow:` list) and projects it into neutral, greyscale output.
It makes no design decision: no color, no type scale, no token — only the
structure the region tree already states, made visible.

Usage:
    python3 render_wireframe.py <path-to-WIREFRAME.md> [--format all|html|ascii|mermaid] [--outline]

Default format is `all`. Behaviour per format:
    - html    → writes `wireframe.html` next to the input file — a greybox:
                neutral filled boxes arranged in 2D by shape
    - ascii   → prints an indented region sketch per surface to stdout
    - mermaid → prints a `flowchart` built from `flow:` to stdout
    - all     → writes the HTML and prints the ASCII sketch + Mermaid flow

`--outline` switches the HTML projection to the b&w annotated view (each box
shows its `name · shape` label and its `note`) and writes it to
`wireframe-outline.html` — a scratch view, not the committed artifact. The
greybox `wireframe.html` stays the source of truth the drift check compares.

The HTML carries no timestamp, so re-running on an unchanged source produces a
byte-identical file — `validate_wireframe.py` relies on that to detect drift.

Exit codes: 0 = rendered, 2 = usage / IO / parse error.
"""

import os
import re
import sys

# The fixed shape vocabulary the region tree may use. Block labels are free;
# only the shape is constrained, so a deterministic renderer can draw it.
SHAPES = ("full-width", "split", "stack", "sidebar", "modal", "overlay")
GRID = re.compile(r"^grid-(\d+)$")  # grid-N — N-column grid, N parsed inline

# A neutral box width (in characters) for the ASCII sketch's top rule. 60 is
# wide enough for a labelled surface header without wrapping in a terminal.
ASCII_RULE = 60


def unquote(value):
    return re.sub(r'^["\']|["\']$', "", value.strip())


def extract_frontmatter(markdown):
    match = re.match(r"^---\r?\n(.*?)\r?\n---", markdown, re.S)
    return match.group(1) if match else None


def split_kv(text):
    # Split a `key: value` line into (key, raw_value). A bare `key:` returns
    # ("key", "") so the caller knows a nested block follows. Keys may be a
    # bare token (`block:`) or a quoted surface name (`"home":`); a line with no
    # key (a `- "a -> b"` scalar) returns (None, None).
    match = re.match(r'^(?:"([^"]*)"|([\w-]+)):\s*(.*)$', text)
    if not match:
        return None, None
    key = match.group(1) if match.group(1) is not None else match.group(2)
    return key, match.group(3)


def tokenize(yaml_text):
    # Drop blank and comment lines; keep (indent, stripped_text) for the rest.
    rows = []
    for raw in re.split(r"\r?\n", yaml_text):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        rows.append((indent, raw.strip()))
    return rows


def parse_node(rows, pos, indent):
    # Recursive-descent over the indentation token stream. Returns (value, pos).
    # A run of `- ` lines at `indent` is a sequence; `key:` lines are a mapping.
    if pos >= len(rows):
        return None, pos
    if rows[pos][1].startswith("- "):
        return parse_sequence(rows, pos, indent)
    return parse_mapping(rows, pos, indent)


def parse_sequence(rows, pos, indent):
    seq = []
    while pos < len(rows):
        cur_indent, cur_text = rows[pos]
        if cur_indent != indent or not cur_text.startswith("- "):
            break
        inner = cur_text[2:]
        key, val = split_kv(inner)
        if key is None:
            seq.append(unquote(inner))
            pos += 1
            continue
        # A `- key: value` item opens a map; its continuation keys sit one
        # column past the dash (the column where `key` began).
        item = {}
        item_indent = indent + 2
        if val == "":
            child, pos = parse_node(rows, pos + 1, rows[pos + 1][0]) if pos + 1 < len(rows) else (None, pos + 1)
            item[key] = child
        else:
            item[key] = unquote(val)
            pos += 1
        while pos < len(rows) and rows[pos][0] == item_indent and not rows[pos][1].startswith("- "):
            k, v = split_kv(rows[pos][1])
            if k is None:
                break
            if v == "":
                child, pos = parse_node(rows, pos + 1, rows[pos + 1][0]) if pos + 1 < len(rows) else (None, pos + 1)
                item[k] = child
            else:
                item[k] = unquote(v)
                pos += 1
        seq.append(item)
    return seq, pos


def parse_mapping(rows, pos, indent):
    mapping = {}
    while pos < len(rows):
        cur_indent, cur_text = rows[pos]
        if cur_indent != indent or cur_text.startswith("- "):
            break
        key, val = split_kv(cur_text)
        if key is None:
            break
        if val == "":
            if pos + 1 < len(rows) and rows[pos + 1][0] > indent:
                child, pos = parse_node(rows, pos + 1, rows[pos + 1][0])
                mapping[key] = child
            else:
                mapping[key] = None
                pos += 1
        else:
            mapping[key] = unquote(val)
            pos += 1
    return mapping, pos


def parse_region_tree(yaml_text):
    # Parse the whole frontmatter, then pull `surfaces:` (map) and `flow:` (list).
    rows = tokenize(yaml_text)
    tree, _ = parse_mapping(rows, 0, 0)
    surfaces = tree.get("surfaces")
    if not isinstance(surfaces, dict):
        raise ValueError("frontmatter has no `surfaces:` mapping")
    flow = tree.get("flow") or []
    if not isinstance(flow, list):
        flow = []
    return surfaces, [unquote(str(step)) for step in flow]


def shape_of(block):
    raw = block.get("shape")
    return unquote(raw) if isinstance(raw, str) else ""


def blocks_of(surface):
    # A surface value is a sequence of block maps; tolerate an empty surface.
    return surface if isinstance(surface, list) else []


# ---- HTML projection -------------------------------------------------------

# Two greyscale-only stylesheets. Every value is a shade or a structural
# primitive (border, gap, padding, min-height) — no hue, no token, no type
# scale beyond the browser default. Both show arrangement, never a visual
# identity; they differ only in how a block presents itself.

# Greybox (default) — each block is a neutral filled box with a discreet
# caption, arranged in 2D by shape. Leaves carry a min-height so a region reads
# as a placeholder; `.wf-kids` fills the block and stretches side-by-side
# children to equal height, which gives nested regions believable weight
# without any per-block size.
GREYBOX_STYLE = """\
* { box-sizing: border-box; }
body { margin: 0; padding: 24px; background: #fff; color: #111;
       font: 11px/1.4 ui-monospace, monospace; }
.wf-surface { border: 2px solid #111; margin: 0 0 24px; }
.wf-surface > .wf-name { background: #111; color: #fff; padding: 4px 8px;
                         font-weight: 700; }
.wf-surface > .wf-children { padding: 12px; display: flex;
                             flex-direction: column; gap: 12px; }
.wf-block { border: 1px solid #b0b0b0; background: #e8e8e8;
            padding: 6px; display: flex; flex-direction: column; gap: 6px; }
.wf-block.wf-leaf { min-height: 32px; }
.wf-block > .wf-label { color: #7a7a7a; font-size: 9px; letter-spacing: 0.06em;
                        text-transform: uppercase; }
.wf-kids { display: flex; flex-direction: row; gap: 8px; flex: 1;
           align-items: stretch; }
.wf-stack > .wf-kids, .wf-full-width > .wf-kids { flex-direction: column; }
.wf-split > .wf-kids > * { flex: 1; }
.wf-grid > .wf-kids { display: grid; gap: 8px; }
.wf-sidebar > .wf-kids > :first-child { flex: 0 0 200px; }
.wf-sidebar > .wf-kids > :not(:first-child) { flex: 1; }
.wf-modal, .wf-overlay { border-style: dashed; background: #f2f2f2; }
"""

# Outline (--outline) — the annotated b&w view: each box shows its `name · shape`
# label and its `note` in italic. Reads as a documentation outline; kept as a
# scratch alternative to the greybox, never the committed artifact.
OUTLINE_STYLE = """\
* { box-sizing: border-box; }
body { margin: 0; padding: 24px; background: #fff; color: #111;
       font: 13px/1.4 ui-monospace, monospace; }
.wf-surface { border: 1px solid #111; margin: 0 0 24px; }
.wf-surface > .wf-name { background: #111; color: #fff; padding: 4px 8px;
                         font-weight: 700; }
.wf-children { padding: 8px; display: flex; flex-direction: column; gap: 8px; }
.wf-block { border: 1px solid #999; background: #f4f4f4; padding: 8px; }
.wf-block > .wf-label { color: #555; }
.wf-block > .wf-note { color: #888; font-style: italic; margin-top: 4px; }
.wf-kids { margin-top: 8px; display: flex; gap: 8px; }
.wf-stack > .wf-kids { flex-direction: column; }
.wf-split > .wf-kids > * { flex: 1; }
.wf-grid > .wf-kids { display: grid; gap: 8px; }
.wf-sidebar > .wf-kids > :first-child { flex: 0 0 200px; }
.wf-sidebar > .wf-kids > :not(:first-child) { flex: 1; }
.wf-modal, .wf-overlay { border-style: dashed; }
"""

GENERATED_HEADER = (
    "<!-- generated from WIREFRAME.md by wireframe-sketch — do not edit. "
    "Regenerate: python3 ${CLAUDE_SKILL_DIR}/scripts/render_wireframe.py "
    "docs/design/WIREFRAME.md -->"
)

OUTLINE_HEADER = (
    "<!-- generated from WIREFRAME.md by wireframe-sketch (outline view) — do "
    "not edit, not committed. Regenerate: python3 "
    "${CLAUDE_SKILL_DIR}/scripts/render_wireframe.py docs/design/WIREFRAME.md "
    "--outline -->"
)


def esc(text):
    # Escapes for both text nodes and double-quoted attribute values, so a label
    # or note carrying a `"` cannot break out of a `class="..."` or `title="..."`.
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_block_html(block, depth, outline=False):
    shape = shape_of(block)
    grid = GRID.match(shape)
    css_shape = "grid" if grid else shape
    children = block.get("children")
    child_blocks = [c for c in children if isinstance(c, dict)] if isinstance(children, list) else []
    classes = "wf-block"
    if css_shape:
        classes += f" wf-{css_shape}"
    if not child_blocks:
        classes += " wf-leaf"  # a childless block is a leaf cell — the only box that needs a floor
    label = esc(block.get("block") or "block")
    note = block.get("note")
    has_note = isinstance(note, str) and note.strip()
    if outline:
        parts = [f'<div class="{esc(classes)}">']
        parts.append(f'<span class="wf-label">{label} · {esc(shape or "?")}</span>')
        if has_note:
            parts.append(f'<div class="wf-note">{esc(note)}</div>')
    else:
        # greybox: the box is the region. The label is a caption; any note rides
        # along as a hover title so intent survives without cluttering the draw.
        title = f' title="{esc(note)}"' if has_note else ""
        parts = [f'<div class="{esc(classes)}"{title}>']
        parts.append(f'<span class="wf-label">{label}</span>')
    if child_blocks:
        # grid-N columns are emitted inline so N drives the template directly.
        style = ""
        if grid:
            style = f' style="grid-template-columns: repeat({int(grid.group(1))}, 1fr);"'
        parts.append(f'<div class="wf-kids"{style}>')
        for child in child_blocks:
            parts.append(render_block_html(child, depth + 1, outline))
        parts.append("</div>")
    parts.append("</div>")
    return "".join(parts)


def render_html(surfaces, outline=False):
    style = OUTLINE_STYLE if outline else GREYBOX_STYLE
    header = OUTLINE_HEADER if outline else GENERATED_HEADER
    body = []
    for name, surface in surfaces.items():
        body.append('<div class="wf-surface">')
        body.append(f'<div class="wf-name">{esc(name)}</div>')
        body.append('<div class="wf-children">')
        for block in blocks_of(surface):
            if isinstance(block, dict):
                body.append(render_block_html(block, 0, outline))
        body.append("</div></div>")
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"{header}\n<title>Wireframe</title>\n<style>\n{style}</style>\n"
        "</head>\n<body>\n" + "\n".join(body) + "\n</body>\n</html>\n"
    )


# ---- ASCII projection ------------------------------------------------------

def render_block_ascii(block, prefix, is_last, lines):
    # An indented region tree: reliable for any nesting, honest about being a
    # low-fi sketch. 2D box packing is deliberately avoided.
    connector = "└─ " if is_last else "├─ "
    label = block.get("block") or "block"
    shape = shape_of(block) or "?"
    lines.append(f"{prefix}{connector}{label} · {shape}")
    children = block.get("children")
    if isinstance(children, list) and children:
        kids = [c for c in children if isinstance(c, dict)]
        extension = "   " if is_last else "│  "
        for index, child in enumerate(kids):
            render_block_ascii(child, prefix + extension, index == len(kids) - 1, lines)


def render_ascii(surfaces):
    out = []
    for name, surface in surfaces.items():
        out.append(name)
        out.append("─" * ASCII_RULE)
        blocks = [b for b in blocks_of(surface) if isinstance(b, dict)]
        for index, block in enumerate(blocks):
            render_block_ascii(block, "", index == len(blocks) - 1, out)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---- Mermaid projection ----------------------------------------------------

def mermaid_id(name):
    # A safe node id: non-alphanumeric runs collapse to underscores.
    ident = re.sub(r"[^0-9A-Za-z]+", "_", name.strip()).strip("_")
    return ident or "node"


def render_mermaid(flow):
    if not flow:
        return ""
    lines = ["```mermaid", "flowchart LR"]
    for step in flow:
        ends = re.split(r"\s*-+>\s*", step)
        if len(ends) < 2:
            continue
        for src, dst in zip(ends, ends[1:]):
            lines.append(
                f"    {mermaid_id(src)}[{src.strip()}] --> {mermaid_id(dst)}[{dst.strip()}]"
            )
    lines.append("```")
    return "\n".join(lines) + "\n"


# ---- driver ----------------------------------------------------------------

def load(path):
    try:
        with open(path, "r", encoding="utf8") as handle:
            markdown = handle.read()
    except OSError:
        print(f"Cannot read {path}", file=sys.stderr)
        return None
    yaml_text = extract_frontmatter(markdown)
    if yaml_text is None:
        print(f"No YAML frontmatter found in {path}", file=sys.stderr)
        return None
    try:
        return parse_region_tree(yaml_text)
    except (ValueError, IndexError) as error:
        print(f"Cannot parse region tree in {path}: {error}", file=sys.stderr)
        return None


def main(argv):
    args = argv[1:]
    if not args or args[0].startswith("--"):
        print(
            "Usage: render_wireframe.py <path-to-WIREFRAME.md> "
            "[--format all|html|ascii|mermaid] [--outline]",
            file=sys.stderr,
        )
        return 2
    path = args[0]
    fmt = "all"
    if "--format" in args:
        index = args.index("--format")
        fmt = args[index + 1] if index + 1 < len(args) else "all"
    outline = "--outline" in args

    parsed = load(path)
    if parsed is None:
        return 2
    surfaces, flow = parsed

    if fmt in ("all", "html"):
        # greybox is the committed artifact; --outline is a scratch alt view.
        out_name = "wireframe-outline.html" if outline else "wireframe.html"
        out_path = os.path.join(os.path.dirname(os.path.abspath(path)), out_name)
        try:
            with open(out_path, "w", encoding="utf8") as handle:
                handle.write(render_html(surfaces, outline=outline))
        except OSError:
            print(f"Cannot write {out_path}", file=sys.stderr)
            return 2
        print(f"Wrote {out_path}")
    if fmt in ("all", "ascii"):
        print("\n# ASCII region sketch\n")
        print(render_ascii(surfaces))
    if fmt in ("all", "mermaid"):
        mermaid = render_mermaid(flow)
        if mermaid:
            print("\n# Screen flow (Mermaid)\n")
            print(mermaid)
        elif fmt == "mermaid":
            print("No `flow:` defined — nothing to draw.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
