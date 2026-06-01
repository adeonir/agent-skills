# Preview

Render the `DESIGN.md` tokens as a visual specimen sheet, tune them live with
sliders, and hand the tuned deltas to reconcile for commit-back. This previews
the **design system**, not a product page — swatches, type ramp, component
samples, all from `DESIGN.md` alone.

Visual choices compound and a commit mutates the source of truth, so tune is
live-and-throwaway while the patch back goes through confirm-before-write.

## When to Use

- After visual identity is in `docs/design/DESIGN.md` — see the tokens applied before handoff
- User wants to refine design tokens visually — "preview the tokens", "show the styleguide", "tune the design", "spacing feels tight", "primary is too saturated", "make the radius softer"
- User wants to compare token tweaks side by side, live

This is an optional phase that runs after `design`. It needs a populated
`DESIGN.md`; it never authors one.

## Prerequisites

- `docs/design/DESIGN.md` — visual identity. Tokens are read from the YAML frontmatter. **Hard prerequisite** — if absent, route to [design.md](design.md) to author one first; there is nothing to preview otherwise.
- [aesthetics.md](../references/aesthetics.md) (required) — design principles applied to every specimen.
- [anti-patterns.md](../references/anti-patterns.md) (required) — failure modes. Only token-value rules (contrast, drift) judge the specimen sheet; the page-layout rules do not (see [Neutral Scaffolding](#neutral-scaffolding)).

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Token Extraction

The YAML frontmatter at the top of `DESIGN.md` is the source of truth for tokens.
At generation time, parse the frontmatter, resolve every `{path.to.token}`
reference, and embed CSS custom properties directly in the generated HTML:

- **Colors** — from `colors.*`. Each token becomes a CSS custom property (`--primary`, `--background`, `--accent-foreground`). String hex emits directly; an object `{ hex, oklch }` emits the oklch value (Tailwind-native) with hex as a fallback comment.
- **Typography** — from `typography.*`. Each role becomes related properties (`--font-display-family`, `--font-display-size`, `--font-display-weight`, ...). Role keys map 1:1 to kebab-case prefixes.
- **Spacing** — from `spacing.*`. Numeric Tailwind scale keys become `--spacing-1`, `--spacing-2`, ...
- **Radius** — from `rounded.*`. Scale keys become `--rounded-xs`, `--rounded-sm`, ...
- **Elevation** — from `elevation.*`. Scale keys become `--elevation-sm`, ... carrying CSS shadow strings.
- **Motion** — from `duration.*` and `easing.*`. Keys become `--duration-fast`, `--easing-standard`, ...
- **Breakpoints** — from `breakpoints.*`. Keys become `--breakpoint-sm`, ...
- **Components** — from `components.*`. Each entry becomes a class (`.button-primary`, `.card`, `.input`) with properties resolved through the reference chain.

No external parser, no token endpoint. Read the YAML, resolve references, map
everything to CSS variables in the HTML output, ship the file.

## Generated HTML Stack

Dependencies load via CDN — no build step. Resolve the canonical CDN entry from
each library's official documentation at generation time; do not hardcode version
pins inside this skill.

- **Tailwind CSS** — include the official browser-build script in `<head>` so utility classes resolve client-side.
- **Icons (iconify-icon)** — include the official `iconify-icon` web-component script before `</body>`. A single include covers every set (`lucide`, `tabler`, `simple-icons`, ...). Markup `<iconify-icon icon="<set>:<name>"></iconify-icon>`. Decorative icons add `aria-hidden="true"`; meaningful icons keep `aria-label` on the containing control.
- **Tailwind theme customization** goes inline via `<style type="text/tailwindcss">@theme { ... }</style>` after the Tailwind script, mapping the tokens read from the frontmatter (`colors`, `typography`, `rounded`, `spacing`, `elevation`, `duration`, `easing`, `breakpoints`) to Tailwind theme keys.
- The sheet must work offline-of-build: opening `styleguide.html` directly in a browser renders correctly without a bundler.

## Tailwind Token Conventions

Prefer standard Tailwind tokens over arbitrary `[value]` syntax. Arbitrary values
bypass the theme and erode design-system consistency.

- Map frontmatter tokens into the theme via `<style type="text/tailwindcss">@theme { --color-primary: ...; --radius-md: ...; }</style>` so `bg-primary`, `rounded-md`, `text-lg` resolve to project values.
- Use the nearest standard token when an exact value lacks a named key (`p-4` vs `p-[15px]`, `rounded-lg` vs `rounded-[10px]`).
- Colors always go through the theme — never inline hex in class names when the value belongs to the palette.

| Avoid | Prefer |
|-------|--------|
| `bg-[#3b82f6]` | `bg-primary` (mapped) |
| `p-[16px]` | `p-4` |
| `text-[14px]` | `text-sm` |
| `rounded-[8px]` | `rounded-lg` |

## Specimen Sheet

One self-contained `styleguide.html` that renders all nine token groups as a
design-system reference. It is the visual proof of `DESIGN.md` — the kind of page
a real design system ships as its styleguide.

### Neutral Scaffolding

The sheet has two layers, kept strictly separate:

- **Chrome** — section headers, labels, jump-nav, cards, the tune panel. Styled with **neutral system UI** (`system-ui`, a grey scale), never the project tokens. The chrome must stay legible even when a token is broken or mid-tune. The page-layout anti-patterns (hero-centered, section-rhythm-flat, all-sections-centered) describe *product pages* and do **not** judge this systematic chrome.
- **Specimens** — the actual rendered tokens. These use the project's values. Only token-value rules apply here: contrast (`gray-text-on-saturated-color`), drift (`font-family-not-in-tokens`, `inline-hex-not-in-tokens`).

### UI Quality

This sheet is looked at, so it must read well — internal, but good:

- A sticky top bar with jump-nav to the nine groups.
- Each group is a titled section with a one-line caption and generous neutral spacing.
- A consistent token-card system: the rendered specimen, its key, its value, its role.
- The tune panel is a sticky side or bottom panel — grouped sliders, live value readouts, a reset.
- Responsive grids for swatches and cards; nothing cramped.

### Per-group specimens

- **`colors`** — swatch grid grouped by role (Primary, Secondary & Accent, Surface, Neutrals, Semantic) mirroring DESIGN.md Section 2. Each swatch: the color chip, evocative name, token key, hex (and `oklch` when the YAML carries the object), role. For any token with a paired `-foreground`, show a text-on-fill sample plus the computed WCAG contrast ratio and an AA / AAA badge.
- **`typography`** — type ramp, one row per role: the role name and spec (font / size / weight / line-height / letter-spacing) beside a live specimen rendered at the actual values. Name the loaded family.
- **`spacing`** — a ruler of horizontal bars, one per scale step, bar length equal to the value, labeled key + rem/px.
- **`rounded`** — a row of squares each with its corner radius applied, labeled key + value.
- **`elevation`** — a row of resting cards each at its shadow tier, labeled key.
- **`duration` / `easing`** — animated chips: a small element that loops a transform using each duration and easing pairing, labeled; hover to replay.
- **`components`** — each entry rendered live, resolved through `{path.to.token}`: `button-primary` with its hover/active/disabled variants side by side, `card`, `input`, plus any badge / nav / distinctive entries the frontmatter defines.
- **`breakpoints`** — a labeled scale marking each breakpoint width.

If a group is empty in the frontmatter, render a quiet placeholder for it rather
than omitting the section silently.

## Generating the Specimen Sheet

### Workflow

1. **Read the frontmatter.** Parse `docs/design/DESIGN.md` and resolve every `{path.to.token}`.

2. **Start the preview server** (if not running):

   ```bash
   bun run ${CLAUDE_SKILL_DIR}/scripts/preview-server.ts --session .artifacts/design/preview
   ```

3. **Generate `styleguide.html`.** Build the one sheet per [Specimen Sheet](#specimen-sheet) above — neutral chrome, token specimens, Tailwind + iconify wired per [Generated HTML Stack](#generated-html-stack). Write it to `.artifacts/design/preview/styleguide.html`.

4. **Serve** through the server and let the user view it. The server live-reloads the browser when the file changes.

## Tune

Sliders adjust tokens live without regenerating the HTML — they swap CSS custom
properties on the document. The server serves the sheet; sliders write `tune` and
`tune-preset` events to `.events`.

### Sliders

**Single-token** — one slider, one `data-tune="<token-path>"`, one `tune` event per change. The token-path matches the YAML path (`colors.primary`, `rounded.lg`, `spacing.4`):

- Spacing scale multiplier (0.75x — 1.5x) → `data-tune="spacing.scale"`
- Color saturation (desaturated — vivid) → `data-tune="colors.saturation"`
- Typography contrast (flat — high-contrast hero vs body) → `data-tune="typography.contrast"`
- Border radius scale (sharp — pill) → `data-tune="rounded.scale"`

**Preset-composite** — one slider, one `data-tune-preset="<preset-name>"`, one `tune-preset` event per change. The agent expands the event into a grouped patch list via the Preset Registry below:

- Font character (sans — serif, or light — heavy) → `data-tune-preset="font-character"`
- Motion intensity (still — playful) → `data-tune-preset="motion-intensity"`
- Density (airy — dense) → `data-tune-preset="density"`
- Decoration (austere — playful) → `data-tune-preset="decoration"`

Custom sliders are fine when the user wants to tune something specific ("more
lavender accent", "tighter cards"). Custom sliders default to single-token
`data-tune="<token-path>"`.

### Preset Registry

Maps each preset-composite slider to the token-paths it touches and the transform
per unit of movement. Read this when expanding a `tune-preset` event into the
patch list during commit-back.

| Preset | Affected token-paths | Transform |
|--------|----------------------|-----------|
| `font-character` | `typography.display.fontFamily`, `typography.body.fontFamily` (and matching `fontWeight` when a family swap is unavailable) | swap (slider picks from a curated stack: sans-grotesk, sans-humanist, serif-display, serif-body, mono) |
| `motion-intensity` | `duration.fast`, `duration.base`, `duration.slow`, `easing.standard`, `easing.bounce` | scale durations by `value` (0 = none, 1 = base, 2 = playful); pick easing per intensity tier |
| `density` | `spacing.*` (all numeric keys), `components.*.padding` | multiply by `value` (0.7 = airy → 1.3 = dense) |
| `decoration` | `elevation.*`, `rounded.*`, `colors.accent` saturation | elevation scale × `value`, rounded scale × `value`, accent saturation × `value` |

The client emits a single `tune-preset` event `{ type: "tune-preset", preset, value, timestamp }`. Live preview applies the resolved properties for all affected
paths at once (client-side expansion). Commit-back uses the same registry to
compose the grouped patch list under one `Preset: <name>` header.

## Comment

User alt+clicks any swatch or specimen in the served sheet. An overlay opens with
a text input; on submit the client posts a `comment` event with the element's CSS
`selector` and the `text`. Read `comment` events on the next turn, address each,
and re-show the sheet.

## Commit Back to `DESIGN.md`

Tuning is live-and-throwaway until the user commits. Commit-back does **not** write
`DESIGN.md` here — it builds the patch list and hands it to
[reconcile.md](reconcile.md), the single patcher of `DESIGN.md`.

### Workflow

1. **Read `.events`** for the session. Keep the **last value** per token-path (`tune`) and per preset name (`tune-preset`).

2. **Resolve into a patch list.** For each `tune`, take the token-path and new value directly. For each `tune-preset`, expand via the [Preset Registry](#preset-registry) into the affected single-token paths and their new values. Build entries `{ group, path, old, new }`, where `group` is the preset name (or `null` for single-token). Compute `old` from the current frontmatter value.

3. **Flag edge cases on the list:**
   - **Stale evocative name** — a hue shift (e.g. "Indigo Brand" tuned toward red) makes the prose name stale. Note a suggested rename alongside the hex change.
   - **Token-path not in `DESIGN.md`** — ask whether to add a new token (and its prose bullet) or remap to an existing path.
   - **Color object token** — when the source is `{ hex, oklch }`, patch both fields so they stay equivalent.
   - **Same path tuned by a single-token slider and a preset** — the single-token (most recent) wins; record the preset override as ignored.

4. **Hand the patch list to [reconcile.md](reconcile.md)** as its Mode B input. reconcile presents the diff (confirm-before-write), patches the YAML frontmatter first and the citing prose bullets second, and runs validate as the gate. preview produces the diff; reconcile applies it.

## Guidelines

**DO:**

- Read the `DESIGN.md` frontmatter before generating, so every specimen is grounded in the current tokens
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Keep chrome neutral (system UI) and let only the specimens carry the project tokens
- Render all nine groups; show a quiet placeholder for an empty group rather than dropping it
- Serve every generated sheet through the preview server
- Swap CSS custom properties during tune — keep the DOM, change only tokens
- Hand tuned deltas to `reconcile.md`; never write `DESIGN.md` from here

## Anti-Pattern: Writing `DESIGN.md` from Preview

preview is a visual aid plus a diff producer. Patching `DESIGN.md` here would give
the file a second writer and duplicate the surgical-patch discipline that
`reconcile.md` already owns. The tuned deltas are reconcile's Mode B input — build
the patch list, hand it over, let reconcile confirm, patch, and validate.

## Error Handling

- No `DESIGN.md` in `docs/design/`: route the user to [design.md](design.md); do not proceed
- Frontmatter missing or unparseable: route the user to [validate.md](validate.md) before previewing
- Server port in use: try an alternative port
- Comment event has no selector: ask the user to re-click the target element
- Tune event targets a token-path not in the frontmatter: ask whether to add the token or remap the slider to an existing path
- `.events` empty at commit-back: nothing to commit; report and stop
