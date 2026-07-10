# Drawing Rubric

How to draw a low-fi wireframe from a region tree — the glyph vocabulary, the label-to-glyph mapping, and the composition rules that keep the generative render consistent across runs.

## When to Use

Composed by [render.md](../instructions/render.md) whenever the render operation draws `wireframe.html` (HTML) or an ASCII wireframe. The render is **generative** — it reads the plan and draws the page with judgment — and this rubric is what makes independent runs land in the same low-fi style. Not a direct trigger.

## The Contract

Draw a **low-fi wireframe**, the kind you would sketch in Figma before any visual design: greyscale boxes, bars standing in for text, crossed boxes for images, filled shapes for buttons. It reads as a *page*, never as a labelled block diagram. Two hard constraints:

- **Design-blind** — greyscale only. No hue, no brand, no font choice, no type scale, no design token. The kit in `assets/wireframe.css` is the only palette.
- **Content-blind** — no real copy. Text is bars, a heading is a thick bar, a price is `$—`. The wireframe shows *where* content goes and *what kind* it is, never the words.

Region **names** from the tree do not become on-page labels — they ride only in the faint `.annot` in a section's corner. What tells the reader "this is a headline" is the **glyph** (a thick bar), not text saying "headline".

## Glyph Vocabulary

The kit (`assets/wireframe.css`) draws these. Compose them; do not invent new visual treatments.

| Content | Glyph | Class |
|---------|-------|-------|
| heading | one or two thick bars | `.bar.lg` (width `.w40`–`.w85`) |
| body / paragraph | a stack of thin bars | `.lines` of `.bar.sm`, last one short |
| eyebrow / kicker | dash + short label | `.eyebrow` |
| image / media / logo | filled box with an X | `.xbox` + a height (`.h120`–`.h420`, `.sq`) |
| button / CTA | filled pill (primary) or outline (secondary) | `.pill`, `.pill.ghost`, `.pill.sm` |
| list / menu rows | name, a dotted leader, then value | `.rowline` (name bar + `.leader` + `.price` or `.bar.sm`) |
| price | `$—` | `.price` |
| rating | five stars | `.stars` (`★★★★★`) |
| carousel / pagination | dots, first active | `.dots` with one `.on` |
| tag / chip | outlined pill | `.tag` |
| icon / avatar | small square or circle | `.icon`, `.icon.rnd` |
| section opener ornament | line · diamond · line | `.zone` |
| nav links | row of short bars | `.navlinks .lk` |
| divider | short centered rule | `.divider` |
| form field / input | bordered box + placeholder bar | `.field` (`.area`, `.sm`) |
| labelled field | caption bar above the input | `.formrow` (`.cap` + `.field`) |
| select / dropdown | field with a caret | `.field.select` |
| search | field with a magnifier | `.field.search` |
| checkbox / radio | small box / circle | `.check`, `.check.rnd`, `.check.on` |
| toggle / switch | pill track + knob | `.toggle`, `.toggle.on` |
| tabs | strip, one active underlined | `.tabs` + `.tab` / `.tab.on` |
| toolbar | light action bar | `.toolbar` (search + actions inside) |
| table | header + cell rows | `.table` + `.trow` / `.trow.thead` + `.tcell` |
| breadcrumb | short bars + separators | `.crumbs` |
| pagination | small numbered cells | `.pager` with one `.on` |
| sidebar rail | fixed nav column | `.rail` + `.item` / `.item.on` |

## Mapping Labels to Glyphs

Infer the glyph from the block's label and register — the tree already names things by context (`headline`, `hero-image`, `reservation-cta`, `course-list`).

- `headline`, `title`, `heading` → `.bar.lg`; `subheadline` → a shorter `.bar`
- `eyebrow`, `kicker`, `label` → `.eyebrow`
- `body`, `text`, `copy`, `teaser`, `description`, `quote` → `.lines`
- `image`, `photo`, `media`, `logo`, `thumb`, `dish`, `hero-*` visual → `.xbox`
- `*-cta`, `button`, `action`, `reservation`, `submit` → `.pill` (primary) / `.pill.ghost` (secondary, when two sit together)
- `*-list`, `menu`, `courses`, `index`, `nav-links` → `.rowline` rows or `.navlinks`
- `price`, `cost` → `.price`; `rating`, `stars`, `reviews` → `.stars`
- `scroll-cue`, `carousel`, `dots` → `.dots`
- `highlight`, `tag`, `badge` → `.tag`; `icon`, `avatar`, `social` → `.icon`
- `form`, `field`, `input`, `email`, `password` → `.field`, wrapped in a `.formrow` with a caption
- `select`, `dropdown`, `filter` → `.field.select`; `search` → `.field.search`
- `checkbox`, `radio`, `option`, `consent` → `.check`; `toggle`, `switch` → `.toggle`
- `table`, `data-table`, data `grid`, `results` → `.table` (a `.trow.thead` + `.trow`s); `tabs`, `segmented` → `.tabs`
- `toolbar`, `filters-bar`, `actions` → `.toolbar`; `breadcrumb` → `.crumbs`; `pagination`, `pager` → `.pager`
- `sidebar`, `side-nav`, `rail` → `.rail`

