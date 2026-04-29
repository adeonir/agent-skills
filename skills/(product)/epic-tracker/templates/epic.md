---
name: {{epic-name}}
title: {{Epic Title}}
status: planned
created: {{YYYY-MM-DD}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Epic Title}}

{{What the epic is about, why it exists, what changes for the user. Use a real scenario to illustrate the problem and the desired outcome.}}

## Stories

- [ ] {{story-name}} -- {{brief description of what this story delivers}}
- [ ] {{story-name}} -- {{brief description}}

{Stories are linked when created: [001-story-name](001-story-name.md) -- description}

## Scope

**In:**
- {{What's included}}

**Out:**
- {{What's explicitly excluded}}

## Rabbit Holes

- {{Known complexity or trap to avoid}}

## Acceptance Criteria

- [ ] {{High-level verifiable condition for the epic as a whole}}
- [ ] {{Another testable condition}}

## References

- **PRD:** {{link or "None"}}
- **Design Doc:** {{link or "None"}}
- **Figma:** {{link or "None"}}
