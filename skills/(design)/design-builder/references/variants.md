# Variant Generation

Generate 4 HTML+CSS layout variants for visual comparison before building React.

## Prerequisites

- **design.json** (required) -- must include the `layout` block with hero type, section flow, and patterns
- **reference image** (required) -- the original image used to extract design tokens
- **copy.yaml** (optional) -- structured content for all sections
- **[aesthetics.md](aesthetics.md)** (required) -- design principles for typography, color, motion, spatial composition, and backgrounds. Follow its rules to avoid generic AI aesthetics.

## When to Use

- User wants to preview different visual treatments before committing
- User wants to compare design directions side-by-side
- User wants to explore how design tokens look with different aesthetics

## Process

### Step 1: Gather Context

1. Locate **design.json** (required) at `.specs/docs/{project-name}/design.json`
2. Locate **copy.yaml** (optional) at `.specs/docs/{project-name}/copy.yaml`
3. Locate **reference image** (required) at `.specs/docs/reference.*`
4. If no design.json exists, suggest running extract design first
5. If no copy.yaml exists, ask user for brief project description

### Step 2: Read Layout + Reference

Read both sources to build a complete picture:

1. **Reference image**: re-read it to understand the full visual composition -- hero arrangement, section flow, card layouts, decorative elements, image placements, background treatments
2. **design.json `layout` block**: read hero type, sectionFlow, and patterns
3. **design.json tokens**: colors, typography, spacing, components, effects, animations, backgrounds

The reference image + layout block define the **structural skeleton**. The tokens define the **visual vocabulary**. Both are inputs for every variant.

### Step 3: Generate All Presets

Generate all 4 presets. Each one uses the same structural skeleton (from reference + layout) but applies a unique mix of visual properties.

Every preset must define its own combination across ALL of these dimensions:

| Dimension | Description |
|-----------|-------------|
| Typography | Font pairing, size scale, weight contrast |
| Color | 60-30-10 distribution, saturation, contrast |
| Spacing | Density -- generous to compact |
| Backgrounds | Section background treatments, gradients, textures |
| Decorative | Which elements are shown, their intensity |
| Motion | Animation style, speed, stagger |
| Hero | Visual treatment of the hero (overlay, gradient, text size) |
| Cards | Shadow, border, background, radius, hover effect |
| Sections | How alternating backgrounds are applied |
| 60-30-10 | How the dominant/secondary/accent ratio shifts |
| Hierarchy | How visual importance is communicated |
| Rhythm | Vertical spacing pattern, repetition vs breaks |

### Step 4: Generate Comparison Page

Create the side-by-side comparison page.

### Step 5: Serve

```bash
npx http-server .specs/docs/{project-name}/variants -o -p 8080
```

Inform user: "Open http://localhost:8080 to compare variants. Tell me which one you prefer (e.g., 'use editorial') and I'll build the React application, or say 'send to Figma' to export for refinement."

Ask this in the user's preferred language (detect from copy.yaml language field or conversation context).

## Output Structure

```
.specs/docs/{project-name}/variants/
  minimal/index.html
  editorial/index.html
  startup/index.html
  bold/index.html
  {custom}/index.html        # If user requested a custom preset
  index.html                 # Side-by-side comparison
```

## How Presets Work

All presets share the **same structural skeleton**:

- Same sections (from `copy.yaml` if available, otherwise from `layout.sectionFlow`)
- Same grid columns per section (from `layout.sectionFlow`)
- Same hero composition type (from `layout.hero`)
- Same content placement (copy in same positions)
- Same image/placeholder positions (from `layout.patterns.imagePlacement`)

The reference image is re-read only for **validation** -- to confirm the generated variants match the original visual structure.

What changes is the **visual treatment** -- each preset is a unique mix across the 12 dimensions listed above.

## 4 Fixed Presets

### minimal -- Refined restraint

A stripped-back interpretation that lets content breathe:

