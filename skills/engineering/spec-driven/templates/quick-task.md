---
slug: {{slug}}
status: pending
branch: {{branch-name or main}}
created: {{YYYY-MM-DD}}
completed: {{YYYY-MM-DD or empty}}
patterns_discovered: {{list or empty}}
follow_up: {{list or empty}}
---

# Quick Task: {{Description}}

## What

{{One-sentence description of the change}}

## Files

- {{file to modify, if known}}

## Expected Outcome

{{What should be different after the change}}

## Quality Gates

Run after the change, before marking done:

- {{lint command}}
- {{typecheck command}}
- {{test command}}
