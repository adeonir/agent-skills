# Presets

Curated tone library for variant generation. Each preset is a pre-blended
direction across the Style Axes — token overrides, prompt addendum, and
layout hints packed into a single named recipe.

## When to Use

Auto-loaded by `preview.md` whenever the user invokes a named vibe
("Editorial", "Cyberpunk", "Bento", "Luxury", ...) instead of composing
freely across Style Axes. Presets are *starting points*, not constraints —
the agent may compose further or blend two adjacent presets.

## How Presets Work

A preset overlays its token map on top of the project's `DESIGN.md`
frontmatter for variant generation only — the underlying DESIGN.md is not
mutated. If the user approves a variant and runs the preview commit-back
workflow, the preset overlay propagates through the usual surgical patch
list (`preview.md` Commit Back to DESIGN.md).

Presets are orthogonal to the surfaces a project has: any preset is usable
on marketing pages, app screens, or storefronts. Layout hints adapt the
recipe to the project's structure.

## Recipe Template

ALWAYS use this exact template structure:

```markdown
### {preset-name}
**Vibe:** {one-line aesthetic description}
**Token overrides:**
- `colors.background`: {value or characterization}
- `colors.primary`: {value or characterization}
- `colors.accent`: {value or characterization}
- `typography.display.fontFamily`: {value or characterization}
- `typography.body.fontFamily`: {value or characterization}
- `spacing` scale multiplier: {factor}
- `rounded` scale: {sharp | subtle | medium | pill}
- `elevation` profile: {flat | subtle | layered | dramatic}
- `duration` profile: {snappy | gentle | bouncy | none}
**Prompt addendum:** "{one-sentence aesthetic guidance appended to variant generation prompt}"
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
**Token overrides:**
- `colors.background`: warm off-white (`#fafaf7`) or true white
- `colors.primary`: near-black (`#0a0a0a`)
- `colors.accent`: single charged hue used 5% of the surface only
- `typography.display.fontFamily`: refined sans (Inter Tight, GT America, Söhne) at weight 200-300
- `typography.body.fontFamily`: matching sans at weight 400
- `spacing` scale multiplier: `1.5x` (generous gaps)
- `rounded` scale: sharp (0-2px)
- `elevation` profile: flat (no shadows)
- `duration` profile: snappy (150-200ms)
**Prompt addendum:** "Strip every non-essential element; let one typographic move carry the entire screen."
**Layout hints:**
- Single column, left-aligned, max-measure 60ch
- Section padding 8-12rem vertical on desktop
- One accent color appears in exactly one element per viewport
**Signature move:** Display heading at 120-160px weight 200, body at 16px weight 400 — 7-8x size ratio.
**Best for:** marketing and content surfaces (editorial, agency, portfolio)
**Avoid for:** storefronts (needs catalog density), app dashboards

### maximalist-chaos
**Vibe:** Dense layering, clashing textures, overwhelming detail — the design as visual onslaught.
**Token overrides:**
- `colors.background`: gradient mesh or noise overlay (warm + cool + neutral mixed)
- `colors.primary`: high-saturation brand color
- `colors.accent`: three to four conflicting accents (orange, magenta, lime, electric blue)
- `typography.display.fontFamily`: characterful display (Cabinet Grotesk, Migra, Editorial New, custom)
- `typography.body.fontFamily`: contrasting sans (mono or condensed grotesk)
- `spacing` scale multiplier: `0.85x` (tight density)
- `rounded` scale: mixed (sharp + pill in same layout)
- `elevation` profile: dramatic (heavy layered shadows + glow + grain)
- `duration` profile: bouncy + snappy mix
**Prompt addendum:** "Pile texture, color, and decoration on top of each other; commit fully to overwhelm."
**Layout hints:**
- Overlap elements across grid boundaries
- Multiple focal points per viewport, intentionally competing
- Background patterns, gradient meshes, sticker-style badges, marquee text
**Signature move:** A floating badge or sticker that rotates `-12deg` and breaks the grid with a 4-color gradient border.
**Best for:** marketing surfaces (brand statement, music, fashion, creator economy)
**Avoid for:** app and mobile screens (cognitive load), checkout flows

