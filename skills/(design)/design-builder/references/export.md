# Design Export

Generate HTML optimized for import into design tools (Figma, Penpot).

## When to Use

- User wants to export design to Figma for refinement
- User wants to import HTML into Penpot or other design tools
- User needs a clean HTML representation of the design for handoff

## Supported Tools

### Figma (via YashiTech)

**Prerequisites:**
- [Chrome Extension](https://chromewebstore.google.com/detail/html-to-figma-by-yashi-te/apgdhlibcimkkffajannbmpnbjaealmo)
- [Figma Plugin](https://www.figma.com/community/plugin/1459487250118622106)
- Free tier: 40 imports/week

**Import workflow:**
1. Open Chrome and navigate to http://localhost:8081
2. Click the YashiTech Chrome Extension icon
3. Click "Capture" to save the page
4. Open Figma and run the "HTML to Figma" plugin
5. Upload the captured file

### Penpot

Native HTML/SVG import support (future).

## Process

### Step 1: Gather Context

1. Locate **design.json** (required) at `.specs/docs/{project-name}/design.json`
2. Locate **copy.yaml** (optional) at `.specs/docs/{project-name}/copy.yaml`
3. If no design.json exists, suggest running extract design first

### Step 2: Generate HTML

Generate a single HTML file with embedded CSS:

- Clean semantic HTML structure
- Design tokens mapped to CSS variables
- All sections from copy.yaml
- Proper visual hierarchy

### Step 3: Serve and Instruct

```bash
npx http-server .specs/docs/{project-name}/export -o -p 8081
```

Provide tool-specific import instructions based on what the user is using.

## Output

Save to: `.specs/docs/{project-name}/export/index.html`

## HTML Guidelines for Design Tool Import

For best results when importing to design tools:

1. **Semantic HTML** -- use `nav`, `section`, `article`, `header`, `footer`
2. **Flat structure** -- avoid deeply nested divs (parsers struggle with deep nesting)
3. **Inline styles for key elements** -- ensures styles are captured by the parser
4. **Fixed dimensions for containers** -- use px for main container width
5. **No JavaScript** -- static HTML only
6. **Real text content** -- use actual copy from copy.yaml
7. **Placeholder images** -- use solid color divs with aspect-ratio instead of image tags

## HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{Project Name} - Design Export</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    :root {
      --color-primary: {colors.primary.main};
      --color-accent: {colors.accent.main};
      --color-neutral-white: {colors.neutral.white};
      --color-neutral-cream: {colors.neutral.cream};
      --font-heading: '{typography.fonts.heading}', serif;
      --font-body: '{typography.fonts.body}', sans-serif;
    }

    body {
      font-family: var(--font-body);
      background: var(--color-neutral-white);
      color: var(--color-neutral-charcoal);
    }
  </style>
</head>
<body>
  <nav>...</nav>
  <section class="hero">...</section>
  <section class="features">...</section>
  <footer>...</footer>
</body>
</html>
```

## Rules

1. **Design tokens first** -- always map design.json to CSS variables
2. **Complete content** -- include all sections from copy.yaml
3. **Clean structure** -- semantic HTML, minimal nesting
4. **Visual fidelity** -- match the intended design as closely as possible
5. **Single file** -- everything in one HTML file (no external CSS/JS)

## Error Handling

- **No design.json**: Suggest running extract design first
- **No copy.yaml**: Ask for brief project description
- **Port 8081 in use**: Suggest an alternative port
