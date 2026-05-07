---
name: {{story-name}}
title: {{Story Title}}
epic: {{epic-name}}
status: planned
created: {{YYYY-MM-DD}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Story Title}}

{{What this story delivers, who benefits, what changes for the user. One story, one outcome.}}

## Acceptance Criteria

> Format: Given/When/Then, 1:1 per AC. No compound clauses. Each AC has a stable id (`AC-1`, `AC-2`, ...; dash-separated, no zero-padding). The skill validates this on create and on edits that change AC text. See `references/ac-validation.md` for the rules.

### AC-1

- **Given:** {{precondition -- single, concrete state}}
- **When:** {{single user or system action}}
- **Then:** {{single observable outcome}}

### AC-2

- **Given:** {{precondition}}
- **When:** {{action}}
- **Then:** {{observable outcome}}

## Rabbit Holes

- {{Known complexity specific to this story}}

## References

- **Epic:** {{link to parent epic}}
- **Design Doc:** {{link or "None"}}
- **Figma:** {{link or "None"}}
