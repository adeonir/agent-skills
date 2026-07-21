# Preview

Render the `DESIGN.md` tokens as a visual styleguide, serve it with live-reload, and refine the tokens — by conversation for most groups, or through an optional color tuner. This previews the **design system**, not a product page — swatches, type ramp, component samples, all from `DESIGN.md` alone.

Visual choices compound, so tuner edits stay live-and-throwaway until the user commits; conversational tweaks patch `DESIGN.md` directly and the sheet live-reloads on every write.

## When to Use

- After visual identity is in `docs/design/DESIGN.md` — see the tokens applied before handoff
- User wants to refine design tokens visually — "preview the tokens", "show the styleguide", "tune the design", "spacing feels tight", "primary is too saturated", "make the radius softer"
- User wants to compare token tweaks side by side, live

This is an optional phase that runs after `design`. It needs a populated `DESIGN.md`; it never authors one.

## Prerequisites

- `docs/design/DESIGN.md` — visual identity. Tokens are read from the YAML frontmatter. **Hard prerequisite** — if absent, route to [design.md](design.md) to author one first; there is nothing to preview otherwise.
- [anti-patterns.md](../references/anti-patterns.md) (required) — the contrast and drift rules that judge the styleguide; chrome is never judged (see [Neutral Scaffolding](#neutral-scaffolding)).

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Token Extraction

The YAML frontmatter at the top of `DESIGN.md` is the source of truth for tokens. At generation time, parse the frontmatter, resolve every `{path.to.token}` reference, and embed CSS custom properties directly in the generated HTML:

- **Colors** — from `colors.*`. Each token becomes a CSS custom property in Tailwind's `--color-*` namespace (`--color-primary`, `--color-background`, `--color-accent-foreground`). String hex emits directly; an object `{ hex, oklch }` emits the oklch value (Tailwind-native) with hex as a fallback comment. Flat tokens emit into the root theme block; a skin override group (`colors.<skin>.*`) emits a scoped block — `[data-skin="<name>"] { --color-background: ...; }` — redefining only the variables it overrides, so everything else inherits from the root through the cascade, mirroring the frontmatter's inheritance.
- **Typography** — from `typography.*`. Each role becomes related properties (`--font-display-family`, `--font-display-size`, `--font-display-weight`, ...). Role keys map 1:1 to kebab-case prefixes.
- **Spacing** — from `spacing.*`. Numeric Tailwind scale keys become `--spacing-1`, `--spacing-2`, ...
- **Radius** — from `rounded.*`. Scale keys become Tailwind's `--radius-*` (`--radius-xs`, `--radius-sm`, ...).
- **Border width** — from `borderWidth.*`. Scale keys become `--border-width-default`, `--border-width-2`, ... carrying `px` values. No Tailwind `@theme` namespace exists for border width, so specimens read these custom properties directly rather than mapping to a theme key.
- **Elevation** — from `elevation.*`. Scale keys become Tailwind's `--shadow-*` (`--shadow-sm`, ...) carrying CSS shadow strings.
- **Motion** — from `duration.*` and `easing.*`. Keys become `--duration-fast`, `--ease-in`, ... — easing maps to Tailwind's `--ease-*` namespace.
- **Breakpoints** — from `breakpoints.*`. Keys become `--breakpoint-sm`, ...
- **Components** — from `components.*`. Each entry becomes a class (`.button-primary`, `.card`, `.input`) with properties resolved through the reference chain. A color reference with a `/NN` opacity modifier (`{colors.primary}/90`) emits `color-mix(in oklab, var(--color-primary) NN%, transparent)`.

No external parser, no token endpoint. Read the YAML, resolve references, map everything to CSS variables in the HTML output, ship the file.

**Render through variables, never literals.** Define each token once in the theme block, then render every specimen through `var(--token)` — never a literal hex or value in markup or an inline `style`. A token's literal value appears only as displayed label text.

## Generated HTML Stack

Dependencies load via CDN — no build step. Resolve the canonical CDN entry from each library's official documentation at generation time; do not hardcode version pins inside this skill.

- **Tailwind CSS** — include the official browser build via CDN in `<head>` so utility classes resolve client-side. Theme mechanism and syntax follow the current major release — resolve both from the official Tailwind documentation at generation time; training-data syntax lags the current release, so never emit theme configuration from memory.
- **Icons (iconify-icon)** — include the official `iconify-icon` web-component script before `</body>`. A single include covers every set (`lucide`, `tabler`, `simple-icons`, ...). Markup `<iconify-icon icon="<set>:<name>"></iconify-icon>`. Decorative icons add `aria-hidden="true"`; meaningful icons keep `aria-label` on the containing control.
- **Tailwind theme customization** goes inline via `<style type="text/tailwindcss">@theme { ... }</style>` after the Tailwind script, mapping the tokens read from the frontmatter (`colors`, `typography`, `rounded`, `spacing`, `elevation`, `duration`, `easing`, `breakpoints`) to Tailwind theme keys.
- The sheet must work offline-of-build: opening `styleguide.html` directly in a browser renders correctly without a bundler.

## Tailwind Token Conventions

Prefer standard Tailwind tokens over arbitrary `[value]` syntax. Arbitrary values bypass the theme and erode design-system consistency.

- Map frontmatter tokens into the theme via `<style type="text/tailwindcss">@theme { --color-primary: ...; --radius-md: ...; }</style>` so `bg-primary`, `rounded-md`, `text-lg` resolve to project values.
- Use the nearest standard token when an exact value lacks a named key (`p-4` vs `p-[15px]`, `rounded-lg` vs `rounded-[10px]`).
- Colors always go through the theme — never inline hex in class names when the value belongs to the palette.

| Avoid | Prefer |
|-------|--------|
| `bg-[#3b82f6]` | `bg-primary` (mapped) |
| `p-[16px]` | `p-4` |
| `text-[14px]` | `text-sm` |
| `rounded-[8px]` | `rounded-lg` |

## Styleguide

One self-contained `styleguide.html` that renders all ten token groups as a design-system reference. It is the visual proof of `DESIGN.md` — the kind of page a real design system ships as its styleguide.

### Neutral Scaffolding

The sheet has two layers, kept strictly separate:

- **Chrome** — section headers, labels, jump-nav, cards. Styled with **neutral system UI** (`system-ui`, a grey scale), never the project tokens. The chrome must stay legible even when a token is broken or mid-tune. The page-layout anti-patterns (hero-centered, section-rhythm-flat, all-sections-centered) describe *product pages* and do **not** judge this systematic chrome.
- **Specimens** — the actual rendered tokens. These use the project's values. Only token-value rules apply here: contrast (`gray-text-on-saturated-color`), drift (`font-family-not-in-tokens`, `inline-hex-not-in-tokens`).

### UI Quality

This sheet is looked at, so it must read well — internal, but good:

- A sticky top bar with jump-nav to each token group (`duration` and `easing` share one motion specimen).
- When `colors` carries a skin override group, the top bar adds a skin switcher that toggles `data-skin` on `<body>` (never `<html>` — root-level inline tunes must not out-cascade the skin blocks), re-rendering every specimen under the active skin. The switcher is chrome — neutral styling, never project tokens.
- Each group is a titled section with a one-line caption — no token counts — and generous neutral spacing.
- A consistent token-card system: the rendered specimen, its key, its value, its role.
- Responsive grids for swatches and cards; nothing cramped.

### Per-group specimens

- **`colors`** — when the palette has a **raw layer** (brand-named hues that the semantic roles alias — detected by color keys outside the standard role vocabulary, or semantic values referencing `{colors.*}`), lead with a **Brand Raw** subgroup showing those canonical hues, then the semantic role groups. Otherwise go straight to the role groups. Role groups follow the DESIGN.md Colors section (Primary, Secondary & Accent, Surface, Neutrals, Semantic). Each swatch: the color chip, evocative name, token key, hex (and `oklch` when the YAML carries the object), role. For any color that carries text or sits as a fill, show a text-on-fill sample plus the computed WCAG contrast ratio and an AA / AAA badge — paired against the color it meets in use: a fill pairs with the `textColor` its component sets, a text color pairs with its surface (usually `background`). Derive the pairing from `components.*`, with `<token>-foreground` as the common shortcut — not the token name alone. When a skin override group exists, each overridden token gets its own swatch under the active skin with `data-token` carrying the full skinned path (`colors.<skin>.<token>`), and contrast badges recompute against the skin's resolved pairing — an inherited partner resolves to its flat value. Each swatch carries tuner metadata — `data-tune-swatch`, `data-token`, `data-var`, `data-pair` (the pairing), `data-original` (the hex) — so the preview server can build the color tuner overlay from the swatches, no separate file.
- **`typography`** — type ramp, one row per role: the role name and spec (font / size / weight / line-height / letter-spacing) beside a live specimen rendered at the actual values. Name the loaded family.
- **`spacing`** — a ruler of horizontal bars, one per scale step, bar length equal to the value, labeled key + rem/px.
- **`rounded`** — a row of squares each with its corner radius applied, labeled key + value.
- **`borderWidth`** — a row of boxes each rendered with its border thickness applied, labeled key + value.
- **`elevation`** — a row of resting cards each at its shadow tier, labeled key.
- **`duration` / `easing`** — animated chips: a small element that loops a transform using each duration and easing pairing, labeled; hover to replay.
- **`components`** — each entry rendered live, resolved through `{path.to.token}`: `button-primary` with its hover/active/disabled variants side by side, `card`, `input`, plus any badge / nav / distinctive entries the frontmatter defines.
- **`breakpoints`** — a labeled scale marking each breakpoint width.

If a group is empty in the frontmatter, render a quiet placeholder for it rather than omitting the section silently.

## Generating the Styleguide

### Workflow

1. **Read the frontmatter.** Parse `docs/design/DESIGN.md` and resolve every `{path.to.token}`.

2. **Start the preview server** (if not running):

   ```bash
   bun run ${CLAUDE_SKILL_DIR}/scripts/preview-server.ts --root docs/design
   ```

3. **Generate `styleguide.html`.** Build the one sheet per [Styleguide](#styleguide) above — neutral chrome, token specimens, Tailwind + iconify wired per [Generated HTML Stack](#generated-html-stack). Write it to `docs/design/styleguide.html`.

4. **Serve** through the server and let the user view it. The server live-reloads the browser when the file changes, and injects a **Tune colors** toggle that opens the color tuner overlay over the page.

## Tune

Two paths refine the tokens. Both write back to `DESIGN.md` here — frontmatter first, citing prose second — and the sheet live-reloads on every write.

**Conversational (default).** No UI. The user views the served sheet and describes the change ("primary too saturated", "spacing feels tight", "softer radius"). Patch `DESIGN.md` surgically — the frontmatter group first, then only the prose bullets that cite the patched tokens; narrative sections (Overview, Do's and Don'ts, Agent Prompt Guide) stay untouched — and regenerate the sheet. A color change passes the contrast script against its pairing before writing. Spacing, typography, radius, and shadow follow the Tailwind scale — discrete steps, nothing continuous to drag — so they are tuned by description, not sliders.

**Color tuner (optional).** Color is the one continuous axis the eye can't judge — WCAG contrast — so it gets an interactive tuner when the user asks ("tune the colors", "let me adjust the palette"). The tuner is an **overlay the preview server injects over the committed styleguide** — no separate file. A **Tune colors** toggle (server-injected) opens a panel built from the styleguide's `data-tune-swatch` color swatches. Tuning swaps the token's `var(--color-<key>)` live, so the whole styleguide is the preview — every specimen that references the token shifts at once.

### Color tuner overlay

The engine (OKLCH ↔ sRGB, gamut clamp, WCAG contrast) lives in `scripts/preview-server.ts` and is injected at serve-time. The agent generates **only the clean styleguide** with swatch metadata; it never authors tuner HTML or JS. The server reads each `data-tune-swatch` swatch (`data-token`, `data-var`, `data-pair`, `data-original`) and builds one row per color:

- **Current / New** — the original color (frozen) beside the live `var(--color-<key>)`, each with its WCAG ratio and AA / AAA / fail badge.
- **Pairing sample** — an `Aa` specimen rendered in the actual pairing (a fill shows its text on the color; a text color shows the color on its surface), so the contrast target is visible, not just named.
- **OKLCH sliders** — `L`, `C`, `H`, each with a reset to its original.
- **Hex input** — optional, to set or paste an exact hex.

Editing a control swaps `--color-<key>` on the document (cascading through every specimen), recomputes the paired contrast live, and records a `tune` event keyed by the token path. A skinned swatch (`data-token` with a skin segment) swaps the variable inside that skin's scoped block, leaving the root values untouched, and its `tune` event keys by the full skinned path. A **Commit** button in the panel records a `commit` event. All contrast is engine-computed — never hand-entered.

## Comment

User alt+clicks any swatch or specimen in the served sheet. An overlay opens with a text input; on submit the client posts a `comment` event with the element's CSS `selector` and the `text`. Read `comment` events on the next turn, address each, and re-show the sheet.

## Commit Back to `DESIGN.md`

Tuner edits are live-and-throwaway until the user commits. The commit writes `DESIGN.md` here — preview is one of its two writers (the other is [design.md](design.md)), under the same surgical rules.

### Workflow

1. **Read `.events`** for the session — triggered by a `commit` event (the panel's Commit button) or a chat request. The `commit` event marks intent; keep the **last value** per token path from the `tune` events.

2. **Resolve into a patch list.** For each `tune`, take the token path and new hex. Build entries `{ path, old, new }`; compute `old` from the current frontmatter value.

3. **Flag edge cases on the list:**
   - **Color object token** — when the source is `{ hex, oklch }`, patch both fields so they stay equivalent.
   - **Skinned token** — the path keeps its skin segment (`colors.<skin>.<token>`) so the patch lands inside that override group, never on the flat token.
   - **Stale evocative name** — a large hue shift (e.g. an "Indigo" token tuned toward red) makes the prose name stale. Note a suggested rename alongside the hex change.

4. **Patch `DESIGN.md` surgically.** Frontmatter first (authoritative), then the prose bullets that cite the patched tokens. Narrative sections stay untouched — flag them as potentially stale. Verify each patched color against its pairing with the contrast script before writing. Report the applied patch list so the user can revert anything via git.

5. **Regenerate the sheet** — the server live-reloads.

## Validate at Session Close

Per tweak, the contrast script is the only guard. When the user closes the tuning session, run [validate.md](validate.md) against the patched `DESIGN.md` as the gate. Do not declare the session done with `errors > 0` — surface the findings and let the user fix or accept trade-offs.

## Guidelines

**DO:**

- Read the `DESIGN.md` frontmatter before generating, so every specimen is grounded in the current tokens
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Define each token once and render every specimen through `var(--token)`; the literal value shows only as label text
- Write the committed styleguide to `docs/design/styleguide.html` with `data-tune-swatch` metadata on color swatches; the server builds the tuner overlay and records events in `.artifacts/design/preview`
- Never hand-author tuner HTML or JS — the OKLCH/WCAG engine and the panel are the server's job; contrast is always engine-computed, never hand-entered
- Keep chrome neutral (system UI) and let only the specimens carry the project tokens
- Render all ten groups; show a quiet placeholder for an empty group rather than dropping it
- Serve the sheet through the preview server so the browser live-reloads on change
- Tune most groups by conversation; reach for the color tuner only for palette and contrast work
- Patch `DESIGN.md` surgically on every write — frontmatter group first, then only the prose bullets that cite the patched tokens; narrative sections untouched

## Anti-Pattern: Regenerating `DESIGN.md` on Tune

Tuning produces deltas, not a new identity. Rewriting the whole file from the tuned values clobbers sections the tune never touched — patch the frontmatter group first, then only the prose bullets that cite the patched tokens. The full validate gate runs at session close; per tweak, only the contrast script guards color changes.

## Error Handling

- No `DESIGN.md` in `docs/design/`: route the user to [design.md](design.md); do not proceed
- Frontmatter missing or unparseable: route the user to [validate.md](validate.md) before previewing
- Server port in use: try an alternative port
- Comment event has no selector: ask the user to re-click the target element
- Tune event targets a color not in the frontmatter: ask whether to add the token or remap to an existing one
- `.events` empty at commit-back: nothing to commit; report and stop
- Validation gate fails at session close: surface findings; the user fixes or accepts trade-offs
