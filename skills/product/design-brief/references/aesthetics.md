# Design Aesthetics

Self-contained design principles for visual direction and token authoring.
Apply these when exploring a mood and when choosing token values for DESIGN.md.

## When to Use

Auto-loaded by `direction.md` (mood vocabulary — Four Questions, Style Axes) and
by `design.md` (token-authoring principles — Typography, Color, Spatial, Motion,
Depth). Not a direct trigger.

## Design Thinking

### Four Questions

Before any visual work, answer these to lock in a direction:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick a clear aesthetic — compose across the Style Axes below, biased by the register ([brand.md](brand.md) / [product.md](product.md)).
3. **Constraints**: Technical requirements (framework, performance, accessibility).
4. **Signature**: What single detail will make this _unforgettable_? (A motion moment, a typographic trick, an unusual color move.) Every project needs one.

### Style Axes

Visual direction is a composition of four orthogonal axes. Pick one pattern
from each axis — or blend two within the same axis — to construct a unique
direction. Compositions like "Bento Grid + Glassmorphism + Cyberpunk + Duotone"
produce more distinctive results than single-tone choices.

| Axis | Patterns |
|------|----------|
| **Layout & Structure** | Bento Grid (modular boxy cards), Editorial (magazine feel, large serifs, asymmetric placement, generous whitespace), Swiss Style (strict grids, sans-serif, flush-left, objective clarity), Split-Screen (vertical division, color block paired with full-bleed imagery), Asymmetric Modular (intentional off-grid composition with rhythm) |
| **Texture & Depth** | Glassmorphism (translucency, backdrop blur, frosted edges), Claymorphism (soft inflated 3D shapes, inner shadows, tactile), Skeuomorphic (realistic materials — leather, paper, metal), Grainy / Noise (film grain or noise overlay reduces digital shine), Flat (no texture, intentional restraint) |
| **Atmosphere & Era** | Brutalist (raw, default fonts, hard edges, "ugly-cool"), Cyberpunk (neon on dark, glitch effects, tech-heavy), Y2K (late 90s/2000s optimism, chrome, pill shapes, bright), Retro-Futurism (80s synthwave, sunsets, wireframe grids, glow), Modern Minimal (timeless restraint, no era signals) |
| **Color & Contrast** | Duotone (two contrasting colors and their shades only), Monochromatic (single hue across all surfaces), Pastel Goth (milky pastels with stark black type and borders), Dark Mode OLED (true `#000000` for OLED punch on hero surfaces; soften body surfaces to dark grey to avoid halation and improve legibility), Earth Tones (warm naturals, restrained saturation) |

## Token Authoring Principles

What makes a good choice for each token group. Compose these biased by the
register ([brand.md](brand.md) / [product.md](product.md)).

### Typography

- **Pairings must be distinctive**: never default to Inter, Roboto, Arial, or system fonts as primary choice for a marketing or editorial identity. Pair a characterful display font with a refined body font. System stacks are acceptable for app and dashboard surfaces where performance and native feel matter.
- **Weight extremes**: use 100-200 for subtlety and 800-900 for impact within the same scale.
- **Size jumps**: display should be at least 3x body size. Timid 1.5x ratios flatten hierarchy.
- **Loading strategy**: author `font-display: swap` (or `optional` for zero layout shift) with a metric-matched fallback (`size-adjust`) to tame it; preload only the critical above-the-fold weight, and reach for a variable font once a family needs 3+ weights.

### Color and Theme

- **Token-first**: define each color once as a named role and reference it by role everywhere, never as a loose literal.
- **60-30-10**: 60% dominant surface, 30% secondary, 10% accent. Sharp accents on a committed base outperform timid evenly-distributed palettes.
- **Dominant + accent**: pick one hero color and one contrast accent. Two accents maximum.
- **Theme commitment**: go fully dark or fully light per surface. Half-measures read as unfinished.
- **Tinted neutrals**: pure gray is dead — give each neutral a trace of chroma (~0.005–0.015 in OKLCH) hued toward the brand. Don't reflexively reach for warm-orange or cool-blue neutrals; the tint is a deliberate choice.
- **Alpha is a smell**: heavy `rgba`/`hsla` overlays signal an incomplete palette — author explicit overlay and surface tokens instead of leaning on opacity.
- **Dark mode is not inverted light**: build depth from a stepped surface-lightness scale, not borrowed shadows, and desaturate accents so they don't vibrate on dark.

### Spatial Composition and Whitespace

- **Generous whitespace or controlled density**: both work — the crime is the lukewarm middle. Pick a spacing scale that commits.
- **Rhythm**: a consistent base unit (4px / 8px grid) with a deliberate scale reads as intentional; ad-hoc values read as noise.
- **Measure & leading**: body copy at 60-75 characters per line — size the body token and container width to land there; loosen line-height as the measure widens, since long lines need more leading to track.

### Motion and Interaction

- **Easing per tone**: pick `cubic-bezier` curves that match the tone — snappy (`0.22, 1, 0.36, 1`) for tech, gentle (`0.25, 0.1, 0.25, 1`) for editorial, bouncy (`0.34, 1.56, 0.64, 1`) for playful. Never leave `ease` as default without intention.
- **Duration tiers**: a fast tier for state feedback (hover/focus), a base tier for transitions, a slow tier for deliberate reveals. Keep the spread perceptible.

### Depth and Elevation

- **Shadow system, three levels**: subtle (cards at rest), medium (raised / hover), elevated (modals, dropdowns, popovers). Define the elevation scale once and apply by role.
- **Match shadow to surface**: on dark backgrounds light shadows vanish — use denser, higher-opacity shadows so depth registers.