### retro-futuristic
**Vibe:** CRT glow, scanlines, neon on dark, monospace type — late-80s synthwave or early Y2K computer.
**Token overrides:**
- `colors.background`: deep navy / purple-black (`#0a0420` or `#100822`)
- `colors.primary`: neon cyan or magenta (`oklch(0.75 0.25 200)`)
- `colors.accent`: complement neon (yellow on cyan, lime on magenta)
- `typography.display.fontFamily`: monospace display (JetBrains Mono, Berkeley Mono, Departure Mono)
- `typography.body.fontFamily`: matching mono at smaller size
- `spacing` scale multiplier: `1x`
- `rounded` scale: subtle (2-4px) with sharp corners on cards
- `elevation` profile: glow-shadow (neon-tinted box-shadow blur)
- `duration` profile: snappy with occasional bounce
**Prompt addendum:** "Treat the screen as a CRT terminal; let neon glow and scanline texture carry the era signal."
**Layout hints:**
- Grid-locked composition, wireframe horizons, sunset gradient overlays
- Subtle scanline overlay (`repeating-linear-gradient` 1px lines)
- Glow on every interactive accent
**Signature move:** Hero headline glows in neon cyan with a soft drop-shadow halo and a subtle TV scanline overlay across the section.
**Best for:** marketing surfaces (gaming, dev tools, music tech, AI brand)
**Avoid for:** financial, healthcare, editorial

### organic-natural
**Vibe:** Soft shapes, earth tones, hand-drawn textures, rounded corners — calm and rooted.
**Token overrides:**
- `colors.background`: cream / sand (`#f5efe3` or `oklch(0.96 0.02 80)`)
- `colors.primary`: forest green / clay / terracotta
- `colors.accent`: warm rust or muted ochre
- `typography.display.fontFamily`: humanist serif (Source Serif, Lora, Crimson) or warm sans (Quincy)
- `typography.body.fontFamily`: friendly sans (Plus Jakarta Sans, Inter at relaxed leading)
- `spacing` scale multiplier: `1.3x`
- `rounded` scale: medium (12-20px on cards, full on buttons)
- `elevation` profile: subtle (soft warm-tinted shadows)
- `duration` profile: gentle (300-400ms)
**Prompt addendum:** "Use warm earth tones, generous rounded shapes, hand-touched textures; feel inhabited rather than engineered."
**Layout hints:**
- Asymmetric layered composition (organic blob shapes behind content)
- Mix of sans and serif within hierarchy
- Subtle grain texture across surfaces
**Signature move:** A blob-shaped accent color shape sits behind the hero headline, slightly off-axis, with hand-drawn vector decorations nearby.
**Best for:** marketing and content surfaces (wellness, food, sustainability, lifestyle DTC)
**Avoid for:** app dashboards, fintech

### luxury-refined
**Vibe:** Thin serifs, muted metallics, generous spacing, restrained palette — quiet money.
**Token overrides:**
- `colors.background`: ivory / champagne / charcoal
- `colors.primary`: brass, deep oxblood, ink black
- `colors.accent`: single jewel-tone (emerald, ruby, sapphire) used 3% of surface
- `typography.display.fontFamily`: high-contrast serif (Didone — Bodoni, Didot, GT Sectra)
- `typography.body.fontFamily`: classic sans or refined serif at small size
- `spacing` scale multiplier: `1.6x`
- `rounded` scale: sharp (0-2px)
- `elevation` profile: subtle (no flashy shadows; rely on color contrast for hierarchy)
- `duration` profile: gentle (400-600ms with elegant easing)
**Prompt addendum:** "Restrained palette, generous whitespace, high-contrast serif headlines; let absence of decoration signal quality."
**Layout hints:**
- Center-anchored composition with breathing room
- Image-led with one hero photograph at extreme detail
- Hairline rules (1px) separating sections
**Signature move:** A 96-128px high-contrast Didone display headline sits above generous whitespace with a single thin gold rule beneath.
**Best for:** marketing and content surfaces (luxury brand, jewelry, hospitality, agency)
**Avoid for:** SaaS dashboards, gaming, casual storefronts

### playful-toy
**Vibe:** Rounded sans, bright primaries, bouncy motion, oversized elements — toy-like joy.
**Token overrides:**
- `colors.background`: cream or pastel tint
- `colors.primary`: candy red, bright cobalt, sunshine yellow
- `colors.accent`: complementary candy color
- `typography.display.fontFamily`: rounded geometric sans (Recoleta, Nunito, Quicksand, DM Sans)
- `typography.body.fontFamily`: matching rounded sans
- `spacing` scale multiplier: `1x`
- `rounded` scale: pill (full radius on buttons; 20-32px on cards)
- `elevation` profile: layered (cheerful drop shadows in primary color)
- `duration` profile: bouncy (`cubic-bezier(0.34, 1.56, 0.64, 1)`)
**Prompt addendum:** "Round every corner, oversize the headline, animate with bounce; aim for childlike delight."
**Layout hints:**
- Oversized hero copy (`text-9xl` or larger)
- Sticker badges, bouncy hover transforms
- Solid block-color sections with rounded transitions between them
**Signature move:** Hover on the primary CTA triggers a `scale(1.05)` + `rotate(-3deg)` bounce with a cheerful drop-shadow shift.
**Best for:** marketing surfaces (kids, education, creator tools, casual mobile apps)
**Avoid for:** enterprise, finance, healthcare

