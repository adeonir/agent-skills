Use this template as written:

```yaml
metadata:
  source: "{{URL, brief file, screenshot description, or 'none'}}"
  extraction_date: "{{YYYY-MM-DD}}"

project:
  name: "{{Project Name}}"
  language: "{{en | pt | es | ...}}"
  industry: "{{fintech | health | saas | ecommerce | ...}}"
  description: "{{Brief project description}}"

intent:
  status: "{{confirmed | inferred}}"
  purpose: "{{what this copy is trying to do}}"
  reader_goal: "{{what the reader should understand, decide, or do}}"
  function: "{{conversion | brand/editorial | product/UX | informational}}"
  constraints:
    - "{{functional constraint observed in the source, such as no sales CTA}}"

voice:
  status: "{{confirmed | inferred}}"
  line: "{{the voice in one line: 'confident but warm'}}"
  axes: "{{formal|casual, reserved|bold, earnest|dry, plain|playful}}"
  avoid:
    - "{{word or cliché the author refuses}}"

# The content tree mirrors the source. Name surfaces and parts by context.
# `intent` is reserved metadata at this level and at each surface; never use it
# as a content-part key.
# MUST NOT carry upstream scaffolding: no requirement IDs, milestones, sprint
# or release names, roadmap language, or sibling-artifact references: copy only.
# No conversation narrative ("as discussed", "the user confirmed", "we agreed")
# and no history of a value, in any field including `notes`.

content:
  "{{surface key, named by context: home, dashboard, product, checkout}}":
    # Add an intent block only when this surface differs from the root intent.
    # It inherits purpose, reader_goal, and constraints not stated here.
    # intent:
    #   function: "{{surface-specific function}}"
    "{{part key, named by context: hero, features, summary, form}}":
      headline: "{{primary heading, if any}}"
      subheadline: "{{secondary supporting text, if any}}"
      body:
        - "{{block of body copy}}"
      cta:
        text: "{{button or link label}}"
        link: "{{destination URL or #anchor}}"
      images:
        - description: "{{what the image shows: required}}"
          url: "{{source URL: optional, when captured}}"
          alt: "{{alt text: optional, when source declares it}}"
    # Add whatever fields the surface needs: states (empty/loading/error),
    # entry points, product specs, variants, prices: named by what they are.
    # Nest freely; the tree mirrors the source's own structure.

notes: |
  {{Facts about the source, in present tense: content that is unclear,
  surfaces or parts that are empty or dynamically loaded,
  tone or language patterns worth preserving.}}
```
