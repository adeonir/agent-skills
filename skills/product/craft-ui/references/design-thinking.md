# Design Thinking

How to decide a visual direction before any pixels — the questions, axes, and reflex-checks that keep a result from collapsing into the generic default.

## When to Use

Composed by `render.md` to choose a direction before generating, and by `critique.md` for the slop verdict (Step 2). Not a direct trigger.

## Four Questions

Before any visual work, answer these to lock in a direction:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick a clear aesthetic — compose across the Style Axes below.
3. **Constraints**: Technical requirements (framework, performance, accessibility).
4. **Signature**: What single detail will make this _unforgettable_? (A motion moment, a typographic trick, an unusual color move.) Every project needs one.

## Style Axes

Visual direction is a composition of four orthogonal axes. Pick one pattern from each axis — or blend two within the same axis — to construct a unique direction. Compositions like "Bento Grid + Glassmorphism + Cyberpunk + Duotone" produce more distinctive results than single-tone choices.

| Axis | Patterns |
|------|----------|
| **Layout & Structure** | Bento Grid (modular boxy cards), Editorial (magazine feel, large serifs, asymmetric placement, generous whitespace), Swiss Style (strict grids, sans-serif, flush-left, objective clarity), Split-Screen (vertical division, color block paired with full-bleed imagery), Asymmetric Modular (intentional off-grid composition with rhythm) |
| **Texture & Depth** | Glassmorphism (translucency, backdrop blur, frosted edges), Claymorphism (soft inflated 3D shapes, inner shadows, tactile), Skeuomorphic (realistic materials — leather, paper, metal), Grainy / Noise (film grain or noise overlay reduces digital shine), Flat (no texture, intentional restraint) |
| **Atmosphere & Era** | Brutalist (raw, default fonts, hard edges, "ugly-cool"), Cyberpunk (neon on dark, glitch effects, tech-heavy), Y2K (late 90s/2000s optimism, chrome, pill shapes, bright), Retro-Futurism (80s synthwave, sunsets, wireframe grids, glow), Modern Minimal (timeless restraint, no era signals) |
| **Color & Contrast** | Duotone (two contrasting colors and their shades only), Monochromatic (single hue across all surfaces), Pastel Goth (milky pastels with stark black type and borders), Dark Mode OLED (true `#000000` for OLED punch on hero surfaces; soften body surfaces to dark grey to avoid halation and improve legibility), Earth Tones (warm naturals, restrained saturation) |

Executing a named axis well is not wearing its costume. A cell names the lane; the craft is in *how* you build it. Brutalist done right, for instance, is engineered extreme type-scale contrast (a heavy grotesque display against small wide-tracked mono, or a deliberate raw-default-font take), a single utilitarian accent held under strict restraint, grid-anchored compartmentalization with 90° rigidity, and bimodal density (dense data against vast negative space). The costume version copies the hard corners and stops, with no structure beneath. Test any named style: do its elements reference a real function, or only cosplay one?

## Density & Variance

Two dials name what the Style Axes leave qualitative — read each 1–10 against the brief:

- **Visual density** (1 = art gallery, huge gaps and few elements → 10 = cockpit, tight rows, 1px separators, mono figures). A dashboard for scanning wants high density; a premium landing wants low.
- **Design variance** (1 = symmetric, predictable grid → 10 = offset overlaps, fractional grids, large empty zones). Low reads calm and safe; high reads editorial and bold.

`render` targets the level the brief implies; `critique` reports the level it measures against the level intended ("reads density 8, the brief wanted 4"). The dials are a read, not a score — they sharpen the verdict, they do not enter the `/40` or `/20`.

## Scene Sentence

Before choosing light vs dark or warm vs cool, write one sentence of physical scene: who uses this surface, where, under what ambient light, in what mood. The sentence should force the answer — "a barista checking inventory on a bright tablet behind the counter" forces light; "a trader scanning positions at 2am" forces dark. If the sentence does not decide it, it is not concrete enough — add detail until it does.

## Color Strategy

Color commitment is an axis, not a binary. Name the step before picking values:

- **Restrained** — tinted neutrals plus one accent ≤10% of the surface.
- **Committed** — one saturated color carries 30–60% of the surface.
- **Full palette** — 3–4 named roles, each used deliberately.
- **Drenched** — the surface *is* the color.

