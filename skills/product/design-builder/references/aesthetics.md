# Design Aesthetics

Self-contained design principles for variant generation and frontend building.
Apply these guidelines to every visual decision -- they replace any external design skill dependency.

## When to Use

Auto-loaded by preview.md as design principles. Not a direct trigger.

## Design Thinking

### Four Questions

Before any visual work, answer these to lock in a direction:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick a clear aesthetic — invoke a named preset from [presets.md](presets.md) or compose across Style Axes below.
3. **Constraints**: Technical requirements (framework, performance, accessibility).
4. **Signature**: What single detail will make this _unforgettable_? (A motion moment, a typographic trick, an unusual color move.) Every project needs one.

### Style Axes

Visual direction is a composition of four orthogonal axes. Pick one pattern
from each axis -- or blend two within the same axis -- to construct a unique
direction. Compositions like "Bento Grid + Glassmorphism + Cyberpunk + Duotone"
produce more distinctive results than single-tone choices.

| Axis | Patterns |
|------|----------|
| **Layout & Structure** | Bento Grid (modular boxy cards), Editorial (magazine feel, large serifs, asymmetric placement, generous whitespace), Swiss Style (strict grids, sans-serif, flush-left, objective clarity), Split-Screen (vertical division, color block paired with full-bleed imagery), Asymmetric Modular (intentional off-grid composition with rhythm) |
| **Texture & Depth** | Glassmorphism (translucency, backdrop blur, frosted edges), Claymorphism (soft inflated 3D shapes, inner shadows, tactile), Skeuomorphic (realistic materials -- leather, paper, metal), Grainy / Noise (film grain or noise overlay reduces digital shine), Flat (no texture, intentional restraint) |
| **Atmosphere & Era** | Brutalist (raw, default fonts, hard edges, "ugly-cool"), Cyberpunk (neon on dark, glitch effects, tech-heavy), Y2K (late 90s/2000s optimism, chrome, pill shapes, bright), Retro-Futurism (80s synthwave, sunsets, wireframe grids, glow), Modern Minimal (timeless restraint, no era signals) |
| **Color & Contrast** | Duotone (two contrasting colors and their shades only), Monochromatic (single hue across all surfaces), Pastel Goth (milky pastels with stark black type and borders), Dark Mode OLED (true `#000000` for OLED punch on hero surfaces; soften body surfaces to dark grey to avoid halation and improve legibility), Earth Tones (warm naturals, restrained saturation) |

For pre-blended named tones with full token recipes, see [presets.md](presets.md).

## UX Heuristics

Nielsen's ten usability heuristics applied to visual interface decisions.
Each heuristic shapes how a design communicates state, action, and recovery
through the rendered surface — not just the underlying interaction logic.

### 1. Visibility of system status

The interface always shows where the user is and what is happening.
Loading skeletons mirror the final layout shape; progress bars step through
states with intentional pacing; scroll progress, save state, and sync state
are surfaced visually rather than hidden.

### 2. Match between system and the real world

Icons, vocabulary, and metaphors track conventions the user already
recognizes. Trash for delete, gear for settings, magnifier for search.
Domain surfaces pick icons from the user's industry vocabulary, never
invented glyphs.

### 3. User control and freedom

Every destructive or non-trivial action has a visible escape: cancel, undo,
back, close. Modals close on `Esc` and on backdrop click. Multi-step flows
show progress and allow stepping backward.

### 4. Consistency and standards

Same action, same affordance — primary buttons share one color, one shape,
one weight; destructive actions share another. Reuse component patterns
across pages rather than inventing per-context variants.

### 5. Error prevention

Disable irreversible actions until the user confirms prerequisites (checkbox,
typed confirmation). Inline validation as the user types rather than after
submit when possible. Format-aware inputs (number fields, date pickers)
prevent invalid entry at source.

### 6. Recognition rather than recall

Labels stay visible; icons carry text labels when meaning is not unambiguous.
Recent actions, breadcrumbs, and autocomplete suggestions relieve the user
from remembering the path.

### 7. Flexibility and efficiency of use

Keyboard shortcuts visible in tooltips and menus. Bulk actions, density
toggles, and customizable views serve advanced users without burdening
beginners.

### 8. Aesthetic and minimalist design

Every element earns its place. Decoration competes with content for
attention — restrain visual noise to amplify the signal. The Four Questions
decide what stays; everything else goes.

### 9. Help users recognize, diagnose, and recover from errors

Error states describe the problem in plain language, identify the specific
input that failed, and suggest the next action. Never show a raw error code
without translation.

