---
name: wrap-up
description: >-
  End-of-session command that persists context to Obsidian. Resolves
  project from local registry, loads any session handoff, then writes
  an Obsidian session note (when configured) and an Obsidian daily
  note. Use when finishing a work session, saving progress before
  clearing context, or documenting what was accomplished. Triggers:
  "wrap up", "wrap-up", "end session", "finish up", "close session".
  Not for mid-session note-taking (Obsidian writes happen at the end
  only).
---

# Wrap Up Session

End-of-session documentation to Obsidian.

## Workflow

```
mapping --> handoff:Load --> obsidian-notes (enrich + compose) --> handoff:Detect+Cleanup
```

Resolve project from current working directory, load any session
handoff (when present), then write Obsidian notes. `obsidian-notes`
opens with an Enrich step that folds relevant current-session
observations from claude-mem into working context (silent skip when
MCP unavailable). No confirmation between note-writing steps. The
closing step runs structural-delta detection — silent unless a delta
fires — then clears the handoff file automatically (wrap-up has
already persisted the snapshot to Obsidian, so the on-disk copy is
redundant).

## Triggers

- **End-of-session command** ("wrap up", "wrap-up", "end session",
  "finish up", "close session") → run all references in sequence

The skill is single-trigger: every invocation runs the full workflow.
Loading order:

1. [mapping.md](references/mapping.md) — resolve project paths and base tags
2. [handoff.md](references/handoff.md) (Load phase) — fold latest snapshot when present
3. [obsidian-notes.md](references/obsidian-notes.md) — write Obsidian session + daily notes
4. [handoff.md](references/handoff.md) (Detect + Cleanup phases) — re-index hint + auto-clear

## Guidelines

- Call Obsidian MCP tools directly — no skill indirection
- Execute all steps in order without confirmation between them
- Search existing notes before creating new ones to avoid duplicates
- Skip Obsidian session note when mapping returns `--` for Obsidian session
- Always create or update the Obsidian daily note, regardless of mapping
- Keep session and daily notes brief and human-scannable
- Use Obsidian `#hashtags` for observations and `## Relations` typed edges

## Anti-Pattern: Confirmation Between Steps

Pausing for user approval between mapping and obsidian-notes breaks
the wrap-up promise: a single command persists everything. The user
has already invoked the skill — that is the confirmation. Run all
steps and report at the end.

## Anti-Pattern: Re-Reading the Session Handoff

The session handoff is read once during the Load phase and shared via
working context with downstream references. Re-reading the file in
obsidian-notes wastes I/O and risks divergence if the file changes
mid-flow. Load once, share, then clear at the end.
