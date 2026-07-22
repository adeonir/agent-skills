# Validate

Audit `DESIGN.md` against the linter rules. Read-only: never patches the file. Reports findings; user decides what to fix.

Runs twelve named linter rules — `broken-ref`, `missing-primary`, `contrast-ratio`, `orphaned-tokens`, `token-summary`, `missing-sections`, `missing-typography`, `section-order`, `oklch-hex-pair`, `token-groups-shape`, `content-leakage`, `library-name-leakage` — plus schema checks, prose↔YAML parity, and a Drift anti-pattern audit. Runs inline — no external CLI dependency; only the `contrast-ratio` rule delegates its arithmetic to the skill's bundled contrast script (Step 4).

## When to Use

- User asks to validate, check, audit, or lint `DESIGN.md`
- After a manual edit to `DESIGN.md`
- Before handoff to the implementation phase, an external design tool, or a teammate
- Auto-loaded by [design.md](design.md) Step 5 as the gate before reporting done

## Prerequisites

- `docs/design/DESIGN.md` exists

## Output

Findings report printed to the user. Severities:

- **error**: blocks "done" reporting; must be fixed or explicitly accepted as a trade-off
- **warning**: surfaces a likely issue but does not block
- **info**: noteworthy observation, no action required

No files written. No tokens rewritten.

## Workflow

### Step 1: Parse Frontmatter and Body

Read `docs/design/DESIGN.md`. Split into:

- **YAML frontmatter** — the block between the opening `---` and closing `---` fences. Parse into the design system state with top-level keys: `name`, `description`, `colors`, `typography`, `rounded`, `borderWidth`, `spacing`, `components`, `elevation`, `duration`, `easing`, `breakpoints`.
- **Markdown body** — everything after the frontmatter. Walk H2 headings to enumerate sections and their order.
- **Token reference index** — collect every `{path.to.token}` occurrence inside `components`, `rounded`, and `spacing` values for the `broken-ref` check. A color reference may carry a trailing `/NN` opacity modifier; strip it to the base path before resolving.

If the frontmatter block is missing or unparseable, emit a single error and stop — no downstream check is meaningful without it.

### Step 2: Schema Checks

Validate the YAML against the expected shape.

| Check | Severity |
|-------|----------|
| `name` is a non-empty string | error |
| `description` is a non-empty string when present | warning |
| Every color value is either a hex string (`#RRGGBB` or `#RGB`) or an object with `hex` (required) and `oklch` (required) keys | error |
| Every typography entry has `fontFamily` and `fontSize`; optional `fontWeight`, `fontStyle`, `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation` typed correctly | error |
| Every dimension uses a valid unit (`px`, `em`, `rem`) or unitless number where allowed (`lineHeight`) | error |
| `lineHeight` values are either a Dimension or a unitless number (recommended) | info |
| Token keys are unique within their group | error |
| Variant entries follow `<component>-<modifier>` naming — a state (`button-primary-hover`) or a size (`button-sm`, `button-lg`) | warning |

### Step 3: Reference Resolution — `broken-ref`

Walk every `{path.to.token}` in the YAML. Resolve against the parsed model.

| Check | Severity |
|-------|----------|
| Each reference resolves to a defined token at the cited path | error |
| References inside `components.*` point to primitives in `colors`, `typography`, `rounded`, `borderWidth`, `spacing`, or `elevation` (component-to-component refs not allowed) | error |
| References inside `rounded` and `spacing` resolve to siblings in the same group | error |
| A color reference's optional `/NN` opacity modifier is an integer 0–100; the base token resolves after stripping it | error |

### Step 4: Color Rules — `missing-primary` + `contrast-ratio` + `orphaned-tokens` + `oklch-hex-pair`

