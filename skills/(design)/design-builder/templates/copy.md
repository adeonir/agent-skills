---
name: {{project-name}}
source: {{url, captured region, brief file, or description}}
project_type: {{landing-page/website/web-app/mobile-app}}
language: {{en/pt/es/etc}}
industry: {{fintech/health/saas/ecommerce/etc}}
created: {{YYYY-MM-DD}}
---

# Copy Extraction: {{Project Name}}

## Output

Save as `.artifacts/design/copy.yaml` using the schema below.

## Schema

```yaml
metadata:
  source: "{{url, captured region, brief file, or description}}"
  extraction_date: "{{YYYY-MM-DD}}"
  version: "1.0.0"

project:
  name: "{{project-name}}"
  type: "{{landing-page/website/web-app/mobile-app}}"
  language: "{{en/pt/es/etc}}"
  industry: "{{fintech/health/saas/ecommerce/etc}}"
  description: "{{Brief project description}}"

# For page-based (landing-page, website): use `sections`.
# For screen-based (web-app, mobile-app): use `screens`.

sections:
  "{{section_id, e.g., hero, features, testimonials}}":
    headline: "{{primary heading text as it appears on the page}}"
    subheadline: "{{secondary text that supports or expands the headline}}"
    body:
      - "{{first block of body copy, preserving original tone and structure}}"
      - "{{additional body copy if the section has multiple paragraphs}}"
    cta:
      text: "{{button or link label, e.g., Get Started, Learn More}}"
      link: "{{destination url or #anchor reference}}"

screens:
  "{{screen_id, e.g., auth, home, detail, settings}}":
    purpose: "{{what this screen does for the user}}"
    entry_points: ["{{how the user arrives here}}"]
    primary_action:
      label: "{{button or gesture label}}"
      outcome: "{{what happens on trigger}}"
    content:
      headline: "{{primary text if any}}"
      body: ["{{body copy elements}}"]
    states: ["{{empty/loading/error/populated}}"]

notes: |
  {{Observations about the extraction -- content that was unclear,
  sections or screens that appeared empty or dynamically loaded,
  tone or language patterns worth preserving}}
```

## Schema Adapts by Project Type

- **landing-page**: `sections` (hero, features, testimonials, cta, footer)
- **website**: `sections` grouped by page with navigation structure and per-page hierarchy
- **web-app**: `screens` (auth, dashboard, settings) with interactive elements and states
- **mobile-app**: `screens` plus native patterns (tabs, gestures, biometric, sheets)

Keep only the fields relevant to the project type. Remove the unused block
(`sections` or `screens`) before saving.
