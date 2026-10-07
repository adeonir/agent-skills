---
name: handoff
description: "Conversation handoff scoped to the current project, for resuming work in a later session. Use when checkpointing mid-task, pausing work to pick up later, loading or resuming prior context, or clearing a handoff. Not for end-of-session notes, handoffs between projects, or repository-wide project context."
argument-hint: "load | clear | [focus]"
---

# Handoff

## Triggers

- **Save** ("save context", "dump conversation", "checkpoint this", "session handoff", "save handoff") → [save.md](instructions/save.md)
- **Load** ("resume session", "load handoff", "continue from last") → [load.md](instructions/load.md)
- **Clear** ("clear handoff", "reset handoff") → [clear.md](instructions/clear.md)

`/handoff load` → load. `/handoff clear` → clear. Any other argument, or none → save, with the argument as the focus.

Capture conversation state in one consolidated `.artifacts/HANDOFF.md` so a later session resumes with prior context.

## Workflow

```text
save  → consolidate current context into .artifacts/HANDOFF.md
load  → read the consolidated handoff
clear → overwrite .artifacts/HANDOFF.md with empty content
```
