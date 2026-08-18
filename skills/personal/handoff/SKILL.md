---
name: handoff
description: "Saves current conversation state to disk so a later session resumes with prior context. Consolidates focus, context, next step, decisions, findings, open threads, blockers, and references into one current handoff. Use when ending a session before context loss, checkpointing mid-session, saving, loading, or clearing a handoff, or starting a session that should continue prior work. Not for durable session notes or repository-wide project context."
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
