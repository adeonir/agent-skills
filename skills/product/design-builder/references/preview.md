# Preview

Visual preview of the design before implementation. Generate variants from DESIGN.md tokens and the structure artifact, refine the chosen variant with tune sliders and inline comments, commit tuned values back to DESIGN.md.

Variant generation and commit confirmation deserve careful reasoning — visual choices compound and patches mutate the source of truth.

## When to Use

- After visual identity is in `.agents/design/DESIGN.md` and arrangement is in `.agents/design/structure.md`
- User wants to see the design with visual style applied
- User wants to compare visual directions
- User wants to refine a chosen variant (tune tokens, comment on elements)

## Prerequisites

- `.agents/design/DESIGN.md` — visual identity. Tokens are extracted from its prose at generation time.
- `.agents/design/structure.md` — page composition or screen flow
- `.agents/design/copy.yaml` (optional) — structured content
- [aesthetics.md](aesthetics.md) (required) — design principles
- [web-standards.md](web-standards.md) (required) — implementation rules

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Project Type Routes the Presets

Read `project_type` from discovery context or `copy.yaml`. Ask the user if not set.

Presets are **default starting points** when the user has no specific direction. When the user prompts a direction ("Cyberpunk", "Editorial dark mode", "Bento Grid"), the preset list is ignored and direction comes from the prompt plus the Style Axes in [aesthetics.md](aesthetics.md).

**Page-based** (`landing-page`, `website`) defaults:

- Editorial — typography-driven, generous whitespace
- Marketing — hero-forward, conversion-oriented
- Product — feature-dense, modular sections
- Branded — bold color, distinctive shapes

**Screen-based** (`web-app`, `mobile-app`) defaults:

- Utilitarian — dense, efficient, power-user
- Consumer-polished — approachable, friendly, rounded
- Native-platform — respects platform conventions (iOS/Android/macOS/Windows)
- Creative-tool — canvas-first, tool palette, minimal chrome

**Commerce-based** (`e-commerce`) defaults:

- Boutique — minimal, image-led, premium DTC, generous whitespace
- Marketplace — dense grid, multi-vendor feel, filter-heavy, varied catalog
- DTC-bold — single brand voice, opinionated, story-driven hero
- Editorial-shoppable — lookbook or magazine feel, content + commerce mixed

## Token Extraction

DESIGN.md prose is the source of truth for tokens. At variant generation time, the agent reads the prose and embeds CSS custom properties directly in the generated HTML:

- **Colors** — from bullets in `## 2. Color Palette & Roles` (shape `**<Name>** (#HEX) → \`<token-key>\` — <intent>`). Token key becomes the CSS custom property name (`--primary`, `--background`, `--accent-foreground`).
- **Typography** — from bullets in `## 3. Typography Rules > Hierarchy` (shape `**<Role>**: <Font> <Npx> weight <N>, line-height <N>, letter-spacing <Npx>`). Role names map to lower-kebab-case keys (`--font-display-hero`, `--font-body-standard`).
- **Spacing** — from bullets in `## 5. Layout Principles > Spacing System`.
- **Radius** — from bullets in `## 5. Layout Principles > Border Radius Scale`.
- **Motion** — from bullets in `## 7. Motion & Interaction > Duration` and `> Easing`.

No external parser, no token endpoint. The agent reads the prose, maps it to CSS variables in the HTML output, ships the file.

## Generating Variants

User asks for N variants (default 4). Agent generates one HTML per variant from DESIGN.md tokens and structure.md arrangement.

### Workflow

1. **Confirm count and direction.** If the user did not specify N, default to 4. If they did not give direction, use the project-type preset list above. If they gave direction ("Cyberpunk + Bento Grid"), compose across Style Axes from [aesthetics.md](aesthetics.md).

2. **Start the preview server** (if not running):

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/variants
   ```

3. **Generate one HTML per variant.** Read DESIGN.md prose for tokens, structure.md for arrangement, copy.yaml for content. Wire Tailwind + Lucide via CDN — see [web-standards.md](web-standards.md) `## CDN Dependencies` for tags and theme mapping. Write each variant to `.artifacts/design/preview/variants/<slug>.html`.

4. **Serve** all variants side by side via the server. User picks one.

5. **Mark** the chosen variant as `final.html` in the variants directory.

## Refinement Tools

Once a variant is chosen, two tools refine it without regenerating HTML.

### Tune (sliders)

Expose key tokens as sliders that re-render the variant live. The server serves a tune fragment alongside the variant iframe; sliders write `tune` events to `.events`, and the page swaps matching CSS custom properties (`--primary`, `--space-unit`, `--radius-md`, `--font-size-body`, etc.) without regenerating HTML.

Default slider set:

- Spacing scale multiplier (0.75x — 1.5x)
- Color saturation (desaturated — vivid)
- Typography contrast (flat — high-contrast hero vs body ratio)
- Border radius scale (sharp — pill)

