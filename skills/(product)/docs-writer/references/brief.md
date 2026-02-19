# Brief -- Executive Summary

## Context

The Brief is a 1-page executive summary generated as a companion output of the PRD workflow. It is not a standalone document type -- it has no separate trigger and no independent discovery phase.

## When Generated

The Brief is produced during the **drafting** phase of the PRD workflow, after discovery, validation, and synthesis are complete. It uses data already collected -- no additional questions are needed.

## Workflow

```
(PRD discovery -> validation -> synthesis) -> drafting -> PRD + Brief
```

The Brief is always generated alongside the PRD. Both are presented to the user for review before saving.

## Content Source

All Brief sections map directly to information gathered during PRD discovery and validation:

| Brief Section | Source Phase |
|---------------|-------------|
| Problem | Discovery Stage 1 |
| Proposed Solution | Discovery Stage 2 |
| Target Audience | Discovery Stage 2 |
| Competitive Landscape | Discovery Stage 1 + Validation |
| Differentiator | Discovery Stage 2 + Validation |
| Business Model | Discovery Stage 3 |
| Success Metrics | Discovery Stage 3 + Synthesis |
| Scope (MVP) | Validation |
| Key Risks | Validation |
| Hypotheses to Validate | Validation |

## Template

**USE TEMPLATE:** `templates/brief.md`

## Output

Save to: `.specs/docs/brief.md`

## Guidelines

- Keep it to 1 page equivalent -- concise and scannable
- Every section should be 1-3 sentences max (except tables)
- If a section has no data from discovery, write "TBD" rather than omitting it
- The Brief is a summary, not a lite PRD -- avoid duplicating detail
