# Frontend Building

Build production-grade React components from design tokens.

## Prerequisites

- **design.json** (required) -- must include the `layout` block
- **copy.yaml** (optional) -- structured content
- **[aesthetics.md](aesthetics.md)** (required) -- design principles for typography, color, motion, spatial composition, and backgrounds. Follow its rules to avoid generic AI aesthetics.

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
1. Read chosen variant HTML from `.specs/docs/{project-name}/variants/{variant}/index.html`
2. Use the variant HTML as layout reference
3. Generate React components matching the variant structure

## Process

### Step 1: Gather Context

1. Check for variant reference (if user mentioned a variant name)
2. Locate **design.json** (required) at `.specs/docs/{project-name}/design.json`
3. Locate **copy.yaml** (optional) at `.specs/docs/{project-name}/copy.yaml`
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

**CRITICAL**: Apply [aesthetics.md](aesthetics.md) principles to every component.
Read it before generating code -- it defines typography, color, motion, spatial composition, backgrounds, visual hierarchy, and anti-patterns.

## Implementation Concerns

### Accessibility

- **Semantic HTML**: use `nav`, `main`, `section`, `article`, `header`, `footer` -- never build page structure with `div` alone.
- **`prefers-reduced-motion`**: wrap all animations in a media query. Users who opt out get instant transitions, not frozen mid-states.
- **Focus management**: include a skip-to-content link as the first focusable element. Trap focus inside modals when open.
- **Color independence**: never rely on color alone to communicate state. Pair with an icon, text label, or pattern.

### Responsive Implementation

- **Mobile-first CSS**: write base styles for mobile, expand with `min-width` media queries.
- **Baseline width**: 375px (iPhone SE). Nothing should break or scroll horizontally below this.
- **Breakpoints**: `sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px -- or follow the project's framework defaults.
- **Touch targets**: minimum 44x44px tap area on mobile for buttons, links, and interactive elements.
- **No horizontal scroll**: verify at every breakpoint. Overflow is always a bug, not a feature.

### Theme Tokens

- **Semantic naming**: organize CSS custom properties by purpose (`--color-surface`, `--color-on-surface`, `--color-primary`, `--color-border`), not by raw value.
- **Dark mode**: support via `prefers-color-scheme` media query or a `.dark` class toggle on `html`/`body`.
- **Smooth transitions**: apply `transition: background-color 0.2s, color 0.2s` to themed elements for seamless theme switching.

## Image Handling

For images referenced in copy.yaml:
- Use placeholder: `<div className="aspect-video bg-neutral-200" />`
- Add comment: `{/* TODO: Replace with: {visual.description} */}`

## Checklist

- [ ] Variant reference read (if applicable)
- [ ] Stack detected or chosen by user
- [ ] Project scaffolded (if needed)
- [ ] design.json tokens applied as CSS variables
- [ ] Content from copy.yaml or user description included
- [ ] Layout matches variant structure (if applicable)
- [ ] Fonts imported
- [ ] Hover states on all interactive elements
- [ ] Animations implemented
- [ ] Responsive breakpoints

## Error Handling

- **No design.json**: Suggest running extract design first
- **Scaffold failed**: Check package manager availability
- **No copy.yaml**: Ask user for brief project description