Agent can generate custom sliders when the user wants to tune something specific ("make the accent more lavender", "more compact cards"). Each slider is a `data-tune="<token-key>"` element wired to emit `tune` events. The token-key matches the backticked key in DESIGN.md prose (e.g., `primary`, `body-standard`, `radius-card`).

### Comment (inline feedback on elements)

User alt+clicks any element in the served preview. An overlay appears with a text input. On submit, the client posts a `comment` event with:

- `selector` — CSS path to the clicked element
- `text` — the user's comment
- `screenshot` — optional, inline via canvas (skip if heavy)

Agent reads `comment` events on the next turn, addresses each, and shows the updated variant.

## Viewport Switching

Variants page includes viewport controls that resize the iframe: 375 (mobile), 768 (tablet), 1440 (desktop). No device chrome frames — just viewport width — to keep HTML vanilla and self-contained.

Default viewport: 1440 for page-based and commerce-based, 375 for screen-based on mobile-app, 1440 for screen-based on web-app.

## Commit Back to DESIGN.md

DESIGN.md is the source of truth. Tune values reach it via confirm-before-write surgical patches — never whole-section rewrites.

### Workflow

1. **Read `.events`** for the current session. Collect every `tune` event, keep the **last value** per token-key.

2. **Compose a patch list.** For each tuned token-key:
   - Find the bullet in DESIGN.md that ends with `` `<token-key>` `` in backticks (Color Palette) or starts with `**<Role>**:` (Typography Hierarchy), or matches the scale name (Spacing / Radius / Motion).
   - Compute the surgical replacement: hex for color tunes, `Npx` for size tunes, `line-height N` for line-height tunes, `Nms` for motion tunes. For multipliers (spacing scale, radius scale), apply the factor to every numeric value in the affected section.
   - Build a list `{ section, line, old, new }` entries.

3. **Show the user the patch list before writing.** Format:

   ```
   Proposed patches to DESIGN.md:

   ## 2. Color Palette & Roles > Primary
   - **Indigo Brand** (#5e6ad2) → `primary`  →  (#7170ff)
   ## 5. Layout Principles > Spacing System
   - Base unit: 8px  →  12px
   - Scale: 4 / 8 / 12 / 16 / 24 / 32  →  6 / 12 / 18 / 24 / 36 / 48

   Apply? [y/n]
   ```

4. **On approval, write surgical patches** — line-replace each affected bullet only. Never rewrite the surrounding section, never touch unaffected bullets, never touch other sections.

5. **On reject, leave DESIGN.md untouched.** Tuned values stay only in the variant HTML for the session.

### Edge cases

- **Hue shift renders the evocative name stale** (e.g., "Indigo Brand" tuned to red). Agent flags this in the patch list and proposes a name update alongside the hex change. User approves both or only the hex.
- **Custom slider for a token not yet in DESIGN.md.** Ask the user whether to add a new bullet (in the appropriate H3) before writing, or remap the slider to an existing key.
- **Multiple tunes on the same token in one session.** Only the last value counts; intermediate values are discarded.

## Guidelines

**DO:**

- Read DESIGN.md prose before generating to ground every visual choice in current tokens
- Read `.agents/design/structure.md` for arrangement; never re-arrange pages or screens inside preview
- Route presets by project type when the user has no direction; ignore presets when the user prompts direction
- Default variant count to 4; honor any N the user names
- Apply [aesthetics.md](aesthetics.md) and [web-standards.md](web-standards.md) to every output
- Serve every generated preview through the preview server
- Swap CSS custom properties during tune — keep the DOM, change only tokens
- Show the patch list and ask before writing to DESIGN.md
- Patch DESIGN.md prose bullet by bullet — never rewrite whole sections

**DON'T:**

- Generate previews without DESIGN.md and structure populated (contrasts: treat them as prerequisites)
- Change page composition or screen flow between variants (contrasts: arrangement is single-source from `.agents/design/structure.md`; pivots belong there)
- Use CSS frameworks (contrasts: vanilla CSS only, self-contained)
- Skip serving the result (contrasts: serve every generated preview through the preview server)
- Regenerate HTML during tune when a CSS custom property swap is enough (contrasts: swap CSS custom properties, keep the DOM)
- Write to DESIGN.md without showing the patch list and getting approval (contrasts: confirm-before-write is the contract)
- Treat "make it different" as actionable (contrasts: ask for one specific axis pivot or compose across Style Axes)

## Error Handling

- No DESIGN.md in `.agents/design/`: suggest running inputs first; do not proceed
- No `.agents/design/structure.md`: suggest running structure first; do not proceed
- No `copy.yaml`: use generic placeholder strings derived from H1, Category, and tagline of DESIGN.md
- Server port in use: try alternative port
- Comment event has no selector: ask user to re-click the target element
- Tune event targets a token not in DESIGN.md prose: ask user whether to add the token (as a new bullet) or map the slider to an existing key
- User rejects the proposed patch list: leave DESIGN.md untouched; tuned values remain in the variant HTML only

## Next Steps

After preview is approved:

- "Hand the approved design to the implementation phase"
- "Run inputs again if a major shift in DESIGN.md is needed"