Contrast ratios are computed, never estimated by eye. Run the bundled script (execute it; do not read it as reference):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check-contrast.py docs/design/DESIGN.md
```

It parses the frontmatter, checks every `*-foreground`/base token pair and every component with both colors resolved, and prints one PASS/FAIL/SKIP line per pair. It accepts every token shape (hex string, inline flow `{ hex, oklch }`, block map with a `hex` member) and a `colors` block that is flat or carries skin groups — groups are detected structurally, never by name. Flat tokens form the default skin; each named group is an override skin inheriting every flat token it does not redefine (which skin is default is the author's call), and pairs an override touches re-check under that skin. A component fill of `transparent`/`none` resolves to the page (`colors.background`) so the text is checked where it actually sits; with no `colors.background` defined the page is unknown and the component SKIPs rather than assume white. Map its output onto the `contrast-ratio` checks below; a run where every pair skips exits 2 and counts as a failed gate, not a pass. If `python3` is unavailable, compute the WCAG ratio manually from the hex values (relative luminance plus the 0.05 flare term) and mark each contrast finding as estimated.

| Check | Severity |
|-------|----------|
| `colors.primary` exists when any `colors` are defined | warning |
| Every `colors.<base>` / `colors.<base>-foreground` pair meets 4.5:1 — a `*-foreground` token is text on its base surface by construction (`foreground` itself pairs with `background`) | error |
| `colors.muted-foreground` meets 4.5:1 against `colors.background` and `colors.card` — it doubles as secondary text on those surfaces | error |
| For every `components.<name>` with both `backgroundColor` and `textColor` resolved, contrast ratio meets WCAG AA (4.5:1 for body, 3:1 for large text and UI) | warning |
| A `transparent`/`none` component `backgroundColor` resolves to `colors.background` — the text sits on the page; the script SKIPs it when no `colors.background` is defined (the page is unknown and is never assumed white) | info |
| `-disabled` component variants are exempt from contrast checks — WCAG 1.4.3 excludes inactive UI; the script reports them as SKIP | info |
| Color tokens defined but not referenced by any `components.*` entry (excluding paired foreground tokens) | warning |
| When a color is an object `{ hex, oklch }`, both values parse correctly and resolve to the same color within 1 sRGB unit per channel | warning |

### Step 5: Typography Checks — `missing-typography`

| Check | Severity |
|-------|----------|
| `typography` is present when `colors` is present | warning |
| Body role line-height ≥ 1.4 (readability floor) | warning |
| A `label`, `caption`, or `eyebrow` role — or any role the Typography prose describes as uppercase / ALL-CAPS — carries `letterSpacing` ≥ 0.06em (uppercase text reads cramped without positive tracking) | warning |
| A large-display role (`display`, `title`, `heading`, `subheading`) carries non-positive `letterSpacing` (large type wants negative or zero tracking, never loose) | info |

### Step 6: Token Groups Shape — `token-groups-shape`

| Check | Severity |
|-------|----------|
| `borderWidth` keys follow Tailwind border-width scale (`0`, `DEFAULT`, `2`, `4`, `8`); values use `px` (or unitless `0`) | warning |
| `elevation` keys follow Tailwind scale (`2xs`, `xs`, `sm`, `md`, `lg`, `xl`, `2xl`); values are valid CSS shadow strings | warning |
| `duration` keys are named tiers; values use `ms` unit | warning |
| `easing` values are valid `cubic-bezier(...)` strings or CSS easing keywords (`linear`, `ease`, `ease-in`, `ease-out`, `ease-in-out`) | warning |
| `breakpoints` keys follow Tailwind scale (`sm`, `md`, `lg`, `xl`, `2xl`); values use `rem` unit | warning |

### Step 7: Section Order and Coverage — `section-order` + `missing-sections`

Canonical section order in the markdown body — the eight named sections follow the `design.md` spec (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts); the rest are permitted extras that keep their slot in this order:

1. Overview
2. Colors
3. Typography
4. Layout
5. Elevation & Depth
6. Shapes
7. Components
8. Motion & Interaction
9. Responsive Behavior
10. Do's and Don'ts
11. Agent Prompt Guide

| Check | Severity |
|-------|----------|
| Sections present appear in canonical order | warning |
| Optional sections (`Elevation & Depth`, `Shapes`, `Motion & Interaction`, `Responsive Behavior`) absent when their matching YAML group is populated | info |
| Section headings match the canonical names listed above | warning |
| Duplicate section heading | error |

### Step 8: Prose↔YAML Parity

| Check | Severity |
|-------|----------|
| Token keys cited in prose (backticked) exist in the frontmatter | warning |
| Each color bullet's value matches its frontmatter shape — hex-only when YAML is a string, dual `oklch / #HEX` when YAML is an object | warning |
| Quick Token Reference entries in the Agent Prompt Guide section mirror the shape of their matching Colors section bullet | warning |
| Each populated YAML color token has a bullet in the Colors section | info |
| Component variants in YAML (`button-primary-hover`, ...) are narrated in the Components section | info |
| An Agent Prompt Guide Example Component Prompt spells out the property bundle of a component defined in `components.*` (background/text/border/radius/padding) instead of referencing `{components.<name>}` | warning |
| Component-variant behavior narrated in the Components section agrees with that variant's token value (flag a disagreement; do not prescribe which side is right) | warning |
| `duration`/`easing` are populated but the Motion & Interaction section's `Reduced Motion` subsection is missing or left as a placeholder — the a11y fallback the tokens imply is unauthored | warning |

### Step 9: Content & Tooling-Agnostic Check — `content-leakage` + `library-name-leakage`

DESIGN.md must render any copy and stay tool-agnostic — in prose and in the token namespace. Flag prose that bakes product-specific content into the brand identity, token keys that encode a product-domain concept, or names of the UI library or design system used only as reference.