Brand surfaces have permission for Committed, Full palette, and Drenched — unnamed ambition collapses into timid neutrals. Product surfaces default to Restrained, earning Committed only where one screen carries a category color. (The register sets which permissions apply — see [brand.md](brand.md) / [product.md](product.md).)

Register follows the surface's job, not its name. The default is landing = brand, but a landing for a dev tool, CLI, or infra product often reads more premium in a compact *product* register — dense command fields, code cards, live micro-demos, spacing doing the work — than in a wide brand-marketing layout. Let the audience decide the register, not the surface label.

## The Slop Test

The cheapest way to catch a generic result is to try to guess it from the outside. Run two altitudes.

1. **Category reflex.** Could someone name the category and guess the whole look — theme, palette, layout — from the category alone? "Fintech, so a dark-blue gradient and a hero metric." If the category predicts the design, it is the first-order training-data default.
2. **Anti-reference reflex.** Name the aesthetic lane the work is actually in (the reference). Could someone guess that lane from "category plus the anti-references"? Judge against the anti-references declared in `PRODUCT.md` when present, inferring the obvious ones only when it is absent. Reaching for editorial-magazine on a brief that is not editorial is the trap one tier deeper.

Then the inverse: describe in one sentence what you are about to build the way a competitor would describe theirs. If that sentence fits the modal page in the category, restart.

Some categories carry a reflex palette the whole field defaults to — beige-and- cream with brass, clay, or oxblood for cookware, wellness, and premium-consumer brands; dark-blue gradients for fintech. Reaching for the category's stock palette is the anti-reference reflex in color form: name the reflex palette for this category and treat it as a default to earn past, not the safe choice.

### The warm-neutral trap

A near-white warm-tinted background — the cream / sand / beige / paper band — is the default an interface reaches for when a brief says "warm", "editorial", or "traditional". The whole warm-neutral band (very light, barely saturated, a hue in the warm range) reads as cream/sand whatever the token is named. Renaming it `--paper`, `--bone`, `--linen`, or `--parchment` does not make it a decision. "Warm" does not mean near-white-with-a-tint — commit to an actual color strategy instead of defaulting to the warm-neutral wash.

### The craft checks

Four cheap reflexes catch a default before it ships. Run them on any variant:

- **Swap test** — swap the typeface for the category's usual one and the layout for a standard template. If nothing would feel different, that is where you defaulted.
- **Token test** — read the CSS variable names and values aloud. Do they belong to *this* product's world, or would they sit in any project? A `--paper` / `--gray-200` / `--space-4` that fits any file signals no system.
- **Signature test** — point to specific elements where the Signature (Question 4) actually appears. "The overall feel" does not count; name the elements.
- **Squint test** — blur your eyes; hierarchy still readable, nothing jumping out harshly. (Defined in [heuristics.md](heuristics.md) and [layout.md](layout.md).)

Name the defaults before avoiding them: list the 3 obvious choices for this interface type — visual *and* structural — so the reflexes above have something concrete to reject. You cannot avoid a pattern you have not named.

## Complexity Calibration

Match implementation effort to the aesthetic vision:

- **Maximalist / kinetic / retro-futuristic**: elaborate code is expected. Layer animations, textures, custom cursors, parallax, grain overlays. The detail IS the design.
- **Minimal / luxury / neo-grotesque**: restraint is the skill. Fewer elements, each pixel-perfect. Spacing, weight, and color precision carry the result. The failure mode is empty, not busy: disciplined minimal still supplies depth — through near-invisible means (low-opacity imagery, a warm radial light, grain, hairline structure), not by adding elements — and lets contrast migrate to type-role (display serif vs sans vs mono) and whitespace rather than color. Motion stays quiet too.
- **Middle-ground tones** (editorial, startup, organic): balance detail and restraint. One or two signature moments plus polished fundamentals.

If the tone is bold, don't write timid code. If refined, don't overload with effects.

## Creative Mandate

Every generation must feel like a different designer made it. Vary fonts, color temperature, layout geometry, motion style, and density between builds. Never converge on a "house style" across variants or successive generations.

Interpret creatively. Make unexpected choices that feel genuinely designed for the context. Commit fully to the chosen direction.
