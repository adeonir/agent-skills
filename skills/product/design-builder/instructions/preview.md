# Preview

Visual preview of the design before implementation. Generate variants from DESIGN.md tokens and the structure artifact, refine the chosen variant with tune sliders and inline comments, commit tuned values back to DESIGN.md.

Variant generation and commit confirmation deserve careful reasoning — visual choices compound and patches mutate the source of truth.

## When to Use

- After visual identity is in `.agents/design/DESIGN.md` and arrangement is in `.agents/design/structure.md`
- User wants to see the design with visual style applied
- User wants to compare visual directions
- User wants to refine a chosen variant (tune tokens, comment on elements)

## Prerequisites

- `.agents/design/DESIGN.md` — visual identity. Tokens are read from the YAML frontmatter.
- `.agents/design/structure.md` — page composition or screen flow
- `.agents/design/copy.yaml` (optional) — structured content
- [aesthetics.md](../references/aesthetics.md) (required) — design principles
- [web-standards.md](../references/web-standards.md) (required) — implementation rules
- [presets.md](../references/presets.md) (required when user invokes a named tone) — pre-blended direction recipes
- [anti-patterns.md](../references/anti-patterns.md) (required) — failure modes to avoid during generation and review

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Project Type Routes the Presets

Read `project_type` from discovery context or `copy.yaml`. Ask the user if not set.

Presets are **default starting points** when the user has no specific direction. When the user prompts a direction ("Cyberpunk", "Editorial dark mode", "Bento Grid"), the preset list is ignored and direction comes from the prompt plus the Style Axes in [aesthetics.md](../references/aesthetics.md).

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

The YAML frontmatter at the top of DESIGN.md is the source of truth for tokens. At variant generation time, the agent parses the frontmatter, resolves every `{path.to.token}` reference, and embeds CSS custom properties directly in the generated HTML:

- **Colors** — from `colors.*`. Each token becomes a CSS custom property (`--primary`, `--background`, `--accent-foreground`). When a color is a string hex, use it directly. When it is an object `{ hex, oklch }`, emit the oklch value (Tailwind-native) and keep hex as a fallback comment.
- **Typography** — from `typography.*`. Each role becomes a set of related custom properties (`--font-display-family`, `--font-display-size`, `--font-display-weight`, ...). Role keys map 1:1 to kebab-case prefixes.
- **Spacing** — from `spacing.*`. Numeric Tailwind scale keys become `--spacing-1`, `--spacing-2`, ... custom properties.
- **Radius** — from `rounded.*`. Scale keys become `--rounded-xs`, `--rounded-sm`, ... custom properties.
- **Elevation** — from `elevation.*`. Scale keys become `--elevation-sm`, `--elevation-md`, ... custom properties carrying CSS shadow strings.
- **Motion** — from `duration.*` and `easing.*`. Keys become `--duration-fast`, `--easing-standard`, ... custom properties.
- **Breakpoints** — from `breakpoints.*`. Keys become `--breakpoint-sm`, `--breakpoint-md`, ... custom properties.
- **Components** — from `components.*`. Each component entry becomes a class (`.button-primary`, `.card`, `.input`) with properties resolved through the reference chain.

No external parser, no token endpoint. The agent reads the YAML, resolves references, maps everything to CSS variables in the HTML output, ships the file.

## Generated HTML Stack

Dependencies load via CDN — no build step required. Resolve the canonical CDN entry from each library's official documentation at generation time; do not hardcode version pins inside this skill.

- **Tailwind CSS** — include the official browser-build script in `<head>` so utility classes resolve client-side. Refer to the Tailwind docs for the current browser-build entry point.
- **Icons (iconify-icon)** — include the official `iconify-icon` web-component script before `</body>`. A single include covers every icon set (`lucide`, `feather`, `tabler`, `heroicons`, `mdi`, `simple-icons` for brand and social marks, etc.). Use markup `<iconify-icon icon="<set>:<name>"></iconify-icon>` (e.g., `lucide:arrow-right`, `simple-icons:github`). Decorative icons add `aria-hidden="true"`; meaningful icons keep `aria-label` on the containing button.
- **Tailwind theme customization** goes inline via a `<style type="text/tailwindcss">@theme { ... }</style>` block placed after the Tailwind script, mapping tokens read from the DESIGN.md YAML frontmatter (`colors`, `typography`, `rounded`, `spacing`, `elevation`, `duration`, `easing`, `breakpoints`) to Tailwind theme keys. The frontmatter parser lives in `scripts/preview-server.ts`.
- After dependency injection, every variant must work offline-of-build: opening the `.html` file directly in a browser renders correctly without a bundler.
- React/JSX variants follow the same CDN pattern when output is standalone HTML; production builds replace CDN with bundled imports.

