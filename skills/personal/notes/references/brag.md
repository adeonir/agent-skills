# Update Brag Document

Add achievements to a brag document for performance reviews and career growth.

## When to Use

- User says "brag document", "my achievements", "add accomplishment"
- User mentions something they're proud of at work
- User wants to track wins for performance review

## Vault Resolution

Load [mapping.md](mapping.md) first to resolve vault root via the 3-tier
fallback (local symlink → global pointer → bootstrap).

## Workflow

1. **Determine time period**
   - Current year: `{{YYYY}}.md`
   - Or by quarter: `{{YYYY}} Q1.md`
   - Ask user preference on first use

2. **Check if brag doc exists**

   ```
   search_notes query="{{YYYY}}" path="Brags/"
   ```

3. **Create or append**
   - If does not exist: create using the template below
   - If exists: append the new achievement to the appropriate category

4. **Gather achievement details**
   - What was accomplished
   - Context (project, team, situation)
   - Result with metrics (quantify when possible)
   - Category (impact, technical, growth)

5. **Write note**

   New document:

   ```
   write_note path="Brags/{{YYYY}}.md" content="..."
   ```

   Append to existing:

   ```
   read_note path="Brags/{{YYYY}}.md"
   patch_note path="Brags/{{YYYY}}.md" oldString="..." newString="..."
   ```

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{brag-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources: []
tags:
  - brag
  - career
  - {{dynamic tags based on content}}
---
# {{Month YYYY}}

{{What this period looked like — themes, milestones, shifts in focus.
Write enough context that future-you can reconstruct what mattered and
why these achievements stand out.}}

## Impact

- **{{achievement with metrics}}**
  - Context: {{situation}}
  - Result: {{quantified outcome}}

## Technical

- {{technical achievements, architecture decisions}}

## Growth

- {{new skills, mentoring, feedback received}}

## Observations

- #achievement {{key accomplishment with metrics}}
- #growth {{skill or area of development}}
- #impact {{business or team impact}}

## Relations

- [[{{Related Note}}]]
````

## Achievement Format

```markdown
- **Reduced API latency by 40% through query optimization**
  - Context: Checkout refactor project
  - Result: Improved user experience, reduced server costs by $2k/month
```

## Guidelines

- Quantify impact when possible (%, $, time saved)
- Include both technical and soft-skill achievements
- Record achievements as they happen — do not wait for review season
- Categorize by type (impact, technical, growth)
- Use active voice ("led", "built", "shipped" — not "was responsible for")

## Categorization

Common categories for organizing brags:

- **Impact** — Business results, user metrics
- **Technical** — Architecture, performance, reliability
- **Growth** — Learning, mentoring, new skills, feedback received

## Anti-Pattern: Vague Impact Claims

"Improved performance" is invisible at review time. "Reduced p99 latency
from 800ms to 220ms" is concrete and defensible. Always quantify with a
metric, a percentage, or a time saved. When data is unavailable, state
the proxy ("estimated 30% fewer support tickets in the affected flow").