### 10. Help and documentation

Inline help (tooltips, info icons, empty-state guidance) appears at the
moment of need. Documentation links open in-context rather than redirecting
away from the workflow.

## Visual Design Laws

Universal principles that govern how the eye reads a surface. These explain
*why* a layout, color choice, or spacing decision works — the practical
recipes live in **Visual Design Principles** below.

### Gestalt

The mind groups visual elements according to predictable rules. Use the
rules deliberately to compose hierarchy without explicit borders.

- **Proximity** — elements close together are perceived as a group; separate groups by larger gaps.
- **Similarity** — elements that share color, shape, or size are perceived as related; vary attributes to signal difference.
- **Continuity** — the eye follows lines and curves; align elements to invisible continuation paths to guide reading order.
- **Closure** — incomplete shapes are mentally completed; partial borders or dotted lines suggest containment without heavy chrome.
- **Figure-ground** — distinguish foreground from background by contrast (color, sharpness, scale); ambiguous figure-ground confuses focus.
- **Common region** — elements inside a shared container (card, box, tinted surface) are perceived as one group; use sparingly to avoid card-noise overload.

### Hierarchy

Five signals carry visual hierarchy. Use multiple in concert rather than
relying on size alone.

- **Size** — larger reads as more important; ratios beat absolute values (3x for hero-vs-body, not "make it 48px").
- **Weight** — bold beats light; pair extreme weights (100-200 vs 800-900) for tension.
- **Color** — high-contrast text dominates; muted text recedes; saturated accents capture attention disproportionate to size.
- **Position** — top-left dominates in left-to-right reading; center draws focus when surrounded by whitespace; bottom-right anchors call-to-action attention.
- **Spacing** — generous space around an element isolates and elevates it; cramped space groups elements and lowers individual weight.

### Balance, Contrast, Rhythm

- **Balance** — symmetric layouts read as formal/stable; asymmetric layouts read as dynamic/contemporary; radial layouts read as ceremonial. Pick deliberately; default-centering everything reads as generic.
- **Contrast** — typographic contrast (display vs body), color contrast (foreground vs background — minimum WCAG AA 4.5:1 for body, 3:1 for large text), scale contrast (hero vs supporting), and weight contrast (heavy vs light) all carry independent hierarchy. Stack two or three contrast axes for clear focal points.
- **Rhythm** — repetition with variation creates pace. Alternate section backgrounds, alternate spacing density, or alternate layout direction between consecutive sections to keep the page from feeling flat.

### Reading Patterns

The eye does not scan a surface uniformly. Designs that ignore reading
patterns waste attention on the wrong areas.

- **F-pattern** — dense text-heavy surfaces (articles, blogs, search results) get scanned along the top horizontal, then a second horizontal, then a vertical down the left. Anchor key copy along the F.
- **Z-pattern** — sparse marketing surfaces (heroes, landing pages) get scanned top-left → top-right → bottom-left → bottom-right. Anchor brand mark top-left, primary action bottom-right.
- **Gutenberg diagram** — symmetric long-form layouts split into four quadrants with strong primary (top-left) and terminal (bottom-right) areas. Use for editorial centered compositions.
- **Center-out** — heavily centered layouts draw the eye outward from the geometric center; works for short hero pages, fails for scrollable long-form.

Squint at the design — the elements that survive blur are the elements the
eye locks onto first. Reorder visual weight until the surviving elements
match the intended reading sequence.

## Visual Design Principles

Practical recipes — *how* to apply the laws above through CSS, typography,
color, and motion choices. These guidelines compose with the named tones in
[presets.md](presets.md) and are validated against the rules in
[anti-patterns.md](anti-patterns.md).

### Typography

- **Pairings must be distinctive**: never default to Inter, Roboto, Arial, or system fonts as primary choice for marketing/editorial pages. Pair a characterful display font with a refined body font. System font stacks are acceptable for web apps where performance and native feel matter.
- **Weight extremes**: use 100-200 for subtlety and 800-900 for impact within the same layout.
- **Size jumps**: headings should be at least 3x body size. Timid 1.5x ratios flatten hierarchy.
- **Each generation gets a different combination**: never reuse the same pairing across variants or builds.

### Color and Theme

- **CSS variables for everything**: define palette once in `:root`, reference everywhere.
- **60-30-10 rule**: 60% dominant surface, 30% secondary, 10% accent. Sharp accents on a committed base outperform timid evenly-distributed palettes.
- **Dominant + accent**: pick one hero color and one contrast accent. Two accents maximum.
- **Theme commitment**: go fully dark or fully light per section. Half-measures read as unfinished.

