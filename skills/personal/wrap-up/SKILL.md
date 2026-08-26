---
name: wrap-up
description: "End-of-session context persistence to Obsidian. Use when closing a session, saving work, or documenting what was accomplished. Not for mid-session notes, conversation handoffs, or repository-wide project context."
---

# Wrap Up Session

## Triggers

- **End-of-session command** ("wrap up", "wrap-up", "end session", "finish up", "close session") → run the full workflow

End-of-session documentation to Obsidian.

The skill is single-trigger: every invocation runs the full workflow. Loading order:

1. [mapping.md](references/mapping.md) — resolve project paths and base tags
2. [handoff.md](references/handoff.md) (Load phase) — load the consolidated handoff when present
3. [notes.md](references/notes.md) — write Obsidian session + daily notes
4. [handoff.md](references/handoff.md) (Cleanup phase) — auto-clear the handoff file

## Workflow

```text
mapping → handoff:Load → notes (compose) → handoff:Cleanup
```

## Anti-Pattern: Confirmation Between Steps

Do not pause for confirmation between mapping and note creation. The initial invocation authorizes every step. Run the full workflow and report at the end.
