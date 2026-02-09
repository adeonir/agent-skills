# Variant Generation

Generate 4 HTML+CSS layout variants for visual comparison before building React.

## When to Use

- User wants to preview different layout approaches before committing
- User wants to compare design directions side-by-side
- User wants to explore how design tokens look with different structures

## Process

### Step 1: Gather Context

1. Locate **design.json** (required) at `.specs/docs/{project-name}/design.json`
2. Locate **copy.yaml** (optional) at `.specs/docs/{project-name}/copy.yaml`
3. If no design.json exists, suggest running extract design first
4. If no copy.yaml exists, ask user for brief project description

### Step 2: Generate All Presets

Generate all 4 fixed presets plus any custom preset requested by the user.

### Step 3: Generate Comparison Page

Create the side-by-side comparison page.

### Step 4: Serve

```bash
npx http-server .specs/docs/{project-name}/variants -o -p 8080
```

Inform user: "Open http://localhost:8080 to compare variants. Tell me which one you prefer (e.g., 'use editorial') and I'll build the full React application."

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

## 4 Fixed Presets

### minimal -- Ultra clean, content focused

- **Hero**: Large centered text, no background image
- **Spacing**: Extra generous (lots of whitespace)
- **Cards**: No border, no shadow, typography as highlight
- **Sections**: Uniform white background
- **60-30-10**: 70% white, 20% neutral text, 10% accent
- **Hierarchy**: Font size as only differentiation
- **Rhythm**: Wide vertical spacing, simple grid

### editorial -- Magazine feel, elegant and readable

- **Hero**: Split 50/50, image on left
- **Spacing**: Generous (ample whitespace)
- **Cards**: Flat, no shadow
- **Sections**: Uniform background
- **60-30-10**: 60% neutral, 30% primary, 10% accent
- **Hierarchy**: Dramatic typography (high contrast between H1 and body)
- **Rhythm**: Consistent vertical rhythm, 12-column grid

### startup -- Modern SaaS, conversion focused

- **Hero**: Centered, prominent CTA
- **Spacing**: Balanced
- **Cards**: Soft shadows, rounded borders
- **Sections**: Alternating backgrounds (white/gray)
- **60-30-10**: 60% white, 30% primary, 10% CTA color
- **Hierarchy**: Larger and more saturated CTAs, subtle secondary text
- **Rhythm**: Repeating patterns (icon + title + desc), uniform spacing

### bold -- High impact, strong visual statement

- **Hero**: Fullscreen, text over image/gradient
- **Spacing**: Compact (high density)
- **Cards**: Strong borders, solid backgrounds
- **Sections**: Gradients or solid colors
- **60-30-10**: 60% primary dark, 30% accent, 10% white
- **Hierarchy**: Extreme sizes (giant hero text), heavy weights
- **Rhythm**: Intentional asymmetry, pattern breaks for emphasis

### Custom Presets

Users can request a custom preset by describing what they want. Generate it
alongside the 4 fixed presets using the same design.json tokens.

## Design Principles

### 60-30-10 Color Rule

Map colors from design.json according to each preset:

- **60%**: Dominant color (backgrounds, large areas)
- **30%**: Secondary color (headers, key elements)
- **10%**: Accent color (CTAs, highlights)

Each preset distributes these differently -- see the preset definitions above.

### Visual Hierarchy

Each preset applies hierarchy differently:

| Preset | Technique |
|--------|-----------|
| minimal | Font size only |
| editorial | Typography contrast (size + weight) |
| startup | Color saturation for CTAs |
| bold | Extreme scale differences |

### Rhythm and Repetition

| Preset | Approach |
|--------|----------|
| minimal | Maximum whitespace, minimal elements |
| editorial | Consistent vertical rhythm, grid-based |
| startup | Repeating component patterns |
| bold | Intentional breaks for emphasis |

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
        <span class="badge">{Hero Style}</span>
        <span class="badge">{Spacing}</span>
        <span class="badge">{Card Style}</span>
      </div>
    </div>
    <a href="./{preset-name}/index.html" target="_blank">Open</a>
  </div>
  <iframe src="./{preset-name}/index.html"></iframe>
</div>
```

**Badge values per preset:**

| Preset | Hero | Spacing | Cards |
|--------|------|---------|-------|
| minimal | Text Hero | Extra Generous | No Cards |
| editorial | Split Hero | Generous | Flat Cards |
| startup | Centered Hero | Balanced | Shadow Cards |
| bold | Fullscreen Hero | Compact | Bordered Cards |

## Rules

1. **Always 4+ variants**: Generate all 4 fixed presets (plus custom if requested)
2. **Simple HTML+CSS**: No frameworks, no build tools -- just static files
3. **Preserve tokens**: All variants use the same design.json (colors, fonts, spacing base)
4. **Identical copy**: Same textual content across all variants
5. **Comment headers**: Each file starts with variant identifier comment
6. **Validation**: If design.json doesn't exist, suggest running extract design first

## Checklist

- [ ] design.json located and read
- [ ] copy.yaml located (or user provided description)
- [ ] All 4 presets generated
- [ ] Custom preset generated (if requested)
- [ ] All presets use same tokens, different structure
- [ ] Comparison index.html generated
- [ ] http-server started
- [ ] User informed to compare and choose
