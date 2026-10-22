# Anti-Patterns

Deterministic rules for document validation and rendered preview review.

## When to Use

Load from validate for rules whose inspection surface includes `DESIGN.md`. Load from preview for rules whose inspection surface includes `rendered-output`.

## Rule Contract

Each rule declares its inspection surface. Categories describe the defect and never route execution.

ALWAYS use this exact template structure:

````markdown
### [rule-id]
**Category:** [descriptive category]
**Surface:** DESIGN.md | rendered-output | both
**Severity:** error | warning
**Check:** [observable condition]
**Fix:** [smallest sufficient correction]
**Example fail:**
```text
[failing example]
```
**Example pass:**
```text
[passing example]
```
````

## Content and Scope

### content-leakage
**Category:** Scope
**Surface:** DESIGN.md
**Severity:** warning
**Check:** Prose or token keys contain product copy, feature or entity names, audience pitches, requirement IDs, milestones, roadmap language, the section order of a product page, or screen flow.
**Fix:** Keep identity reasoning and structural roles; replace strings with placeholders and product-domain keys with design roles.
**Example fail:**
```markdown
## Agent Prompt Guide
Build the Refund Center hero with “Recover revenue today”.
```
**Example pass:**
```markdown
## Agent Prompt Guide
Build the summary surface with [Headline] and [CTA Label].
```

### library-name-leakage
**Category:** Scope
**Surface:** DESIGN.md
**Severity:** warning
**Check:** Prose or description names a CSS framework class, a UI-library component, or a design-system package as part of the identity. An icon set or a font source does not trigger it.
**Fix:** Describe the visual property and keep implementation tools outside the identity.
**Example fail:**
```markdown
Cards use the default shadcn radius and Tailwind shadow.
```
**Example pass:**
```markdown
Cards use the medium corner tier and a low, cool-toned shadow.
```

## Drift

### inline-color-outside-tokens
**Category:** Drift
**Surface:** rendered-output
**Severity:** error
**Check:** A specimen uses a literal color not declared in `colors`.
**Fix:** Render through the matching color token.
**Example fail:**
```html
<div style="background:#7d3aed"></div>
```
**Example pass:**
```html
<div style="background:var(--color-primary)"></div>
```

### inline-value-bypasses-token
**Category:** Drift
**Surface:** rendered-output
**Severity:** warning
**Check:** A specimen uses a literal spacing or radius where a declared token serves the same role.
**Fix:** Render through the matching token.
**Example fail:**
```html
<div style="padding:15px;border-radius:9px"></div>
```
**Example pass:**
```html
<div style="padding:var(--spacing-md);border-radius:var(--rounded-md)"></div>
```

### font-family-outside-tokens
**Category:** Drift
**Surface:** rendered-output
**Severity:** error
**Check:** A specimen uses a font family not declared under `typography`.
**Fix:** Use a declared typography role.
**Example fail:**
```html
<h1 style="font-family:Arial"></h1>
```
**Example pass:**
```html
<h1 style="font-family:var(--font-display-family)"></h1>
```

## Document Consistency

### prose-yaml-drift
**Category:** Consistency
**Surface:** DESIGN.md
**Severity:** warning
**Check:** Prose cites a missing token or describes a value or component relationship that disagrees with frontmatter.
**Fix:** Treat frontmatter as normative and update only the stale prose statement.
**Example fail:**
```markdown
The primary action uses `colors.accent`, but no `accent` token exists.
```
**Example pass:**
```markdown
The primary action uses `colors.primary`.
```
