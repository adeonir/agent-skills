# Color

How to apply color with purpose — OKLCH, palette structure, contrast, dark mode,
atmosphere. The color *strategy* (Restrained / Committed / Full palette /
Drenched) is a direction decision in [design-thinking.md](design-thinking.md);
this file is the *how*. Strategic color beats rainbow vomit — every color earns
a purpose.

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md` /
`audit.md` (judge a rendered surface against it). Not a direct trigger.

## Register sets the dose

- **Brand** — palette IS voice. Pick a strategy first; Committed / Full palette /
  Drenched deliberately exceed the ≤10% accent rule (that rule is Restrained
  only). A dominant color can own the page. See [brand.md](brand.md).
- **Product** — semantic-first, almost always Restrained. Accent is reserved for
  primary action, current selection, and state — never decoration. Every color
  has one consistent meaning across every screen. See [product.md](product.md).

## Color space: OKLCH

Use **OKLCH**, not HSL. It is perceptually uniform — equal steps in lightness
*look* equal (in HSL, 50% lightness in yellow looks bright, in blue looks dark).

`oklch(lightness chroma hue)` — lightness 0–100%, chroma ~0–0.4, hue 0–360. To
build a color and its lighter/darker shades, hold chroma + hue roughly constant
and vary lightness — but **reduce chroma as you approach white or black**, or
high chroma at the extremes looks garish.

The hue is a **brand decision**, never a default. Don't reach for blue (~250) or
warm orange (~60) by reflex — those are the dominant AI-design defaults, not the
right answer for any specific brand.

## Tinted neutrals

**Pure gray is dead** — zero-chroma neutrals feel lifeless next to a colored
brand. Add a tiny chroma (0.005–0.015) to every neutral, hued toward the brand
color. Small enough not to read as "tinted," big enough to create subconscious
cohesion.

Tint toward **this project's** brand hue, not a "warm = friendly / cool = tech"
formula. Always-warm-orange or always-cool-blue are the two laziest defaults and
breed cross-project monoculture.

One palette per project — the neutral tint points a single direction. Never mix a
warm grey in one section with a cool grey in another; mixed grey temperatures read
as two palettes bolted together, not as variety.

## Palette structure

| Role | Purpose | Shape |
|------|---------|-------|
| **Primary** | Brand, CTAs, key actions | 1 color, 3–5 shades |
| **Neutral** | Text, backgrounds, borders | 9–11 shade scale |
| **Semantic** | Success, error, warning, info | 4 colors, 2–3 shades each |
| **Surface** | Cards, modals, overlays | 2–3 elevation levels |

Skip secondary/tertiary unless genuinely needed — most surfaces work with one
accent. More colors create decision fatigue and noise.

## 60-30-10 (visual weight, not pixel count)

- **60%** — neutral backgrounds, whitespace, base surfaces
- **30%** — secondary: text, borders, inactive states
- **10%** — accent: CTAs, highlights, focus

The accent works *because* it is rare. The common failure is using the brand
color everywhere "because it's the brand"; overuse kills its power. Define the
palette once as CSS variables in `:root`, reference everywhere.

## Semantic color

Consistent meaning across the whole surface — green always = success.

- Success → green (emerald/forest/mint); Error → red/rose/coral; Warning →
  amber; Info → blue/sky/indigo; Neutral/inactive → gray/slate.
- Status badges: colored background or full hairline border. Progress: colored
  bars/rings.

## Accent application

Primary actions, links (keep contrast), key icons, active headers, hover/focus.
Reserve heavy color for active states; inactive stays neutral.

Lock the accent page-wide: one accent, applied consistently across every section.
Audit for drift — a slightly different accent hue surfacing in a later section (a
second blue, a shifted teal) reads as the system slipping, not as variety.

## Harmony & orphan accents

Every accent derives from the palette's hue family — never dropped in from
outside it. An accent whose hue has no relation to the brand reads as a mistake,
however small the element (a divider rule, an icon glyph, a badge).

Choose the wheel relationship on purpose:

- **Analogous** (hues within ~30°) — cohesive; the calm brand harmony.
- **Complementary** (~180° apart) — high tension, deliberate only and dosed: one
  side dominant, the other a sharp accent. Two saturated complements at equal
  weight vibrate; the red↔green pair also fails color-blind users.
- **Triadic / split-complementary** — lively, but needs one clear dominant;
  rarely does more than one true accent earn the page.

Two failure shapes:

- **Orphan accent** — a hue that belongs to no defined role. A red divider and a
  green icon on a warm-brown brand are two orphans that also clash across the
  wheel; neither derives from the palette.
- **Borrowed brand color used raw** — a service's own color (a messaging green, a
  social blue) dropped in at full saturation. Reconcile it: tint or desaturate
  toward the palette, or render the mark in a brand or neutral color.

## Backgrounds & atmosphere

- **Create depth, not flatness** — gradient meshes, noise, grain, layered
  transparencies. Match texture to tone (organic → soft gradients, brutalist →
  noise, luxury → subtle grain).
- **Tint surfaces toward the brand hue**, not "for warmth" by reflex. The
  default-warm tint (`oklch(97% 0.01 60)` and neighbors) is the AI cream/sand
  giveaway — be specific to the brand or stay neutral (see the warm-neutral trap
  in [design-thinking.md](design-thinking.md)).
- **Dark sections earn their weight** — a dark hero or footer anchors the page.
- **Never default to flat solid white** unless that IS the statement (minimal).
- Gradients: intentional and brand-relevant, never the generic purple→blue.

## Contrast & accessibility

| Content | AA minimum | AAA target |
|---------|-----------|-----------|
| Body text | 4.5:1 | 7:1 |
| Large text (18px+ / 14px bold) | 3:1 | 4.5:1 |
| UI components, icons | 3:1 | 4.5:1 |

Dangerous combinations that fail or vibrate: light gray on white (the #1 fail);
red↔green (8% of men can't distinguish); blue on red; yellow on white; thin light
text over images. **Don't rely on color alone** — pair with icon, label, or
pattern. Don't trust your eyes; verify with a contrast checker and vision-deficiency
emulation.

## Dark mode is not inverted light mode

Different decisions, not a swap:

| Light | Dark |
|-------|------|
| Shadows for depth | Lighter surfaces for depth (no shadows) |
| Dark text on light | Light text on dark — reduce weight (~350 vs 400) |
| Vibrant accents | Desaturate accents slightly |
| White background | Pure black **or** a brand-tinted near-black (oklch 12–18%) |

Depth comes from **surface lightness**: a 3-step scale where higher elevations
are lighter (15% / 20% / 25%), same hue + chroma as the brand, only lightness
varies. Token hierarchy: primitives (`--blue-500`) + semantic
(`--color-primary: var(--blue-500)`); for dark mode, redefine only the semantic
layer.

## Alpha is a design smell

Heavy `rgba`/`hsla` usually means an incomplete palette — it creates
unpredictable contrast and inconsistency. Define explicit overlay colors per
context instead. Exception: focus rings and interactive states that need
see-through.

## Color anti-defaults

- Gray text on a colored/saturated background → use a darker shade of the
  background's own hue, or a transparency of the text color (never muted gray).
- `border-left/right` > 1px as a colored accent stripe → full hairline border,
  a 4–8% background wash, a leading glyph, or a number (also in
  [anti-patterns.md](anti-patterns.md)).
- Purple→blue gradient default; the warm-neutral cream/sand wash.
- Rainbow vomit — color applied without semantic meaning. 2–4 colors beyond
  neutrals, max.
