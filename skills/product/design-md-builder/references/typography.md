# Typography

Choosing faces, pairing them, and building a scale that reads as designed. Read alongside `anti-slop.md`.

## When to Use

Load only when authoring, assessing, refreshing, or reviewing typography. Preserve exact source values for inherit and sync; use the active register to bias new choices.

## The typeface library

Organized by classification. **(F)** = free/open-source, **(C)** = commercial license required. There are strong open options in every category, so a good typographic system never requires a licensing budget.

### Neo-grotesque sans — neutral, structural, Swiss

The workhorse category. Neutral but not characterless.

- **Söhne** (C) — Klim's Helvetica reinterpretation; the current standard for considered neutral. Excellent Buch/Kräftig weights.
- **Neue Haas Grotesk** (C) — Helvetica as originally drawn, before the 1980s digitization damaged it.
- **Untitled Sans** (C) — Klim; slightly warmer and more workmanlike than Söhne.
- **Basis Grotesque** (C) — Colophon; subtle quirks that survive at small sizes.
- **Archivo** (F) — Omnibus-Type. Genuinely good, variable, with a real condensed family. Strongly underused.
- **Public Sans** (F) — USWDS; neutral, legible, institutionally credible. Used in the DESIGN.md spec's own examples.
- **Geist** (F) — Vercel; clean, modern, with a matching mono.
- **Inter** (F) — excellent, and everywhere. Usable *deliberately* — set optical sizing, enable `cv05`/`cv11` for the single-storey alternates, use the variable axes. Reflexive use is the problem, not the face.
- **Helvetica Now** (C) — the good modern Helvetica, with a genuine Micro optical size.

### Humanist sans — warmer, calligraphic skeleton

- **Ideal Sans** (C) — H&Co; unusually warm, subtle irregularity.
- **Freight Sans** (C) — large family, wide range.
- **IBM Plex Sans** (F) — engineered warmth; superb mono and serif companions in the same family. Excellent for clinical/technical contexts.
- **Source Sans 3** (F) — Adobe; quiet, legible, dependable.
- **Work Sans** (F) — optimized for screen at middle sizes.

### Geometric sans — constructed, Bauhaus-descended

- **Futura** (C) / **Neue Haas Unica** (C) — the originals.
- **Jost** (F) — a well-made Futura interpretation, variable.
- **Space Grotesk** (F) — geometric with mono-derived quirks; distinctive without being loud.
- Avoid **Poppins**, **Montserrat**, **Century Gothic** as defaults — technically fine, but so overused they now signal absence of choice.

### Serif — text

For body copy, long-form, and anything wanting gravity.

- **Tiempos Text** (C) — Klim; the modern standard for screen serif body.
- **Lyon** (C) — Commercial Type; editorial authority.
- **Freight Text** (C) — warm, wide range of optical sizes.
- **Source Serif 4** (F) — Adobe; variable, excellent on screen, genuinely good.
- **Literata** (F) — Google Books; engineered for extended reading.
- **Newsreader** (F) — variable with an optical size axis; editorial character.
- **EB Garamond** (F) — a proper Garamond revival; classical style.
- **IBM Plex Serif** (F) — pairs natively with Plex Sans and Mono.

### Serif — display

High contrast, meant for large sizes.

- **Canela** (C) — Commercial Type; the serif-sans hybrid that defined a decade of luxury branding.
- **GT Sectra** (C) — Grilli Type; calligraphic and sharp, brilliant editorial display.
- **Ogg** (C) — Sharp Type; calligraphic, distinctive.
- **Tiempos Headline** (C) — tighter, more dramatic cut of Tiempos.
- **Fraunces** (F) — variable with `SOFT`, `WONK`, and optical size axes. Genuinely characterful and the strongest free display serif available.
- **Instrument Serif** (F) — high contrast, elegant, free.
- **Playfair Display** (F) — competent, but now the default "elegant" choice; treat it the way you'd treat Inter.

### Slab serif

