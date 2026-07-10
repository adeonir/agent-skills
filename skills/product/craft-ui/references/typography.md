# Typography

Type carries most of the information on a surface. Recipes for scale, pairing, loading, and detail — replacing generic defaults (Inter/Roboto at a flat scale) with type that reflects the brand and scales with intentional contrast. The brand font-selection procedure lives in [brand.md](brand.md); this is the *how*.

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md` (judge a rendered surface against it). Not a direct trigger.

## Register sets the scale

- **Brand** — run the font-selection procedure in [brand.md](brand.md). Fluid `clamp()` scale, ≥1.25 ratio between steps.
- **Product** — system fonts and familiar sans stacks are legitimate; one well-tuned family usually carries the whole UI. Fixed `rem` scale, 1.125–1.2 ratio. See [product.md](product.md).

## Vertical rhythm

Line-height is the base unit for all vertical spacing. Body at `line-height: 1.5` on 16px (= 24px) → spacing values are multiples of 24px. Text and space sharing one mathematical foundation reads as subconscious harmony.

## Modular scale & hierarchy

The common failure is too many sizes too close together (14/15/16/18px) — muddy hierarchy. **Fewer sizes, more contrast.** Five cover most needs:

| Role | Ratio | Use |
|------|-------|-----|
| xs | 0.75rem | captions, legal |
| sm | 0.875rem | secondary UI, metadata |
| base | 1rem | body |
| lg | 1.25–1.5rem | subheadings, lead |
| xl+ | 2–4rem | headlines, hero |

Pick one ratio and commit: 1.25 (major third), 1.333 (perfect fourth), 1.5 (perfect fifth). Combine size + weight + color + space for hierarchy — never size alone. Heading-to-body size jumps want ≥3:1; timid 1.5x flattens.

## Readability & measure

- `max-width` in `ch` (`65ch`); line-height scales inversely with line length — narrow columns tighter, wide columns looser. Headings 1.1–1.2, body 1.5–1.7.
- Body text ≥16px / 1rem.
- **Light-on-dark needs three-axis compensation**, not one: +0.05–0.1 line-height, +0.01–0.02em letter-spacing, and step body weight up one notch (regular → medium). Perceived weight drops on all three; fix all three.
- Paragraph rhythm: space between paragraphs OR first-line indent, never both.

## Pairing

You often don't need a second font — one well-chosen family in multiple weights beats two competing typefaces. Add a second only for genuine contrast, and pair on an axis: serif + sans (structure), geometric + humanist (personality), condensed + wide (proportion). Never pair two fonts that are similar but not identical (two geometric sans). System fonts are underrated for app UI where performance beats personality (`-apple-system, system-ui` loads instantly).

## Selection reflexes to resist

The lazy move maps a brief straight to its cliché font — resist these:

- A technical or developer brief does not need a serif for "warmth".
- An editorial or premium brief does not need the trendy expressive serif.
- A children's product does not need a rounded display font — real kids' books use real type.
- A modern brief does not need yet another geometric sans.

The cliché is the AI default; pick type from the actual voice, not the category.

## Web font loading

The layout-shift problem: fonts load late, text reflows, content jumps.

- `font-display: swap` (show fallback, swap when ready) — or `optional` (use fallback if the web font misses a ~100ms budget; zero shift).
- Metric-matched fallback via `size-adjust` / `ascent-override` / `descent-override` to minimize shift (Fontaine automates it).
- Preload the **critical weight only** (regular body, above the fold).
- Variable fonts for 3+ weights (one file beats three statics, plus `font-optical-sizing: auto`); static is fine for 1–2.

## Fluid vs fixed

- **Marketing / content headings** — fluid `clamp(min, preferred, max)`; bound it `max ≤ ~2.5 × min` or zoom/reflow break and large viewports shout. Scale container width and font-size together to hold 45–75ch.
- **App UI / dashboards** — fixed `rem` scale (optionally adjusted at 1–2 breakpoints). No major design system uses fluid type in product UI; fixed gives the spatial predictability container layouts need. Body stays fixed even on marketing pages.

## Detail & polish

- OpenType: `font-variant-numeric: diagonal-fractions`, `font-variant-caps: all-small-caps`, `font-variant-ligatures: none` in code, `font-kerning: normal`. `tabular-nums` on data/number columns.
- All-caps tracking: capitals sit too close — add 0.05–0.12em on short all-caps labels and eyebrows.
- Semantic token names (`--text-body`, `--text-heading`), not value names (`--font-16`).

## Typography anti-defaults

- More than 2–3 font families.
- Inter/Roboto/Open Sans by default when personality matters.
- Arbitrary sizes; body below 16px; `px` for font sizes (use `rem`).
- Decorative/display fonts for body text.
- `user-scalable=no` / disabled zoom — fix the layout if it breaks at 200%.
