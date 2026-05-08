# Validate

Audit an existing `DESIGN.md` against the spec. Read-only: never patches the
file, never rewrites tokens. Reports findings; user decides what to fix.

Cross-layer checks (contrast pairs, scale ratio, hierarchy) deserve careful
reasoning — small mistakes cascade across every screen.

## When to Use

- User asks to validate, check, or audit `DESIGN.md`
- After a manual edit to `DESIGN.md` outside the skill
- Before handoff to the implementation phase, an external design tool, or a teammate
- Auto-loaded by [inputs.md](inputs.md) Step 5 as the gate before reporting done

## Prerequisites

- `.agents/design/DESIGN.md` exists with at minimum a YAML frontmatter block

## Output

Findings report printed to the user. Severities:

- **error**: blocks "done" reporting; must be fixed or explicitly accepted as a trade-off
- **warning**: surfaces a likely issue but does not block
- **info**: noteworthy observation, no action required

No files written. No tokens rewritten.

## Workflow

### Step 1: Read DESIGN.md

Read `.agents/design/DESIGN.md` in full. Parse the YAML frontmatter and the
markdown body. If parsing fails (invalid YAML, duplicate `##` heading, missing
fence), stop and report the parse error -- nothing else runs until the file
parses.

### Step 2: Frontmatter Checks

Run these against the parsed frontmatter:

| Check | Severity |
|-------|----------|
| `colors.*` values are valid hex SRGB strings (`#RRGGBB` or `#RGB`) | error |
| `typography.*` entries carry `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` | error |
| `rounded.*` and `spacing.*` values are dimensions (px, em, rem) or unitless numbers | error |
| Token references (`"{path.to.token}"`) resolve to an existing key | error |
| Token references in `colors`, `typography`, `rounded`, `spacing` point at primitive values, not groups | error |
| Token references in `components` may point at primitives or composites (typography is allowed) | info |
| `components.*` properties are within the allowlist: backgroundColor, textColor, typography, rounded, padding, size, height, width | warning |
| `variants.*` only override keys that exist in the base block | error |
| `motion.duration.*` values are time dimensions (`Nms`, `Ns`); `motion.easing.*` are cubic-bezier or named curves | warning |

### Step 3: Prose Checks

Walk the markdown body:

| Check | Severity |
|-------|----------|
| No duplicate `##` headings | error |
| Canonical sections appear in spec order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts | warning |
| `## Screen Flow` only appears for screen-based projects (web-app, mobile-app); omitted for page-based | info |
| `## Motion` and `## Variants` appear when their frontmatter blocks are populated | info |
| Section headings using spec aliases (Brand & Style, Layout & Spacing, Elevation) are treated as the canonical section | info |
| Unknown sections are preserved without error | info |

### Step 4: Cross-Layer Checks

Compare frontmatter and prose together:

| Check | Severity |
|-------|----------|
| Foreground/background color pairs meet WCAG AA: 4.5:1 for body text, 3:1 for large text and UI elements | error |
| Typography scale forms a clear ratio (display > headline > body > label); no two adjacent levels within 10% of each other | warning |
| Spacing values follow a consistent rhythm (multiples of a base unit, or a Fibonacci/geometric scale) | info |
| Every interactive component has at least one variant beyond base (hover, pressed, or disabled) | warning |
| Hierarchy: display sizes are visibly larger than body sizes | warning |
| Token names referenced in prose (e.g., "`primary`", "`body-lg`") exist in frontmatter | warning |

### Step 5: Report Findings

Group findings by severity. Format:

```
DESIGN.md validation -- <path>

Errors (N):
- [path.in.file] description
- ...

Warnings (N):
- [path.in.file] description
- ...

Info (N):
- [path.in.file] description
- ...

Summary: N errors, N warnings, N info
```

If errors > 0: do not declare validation passed. Ask the user whether to fix
or accept as a trade-off.

If errors = 0: report passed. Warnings and info remain visible but do not block.

### Step 6: When Called as a Gate

When this ref is auto-loaded by `inputs.md` as the Step 5 gate, the caller
must:

- Block the "done" report when `errors > 0`
- Surface the findings inline in the inputs Step 6 (Present) output
- Allow the user to accept warnings as trade-offs without re-running validate

## Guidelines

**DO:**
- Read DESIGN.md once, run all checks against the parsed structure
- Group findings by severity; lead with errors
- Reference the exact path in findings (e.g., `colors.primary`, `## Layout`)
- Treat unknown sections and unknown tokens as `info` only -- the spec is permissive
- Use the same checks whether called directly or as a gate by inputs.md

**DON'T:**
- Patch or rewrite `DESIGN.md` (contrasts: read-only audit)
- Block on warnings or info (contrasts: only errors block)
- Re-run discovery or inputs (contrasts: this ref operates on the file as-is)
- Invent fixes; report findings and let the user decide (contrasts: never auto-fix)
- Hide findings the spec calls out; surface unknown property warnings even when minor

## Error Handling

- No DESIGN.md in `.agents/design/`: stop and route the user to `inputs.md` to author one
- DESIGN.md frontmatter empty or absent: report what is missing, suggest running inputs
- YAML parse error or duplicate heading: report the error path and stop further checks
- File too large to parse in one pass: read frontmatter and body separately, run checks per layer

## Next Steps

After validation:

- All passed: suggest `preview` if structure exists, or `structure` if Layout/Screen Flow are still empty
- Errors found: ask user to fix in source (re-run inputs) or edit `DESIGN.md` manually, then re-run validate
- Warnings found: present them as trade-offs; user may accept or address