## Tailwind Token Conventions

Prefer standard Tailwind tokens over arbitrary `[value]` syntax. Arbitrary values bypass the theme, break dark mode and theme switching, and erode design-system consistency.

- Map tokens read from the DESIGN.md YAML frontmatter into the Tailwind theme via `<style type="text/tailwindcss">@theme { --color-primary: ...; --radius-md: ...; }</style>` so utilities like `bg-primary`, `rounded-md`, `text-lg` resolve to project values. Token keys come from the frontmatter groups: shadcn-style names in `colors` (`primary`, `card`, `accent`, `muted`, `destructive`, etc.), kebab-case role keys in `typography` (`display`, `heading-lg`, `body-standard`, `caption`), Tailwind scale keys in `rounded` (`xs`, `sm`, `md`, `lg`, ...) and `spacing` (`1`, `2`, `4`, ...).
- Use the nearest standard token when an exact DESIGN.md value lacks a named theme key (`p-4` vs `p-[15px]`, `rounded-lg` vs `rounded-[10px]`, `text-slate-600` vs `text-[#475569]`).
- Arbitrary values (`w-[317px]`, `bg-[#abc123]`, `mt-[7px]`) are acceptable only when:
  - The value is genuinely one-off (computed offset, magic asset width, third-party embed dimension).
  - No theme extension would be reused -- adding it would bloat the theme for a single site.
  - The constraint is documented in a comment on the same line or in DESIGN.md.
- When the same arbitrary value appears 2+ times, promote it to `@theme` instead of repeating the literal.
- Colors always go through the theme -- never inline hex in class names when the value belongs to the palette.

| Avoid | Prefer |
|-------|--------|
| `bg-[#3b82f6]` | `bg-primary` (mapped) or `bg-blue-500` |
| `p-[16px]` | `p-4` |
| `text-[14px]` | `text-sm` |
| `rounded-[8px]` | `rounded-lg` |
| `gap-[12px]` | `gap-3` |
| `h-[100vh]` | `h-screen` |

## Generating Variants

User asks for N variants (default 4). Agent generates one HTML per variant from DESIGN.md tokens and structure.md arrangement.

### Workflow

1. **Confirm count and direction.** If the user did not specify N, default to 4. If they did not give direction, use the project-type preset list above. If they invoked a named tone ("Editorial", "Brutalist", "Cyberpunk", "Luxury", ...), load the matching recipe from [presets.md](../references/presets.md) and apply its token overrides + prompt addendum + layout hints. If they gave a free-form direction ("Cyberpunk + Bento Grid"), compose across Style Axes from [aesthetics.md](../references/aesthetics.md).

2. **Start the preview server** (if not running):

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/variants
   ```

3. **Generate one HTML per variant.** Read the DESIGN.md frontmatter for tokens, structure.md for arrangement, copy.yaml for content. Wire Tailwind + iconify-icon via CDN — see `## Generated HTML Stack` and `## Tailwind Token Conventions` above for tags and theme mapping. Write each variant to `.artifacts/design/preview/variants/<slug>.html`.

4. **Serve** all variants side by side via the server. User picks one.

5. **Mark** the chosen variant as `final.html` in the variants directory.

## Refinement Tools

Once a variant is chosen, two tools refine it without regenerating HTML.

### Tune (sliders)

Expose key tokens as sliders that re-render the variant live. The server serves a tune fragment alongside the variant iframe; sliders write `tune` events to `.events`, and the page swaps matching CSS custom properties (`--primary`, `--spacing-4`, `--rounded-md`, `--font-body-standard-size`, etc.) without regenerating HTML.

Default slider set:

- Spacing scale multiplier (0.75x — 1.5x)
- Color saturation (desaturated — vivid)
- Typography contrast (flat — high-contrast hero vs body ratio)
- Border radius scale (sharp — pill)

Agent can generate custom sliders when the user wants to tune something specific ("make the accent more lavender", "more compact cards"). Each slider is a `data-tune="<token-path>"` element wired to emit `tune` events. The token-path matches the YAML path in the DESIGN.md frontmatter (e.g., `colors.primary`, `typography.body-standard.fontSize`, `rounded.lg`).

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

DESIGN.md is the source of truth. Tune values reach it via confirm-before-write surgical patches — frontmatter first, prose follows.

### Workflow

1. **Read `.events`** for the current session. Collect every `tune` event, keep the **last value** per token-path.

