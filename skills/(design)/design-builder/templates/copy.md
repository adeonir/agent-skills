---
name: {{project-name}}
source: {{url or file used for extraction}}
project_type: {{landing/website/web-app/mobile-app}}
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
  source: "{{url or file}}"
  extraction_date: "{{YYYY-MM-DD}}"
  version: "1.0.0"

project:
  name: "{{project-name}}"
  type: "{{landing/website/web-app/mobile-app}}"
  language: "{{en/pt/es/etc}}"
  industry: "{{fintech/health/saas/ecommerce/etc}}"
  description: "{{Brief project description}}"

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

notes: |
  {{Observations about the extraction -- content that was unclear,
  sections that appeared empty or dynamically loaded,
  tone or language patterns worth preserving}}
```

## Schema Adapts by Project Type

- **Landing page**: sections (hero, features, testimonials, cta, footer)
- **Website**: pages with navigation structure and section hierarchy
- **Web app**: screens (auth, dashboard, settings) with interactive elements
- **Mobile app**: screens + native features (gestures, biometric, tabs)