### Spatial Composition and Whitespace

- **Asymmetry over centering**: centered hero + centered sections + centered footer = generic. Break symmetry at least once per page.
- **Overlap and layering**: elements that break grid boundaries create depth and visual interest.
- **Generous whitespace or controlled density**: both work — the crime is the lukewarm middle.
- **Section alternation**: vary backgrounds, spacing density, or layout direction between consecutive sections to create rhythm.
- **Measure**: body copy at 60-75 characters per line for readability; never run text flush across full viewport.

### Backgrounds and Atmosphere

- **Create depth, not flatness**: gradient meshes, noise textures, geometric patterns, layered transparencies, grain overlays.
- **Match texture to tone**: organic tones get soft gradients, brutalist gets noise, luxury gets subtle grain.
- **Dark sections earn their weight**: a dark hero or footer anchors the page — use them intentionally.
- **Never default to flat solid white** unless that IS the design statement (minimalist).

### Motion and Interaction

- **One page-load moment**: a well-orchestrated entrance with staggered `animation-delay` creates more delight than scattered micro-interactions.
- **Easing curves**: use `cubic-bezier` curves that match the tone — snappy (`0.22, 1, 0.36, 1`) for tech, gentle (`0.25, 0.1, 0.25, 1`) for editorial, bouncy (`0.34, 1.56, 0.64, 1`) for playful. Never leave `ease` as default without intention.
- **Hover states on everything interactive**: buttons, links, cards, images. Missing hover states signal unfinished work.
- **Scroll-triggered reveals**: use `IntersectionObserver` or scroll-driven animations to reward scrolling.
- **Prefer CSS-only** for HTML outputs. Use Motion library for React when available.

### Component States

- **Hover**: not just color change — combine with `transform` (slight scale or translate) and `box-shadow` shift for tactile feedback.
- **Focus-visible**: visible `outline` or `ring` for keyboard navigation. Never remove default focus styles without replacing them.
- **Disabled**: `opacity: 0.5` + `cursor: not-allowed` + `pointer-events: none`. Must remain visible, never hidden.
- **Loading**: skeleton screens that mirror the final layout shape. Shimmer animation (`background-position` slide) on skeleton placeholders.
- **Empty**: illustration or descriptive message with a CTA when possible. Never leave blank whitespace with no explanation.
- **Icon anchoring**: small monochrome icons without containers vanish; pair every icon with a colored container, text label, or both.

### Depth and Elevation

- **Shadow system**: three consistent levels — subtle (cards at rest), medium (hover/raised cards), elevated (modals, dropdowns, popovers).
- **Z-index strategy**: base (0) < cards (10) < dropdowns (20) < modals (30) < overlays (40). Document the scale, don't improvise.
- **Glass/blur effects**: use sparingly. Always provide a solid-color fallback for browsers without `backdrop-filter` support.
- **Intentional layering**: overlapping elements should create depth and guide the eye, not produce visual confusion. Every overlap needs a clear foreground/background relationship.

### Responsive Behavior

- **Two breakpoints minimum**: layouts must communicate intent at mobile (375px) and desktop (1280px+). Anything in between should interpolate gracefully.
- **Hero reorganization**: split heroes stack vertically on mobile — text-over-image becomes text-above-image. Never just shrink the desktop layout.
- **Grid collapse**: columns go from N to 1-2 on small screens. Content reflows, never hides.
- **Typography scaling**: headings reduce in size but maintain the hierarchy ratio. A 3x jump at desktop can become 2x at mobile — never 1x.
- **Spacing reduction**: margins and padding shrink proportionally. Mobile spacing should feel tighter but never identical to desktop values.

## Complexity Calibration

Match implementation effort to the aesthetic vision:

- **Maximalist / kinetic / retro-futuristic**: elaborate code is expected. Layer animations, textures, custom cursors, parallax, grain overlays. The detail IS the design.
- **Minimal / luxury / neo-grotesque**: restraint is the skill. Fewer elements, but each one pixel-perfect. Spacing, typography weight, and color precision carry the entire result.
- **Middle-ground tones** (editorial, startup, organic): balance detail and restraint. One or two signature moments plus polished fundamentals.

If the tone is bold, don't write timid code. If the tone is refined, don't overload with effects.

## Creative Mandate

Every generation must feel like a different designer made it. Vary fonts, color temperature, layout geometry, motion style, and density between builds. Never converge on a "house style" across variants or successive generations.

Interpret creatively. Make unexpected choices that feel genuinely designed for the context. Commit fully to the chosen direction.
