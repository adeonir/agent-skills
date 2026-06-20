# Anti-Patterns

Deterministic anti-pattern catalog for DESIGN.md validation and styleguide
review. Each rule documents a recognizable failure mode with the smallest
sufficient fix and a paired example.

## When to Use

Auto-loaded by `validate.md` as a gate before DESIGN.md lands, and by
`preview.md` to judge the styleguide. Two families apply: **Drift**
(single-source violations between DESIGN.md and rendered output) and **Color
and Theme** (token-value legibility). Page-rendering anti-patterns (layout,
motion, component states, hydration, performance) are out of scope — this skill
authors tokens, it does not render product pages.

## Categories

- [Color and Theme](#color-and-theme) — palette legibility, contrast
- [Drift](#drift) — output not aligned with DESIGN.md tokens (single-source violations)

## Rule Template

ALWAYS use this exact template structure:

````markdown
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
````

## Color and Theme

### gray-text-on-saturated-color
**Category:** Color and Theme
**Severity:** error
**Check:** Gray text (`#6b7280`, `#9ca3af`, `slate-500`, etc.) placed on saturated colored background fails WCAG AA 4.5:1 contrast.
**Fix:** Use the corresponding `*-foreground` token from DESIGN.md or recompute contrast: white/near-white on saturated backgrounds, dark gray only on neutral backgrounds.
**Example fail:**
```html
<button style="background: #3b82f6; color: #6b7280">Action</button>
```
**Example pass:**
```html
<button style="background: var(--color-primary); color: var(--color-primary-foreground)">Action</button>
```

## Drift

### inline-hex-not-in-tokens
**Category:** Drift
**Severity:** error
**Check:** Rendered HTML contains an inline color hex (`style="color: #abc123"` or class `bg-[#abc123]`) that is not present in DESIGN.md `colors` frontmatter.
**Fix:** Either add the color to DESIGN.md as a token and reference it via `bg-{name}` / `var(--{name})`, or replace with the nearest existing token.
**Example fail:**
```html
<div style="background: #7d3aed">Hero</div>
```
**Example pass:**
```html
<div class="bg-primary">Hero</div>
```

### inline-style-bypass-tokens
**Category:** Drift
**Severity:** warning
**Check:** Inline `style="padding: 12px"`, `style="border-radius: 9px"`, or `class="p-[15px]"` used for properties that have token equivalents in DESIGN.md `spacing` / `rounded` / `elevation`.
**Fix:** Replace inline literal with the nearest token (`p-4`, `rounded-md`, or `var(--spacing-4)`).
**Example fail:**
```html
<div style="padding: 12px; border-radius: 9px">A</div>
```
**Example pass:**
```html
<div class="p-3 rounded-md">A</div>
```

### font-family-not-in-tokens
**Category:** Drift
**Severity:** error
**Check:** Rendered HTML uses a font-family not declared in DESIGN.md `typography.*.fontFamily`.
**Fix:** Either declare the font in DESIGN.md as a token role and reference it, or swap to an existing token role.
**Example fail:**
```html
<h1 style="font-family: Playfair Display">Title</h1>
```
**Example pass:**
```html
<h1 style="font-family: var(--font-display)">Title</h1>
```

### arbitrary-tailwind-value-repeated
**Category:** Drift
**Severity:** warning
**Check:** Same arbitrary Tailwind value (`w-[317px]`, `bg-[#abc123]`, `mt-[7px]`) appears 2+ times in the same variant.
**Fix:** Promote to `@theme` in the inline `<style type="text/tailwindcss">` block once, then reference everywhere as a named utility.
**Example fail:**
```html
<div class="bg-[#abc123]">A</div>
<div class="bg-[#abc123]">B</div>
```
**Example pass:**
```html
<style type="text/tailwindcss">@theme { --color-brand: #abc123; }</style>
<div class="bg-brand">A</div>
<div class="bg-brand">B</div>
```

### copy-string-in-design-md
**Category:** Drift
**Severity:** warning
**Check:** DESIGN.md prose (Section 1 Visual Theme & Atmosphere, Section 4 Component Stylings, Section 11 Agent Prompt Guide) contains literal product copy — real headlines, CTAs, feature names, or product pitches.
**Fix:** Move every product string out of DESIGN.md. Keep DESIGN.md content-agnostic; use placeholders like `[Headline]`, `[CTA Label]` in Section 11 prompts.
**Example fail:**
```markdown
## 11. Agent Prompt Guide
- Use the hero pattern: "Ship Faster With Acme — Start Free Today"
```
**Example pass:**
```markdown
## 11. Agent Prompt Guide
- Use the hero pattern: "[Eyebrow] — [Headline] — [CTA Label]"
```
