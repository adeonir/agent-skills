---
name: handoff
description: "Conversation handoff scoped to the current project, for resuming work across sessions. Use when checkpointing, ending a session, loading prior context, or clearing a handoff. Not for handoffs between projects, durable session notes, or repository-wide project context."
argument-hint: "[focus]"
---

# Handoff

## Triggers

- **Save** ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff") → [save.md](references/save.md)
- **Load** ("resume session", "load handoff", "continue from last") → [load.md](references/load.md)
- **Clear** ("clear handoff", "reset handoff") → see Clear below

Capture conversation state in one consolidated `.artifacts/HANDOFF.md` so a later session resumes with prior context. Three operations: save, load, clear.

## Workflow

```text
save  → consolidate current context into .artifacts/HANDOFF.md
load  → read the consolidated handoff
clear → overwrite .artifacts/HANDOFF.md with empty content
```

## Clear

If `.artifacts/HANDOFF.md` is absent, return no output. Otherwise, write empty content to the file. Do not delete the file. An empty file is treated as missing on the next load, and writing avoids a Bash permission prompt.
