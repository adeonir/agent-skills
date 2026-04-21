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

### P1: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P1:** {{why this is critical for MVP}}
- **Independent Test:** {{how to verify this story works alone}}

**Acceptance Criteria:**

- [ ] AC-001 `pending`: WHEN {{trigger}} THEN system SHALL {{expected behavior}}
- [ ] AC-002 `pending`: WHEN {{trigger}} THEN system SHALL {{expected behavior}}

### P2: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P2:** {{why this matters but is not MVP}}

**Acceptance Criteria:**

- [ ] AC-003 `pending`: WHEN {{trigger}} THEN system SHALL {{expected behavior}}

### P3: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P3:** {{why this is nice-to-have}}

**Acceptance Criteria:**

- [ ] AC-004 `pending`: WHEN {{trigger}} THEN system SHALL {{expected behavior}}

{{#if designs}}
## Visual References

{{#each designs}}
![{{description}}](designs/{{filename}})
{{description of what this image shows}}

{{/each}}
{{/if}}

## Edge Cases

- WHEN {{boundary condition}} THEN system SHALL {{behavior}}
- WHEN {{error scenario}} THEN system SHALL {{graceful handling}}
- WHEN {{unexpected input}} THEN system SHALL {{validation response}}

## Success Criteria

- [ ] {{Measurable outcome -- e.g., "User can complete X in under 2 minutes"}}
- [ ] {{Measurable outcome -- e.g., "Zero errors in Y scenario"}}

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
