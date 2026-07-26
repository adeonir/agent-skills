---
name: wrap-up
description: >-
  End-of-session command that persists context to Obsidian. Resolves project
  from local registry, loads any session handoff, then writes an Obsidian
  session note (when configured) and an Obsidian daily note. Use when finishing
  a work session, saving progress before clearing context, or documenting what
  was accomplished. Not for mid-session note-taking (Obsidian writes happen at
  the end only).
---

# Wrap Up Session

End-of-session documentation to Obsidian.

## Triggers

- **End-of-session command** ("wrap up", "wrap-up", "end session", "finish up", "close session") → run all references in sequence

The skill is single-trigger: every invocation runs the full workflow. Loading order:

1. [mapping.md](references/mapping.md) — resolve project paths and base tags
2. [handoff.md](references/handoff.md) (Load phase) — fold all snapshots, grouped by date, when present
3. [notes.md](references/notes.md) — write Obsidian session + daily notes
4. [handoff.md](references/handoff.md) (Cleanup phase) — auto-clear the handoff file

## Workflow

```text
mapping → handoff:Load → notes (enrich + compose) → handoff:Cleanup
```

## Anti-Pattern: Confirmation Between Steps

Pausing for user approval between mapping and notes breaks the wrap-up promise: a single command persists everything. The user has already invoked the skill — that is the confirmation. Run all steps and report at the end.