### editorial-magazine
**Vibe:** High-contrast serif headings, warm neutrals, editorial grid, section numbering — long-form sanctuary.
**Token overrides:**
- `colors.background`: warm paper (`#faf7f0` or `oklch(0.97 0.015 75)`)
- `colors.primary`: deep ink (`#1a1410`)
- `colors.accent`: single muted hue (terracotta, mustard, deep teal)
- `typography.display.fontFamily`: characterful serif (Fraunces, GT Super, Tiempos Headline, Spectral)
- `typography.body.fontFamily`: refined body serif (Source Serif, Lora) or grotesk for contrast
- `spacing` scale multiplier: `1.4x`
- `rounded` scale: subtle (2-4px)
- `elevation` profile: flat (rely on rule lines and typography)
- `duration` profile: gentle (300-400ms)
**Prompt addendum:** "Treat the page as a magazine spread: numbered sections, drop caps, hairline rules, asymmetric grid placement."
**Layout hints:**
- Asymmetric multi-column grid with text wrapping image
- Section numbers (`01.`, `02.`) in display weight
- Drop caps on opening paragraphs
**Signature move:** Section opens with a large-numbered display character (`01`) at 200px weight 200, followed by a drop-cap paragraph that fills the column.
**Best for:** marketing and content surfaces (publication, podcast, long-form storytelling)
**Avoid for:** app screens, checkout flows

### brutalist-raw
**Vibe:** System fonts pushed to extremes, exposed structure, anti-polish — ugly-cool.
**Token overrides:**
- `colors.background`: stark white or stark black
- `colors.primary`: pure black or pure white
- `colors.accent`: single shocking color (electric blue, hazard yellow, blood red)
- `typography.display.fontFamily`: system grotesque or Helvetica at extreme size
- `typography.body.fontFamily`: same system font
- `spacing` scale multiplier: `0.9x` (tight)
- `rounded` scale: sharp (0px everywhere)
- `elevation` profile: flat (zero shadows)
- `duration` profile: none (no transitions, instant state changes)
**Prompt addendum:** "Push system fonts to extreme sizes; expose grid lines; refuse to soften anything; commit fully to anti-polish."
**Layout hints:**
- Hard rule borders (`border: 2px solid black`) everywhere
- Marquee headlines at 200-400px
- Grid lines visible, exposed HTML structure aesthetic
**Signature move:** A `400px` Helvetica Bold headline runs full-bleed across the hero with a hard black border below and a marquee-style auto-scroll subtext.
**Best for:** marketing surfaces (agency, fashion, music label, brand statement)
**Avoid for:** storefronts, app and mobile screens, healthcare

### art-deco
**Vibe:** Gold + black, symmetrical patterns, angular type, ornamental borders — 1920s glamour.
**Token overrides:**
- `colors.background`: deep navy / charcoal / ivory
- `colors.primary`: brass / gold leaf
- `colors.accent`: emerald or oxblood
- `typography.display.fontFamily`: geometric display (Limelight, Poiret One, custom angular)
- `typography.body.fontFamily`: refined serif or geometric sans
- `spacing` scale multiplier: `1.4x`
- `rounded` scale: sharp (0px)
- `elevation` profile: subtle with metallic gradient borders
- `duration` profile: gentle
**Prompt addendum:** "Symmetric ornamental layout, gold-on-dark color, angular geometric type; lean theatrical."
**Layout hints:**
- Symmetric centered composition
- Ornamental geometric borders (chevron, sunburst, fan)
- Hairline gold rules separating sections
**Signature move:** A symmetric sunburst geometric ornament sits behind the hero headline in gold leaf.
**Best for:** marketing surfaces (luxury, hospitality, theatre, event), event microsites
**Avoid for:** app and mobile screens, modern storefronts

