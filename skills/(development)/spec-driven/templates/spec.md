---
id: {{ID}}
feature: {{name}}
type: {{greenfield|brownfield}}
status: draft
branch: {{branch-name or main}}
created: {{YYYY-MM-DD}}
---

# Feature: {{Title}}

## Overview

{{description}}

## User Stories

### P1: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Independent Test:** {{How to verify this story works alone -- e.g., "Can demo by doing X and seeing Y"}}

### P2: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}

### P3: {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}

## Functional Requirements

- [ ] FR-001: {{requirement}}

## Acceptance Criteria

- [ ] AC-001: WHEN {{trigger}} THEN {{expected behavior}}

## Edge Cases

- WHEN {{boundary condition}} THEN system SHALL {{behavior}}
- WHEN {{error scenario}} THEN system SHALL {{graceful handling}}
- WHEN {{unexpected input}} THEN system SHALL {{validation response}}

## Success Criteria

- [ ] {{Measurable outcome -- e.g., "User can complete X in under 2 minutes"}}
- [ ] {{Measurable outcome -- e.g., "Zero errors in Y scenario"}}

## Out of Scope

- {{What is NOT included in this feature}}

## Open Questions

- {{Any unresolved questions from Step 5, or "None" if all resolved}}

## Notes

{{additional context}}

{{#if brownfield}}
## Baseline

### Current Behavior

- {{What system currently does}}

### Gaps / Limitations

- {{What's missing or problematic}}
{{/if}}
