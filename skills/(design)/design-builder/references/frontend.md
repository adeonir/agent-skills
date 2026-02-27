# Frontend Building

Build production-grade React components from design tokens.

## Prerequisites

- **design.json** (required) -- must include the `layout` block
- **copy.yaml** (optional) -- structured content
- **[aesthetics.md](aesthetics.md)** (required) -- design principles for typography, color, motion, spatial composition, and backgrounds. Follow its rules to avoid generic AI aesthetics.
- **[web-standards.md](web-standards.md)** (required) -- implementation rules for accessibility, forms, performance, touch, hydration, and anti-patterns. Follow its rules for technically correct output.

## When to Use

- User wants to generate frontend code from design.json
- User selected a variant and wants to build React from it
- User wants to scaffold a new project with design tokens applied

## Two Modes

### Mode 1: Direct Build

When called without a variant reference:
1. Detect existing project or scaffold new
2. Read design.json and copy.yaml
3. Generate React components in `./src/`

### Mode 2: Build from Variant

When user says "use editorial" (or another variant name):
1. Read chosen variant HTML from `.artifacts/design/variants/{variant}/index.html`
2. Use the variant HTML as layout reference
3. Generate React components matching the variant structure

## Workflow

### Step 1: Gather Context

1. Check for variant reference (if user mentioned a variant name)
2. Locate **design.json** (required) at `.artifacts/design/design.json`
3. Locate **copy.yaml** (optional) at `.artifacts/design/copy.yaml`
4. If no design.json exists, suggest running extract design first

### Step 2: Detect Stack

Check the current directory for existing projects:

1. **package.json** -- look for framework dependencies:
   - `react`, `next` -> React/Next.js
   - `vue`, `nuxt` -> Vue/Nuxt
   - `svelte`, `@sveltejs/kit` -> Svelte/SvelteKit
   - `astro` -> Astro
2. **Config files**: `vite.config.*`, `next.config.*`, etc.
3. If no project detected, ask user:
   - React + Vite + Tailwind
   - Next.js + Tailwind
   - Vue + Vite + Tailwind
   - Svelte + Vite + Tailwind
   - Other (specify)

### Step 3: Scaffold (if needed)

If no project exists, scaffold with the chosen stack.

### Step 4: Generate Components

Map design tokens to CSS variables:

```css
:root {
  --color-primary: {colors.primary.main};
  --color-accent: {colors.accent.main};
  --font-heading: '{typography.fonts.heading}', serif;
  --font-body: '{typography.fonts.body}', sans-serif;
}
```

Import fonts from Google Fonts:

```css
@import url("https://fonts.googleapis.com/css2?family={heading}&family={body}&display=swap");
```

Generate components in:
```
src/
  components/       # Reusable components
  styles/           # Global styles, CSS variables
  pages/ or routes/ # Page components (if applicable)
```

### Step 5: Apply Variant Layout (Mode 2)

When building from a variant:
1. Analyze the HTML structure -- sections, components, layout patterns
2. Extract layout decisions:
   - Hero style (split, centered, fullscreen, text-only)
   - Spacing approach (generous, balanced, compact)
   - Card style (flat, shadow, bordered, none)
   - Section backgrounds (uniform, alternating, gradients)
3. Map to React components matching the variant
4. Apply design.json tokens
5. Populate with copy.yaml content

## Design Quality

**CRITICAL**: Apply [aesthetics.md](aesthetics.md) principles and [web-standards.md](web-standards.md) rules to every component.
Read both before generating code -- aesthetics defines visual direction, web-standards defines technical correctness.

## Implementation Concerns

### Accessibility and Web Standards

Follow [web-standards.md](web-standards.md) for all accessibility, forms, performance, touch, hydration, and anti-pattern rules.

Key design-specific points:
- **Color independence**: never rely on color alone to communicate state. Pair with an icon, text label, or pattern.
- **Focus management**: trap focus inside modals when open.

### Responsive Implementation

- **Mobile-first CSS**: write base styles for mobile, expand with `min-width` media queries.
- **Baseline width**: 375px (iPhone SE). Nothing should break or scroll horizontally below this.
- **Breakpoints**: `sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px -- or follow the project's framework defaults.
- **Touch targets**: minimum 44x44px tap area on mobile for buttons, links, and interactive elements.
- **No horizontal scroll**: verify at every breakpoint. Overflow is always a bug, not a feature.

### Theme Tokens

- **Semantic naming**: organize CSS custom properties by purpose (`--color-surface`, `--color-on-surface`, `--color-primary`, `--color-border`), not by raw value.
- **Dark mode**: support via `prefers-color-scheme` media query or a `.dark` class toggle on `html`/`body`. See web-standards.md for `color-scheme` and `<meta name="theme-color">` rules.
- **Smooth transitions**: list properties explicitly (`transition: background-color 0.2s, color 0.2s`) -- never `transition: all`.

## Image Handling

For images referenced in copy.yaml:
- Use placeholder: `<div className="aspect-video bg-neutral-200" />`
- Add comment: `{/* TODO: Replace with: {visual.description} */}`

## Guidelines

- Always load aesthetics.md and web-standards.md before generating code
- Apply design.json tokens as CSS custom properties, not hardcoded values
- Use placeholder divs for images, never reference external URLs
- Mobile-first CSS with 375px baseline
- Don't use `transition: all` -- list properties explicitly

## Error Handling

- No design.json: suggest running extract design first
- Scaffold failed: check package manager availability
- No copy.yaml: ask user for brief project description
