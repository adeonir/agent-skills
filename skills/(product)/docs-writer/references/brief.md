# Brief -- Executive Summary

## Context

The Brief is a 1-page executive summary generated as a companion output of the PRD workflow. It is not a standalone document type -- it has no separate trigger and no independent discovery phase.

## When Generated

The Brief is produced during the **drafting** phase of the PRD workflow, after discovery, validation, and synthesis are complete. It uses data already collected -- no additional questions are needed.

## When to Use

Generated automatically during PRD drafting. Do not trigger independently -- the PRD workflow handles Brief creation.

## Workflow

```
(PRD discovery -> validation -> synthesis) -> drafting -> PRD + Brief
```

The Brief is always generated alongside the PRD. Both are presented to the user for review before saving.

## Content Source

The Brief distills PRD discovery into a narrative. Each section pulls from discovery topics collected during the PRD workflow:

| Brief Section | Discovery Source |
|---------------|-----------------|
| What | Topic 1: Problem + Topic 4: Value & Scope (what is being built and why) |
| Why | Topic 3: Market & Differentiation + Topic 4: Value & Scope (gap, differentiator, value model) |
| Who | Topic 2: Users (persona, job to be done, switching motivation) |
| Scope | Topic 4: Value & Scope (must-haves only) |
| Success Metrics | Topic 1: Problem (goals and targets from PRD section 2) |
| Risks | Validation phase (risks and unvalidated hypotheses) |

Note: Topic 3 (Market & Differentiation) is discovered during PRD discovery but flows exclusively to the Brief, not to the PRD.

## Template

**USE TEMPLATE:** `templates/brief.md`

## Guidelines

**DO:**
- Keep it to 1 page equivalent -- concise and scannable
- Write What, Why, Who as narrative paragraphs
- List only must-haves in Scope -- the full MoSCoW breakdown lives in the PRD
- Pull Success Metrics from Goals & Success Metrics in PRD section 2
- Surface risks that could change the direction
- Omit sections that have no data from discovery rather than writing TBD -- the brief should only contain what is known
- Tell the story of the product -- the PRD provides the specification

**DON'T:**
- Use bullet lists for What, Why, Who sections
- Include the full MoSCoW breakdown -- that belongs in the PRD
- Turn Risks into an exhaustive risk register
- Write TBD for sections with no discovery data -- omit them instead
- Duplicate structure between the Brief and the PRD

## Output

Save to: `.artifacts/docs/brief.md`
