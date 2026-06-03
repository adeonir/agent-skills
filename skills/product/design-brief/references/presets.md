# Presets

Curated tone library for visual direction. Each preset is a pre-blended
direction across the Style Axes — a named mood with its signature move and
layout character.

## When to Use

Auto-loaded by `direction.md` whenever the user invokes a named vibe
("Editorial", "Cyberpunk", "Bento", "Luxury", ...) instead of composing
freely across Style Axes. Presets are *starting points*, not constraints —
the agent may compose further or blend two adjacent presets.

## How Presets Work

A preset is read as a **mood seed**: its Vibe, Signature move, and layout hints
inform a candidate direction. Tokens do not exist yet at the direction stage —
a preset describes the look in words; token values are chosen later in design.

Presets are orthogonal to the surfaces a project has: any preset is usable on
marketing pages, app screens, or storefronts. Layout hints adapt the recipe to
the project's structure.

## Recipe Template

ALWAYS use this exact template structure:

```markdown
### {preset-name}
**Vibe:** {one-line aesthetic description}
**Layout hints:**
- {composition hint 1}
- {composition hint 2}
- {density / asymmetry / focal point guidance}
**Signature move:** {the one unforgettable detail per the Four Questions}
**Best for:** {surface kinds where preset excels}
**Avoid for:** {surface kinds where preset misfires}
```

## Presets

### Recipes Index

