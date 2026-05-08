# Brief — Executive Summary

1-page executive summary of the PRD, generated alongside the PRD draft.

## When to Use

Generated automatically during PRD drafting. Do not trigger
independently — the PRD workflow handles Brief creation.

## Scope

The Brief distills the PRD into a narrative readable in under a minute —
the story of the product, while the PRD remains the specification. Not a
standalone document type: no separate trigger, no independent discovery
phase.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

```
(PRD discovery -> validation -> synthesis) -> drafting -> PRD + Brief
```

The Brief is always generated alongside the PRD. Both are presented to
the user for review before saving.

## Content Source

The Brief distills PRD discovery into a narrative. Each section pulls
from discovery topics collected during the PRD workflow:

| Brief Section | Discovery Source |
|---------------|-----------------|
| What | Topic 1: Problem + Topic 4: Value & Scope (what is being built and why) |
| Why | Topic 3: Market & Differentiation + Topic 4: Value & Scope (gap, differentiator, value model) |
| Who | Topic 2: Users (persona, job to be done, switching motivation) |
| Scope | Topic 4: Value & Scope (must-haves only) |
| Success Metrics | Topic 1: Problem (goals and targets from PRD section 2) |
| Risks | Validation phase (risks and unvalidated hypotheses) |

Note: Topic 3 (Market & Differentiation) is discovered during PRD
discovery but flows exclusively to the Brief, not to the PRD.

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
---

# Brief

## What

{{One paragraph: what is being built and what problem it solves. Include who has the problem and what evidence supports it.}}

## Why

{{One paragraph: why this matters now. What gap exists in current solutions, what makes this approach different, and how it generates value.}}

## Who

{{One paragraph: the primary user, their job to be done, and why they would switch from the status quo.}}

## Scope

- {{Core deliverable that defines this product}}
- {{Another must-have capability}}

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| {{Key performance indicator}} | {{Concrete target or threshold}} | {{Method or tool}} |

## Risks

- {{Top risk or unvalidated assumption that could change the direction}}
- {{Known complexity or trap to avoid (rabbit hole)}}
- {{Another risk or hypothesis that needs evidence}}
````

## Guidelines

- Keep it to 1 page equivalent — concise and scannable
- Write What, Why, Who as narrative paragraphs
- List only must-haves in Scope — the full MoSCoW breakdown lives in the PRD
- Pull Success Metrics from Goals & Success Metrics in PRD section 2
- Surface risks that could change the direction
- Omit sections that have no data from discovery rather than writing TBD
- Tell the story of the product — the PRD provides the specification

## Anti-Pattern: Bullet-Listed Narrative

What, Why, and Who are stories, not feature lists. Bullet-listing them
strips the narrative thread that makes the Brief readable in under a
minute. Use prose paragraphs; reserve bullets for Scope and Risks.

## Anti-Pattern: Duplicated Specification

The Brief is not a shorter PRD. Don't recreate the MoSCoW breakdown,
exhaustive risk register, or full requirements list. Each section
distills discovery into a narrative summary; the PRD holds the
specification.

## Output

Save to: `.artifacts/docs/brief.md`
