# Copy Extraction

Extract structured content from URLs and organize into copy.yaml.

## When to Use

- User provides a URL to extract content from
- User wants to structure website content for redesign
- User needs copy.yaml as input for design extraction or frontend building

## Process

### Step 1: Establish Context

1. Ask user for the project name (kebab-case for directories)
2. Check for existing context in `.specs/docs/`:
   - `prd-{project-name}.md` -- read and extract purpose, audience, tone
   - `brief-{project-name}.md` -- read and extract purpose, audience, tone
3. If neither exists, ask up to 4 context questions:
   - What is the project purpose? (landing page, app, tool)
   - Who is the target audience?
   - What tone should the copy follow? (professional, casual, bold)
   - Any content constraints? (word count, mandatory sections)
4. Summarize understanding before proceeding

### Step 2: Get Source URL

1. Ask user for the URL to analyze
2. Fetch the URL using WebFetch
3. If fetch fails, ask user to paste a screenshot instead

### Step 3: Identify Project Type

Analyze the content and identify the project type:

- Landing page: single page with hero, features, CTA, footer
- Website: multi-page site with navigation between pages
- Web app: interactive application with screens, widgets, auth
- Mobile app: screens, tabs, gestures, native features

Do not use prefixed types. Ask the user and adapt the schema to match what they are building.
Confirm project type with user if unclear.

### Step 4: Extract Content

Analyze the structure and extract all content:

- Navigation structure (logo, links, CTA)
- Section hierarchy with layout information
- Text content (headlines, body, CTAs) preserving original tone
- Visual placeholders with descriptions for image generation
- Copywriting patterns (tone, power words, CTA style)

### Step 5: Generate copy.yaml

**USE TEMPLATE:** `templates/copy.md`

Generate structured content following the template schema. The schema adapts to project type:
- **Landing page**: sections (hero, features, testimonials, cta)
- **Web app**: screens (auth, dashboard, widgets)
- **Mobile app**: screens + native features (gestures, biometric)

Save to `.specs/docs/{project-name}/copy.yaml`. Create directories if needed.

## Rules

1. **Preserve original tone** -- structure content, don't rewrite it
2. **Use Lucide icons** -- suggest appropriate icon names
3. **Mark visuals** -- use `type: "generate"` with detailed descriptions
4. **Document patterns** -- capture copywriting patterns in `copywriting_notes`
5. **Be thorough** -- capture every section, don't skip content

## Fallback

If WebFetch fails:
1. Inform user the URL could not be accessed
2. Ask them to paste a screenshot
3. Analyze the screenshot and extract content

## Next Steps

After generating copy.yaml, suggest:
- "Run extract design to create design tokens from reference images"
- "Or provide reference images for design extraction"
