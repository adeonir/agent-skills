---
id: {{ID}}
feature: {{name}}
type: {{greenfield|brownfield}}
scope: {{medium|large|complex}}
status: draft
branch: {{branch-name or main}}
created: {{YYYY-MM-DD}}
---

# Feature: {{Title}}

## Overview

{{Problem description: what pain point are we solving, who is affected, why now}}

## Goals

- [ ] {{Primary goal with measurable outcome}}
- [ ] {{Secondary goal with measurable outcome}}

## Out of Scope

| Feature | Reason |
|---------|--------|
| {{feature}} | {{why excluded}} |

## User Stories

### S-1 [P1] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P1:** {{why this is critical for MVP}}
- **Independent Test:** {{how to verify this story works alone}}

**Acceptance Criteria:**

- [ ] AC-1 `pending`: GIVEN {{precondition}} WHEN {{action}} THEN {{observable outcome}}
  - **Audit-tool measurement:** {{tool name}} -- {{exact metric}} -- pass threshold: {{numeric or boolean}}
- [ ] AC-2 `pending`: GIVEN {{precondition}} WHEN {{action}} THEN {{observable outcome}}

### S-2 [P2] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P2:** {{why this matters but is not MVP}}

**Acceptance Criteria:**

- [ ] AC-3 `pending`: GIVEN {{precondition}} WHEN {{action}} THEN {{observable outcome}}

### S-3 [P3] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P3:** {{why this is nice-to-have}}

**Acceptance Criteria:**

- [ ] AC-4 `pending`: GIVEN {{precondition}} WHEN {{action}} THEN {{observable outcome}}

{{#if designs}}
## Visual References

{{#each designs}}
![{{description}}](designs/{{filename}})
{{description of what this image shows}}

{{/each}}
{{/if}}

## Edge Cases

- GIVEN {{precondition}} WHEN {{boundary condition}} THEN {{observable handling}}
- GIVEN {{precondition}} WHEN {{error scenario}} THEN {{graceful handling}}
- GIVEN {{precondition}} WHEN {{unexpected input}} THEN {{validation response}}

## Success Criteria

- [ ] {{Measurable outcome -- e.g., "User can complete X in under 2 minutes"}}
- [ ] {{Measurable outcome -- e.g., "Zero errors in Y scenario"}}

## Operational Follow-ups

Post-deploy observations, monitoring windows, or runbook tasks that cannot be verified at audit time. Recorded here so the spec captures intent, but **not audit targets** -- audit only checks Goals and Success Criteria.

- {{Operational item, e.g., "Post-deploy monitoring: zero rejections in payment flow over 7 days"}}
- {{or write "None" if every criterion is pre-merge verifiable}}

## Open Questions

- {{Any unresolved questions, or "None" if all resolved}}

## Notes

{{additional behavioral context -- evidence, stakeholders, deadlines; never technology choices, component names, or file paths}}

{{#if brownfield}}
## Baseline

### Current Behavior

- {{What users observe today -- no component names, no code identifiers}}

### Gaps / Limitations

- {{What's missing or problematic, described as user impact}}
{{/if}}
