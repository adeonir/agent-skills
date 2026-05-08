---
name: {{bug-name}}
title: {{Bug Title}}
epic: {{epic-name or omit for standalone}}
type: bug
status: planned
severity: {{critical/high/medium/low}}
created: {{YYYY-MM-DD}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Bug Title}}

{{Brief one-sentence description of the defect.}}

## Expected

{{What should happen}}

## Actual

{{What actually happens}}

## Impact

{{Who is affected and how severely}}

## Steps to Reproduce

1. {{First action}}
2. {{Next step}}
3. {{Step where the bug manifests}}

## Environment

| Field | Value |
|-------|-------|
| Browser | {{e.g., Chrome 122}} |
| OS | {{e.g., macOS 15}} |
| Device | {{e.g., Desktop / iPhone 15}} |
| Version | {{App version or commit hash}} |
| Environment | {{Production / Staging / Local}} |

## Workaround

{{Known mitigation, or "None known"}}

## References

- **Epic:** {{link to parent epic, or "None"}}
- **Related stories:** {{links or "None"}}
