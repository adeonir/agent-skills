---
name: handoff
description: "Save current conversation state to disk so a later session resumes with prior context. Captures focus, next step, and working state, plus optional decisions, findings, open threads, blockers, and references; appends snapshots newest-at-top. Use when ending a session before context loss, checkpointing mid-session, saving, loading, or clearing a handoff, or starting a session that should continue prior work. Not for end-of-session persistence across memory systems or for repository-wide project context. argument-hint: \"[focus]\""
---

# Handoff

Capture conversation state to `.artifacts/HANDOFF.md` so a later session resumes with prior context. Three ops: save, load, clear.

## Triggers

- **Save** ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff") → [save.md](references/save.md)
- **Load** ("resume session", "load handoff", "continue from last") → [load.md](references/load.md)
- **Clear** ("clear handoff", "reset handoff") → see Clear below

## Workflow

```text
save  → prepend snapshot at top of .artifacts/HANDOFF.md
load  → read topmost snapshot, index the older ones
clear → overwrite .artifacts/HANDOFF.md with empty content
```

## Clear

Write empty content to `.artifacts/HANDOFF.md`. Do not delete the file — an empty file is treated as missing on next load, and writing avoids a Bash permission prompt. Silent no-op when the file is already absent.
