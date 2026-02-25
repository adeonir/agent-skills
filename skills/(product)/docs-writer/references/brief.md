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

The Brief distills the PRD into a narrative. Each section pulls from multiple discovery topics:

| Brief Section | Source |
|---------------|--------|
| What | Problem + Value & Scope (what is being built and why) |
| Why | Market & Differentiation + Value & Scope (gap, differentiator, value model) |
| Who | Users (persona, job to be done, switching motivation) |
| Scope | Value & Scope (must-haves only) |
| Open Risks | Validation (risks and unvalidated hypotheses) |

## Template

**USE TEMPLATE:** `templates/brief.md`

## Output

Save to: `.artifacts/docs/brief.md`

## Guidelines

- Keep it to 1 page equivalent -- concise and scannable
- What, Why, Who are narrative paragraphs, not bullet lists
- Scope lists only must-haves -- the full MoSCoW breakdown lives in the PRD
- Open Risks surfaces what could change the direction, not an exhaustive risk register
- If something has no data from discovery, omit it rather than writing TBD -- the brief should only contain what is known
- The Brief tells the story of the product. The PRD provides the specification. Never duplicate structure between them
