# Validate

Audit semantic quality of `DESIGN.md` — contrast, hex validity, hierarchy ratio, cross-section consistency. Read-only: never patches the file. Reports findings; user decides what to fix.

Cross-section checks (contrast pairs, scale ratios) deserve careful reasoning — small mistakes cascade across every screen.

## When to Use

- User asks to validate, check, or audit `DESIGN.md`
- After a manual edit to `DESIGN.md`
- Before handoff to the implementation phase, an external design tool, or a teammate
- Auto-loaded by [inputs.md](inputs.md) Step 5 as the gate before reporting done

## Prerequisites

- `.agents/design/DESIGN.md` exists

## Output

Findings report printed to the user. Severities:

- **error**: blocks "done" reporting; must be fixed or explicitly accepted as a trade-off
- **warning**: surfaces a likely issue but does not block
- **info**: noteworthy observation, no action required

No files written. No tokens rewritten.

## Workflow

### Step 1: Extract Values from Prose

Walk the DESIGN.md prose and extract:

- Hex codes and their token keys from `## 2. Color Palette & Roles` bullets (shape `**<Name>** (#HEX) → \`<token-key>\` — <intent>`)
- Typography roles, font sizes, line heights from `## 3. Typography Rules > Hierarchy` bullets
- Spacing scale from `## 5. Layout Principles > Spacing System`
- Quick Color Reference entries from `## 10. Agent Prompt Guide > Quick Color Reference`

### Step 2: Color Checks

| Check | Severity |
|-------|----------|
| Every hex is valid SRGB (`#RRGGBB` or `#RGB`) | error |
| Token keys are unique across the section | error |
| Foreground/background pairs (`foreground` over `background`, `primary-foreground` over `primary`, `card-foreground` over `card`, `accent-foreground` over `accent`, `muted-foreground` over `muted`, `destructive-foreground` over `destructive`, `popover-foreground` over `popover`) meet WCAG AA: 4.5:1 for body text, 3:1 for large text and UI elements | error |
| Evocative names follow one mode consistently (descriptive: hue + temperature/density; poetic: brand-voice). Mixing modes within the same file | warning |

### Step 3: Typography Checks

| Check | Severity |
|-------|----------|
| Hierarchy forms a clear ratio (display > heading > body > label); no two adjacent levels within 10% of each other | warning |
| At least one role with weight ≥ 600 OR letter-spacing that signals display-class type | info |
| Body line-height ≥ 1.4 (readability floor) | warning |

### Step 4: Spacing & Rhythm Checks

| Check | Severity |
|-------|----------|
| Scale follows a consistent rhythm (multiples of a base unit, geometric, or Fibonacci progression) | info |
| Base unit present and named explicitly | info |

### Step 5: Visual Theme Checks

| Check | Severity |
|-------|----------|
| Section body length ≥ 1500 chars (target 2000–3000 for full brand voice) | warning |
| At least one hex code appears inline | info |

### Step 6: Cross-Section Consistency

| Check | Severity |
|-------|----------|
| Quick Color Reference entries point at hex values present in Color Palette | warning |
| Token keys referenced in Visual Theme prose match keys defined in Color Palette | warning |
| Example Component Prompts in Agent Prompt Guide reference token keys present in Color Palette and Typography Hierarchy | info |

### Step 7: Report Findings

Group findings by severity. Format:

```
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

### Step 8: When Called as a Gate

When this ref is auto-loaded by `inputs.md` as the Step 5 gate, the caller must:

- Block the "done" report when `errors > 0`
- Surface the findings inline in the inputs Step 6 (Present) output
- Allow the user to accept warnings as trade-offs without re-running validate

## Guidelines

**DO:**

- Read DESIGN.md once, run all checks against the extracted values
- Group findings by severity; lead with errors
- Reference the exact section + sub-heading in findings (e.g., `## 2. Color Palette & Roles > Primary`)
- Use the same checks whether called directly or as a gate by inputs.md

**DON'T:**

- Patch or rewrite `DESIGN.md` (contrasts: read-only audit)
- Block on warnings or info (contrasts: only errors block)
- Re-run discovery or inputs (contrasts: this ref operates on the file as-is)
- Invent fixes; report findings and let the user decide (contrasts: never auto-fix)

## Error Handling

- No DESIGN.md in `.agents/design/`: stop and route the user to `inputs.md` to author one
- Color Palette section empty or unparseable: report what is missing, suggest running inputs

## Next Steps

After validation:

- All passed: suggest `preview`
- Errors found: ask user to fix in source (re-run inputs) or edit `DESIGN.md` manually, then re-run validate
- Warnings found: present them as trade-offs; user may accept or address
