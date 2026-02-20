# Design Aesthetics

Self-contained design principles for variant generation and frontend building.
Apply these guidelines to every visual decision -- they replace any external design skill dependency.

## Design Thinking

### Four Questions

Before any visual work, answer these to lock in a direction:

1. **Purpose**: What problem does this interface solve? Who uses it?
2. **Tone**: Pick a clear aesthetic from the catalog below -- or blend two adjacent ones.
3. **Constraints**: Technical requirements (framework, performance, accessibility).
4. **Signature**: What single detail will make this _unforgettable_? (A motion moment, a typographic trick, an unusual color move.) Every project needs one.

### Tone Catalog

| Tone | Description |
|------|-------------|
| Brutally minimal | Maximum whitespace, typography-only hierarchy, near-monochrome |
| Maximalist chaos | Dense layering, clashing textures, overwhelming detail |
| Retro-futuristic | CRT glow, scanlines, neon on dark, monospace type |
| Organic / natural | Soft shapes, earth tones, hand-drawn textures, rounded corners |
| Luxury / refined | Thin serifs, muted metallics, generous spacing, restrained palette |
| Playful / toy-like | Rounded sans, bright primaries, bouncy motion, oversized elements |
| Editorial / magazine | High-contrast serif headings, warm neutrals, editorial grid, section numbering |
| Brutalist / raw | System fonts pushed to extremes, exposed structure, anti-polish |
| Art deco / geometric | Gold + black, symmetrical patterns, angular type, ornamental borders |
| Soft / pastel | Low-contrast pastels, diffused gradients, gentle rounded UI |
| Industrial / utilitarian | Monospace, high-density data, dark UI, minimal ornamentation |
| Neo-grotesque | Swiss-style grids, tight leading, limited palette, extreme alignment precision |
| Kinetic / motion-first | Interface built around transition -- parallax, morphing shapes, scroll-driven narrative |

Use these as starting points. Blend or push further as the project demands.

## Aesthetics Principles

### Typography

- **Pairings must be distinctive**: never default to Inter, Roboto, Arial, or system fonts as primary choice. Pair a characterful display font with a refined body font.
- **Weight extremes**: use 100-200 for subtlety and 800-900 for impact within the same layout.
- **Size jumps**: headings should be at least 3x body size. Timid 1.5x ratios flatten hierarchy.
- **Each generation gets a different combination**: never reuse the same pairing across variants or builds.

### Color and Theme

- **CSS variables for everything**: define palette once in `:root`, reference everywhere.
- **60-30-10 rule**: 60% dominant surface, 30% secondary, 10% accent. Sharp accents on a committed base outperform timid evenly-distributed palettes.
- **Dominant + accent**: pick one hero color and one contrast accent. Two accents maximum.
- **Theme commitment**: go fully dark or fully light per section. Half-measures read as unfinished.

### Motion and Interaction

- **One page-load moment**: a well-orchestrated entrance with staggered `animation-delay` creates more delight than scattered micro-interactions.
- **Easing curves**: use `cubic-bezier` curves that match the tone -- snappy (`0.22, 1, 0.36, 1`) for tech, gentle (`0.25, 0.1, 0.25, 1`) for editorial, bouncy (`0.34, 1.56, 0.64, 1`) for playful. Never leave `ease` as default without intention.
- **Hover states on everything interactive**: buttons, links, cards, images. Missing hover states signal unfinished work.
- **Scroll-triggered reveals**: use `IntersectionObserver` or scroll-driven animations to reward scrolling.
- **Prefer CSS-only** for HTML outputs. Use Motion library for React when available.

### Spatial Composition

- **Asymmetry over centering**: centered hero + centered sections + centered footer = generic. Break symmetry at least once per page.
- **Overlap and layering**: elements that break grid boundaries create depth and visual interest.
- **Generous whitespace or controlled density**: both work -- the crime is the lukewarm middle.
- **Section alternation**: vary backgrounds, spacing density, or layout direction between consecutive sections to create rhythm.

### Backgrounds and Atmosphere

- **Create depth, not flatness**: gradient meshes, noise textures, geometric patterns, layered transparencies, grain overlays.
- **Match texture to tone**: organic tones get soft gradients, brutalist gets noise, luxury gets subtle grain.
- **Dark sections earn their weight**: a dark hero or footer anchors the page -- use them intentionally.
- **Never default to flat solid white** unless that IS the design statement (minimalist).

