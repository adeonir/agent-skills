# Render

Project the region tree into a low-fi, design-blind view — a neutral
black-and-white `wireframe.html`, an ASCII region sketch, and a Mermaid screen
flow. The render makes the structure visible; it never adds a visual identity.

## When to Use

- User wants to see the planned structure, not just read the region tree
- User asks for a wireframe, an HTML preview, an ASCII sketch, or a screen-flow diagram
- A `WIREFRAME.md` exists and someone wants to eyeball the arrangement before styling
- After editing `WIREFRAME.md`, to refresh the rendered view so it stays current

## Inputs

Reads only `docs/design/WIREFRAME.md` — its own artifact. The render is a pure
projection of the region tree: neutral boxes, greyscale only, no color, type
scale, token, or interactivity. The default projection is a **greybox** — filled
neutral boxes arranged in 2D by shape; `--outline` swaps it for the annotated
b&w view. It carries no visual identity, so the same render holds under any
design. It never reads or infers styling from anywhere.

## Output formats

The format comes from discovery — pick by screen complexity, or honor what the
user names:

| Format | Best for | Lands in |
|--------|----------|----------|
| `html` | the primary view — a greybox: neutral boxes arranged in 2D | `docs/design/wireframe.html` (committed) |
| `html --outline` | eyeballing the tree as an annotated b&w outline | `docs/design/wireframe-outline.html` (scratch, not committed) |
| `ascii` | simple screens; embeds in markdown and PRs | the `WIREFRAME.md` body |
| `mermaid` | screen-to-screen flow | the `WIREFRAME.md` body (Screen Map) |
| `all` | the default — HTML file plus ASCII + Mermaid to stdout | both |

ASCII loses fidelity on dense, multi-column layouts; reach for `html` there.

## Workflow

### Step 1: Render

Run the bundled script (execute it; do not read it as reference):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/render_wireframe.py docs/design/WIREFRAME.md --format all
```

`--format` takes `all` (default), `html`, `ascii`, or `mermaid`. The script
writes the greybox `docs/design/wireframe.html` and prints the ASCII sketch and
the Mermaid flow to stdout. Add `--outline` to write the annotated b&w view to
`docs/design/wireframe-outline.html` instead — a scratch view, not committed.

### Step 2: Place the output

- **`wireframe.html`** — the greybox, already written next to `WIREFRAME.md`. It
  opens directly in a browser; no server. It carries a `generated — do not edit`
  header: it is derived, never a source, and it is the committed view. Hand edits
  belong in `WIREFRAME.md`, then re-render.
- **`wireframe-outline.html`** — the `--outline` annotated view. A scratch
  alternative for reading the tree; leave it uncommitted.
- **ASCII sketch** — when ASCII was requested, paste each surface's block into
  that surface's `## {{surface}}` section in the `WIREFRAME.md` body, as a
  fenced `text` block, so the sketch travels with the source.
- **Mermaid flow** — when a `flow:` exists, place the `mermaid` block in the
  body's `## Screen Map` section in place of the one-line flow.

### Step 3: Keep it current

The render is one-way: `WIREFRAME.md` → outputs. Never hand-edit `wireframe.html`
or the embedded sketches and expect the tree to follow — there is no reverse
parse. After any change to the region tree, re-run Step 1 so the view matches.
[validate.md](validate.md) flags a stale `wireframe.html` as drift.

## Guidelines

- Render only what the region tree states — never invent blocks, states, or styling
- Keep the output neutral: greyscale, no color, type scale, or token
- The greybox `wireframe.html` is the committed view; `--outline` is a scratch alternative, uncommitted
- Treat `wireframe.html` as generated — regenerate, never hand-edit
- Route ASCII to simple screens, HTML to dense ones; offer both when useful

**Out of scope:** visual decisions (color, type, spacing, tokens), interactive
prototypes, and high-fidelity comps. The render stays low-fi and structure-only
so it holds under any later design work.