### soft-pastel
**Vibe:** Low-contrast pastels, diffused gradients, gentle rounded UI — calm bedroom aesthetic.
**Token overrides:**
- `colors.background`: lavender mist / blush / mint pastel
- `colors.primary`: dusty rose / soft lilac / pale teal
- `colors.accent`: warm peach or butter yellow
- `typography.display.fontFamily`: friendly rounded sans (DM Sans, Nunito, Quicksand)
- `typography.body.fontFamily`: same family
- `spacing` scale multiplier: `1.2x`
- `rounded` scale: medium (16-24px)
- `elevation` profile: subtle with diffused color-tinted shadows
- `duration` profile: gentle
**Prompt addendum:** "Diffuse pastel gradients, soft rounded cards, low-contrast hierarchy; aim for calm and welcoming."
**Layout hints:**
- Diffused radial gradient backgrounds
- Card-based layouts with soft shadows in pastel tints
- Avoid hard color blocks
**Signature move:** Hero background is a diffuse radial gradient transitioning between three pastel hues (lavender → blush → peach).
**Best for:** marketing surfaces (wellness, beauty, lifestyle, mental health, journaling apps), mobile app screens
**Avoid for:** financial, enterprise, gaming

### industrial-utilitarian
**Vibe:** Monospace, high-density data, dark UI, minimal ornamentation — terminal as design language.
**Token overrides:**
- `colors.background`: dark gray (`#0f0f10`) or near-black
- `colors.primary`: white or pale green-tinted neutral
- `colors.accent`: amber, terminal green, or single bright signal color
- `typography.display.fontFamily`: monospace (Berkeley Mono, JetBrains Mono, IBM Plex Mono)
- `typography.body.fontFamily`: same monospace
- `spacing` scale multiplier: `0.85x` (data density)
- `rounded` scale: sharp (0-2px)
- `elevation` profile: flat
- `duration` profile: snappy (100-150ms)
**Prompt addendum:** "Treat the screen as a developer terminal; monospace everything; expose data density; minimal chrome."
**Layout hints:**
- Tabular numerics (`font-variant-numeric: tabular-nums`)
- Grid-aligned data tables with hairline borders
- Dot-grid backgrounds, mono-spaced labels
**Signature move:** All numerics use tabular figures aligned to a monospace grid; headlines are uppercase with letter-spacing.
**Best for:** marketing surfaces (dev tools, infra, AI infra, B2B SaaS), app dashboards
**Avoid for:** consumer marketing, lifestyle, storefronts

### neo-grotesque
**Vibe:** Swiss-style grids, tight leading, limited palette, extreme alignment precision — design as system.
**Token overrides:**
- `colors.background`: pure white or near-black
- `colors.primary`: black or white
- `colors.accent`: single bold color (red, blue, yellow — Bauhaus primaries)
- `typography.display.fontFamily`: neo-grotesk (Helvetica Now, GT America, Söhne, Inter Tight)
- `typography.body.fontFamily`: same family
- `spacing` scale multiplier: `1.1x`
- `rounded` scale: sharp (0px)
- `elevation` profile: flat
- `duration` profile: snappy
**Prompt addendum:** "Strict Swiss grid, tight leading, flush-left alignment, single accent; objectivity and clarity."
**Layout hints:**
- 12-column grid visible in baseline
- Tight letter-spacing on display, generous leading on body
- One accent color used at exactly one spot per viewport
**Signature move:** Display headline at weight 900 with `-0.04em` letter-spacing flush-left in column 1, paired with a single small accent dot in column 12.
**Best for:** marketing and content surfaces (design portfolio, agency, brand book, editorial)
**Avoid for:** gaming, kids, festive marketing

### kinetic-motion-first
**Vibe:** Interface built around transition — parallax, morphing shapes, scroll-driven narrative.
**Token overrides:**
- `colors.background`: dynamic (changes per scroll section)
- `colors.primary`: vibrant accent that morphs per section
- `colors.accent`: contrast color for motion focus
- `typography.display.fontFamily`: variable font (Inter Variable, Recursive, Mona Sans) for motion-tuned axes
- `typography.body.fontFamily`: matching variable font
- `spacing` scale multiplier: `1.2x`
- `rounded` scale: medium (8-16px)
- `elevation` profile: layered (depth via motion + parallax)
- `duration` profile: gentle long (600-1200ms with scroll-driven keyframes)
**Prompt addendum:** "Choreograph the page around scroll progress; let motion carry the narrative; use variable font axes for transition moments."
**Layout hints:**
- Scroll-triggered reveals with `IntersectionObserver` or `animation-timeline: scroll()`
- Pinned sections that morph over scroll distance
- Variable font weight/width transitions on hover/scroll
**Signature move:** Hero headline morphs its variable font weight from 100 to 900 over the first 600px of scroll, while background hue shifts across the spectrum.
**Best for:** marketing surfaces (brand statement, product launch, portfolio, agency)
**Avoid for:** app and mobile screens, checkout flows, dashboards