- [brutally-minimal](#brutally-minimal) — maximum whitespace, near-monochrome
- [maximalist-chaos](#maximalist-chaos) — dense layered overwhelm
- [retro-futuristic](#retro-futuristic) — CRT glow, neon on dark, monospace
- [organic-natural](#organic-natural) — earth tones, soft rounded shapes
- [luxury-refined](#luxury-refined) — thin serifs, restrained metallics
- [playful-toy](#playful-toy) — rounded sans, bright primaries, bouncy
- [editorial-magazine](#editorial-magazine) — warm paper, serif headlines, asymmetric grid
- [brutalist-raw](#brutalist-raw) — system fonts, hard edges, anti-polish
- [art-deco](#art-deco) — gold on dark, geometric ornament, symmetric
- [soft-pastel](#soft-pastel) — diffused pastels, low contrast, gentle
- [industrial-utilitarian](#industrial-utilitarian) — monospace, data density, terminal feel
- [neo-grotesque](#neo-grotesque) — Swiss grids, tight leading, objective clarity
- [kinetic-motion-first](#kinetic-motion-first) — scroll-driven, variable font axes

### brutally-minimal
**Vibe:** Maximum whitespace, typography-only hierarchy, near-monochrome — restraint as the design statement.
**Layout hints:**
- Single column, left-aligned, max-measure 60ch
- Section padding 8-12rem vertical on desktop
- One accent color appears in exactly one element per viewport
**Signature move:** Display heading at 120-160px weight 200, body at 16px weight 400 — 7-8x size ratio.
**Best for:** marketing and content surfaces (editorial, agency, portfolio)
**Avoid for:** storefronts (needs catalog density), app dashboards

### maximalist-chaos
**Vibe:** Dense layering, clashing textures, overwhelming detail — the design as visual onslaught.
**Layout hints:**
- Overlap elements across grid boundaries
- Multiple focal points per viewport, intentionally competing
- Background patterns, gradient meshes, sticker-style badges, marquee text
**Signature move:** A floating badge or sticker that rotates `-12deg` and breaks the grid with a 4-color gradient border.
**Best for:** marketing surfaces (brand statement, music, fashion, creator economy)
**Avoid for:** app and mobile screens (cognitive load), checkout flows

### retro-futuristic
**Vibe:** CRT glow, scanlines, neon on dark, monospace type — late-80s synthwave or early Y2K computer.
**Layout hints:**
- Grid-locked composition, wireframe horizons, sunset gradient overlays
- Subtle scanline overlay (`repeating-linear-gradient` 1px lines)
- Glow on every interactive accent
**Signature move:** Hero headline glows in neon cyan with a soft drop-shadow halo and a subtle TV scanline overlay across the section.
**Best for:** marketing surfaces (gaming, dev tools, music tech, AI brand)
**Avoid for:** financial, healthcare, editorial

### organic-natural
**Vibe:** Soft shapes, earth tones, hand-drawn textures, rounded corners — calm and rooted.
**Layout hints:**
- Asymmetric layered composition (organic blob shapes behind content)
- Mix of sans and serif within hierarchy
- Subtle grain texture across surfaces
**Signature move:** A blob-shaped accent color shape sits behind the hero headline, slightly off-axis, with hand-drawn vector decorations nearby.
**Best for:** marketing and content surfaces (wellness, food, sustainability, lifestyle DTC)
**Avoid for:** app dashboards, fintech

### luxury-refined
**Vibe:** Thin serifs, muted metallics, generous spacing, restrained palette — quiet money.
**Layout hints:**
- Center-anchored composition with breathing room
- Image-led with one hero photograph at extreme detail
- Hairline rules (1px) separating sections
**Signature move:** A 96-128px high-contrast Didone display headline sits above generous whitespace with a single thin gold rule beneath.
**Best for:** marketing and content surfaces (luxury brand, jewelry, hospitality, agency)
**Avoid for:** SaaS dashboards, gaming, casual storefronts

### playful-toy
**Vibe:** Rounded sans, bright primaries, bouncy motion, oversized elements — toy-like joy.
**Layout hints:**
- Oversized hero copy (`text-9xl` or larger)
- Sticker badges, bouncy hover transforms
- Solid block-color sections with rounded transitions between them
**Signature move:** Hover on the primary CTA triggers a `scale(1.05)` + `rotate(-3deg)` bounce with a cheerful drop-shadow shift.
**Best for:** marketing surfaces (kids, education, creator tools, casual mobile apps)
**Avoid for:** enterprise, finance, healthcare

### editorial-magazine
**Vibe:** High-contrast serif headings, warm neutrals, editorial grid, section numbering — long-form sanctuary.
**Layout hints:**
- Asymmetric multi-column grid with text wrapping image
- Section numbers (`01.`, `02.`) in display weight
- Drop caps on opening paragraphs
**Signature move:** Section opens with a large-numbered display character (`01`) at 200px weight 200, followed by a drop-cap paragraph that fills the column.
**Best for:** marketing and content surfaces (publication, podcast, long-form storytelling)
**Avoid for:** app screens, checkout flows

### brutalist-raw
**Vibe:** System fonts pushed to extremes, exposed structure, anti-polish — ugly-cool.
**Layout hints:**
- Hard rule borders (`border: 2px solid black`) everywhere
- Marquee headlines at 200-400px
- Grid lines visible, exposed HTML structure aesthetic
**Signature move:** A `400px` Helvetica Bold headline runs full-bleed across the hero with a hard black border below and a marquee-style auto-scroll subtext.
**Best for:** marketing surfaces (agency, fashion, music label, brand statement)
**Avoid for:** storefronts, app and mobile screens, healthcare

### art-deco
**Vibe:** Gold + black, symmetrical patterns, angular type, ornamental borders — 1920s glamour.
**Layout hints:**
- Symmetric centered composition
- Ornamental geometric borders (chevron, sunburst, fan)
- Hairline gold rules separating sections
**Signature move:** A symmetric sunburst geometric ornament sits behind the hero headline in gold leaf.
**Best for:** marketing surfaces (luxury, hospitality, theatre, event), event microsites
**Avoid for:** app and mobile screens, modern storefronts

### soft-pastel
**Vibe:** Low-contrast pastels, diffused gradients, gentle rounded UI — calm bedroom aesthetic.
**Layout hints:**
- Diffused radial gradient backgrounds
- Card-based layouts with soft shadows in pastel tints
- Avoid hard color blocks
**Signature move:** Hero background is a diffuse radial gradient transitioning between three pastel hues (lavender → blush → peach).
**Best for:** marketing surfaces (wellness, beauty, lifestyle, mental health, journaling apps), mobile app screens
**Avoid for:** financial, enterprise, gaming

### industrial-utilitarian
**Vibe:** Monospace, high-density data, dark UI, minimal ornamentation — terminal as design language.
**Layout hints:**
- Tabular numerics (`font-variant-numeric: tabular-nums`)
- Grid-aligned data tables with hairline borders
- Dot-grid backgrounds, mono-spaced labels
**Signature move:** All numerics use tabular figures aligned to a monospace grid; headlines are uppercase with letter-spacing.
**Best for:** marketing surfaces (dev tools, infra, AI infra, B2B SaaS), app dashboards
**Avoid for:** consumer marketing, lifestyle, storefronts

### neo-grotesque
**Vibe:** Swiss-style grids, tight leading, limited palette, extreme alignment precision — design as system.
**Layout hints:**
- 12-column grid visible in baseline
- Tight letter-spacing on display, generous leading on body
- One accent color used at exactly one spot per viewport
**Signature move:** Display headline at weight 900 with `-0.04em` letter-spacing flush-left in column 1, paired with a single small accent dot in column 12.
**Best for:** marketing and content surfaces (design portfolio, agency, brand book, editorial)
**Avoid for:** gaming, kids, festive marketing

### kinetic-motion-first
**Vibe:** Interface built around transition — parallax, morphing shapes, scroll-driven narrative.
**Layout hints:**
- Scroll-triggered reveals (`IntersectionObserver` or `animation-timeline: scroll()`)
- Pinned sections that morph over scroll distance
- Variable font weight/width transitions on hover/scroll
**Signature move:** Hero headline morphs its variable font weight from 100 to 900 over the first 600px of scroll, while background hue shifts across the spectrum.
**Best for:** marketing surfaces (brand statement, product launch, portfolio, agency)
**Avoid for:** app and mobile screens, checkout flows, dashboards