When a label is unfamiliar, fall back to `.lines` (text) — a bar is the safe neutral. Never draw a plain labelled box; that is the diagram we are leaving behind.

## Section Rhythm and Composition

The page is a stack of `.sec`. Give it rhythm and a hierarchy a scanner reads:

- **Page frame** — one `.page` per surface, a `.page-tag` reading `{surface} · {register} · {type}` (from the tree's surface name and register), faint `.annot` naming each region.
- **Alternate bands** — plain and `.band` sections alternate so the page has vertical rhythm; never a flat wall of identical sections.
- **Hero leads** — the first content section is tall (`min-height` ~420), often full-bleed media with the copy lockup overlaid or beside it, primary + ghost CTAs, and a `.dots` or `.zone` cue.
- **Split sections** — a `.row` of a text `.col` beside an `.xbox`; alternate which side the image sits on down the page.
- **Openers** — a centered section (pull-quote, page-hero, a grid intro) opens with a `.zone` ornament and centered `.lines`.
- **Grids** — a `grid-N` block becomes a `.row` of N `.card`s (`.icon` + bars).
- **Footer** — the last section is `.sec.dark`: logo `.xbox`, a CTA, link columns, `.stars`, `.tag`s, `.socials`, and a thin legal row.
- **Modal / overlay** — a `modal` block draws as a centered `.card` floating over a dimmed page; an `overlay` draws as a layer sitting above the section it belongs to. Both keep a visible way out (a close control).
- **Sidebar** — a `sidebar` shape (or a product surface with side-nav) draws as a `.row` of a fixed `.rail` (nav `.item`s, one `.on`) beside a `.fill` main area; run the shell section as `.sec.flush` so the rail meets the edge.
- **Product surfaces** — lead with a persistent nav or sidebar, not a hero. A data view is a `.toolbar` (search + actions) above a `.table` closed by a `.pager`; a form stacks `.formrow`s with a primary `.pill` to submit. Density over rhythm — quieter bands than a brand page — and plan the empty / loading / error states in the narration.
- **Reflow** — the plan's narrow-viewport intent is context, not a second render; draw the default (wide) arrangement unless asked for the narrow one.

Match the arrangement to the block's `shape` (`split`, `stack`, `grid-N`, `sidebar`, `full-width`) and the surface's register (brand builds toward a conversion; product follows the task) — read [brand.md](brand.md) / [product.md](product.md).

## ASCII Wireframes

The ASCII form is the *same* low-fi wireframe in monospace box-art — a page sketch, never an indented region tree. Draw the frame with box-drawing characters and stand in for content the same way:

```text
┌──────────────────────────────────────────────┐
│ [≡]   ▬▬  ▬▬  ▬▬              ⌕  ♡  ⌂          │  nav
├──────────────────────────────────────────────┤
│  ── EYEBROW                    ┌────────────┐  │
│  [LOGO]  ▬▬▬▬▬▬▬▬▬▬            │  ╲      ╱   │  │  hero
│  ▬▬▬▬▬▬                        │    ╳       │  │  (split)
│  ▐ CTA ▌  ▛ CTA ▟              │   ╱     ╲   │  │
│  • ◦ ◦                         └────────────┘  │
└──────────────────────────────────────────────┘
```

Conventions: `▬`/`▭` bars for text, `┌╲╱┐ ╳ └╱╲┘` for an image, `▐ ▌` for a button, `•◦` for dots, `── LABEL` for an eyebrow, box-drawing for section frames. Keep it under ~70 columns so it embeds cleanly in markdown and PRs.

## Output

- **HTML** → inline the kit from `${CLAUDE_SKILL_DIR}/assets/wireframe.css` into the output's `<style>` so `wireframe.html` is standalone, then compose the glyphs. Write to `docs/design/wireframe.html`.
- **ASCII** → a fenced `text` block, placed in the `WIREFRAME.md` body under the surface it draws.

Because the render is generative it is not byte-identical between runs; this rubric plus the fixed kit keep it consistent in *style*, which is what a low-fi wireframe needs.