- **Zilla Slab** (F) — Mozilla; geometric slab with personality.
- **Bitter** (F) — contemporary slab for screen.
- **Roboto Slab** (F) — neutral; the Inter of slabs.

### Monospace

For code, numerics, identifiers, timestamps, and anything tabular.

- **Berkeley Mono** (C) — the current enthusiast standard; genuine technical character.
- **Commit Mono** (F) — neutral, highly legible, customizable at download.
- **JetBrains Mono** (F) — tall x-height, designed for long code sessions.
- **IBM Plex Mono** (F) — pairs with the Plex family.
- **Geist Mono** (F) — pairs with Geist.
- **Departure Mono** (F) — pixel/bitmap; perfect for Retro-Futurist HUD, wrong for almost everything else.
- **SF Mono** / **Menlo** — available on Apple platforms; fine as a fallback.

### Condensed & display

- **Archivo Narrow** / **Archivo Condensed** (F) — the reliable condensed workhorse.
- **Anton** (F) — heavy condensed display; strong poster presence.
- **Roboto Condensed** (F) — neutral, map-and-label style.
- Avoid **Oswald** and **Bebas Neue** as defaults — heavily overused.

## Verdicts

**Pair across classifications, not within them.** Two grotesques together is an accident nobody reads as intentional.

**Divide by job, not by size.** One face carries the *voice* (display, headings, body prose), the other the *apparatus* (labels, metadata, numerics, UI chrome). Reader-facing against machine-facing survives at every size.

**Two faces is the target. Three needs a reason** — a superfamily, or a genuinely distinct third job. One is legitimate when the range is actually used: a single face at three sizes and two weights is not a typographic system.

**Break the scale at the display end.** A generated scale is always too timid where impact matters. The gap between body and display should read as a jump, not a progression. Name levels by role (`display`, `headline-lg`, `body-md`, `label-caps`, `data-md`), never by size.

**Two weights, far apart.** 400 and 700 reads as a decision; 400/500/600 reads as indecision. A third weight is a genuine extreme with a specific job. Prefer size and space to weight for hierarchy — weight is the loudest tool and the first one overused. Never synthesize a cut the face does not ship.

**A single line-height across the whole scale is a tell.** So is default tracking on uppercase. Optical adjustment is where a system stops looking like defaults: invisible one at a time, unmistakable in aggregate.

**Set the measure explicitly** (`max-width: 65ch`) rather than letting the container decide. Space above a heading is larger than space below it — the heading belongs to what follows.

**`onum` is wrong in UI**, right in editorial body text. Disable `liga` in code contexts, where `!=` should not fuse.

**Constrain a variable font anyway.** Pick two or three instances and treat them as the only cuts available.

**Specify a real fallback stack**, not `sans-serif`. If the brand face fails to load, what remains must still be a defensible choice. Note the stack in the DESIGN.md prose; the tokens carry `fontFamily` as a single name.

**Commercial licensing is per-use** — web, app, and desktop are typically separate. If the product ships a native app, flag it.

## Writing typography tokens

Name by role, cover the full range, and set every property that carries a decision:

```yaml
typography:
  display:
    fontFamily: Fraunces
    fontSize: 72px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -0.03em
  headline-lg:
    fontFamily: Fraunces
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: -0.02em
  body-md:
    fontFamily: Archivo
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: Archivo
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: 0.12em
  data-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: 400
    lineHeight: 1.45
    fontFeature: "'tnum' 1"
```

Every level differs in more than size — tracking, line-height, and family all carry information. That is what distinguishes a typographic system from a list of font sizes.

Faces with an `opsz` axis (Fraunces, Newsreader, Source Serif 4, Inter) adjust contrast and spacing for the size they are set at; the spec supports `fontFeature` and `fontVariation` for that and for stylistic sets:

```yaml
typography:
  display-lg:
    fontFamily: Fraunces
    fontSize: 72px
    lineHeight: 1.05
    letterSpacing: -0.03em
    fontVariation: "'wght' 600, 'SOFT' 40, 'WONK' 1, 'opsz' 72"
```