### Visual Hierarchy

- **Reading path**: design a clear eye movement sequence -- typically hero headline > subtext > CTA > first content section. Test by squinting.
- **Contrast ratios**: primary content at WCAG AA minimum (4.5:1 text, 3:1 large text). Decorative elements can be lower.
- **Icon context**: icons floating alone without background, border, or label are invisible. Always provide visual anchoring -- colored container, text label, or both.
- **One focal point per viewport**: if everything is bold, nothing is bold. Each screen-height section gets one dominant element.

### Responsive Behavior

- **Two breakpoints minimum**: layouts must communicate intent at mobile (375px) and desktop (1280px+). Anything in between should interpolate gracefully.
- **Hero reorganization**: split heroes stack vertically on mobile -- text-over-image becomes text-above-image. Never just shrink the desktop layout.
- **Grid collapse**: columns go from N to 1-2 on small screens. Content reflows, never hides.
- **Typography scaling**: headings reduce in size but maintain the hierarchy ratio. A 3x jump at desktop can become 2x at mobile -- never 1x.
- **Spacing reduction**: margins and padding shrink proportionally. Mobile spacing should feel tighter but never identical to desktop values.

### Component States

- **Hover**: not just color change -- combine with `transform` (slight scale or translate) and `box-shadow` shift for tactile feedback.
- **Focus-visible**: visible `outline` or `ring` for keyboard navigation. Never remove default focus styles without replacing them.
- **Disabled**: `opacity: 0.5` + `cursor: not-allowed` + `pointer-events: none`. Must remain visible, never hidden.
- **Loading**: skeleton screens that mirror the final layout shape. Shimmer animation (`background-position` slide) on skeleton placeholders.
- **Empty**: illustration or descriptive message with a CTA when possible. Never leave blank whitespace with no explanation.

### Depth and Elevation

- **Shadow system**: three consistent levels -- subtle (cards at rest), medium (hover/raised cards), elevated (modals, dropdowns, popovers).
- **Z-index strategy**: base (0) < cards (10) < dropdowns (20) < modals (30) < overlays (40). Document the scale, don't improvise.
- **Glass/blur effects**: use sparingly. Always provide a solid-color fallback for browsers without `backdrop-filter` support.
- **Intentional layering**: overlapping elements should create depth and guide the eye, not produce visual confusion. Every overlap needs a clear foreground/background relationship.

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|--------------|--------------|
| Inter/Roboto/Arial as primary font | Signals zero design intention -- every AI tool defaults here |
| Purple gradient on white background | Most overused AI color scheme; instantly reads as template |
| Evenly-distributed colors (25/25/25/25) | No hierarchy, no focus -- the eye has nowhere to land |
| Centered layout for every section | Monotonous rhythm kills engagement after the first scroll |
| Missing hover states | Users perceive interactive elements as broken, not minimal |
| Icons floating without context | Small monochrome icons without containers vanish in the layout |
| Cramped spacing throughout | Signals the design was never reviewed, just generated |
| Identical treatment across variants | Defeats the purpose of comparison -- each must feel distinct |
| System font stack as aesthetic choice | Acceptable for apps, lazy for marketing/editorial pages |
| Animations without easing intention | Default `ease` on everything reads as mechanical, not designed |

## Complexity Calibration

Match implementation effort to the aesthetic vision:

- **Maximalist / kinetic / retro-futuristic**: elaborate code is expected. Layer animations, textures, custom cursors, parallax, grain overlays. The detail IS the design.
- **Minimal / luxury / neo-grotesque**: restraint is the skill. Fewer elements, but each one pixel-perfect. Spacing, typography weight, and color precision carry the entire result.
- **Middle-ground tones** (editorial, startup, organic): balance detail and restraint. One or two signature moments plus polished fundamentals.

If the tone is bold, don't write timid code. If the tone is refined, don't overload with effects.

## Creative Mandate

Every generation must feel like a different designer made it. Vary fonts, color temperature, layout geometry, motion style, and density between builds. Never converge on a "house style" across variants or successive generations.

Interpret creatively. Make unexpected choices that feel genuinely designed for the context. Claude is capable of extraordinary creative work -- commit fully to the chosen direction.