2. **Compose a patch list.** For each tuned token-path:
   - **Frontmatter patch** — locate the YAML entry at the cited path (e.g., `colors.primary`, `rounded.lg`, `spacing.4`). Compute the surgical replacement: hex string or `{ hex, oklch }` object for colors, dimension with unit for sizes, `Nms` for durations. For multipliers (spacing scale, radius scale), apply the factor to every numeric value in the affected group.
   - **Prose patch** — locate the bullet in the markdown body that cites the same token (Section 2 for colors, Section 3 for typography, Section 4 for spacing, Section 6 for radius, Section 9 for motion). Update the displayed value so prose stays in sync with the frontmatter.
   - Build a list `{ layer, path, old, new }` entries where `layer` is `frontmatter` or `prose`.

3. **Show the user the patch list before writing.** Format:

   ```
   Proposed patches to DESIGN.md:

   frontmatter: colors.primary  →  "#7170ff"  (was "#5e6ad2")
   prose: ## 2. Colors > Primary
       - **Indigo Brand** (#5e6ad2) → `primary`
       → **Indigo Brand** (#7170ff) → `primary`

   frontmatter: spacing
       1: 0.25rem  →  0.375rem
       2: 0.5rem  →  0.75rem
       4: 1rem    →  1.5rem
   prose: ## 4. Layout > Spacing System
       (multiplier 1.5x applied to displayed values)

   Apply? [y/n]
   ```

4. **On approval, write surgical patches** — patch the YAML entry first, then patch the prose bullet that cites it. Never rewrite the surrounding section, never touch unaffected entries, never touch unrelated sections.

5. **On reject, leave DESIGN.md untouched.** Tuned values stay only in the variant HTML for the session.

### Edge cases

- **Hue shift renders the evocative name stale** (e.g., "Indigo Brand" tuned to red). Agent flags this in the patch list and proposes a name update in the prose alongside the hex change in the frontmatter. User approves both or only the hex.
- **Custom slider for a token-path not yet in DESIGN.md.** Ask the user whether to add a new token (and its prose bullet) before writing, or remap the slider to an existing path.
- **Multiple tunes on the same token-path in one session.** Only the last value counts; intermediate values are discarded.
- **Tune touches a color object.** When the source token is `{ hex, oklch }`, patch both fields so they stay equivalent within 1 sRGB unit per channel.

## Guidelines

**DO:**

- Read the DESIGN.md frontmatter before generating to ground every visual choice in the current tokens
- Read `.agents/design/structure.md` for arrangement; never re-arrange pages or screens inside preview
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Route presets by project type when the user has no direction; ignore presets when the user prompts direction
- Default variant count to 4; honor any N the user names
- Apply [aesthetics.md](../references/aesthetics.md) and [web-standards.md](../references/web-standards.md) to every output
- Serve every generated preview through the preview server
- Swap CSS custom properties during tune — keep the DOM, change only tokens
- Show the patch list and ask before writing to DESIGN.md
- Patch the frontmatter first, then the prose bullet that cites the same token

**DON'T:**

- Generate previews without DESIGN.md and structure populated (contrasts: treat them as prerequisites)
- Treat prose as the source of truth (contrasts: YAML frontmatter is authoritative)
- Change page composition or screen flow between variants (contrasts: arrangement is single-source from `.agents/design/structure.md`; pivots belong there)
- Use CSS frameworks (contrasts: vanilla CSS only, self-contained)
- Skip serving the result (contrasts: serve every generated preview through the preview server)
- Regenerate HTML during tune when a CSS custom property swap is enough (contrasts: swap CSS custom properties, keep the DOM)
- Write to DESIGN.md without showing the patch list and getting approval (contrasts: confirm-before-write is the contract)
- Patch prose without first patching the frontmatter (contrasts: YAML is the normative layer; prose mirrors it)
- Treat "make it different" as actionable (contrasts: ask for one specific axis pivot or compose across Style Axes)

## Error Handling

- No DESIGN.md in `.agents/design/`: suggest running inputs first; do not proceed
- No `.agents/design/structure.md`: suggest running structure first; do not proceed
- No `copy.yaml`: use generic placeholder strings derived from H1 and `description` of DESIGN.md
- Frontmatter missing or unparseable: route the user to validate.md before previewing
- Server port in use: try alternative port
- Comment event has no selector: ask user to re-click the target element
- Tune event targets a token-path not in DESIGN.md frontmatter: ask user whether to add the token (and its prose bullet) or remap the slider to an existing path
- User rejects the proposed patch list: leave DESIGN.md untouched; tuned values remain in the variant HTML only