| Check | Severity |
|-------|----------|
| The Overview section contains feature lists, audience descriptions ("users who", "teams that"), product-pitch phrasing, or marketing claims rather than brand-voice and atmosphere | warning |
| The Components section narrates a component by a product-specific label (e.g., "the Refund Center card") instead of by structural role ("transactional summary card") | warning |
| A `colors` token key names a product-domain concept (`payment`, `checkout`) rather than a design role, semantic status, or hue — a base and its `-foreground` count as one finding | warning |
| A `typography` or `components` token key names a product-domain concept (`checkout-heading`, `refund-center-card`) rather than a structural role | warning |
| The Agent Prompt Guide Example Component Prompts embed concrete strings that look like real copy (headlines, CTAs, feature names, taglines) instead of placeholders (`[Headline]`, `[CTA Label]`, `[Body Lorem]`, `[Badge Text]`, `[Nav Label]`) | warning |
| Frontmatter `description` reads like a product tagline rather than a brand-voice summary | info |
| Prose or `description` names a specific UI library or design system (`shadcn`, `Tailwind`, `Material UI`, `Bootstrap`, `Chakra`, `Radix`, ...) — reference/inspiration only, never part of the brand identity; name the value, not the tool | warning |

**Token-key vocabulary.** A token key names a design role, a semantic status, or a hue — never a product-domain concept. Accepted without flag: the semantic color roles (`primary`, `secondary`, `accent`, `muted`, `destructive`, `background`, `foreground`, `card`, `popover`, `border`, `input`, `ring`), semantic status roles (`success`, `warning`, `info`, and `error` / `danger` — distinct from `destructive`, the destructive-action role), data-series roles (`chart-1`…), `sidebar-*`, any `<base>-foreground`, and raw/brand hue names (`ink`, `teal`, `blue-500`). Flag a key that reads as a feature, screen, or entity (`payment`, `checkout`, `refund-card`, `checkout-heading`).

### Step 10: Anti-Pattern Audit

Load [anti-patterns.md](../references/anti-patterns.md). For each rule whose `Category` is `Drift`, apply the `Check` against the parsed DESIGN.md model (frontmatter tokens + body prose). Emit a finding per match using the rule's `id` and `severity`.

| Check | Severity |
|-------|----------|
| Drift rule matches (e.g., `font-family-not-in-tokens`, `copy-string-in-design-md`, `arbitrary-tailwind-value-repeated` traces in DESIGN.md prose) | per rule severity |

The Color and Theme rule targets rendered output (preview judges the styleguide with it), not the DESIGN.md model, so it is not applied here.

### Step 11: Token Summary — `token-summary`

Emit an info finding with counts per group:

```text
Tokens: N colors, N typography, N rounded, N borderWidth, N spacing, N components, N elevation, N duration, N easing, N breakpoints
```

### Step 12: Report Findings

Group findings by severity. Format:

```text
DESIGN.md validation -- <path>

Errors (N):
- [section/path] description
- ...

Warnings (N):
- [section/path] description
- ...

Info (N):
- [section/path] description
- ...

Summary: N errors, N warnings, N info
```

If errors > 0: do not declare validation passed. Ask the user whether to fix or accept as a trade-off.

If errors = 0: report passed. Warnings and info remain visible but do not block.

### Step 13: When Called as a Gate

When this ref is auto-loaded by `design.md` as the Step 5 gate, the caller must:

- Block the "done" report when `errors > 0`
- Surface the findings inline in the design.md Step 6 (Present) output
- Allow the user to accept warnings as trade-offs without re-running validate

## Guidelines

**DO:**

- Parse the YAML frontmatter first; treat it as authoritative
- Resolve every `{path.to.token}` reference and report unresolved ones as errors
- Group findings by severity; lead with errors
- Reference the exact YAML path or section + sub-heading in findings (e.g., `colors.primary`, `## Components > Buttons`)
- Use the same checks whether called directly, as a gate by design.md, or at the close of a preview tuning session

**DON'T:**

- Patch or rewrite `DESIGN.md` (contrasts: read-only audit)
- Treat prose as the source of truth (contrasts: YAML frontmatter is authoritative)
- Block on warnings or info (contrasts: only errors block)
- Re-run discovery or design-brief (contrasts: this ref operates on the file as-is)
- Invent fixes; report findings and let the user decide (contrasts: never auto-fix)
- Shell out to an external linter binary (contrasts: rules run inline; the bundled contrast script ships with the skill and is the only executable step)
- Judge which state behavior is correct, or flag it for differing from a convention — state behavior is a project choice; check prose↔token consistency, not behavioral preference

## Error Handling

- No DESIGN.md in `docs/design/`: stop and route the user to `design.md` to author one
- Frontmatter block missing or unparseable: emit one error, stop downstream checks
- YAML parses but `colors` is empty: report what is missing, suggest running design-brief
- `python3` unavailable for the contrast script: compute ratios manually from the hex values and mark every contrast finding as estimated

## Outcomes

- Errors found: ask user to fix in source (re-run design) or edit `DESIGN.md` manually, then re-run validate
- Warnings found: present them as trade-offs; user may accept or address
- All passed: report done
