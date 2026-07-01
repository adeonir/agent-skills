# Render

Draw a low-fi wireframe from the region tree — a greyscale, Figma-style sketch of
the page, in HTML or ASCII. The render is **generative**: it reads the plan and
draws the page with judgment, guided by a fixed glyph kit so runs stay
consistent in style.

## When to Use

- User wants to see the planned page as a low-fi wireframe, not just read the tree
- User asks for a wireframe, an HTML preview, an ASCII sketch, or a screen-flow diagram
- A `WIREFRAME.md` exists and someone wants to eyeball the page before visual design
- After editing `WIREFRAME.md`, to refresh the wireframe so it stays current

## Inputs

Reads `docs/design/WIREFRAME.md` — its own artifact — and draws with the bundled
kit: the glyph stylesheet `assets/wireframe.css` and the composition rubric
[../references/drawing.md](../references/drawing.md). The output is a low-fi
wireframe: greyscale, content-blind (bars for text, crossed boxes for images),
no color, font, or design token. It reads as a page, never as a labelled block
diagram.

## Formats

Pick by intent, or honor what the user names:

| Format | Best for | Lands in |
|--------|----------|----------|
| `html` | the primary view — a full low-fi wireframe of the page | `docs/design/wireframe.html` (committed) |
| `ascii` | a monospace wireframe that embeds in markdown and PRs | the `WIREFRAME.md` body, under its surface |
| `mermaid` | screen-to-screen flow (navigation, not a page) | the `WIREFRAME.md` body (Screen Map) |

`html` and `ascii` are both low-fi wireframes of the page — the ASCII one is the
same drawing in box-art, never a region tree. `mermaid` is the only structural
diagram: it maps the `flow:` between surfaces.

## Workflow

### Step 1: Read the plan

Read `docs/design/WIREFRAME.md` — surfaces, blocks, shapes, `note`s, register per
surface, and the flow. This is the structure to draw; the glyphs and proportions
are yours to choose per the rubric.

### Step 2: Draw the wireframe

Follow [../references/drawing.md](../references/drawing.md) — the glyph
vocabulary, the label-to-glyph mapping, and the section rhythm. Draw a real
low-fi wireframe: heading → thick bar, body → thin bars, image → crossed box,
CTA → filled pill, list → rows, and give the page rhythm (alternating bands, a
tall hero, a dark footer). Region names ride only in the faint corner
annotation, never as on-page labels.

- **HTML** — inline the glyph kit from `${CLAUDE_SKILL_DIR}/assets/wireframe.css`
  into the output `<style>` so the file is standalone, compose the glyph classes,
  and write to `docs/design/wireframe.html`. One `.page` per surface.
- **ASCII** — draw the page in monospace box-art (the drawing rubric shows the
  conventions), under ~70 columns, as a fenced `text` block.

Draw the default (wide) arrangement. The plan's reflow and volume intent is
context; render the narrow view only when asked.

### Step 3: Place the output

- **`wireframe.html`** — written next to `WIREFRAME.md`, opens directly in a
  browser (no server). It is derived from the plan — regenerate it after plan
  changes rather than hand-editing.
- **ASCII** — paste each surface's drawing into that surface's `## {{surface}}`
  section in the `WIREFRAME.md` body, as a fenced `text` block.
- **Mermaid flow** — when a `flow:` exists, place the `mermaid` block in the
  body's `## Screen Map` in place of the one-line flow.

### Step 4: Keep it current

The render is one-way: `WIREFRAME.md` → wireframe. After any change to the plan,
re-draw so the wireframe matches. Because the render is generative it is not
byte-identical between runs; the fixed kit and rubric keep it consistent in
style, and [validate.md](validate.md) questions whether the drawing still
reflects the plan.

## Guidelines

- Draw a page, not a diagram — glyphs stand in for content; names stay in the annotation
- Keep it design-blind and content-blind: greyscale, bars for text, no color, font, token, or real copy
- Compose only the kit's glyphs (`assets/wireframe.css`); do not invent visual treatments
- Give the page rhythm — alternate bands, lead with a hero, close on a dark footer
- Regenerate after the plan changes; the wireframe is derived, never a source

**Out of scope:** visual identity (color, type, spacing, tokens), interactive
prototypes, high-fidelity comps, and real copy. The wireframe stays low-fi and
greyscale so it holds under any later design work.