- **Typography**: Distinctive serif/sans pairing, font size as primary hierarchy
- **Color**: Near-monochrome. Accent color only on CTAs and hover states
- **Spacing**: Extra generous whitespace between all elements
- **Backgrounds**: Uniform or very subtle alternation (almost no contrast between sections)
- **Decorative**: Strip to minimum -- thin rules only, remove ornaments and floating elements
- **Motion**: Subtle, slow fade-ins only
- **Hero**: Same composition but lighter treatment -- reduce overlay, mute gradient
- **Cards**: Remove shadows and borders, let typography carry hierarchy
- **Sections**: Minimal background variation, near-uniform
- **60-30-10**: 70% white/neutral, 20% text colors, 10% accent on CTAs only
- **Hierarchy**: Font size as only differentiation
- **Rhythm**: Wide vertical spacing, maximum breathing room

### editorial -- Magazine sophistication

An editorial interpretation with strong typographic character:

- **Typography**: High-contrast serif headings (large/heavy) vs refined sans body
- **Color**: Warm neutrals dominant, accent used sparingly as editorial highlight
- **Spacing**: Generous with consistent vertical rhythm
- **Backgrounds**: Warm white/cream base, dark footer, thin rules as dividers
- **Decorative**: Section numbers (01, 02, 03), vertical accent bars, thin horizontal rules
- **Motion**: Measured, elegant transitions with editorial pacing
- **Hero**: Same composition but with editorial grid feel -- asymmetric text alignment
- **Cards**: Flat with thin borders, editorial grid divisions
- **Sections**: Warm alternation (white/cream), dark accent on footer
- **60-30-10**: 60% warm neutral, 30% primary for headings, 10% accent highlights
- **Hierarchy**: Dramatic typography contrast (size + weight extremes)
- **Rhythm**: Consistent vertical rhythm, grid-based alignment

### startup -- Premium SaaS polish

A modern tech interpretation with conversion-focused energy:

- **Typography**: Geometric sans-serif, clean and confident
- **Color**: Dark hero with glowing accents, bright white content sections
- **Spacing**: Balanced, optimized for conversion flow
- **Backgrounds**: Dark hero/CTA sections with glow effects, alternating white/lavender between
- **Decorative**: Badges/pills, glass-morphism, subtle grid/dot patterns, glow effects behind CTAs
- **Motion**: Micro-interactions on hover (lift, glow), staggered scroll reveals
- **Hero**: Same composition with gradient glow enhancement, glass-morphism on floating elements
- **Cards**: Soft shadows, rounded borders, gradient border on hover (background-clip trick)
- **Sections**: Strong alternation (dark/white/lavender), clear visual separation
- **60-30-10**: 60% white sections, 30% primary for dark sections, 10% gradient CTAs
- **Hierarchy**: Color saturation and size for CTAs, subtle secondary text
- **Rhythm**: Repeating component patterns, uniform spacing

### bold -- High-impact statement

A dramatic interpretation with maximum visual intensity:

- **Typography**: Display font with extreme size contrast (hero 6rem+)
- **Color**: Primarily dark palette, accent color used aggressively
- **Spacing**: Compact, high-density information, less breathing room
- **Backgrounds**: Dark gradients throughout, solid dark colors, minimal white
- **Decorative**: Marquee ticker, text glow/shadow effects, gradient dividers, noise textures
- **Motion**: Confident, quick transitions with visual impact
- **Hero**: Same composition but dark and intense -- strong glow, large text shadow
- **Cards**: Strong borders, solid colored backgrounds (not white), inverted text
- **Sections**: Dark gradients or solid colors, almost no white sections
- **60-30-10**: 60% dark primary, 30% accent/lighter shades, 10% white for contrast
- **Hierarchy**: Extreme scale differences (giant headlines vs small body)
- **Rhythm**: Intentional asymmetry, pattern breaks for emphasis

### Custom Presets

