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

- [P1] As a {{user}}, I want {{goal}} so that {{benefit}}

## Functional Requirements

- [ ] FR-001: {{requirement}}

## Acceptance Criteria

- [ ] AC-001: WHEN {{trigger}} THEN {{expected behavior}}

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
