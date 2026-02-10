# Frontend Building

Build production-grade React components from design tokens.

## Prerequisites

- **design.json** (required) -- must include the `layout` block
- **copy.yaml** (optional) -- structured content
- **frontend-design skill** (required) -- use it for all design decisions. It provides typography, color, motion, spatial composition, and background guidelines. Follow its rules to avoid generic AI aesthetics.

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

## Design Quality (frontend-design skill)

**CRITICAL**: The `frontend-design` skill is required for generating production-grade code.
Follow its guidelines for typography, color, motion, spatial composition, and backgrounds.
Never generate code without applying these principles.

### DO

1. **Typography extremes**: weights 100/200 vs 800/900, size jumps 3x+
2. **Dominant colors**: sharp accents, not evenly distributed
3. **One animation moment**: well-orchestrated page load with stagger
4. **Atmospheric backgrounds**: gradients, noise, patterns
5. **Generous whitespace**: match design.json spacing
6. **All hover states**: every interactive element
7. **Alternate sections**: different backgrounds between sections

### NEVER

1. Inter, Roboto, Arial as primary fonts (unless design.json specifies them)
2. Purple gradients on white
3. Predictable centered layouts only
4. Missing hover states
5. Icons only without context
6. Cramped spacing

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
