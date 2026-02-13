# Design Extraction

Extract design tokens from reference images and generate design.json.

## When to Use

- User provides reference images (pasted, file path, or URL)
- User wants to extract a design system from screenshots or mockups
- User wants to generate design tokens from a style description (no images)

## Process

### Step 1: Establish Context

1. Ask user for the project name (if not already established)
2. Check for existing context in `.specs/docs/`:
   - `prd-{project-name}.md` -- read and extract purpose, audience, tone, features
   - `brief-{project-name}.md` -- read and extract purpose, audience, tone
   - `{project-name}/copy.yaml` -- content context
3. If no PRD/Brief exists, ask up to 4 context questions:
   - What is the project purpose? (landing page, app, tool)
   - Who is the target audience?
   - What is the visual reference? (URLs, screenshots, descriptions)
   - Any brand or style constraints? (colors, fonts, existing guidelines)
4. Summarize understanding before proceeding

### Step 2: Get Reference Input

**If images are provided** (pasted, file path, or URL):
1. Analyze each image for design tokens
2. If multiple images have conflicting styles, ask user which to prioritize:
   - Option A: describe style 1
   - Option B: describe style 2
   - Option C: merge (use X from A, Y from B)

**If no images are provided:**
1. Ask user about visual direction:
   - Tone (professional, playful, minimal, bold)
   - Color mood (warm neutrals, cool blues, vibrant, monochrome)
   - Typography mood (serif headings + sans body, all geometric, editorial)
   - Any inspirations or websites they admire
2. Generate tokens from the description

### Step 3: Deep Analysis

Extract from each image:
- Exact color values (HEX, not approximations)
- Font families (suggest Google Fonts equivalents if unsure)
- Spacing patterns (section padding, component gaps)
- Component styles (buttons, cards, badges, inputs)
- Animation and interaction patterns
- Background treatments (gradients, textures, patterns)
- **Layout structure** (hero composition, section flow, grid patterns, decorative elements)

### Step 4: Generate design.json

**USE TEMPLATE:** `templates/design.md`

Generate design tokens following the template schema. Key sections:
- **principles**: vision, keywords, follow (guidelines), avoid (anti-patterns)
- **colors**: primary, secondary, background, text, semantic palettes
- **typography**: fonts, scale (hero, h2, h3, body, small, label)
- **spacing**: section padding, container max-width, grid, component gaps
- **components**: button, card, badge, input, icon specs with all states
- **layout**: hero composition, section flow, grid patterns, decorative elements
- **animations**: entrance types, interaction effects, transition defaults
- **backgrounds**: hero treatment, section backgrounds, gradient definitions
- **responsive**: breakpoints, mobile adaptations

Save to `.specs/docs/{project-name}/design.json`. Create directories if needed.

### Step 5: Validate Output

Run the validation checklist before presenting the result:

- [ ] All semantic colors defined (primary, secondary, background, text)
- [ ] Font families resolved with Google Fonts equivalents
- [ ] Layout block filled (hero composition, at least 2 sections)
- [ ] Hover states defined for all interactive components
- [ ] `principles.avoid` has at least 2 anti-patterns
- [ ] `principles.follow` has at least 2 guidelines
- [ ] Animations defined (entrance + interaction)
- [ ] Backgrounds defined for hero and at least one section
- [ ] Typography scale includes hero, body, and label sizes

If any item fails, fix it before saving. Report remaining gaps in `notes.uncertainties`.

## Rules

1. **Extract EXACT values** -- use color picker precision, don't approximate
2. **Identify fonts** -- suggest Google Fonts equivalents if unsure
3. **Capture ALL states** -- hover, focus, active, disabled
4. **Document anti-patterns** -- in `principles.avoid`, list what NOT to do
5. **Be specific** -- values in px, rem, hex. Nothing generic.
6. **Capture layout structure** -- the `layout` block is critical for downstream variant generation. Document hero composition, section flow order, grid patterns, card styles, and decorative elements exactly as they appear in the reference.

## What to AVOID in design.json

- Generic purple gradients
- Inter as the only font
- 8px border-radius on everything
- Heavy drop shadows
- Cramped spacing
- Missing hover states
- Vague descriptions like "nice blue"

## Next Steps

After generating design.json, suggest:
- "Run build frontend to generate React components"
- "Run generate variants to preview 4 layout options before building"
- "Run export design to generate HTML for Figma/Penpot import"
