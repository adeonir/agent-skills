# Anti-Patterns

Deterministic anti-pattern catalog for design validation and HTML preview checks.
Each rule documents a recognizable failure mode with the smallest sufficient fix
and a paired HTML example.

## When to Use

Auto-loaded by `validate.md` as a gate before DESIGN.md lands and during HTML preview review.
Also referenced by `preview.md` during variant generation to avoid known failure shapes upfront.

## Categories

- **Typography** — fonts, weights, scale, pairing
- **Color and Theme** — palette, contrast, theme commitment
- **Layout and Spacing** — composition, density, alignment, rhythm
- **Decoration and Depth** — shadow, radius, glass, layering
- **Component States** — hover, focus, disabled, loading, empty
- **Motion and Interaction** — easing, transitions, hover feedback
- **Accessibility** — keyboard nav, semantic HTML, ARIA, contrast ratios
- **Performance** — CDN abuse, layout shift, blocking renders
- **Hydration and SSR** — React/Next.js client/server divergence
- **Drift** — HTML output not aligned with DESIGN.md tokens (single-source violations)

## Rule Template

ALWAYS use this exact template structure:

```markdown
### {rule-id-kebab-case}
**Category:** {category name from above}
**Severity:** {error | warning}
**Check:** {prose description of what to detect — one or two sentences}
**Fix:** {what to do instead}
**Example fail:**
```html
{minimal HTML snippet that triggers the rule}
```
**Example pass:**
```html
{minimal HTML snippet that satisfies the rule}
```
```

## Typography

(rules pending)

## Color and Theme

(rules pending)

## Layout and Spacing

(rules pending)

## Decoration and Depth

(rules pending)

## Component States

(rules pending)

## Motion and Interaction

(rules pending)

## Accessibility

(rules pending)

## Performance

(rules pending)

## Hydration and SSR

(rules pending)

## Drift

(rules pending)