Users can request a custom preset by describing what they want. Generate it
alongside the 4 fixed presets using the same structural skeleton and a custom
mix of the 12 visual dimensions.

## Design Quality

**CRITICAL**: Apply [aesthetics.md](aesthetics.md) principles to every variant.
Read it before generating -- it defines typography, color, motion, spatial composition, backgrounds, visual hierarchy, and anti-patterns. Each variant must feel like a different designer made it.

## Comparison Page Template

Generate `index.html` with all variants in a dark UI for side-by-side comparison:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Design Variants</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background: #0a0a0a; color: #fafafa;
      font-family: system-ui, -apple-system, sans-serif;
      padding: 24px; min-height: 100vh;
    }
    h1 { font-size: 1.5rem; font-weight: 500; margin-bottom: 24px; color: #a1a1aa; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
      gap: 24px;
    }
    .variant {
      background: #18181b; border-radius: 12px;
      overflow: hidden; border: 1px solid #27272a;
    }
    .variant-header {
      display: flex; justify-content: space-between;
      align-items: center; padding: 12px 16px;
      border-bottom: 1px solid #27272a;
    }
    .variant-info { display: flex; flex-direction: column; gap: 8px; }
    .variant-title h2 { font-size: 0.875rem; font-weight: 500; }
    .badges { display: flex; gap: 6px; flex-wrap: wrap; }
    .badge {
      font-size: 0.625rem; padding: 2px 6px;
      background: #27272a; border-radius: 4px; color: #a1a1aa;
      text-transform: uppercase; letter-spacing: 0.05em;
    }
    .variant-header a { font-size: 0.75rem; color: #3b82f6; text-decoration: none; }
    .variant-header a:hover { text-decoration: underline; }
    .variant iframe { width: 100%; height: 600px; border: none; background: #fff; }
    @media (max-width: 1024px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <h1>Design Variants</h1>
  <div class="grid">
    <!-- One card per variant -->
  </div>
</body>
</html>
```

**Variant card:**

```html
<div class="variant">
  <div class="variant-header">
    <div class="variant-info">
      <div class="variant-title"><h2>{Preset Name}</h2></div>
      <div class="badges">
        <span class="badge">{Font Pairing}</span>
        <span class="badge">{Color Approach}</span>
        <span class="badge">{Density}</span>
      </div>
    </div>
    <a href="./{preset-name}/index.html" target="_blank">Open</a>
  </div>
  <iframe src="./{preset-name}/index.html"></iframe>
</div>
```

## Rules

1. **Always 4+ variants**: Generate all 4 fixed presets (plus custom if requested)
2. **Simple HTML+CSS**: No frameworks, no build tools -- just static files
3. **Preserve tokens**: All variants use the same design.json (colors, fonts base, spacing base)
4. **Preserve layout skeleton**: All variants follow the same structural skeleton from reference image + `design.json > layout`
5. **Identical copy**: Same textual content across all variants
6. **Comment headers**: Each file starts with variant identifier comment
7. **Validation**: If design.json doesn't exist, suggest running extract design first
8. **Apply aesthetics.md**: Follow its guidelines for typography, color, motion, and spatial composition in every variant
9. **Distinct font pairings**: Each variant MUST use a different font combination
10. **Reference validation**: Re-read the reference image to validate structural fidelity
11. **12 dimensions**: Each preset must define its unique mix across all 12 visual dimensions

## Checklist

- [ ] design.json located and read (including `layout` block)
- [ ] copy.yaml located (or user provided description)
- [ ] Reference image re-read for structural validation (if available)
- [ ] All 4 presets generated following layout skeleton
- [ ] Each preset varies all 12 visual dimensions
- [ ] Each preset has a distinct font pairing
- [ ] aesthetics.md principles applied
- [ ] Custom preset generated (if requested)
- [ ] All presets use same structure, different visual treatment
- [ ] Comparison index.html generated
- [ ] http-server started
- [ ] User informed to compare and choose
