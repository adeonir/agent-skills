---
name: wrap-up
description: >-
  End-of-session command that persists context across auto-memory,
  Basic Memory, and Obsidian. Resolves project from local registry,
  loads any session handoff, then writes auto-memory updates, a BM
  session note, an Obsidian session note (when configured), and an
  Obsidian daily note. Use when finishing a work session, saving
  progress before clearing context, or documenting what was
  accomplished. Triggers: "wrap up", "wrap-up", "end session",
  "finish up", "close session". Not for mid-session note-taking
  (Obsidian writes happen at the end only).
---

# Wrap Up Session

End-of-session documentation across auto-memory, Basic Memory, and Obsidian.

## Workflow

```
mapping --> handoff:Load --> auto-memory --> bm-notes -->
  obsidian-notes --> handoff:Detect+Cleanup
```

Resolve project from current working directory, load any session
handoff (when present), then execute the four note-writing steps in
sequence. No confirmation between note-writing steps. The closing
step runs structural-delta detection — silent unless a delta fires —
then asks before clearing the handoff file.

## Triggers

- **End-of-session command** ("wrap up", "wrap-up", "end session",
  "finish up", "close session") → run all references in sequence

The skill is single-trigger: every invocation runs the full workflow.
Loading order:

1. [mapping.md](references/mapping.md) — resolve project paths and base tags
2. [handoff.md](references/handoff.md) (Load phase) — fold latest snapshot when present
3. [auto-memory.md](references/auto-memory.md) — update Claude Code memory
4. [bm-notes.md](references/bm-notes.md) — write Basic Memory session note
5. [obsidian-notes.md](references/obsidian-notes.md) — write Obsidian session + daily notes
6. [handoff.md](references/handoff.md) (Detect + Cleanup phases) — re-index hint + opt-in clear

## Guidelines

- Call BM and Obsidian MCP tools directly — no skill indirection
- Execute all steps in order without confirmation between them
- Search existing notes before creating new ones to avoid duplicates
- Run auto-memory for every session, even trivial ones
- Skip auto-memory and BM when mapping returns `--` for BM project
- Skip Obsidian session note when mapping returns `--` for Obsidian session
- Always create or update the Obsidian daily note, regardless of mapping
- Be concise in auto-memory, detailed in BM session, brief in Obsidian
- Use BM `[brackets]` and Obsidian `#hashtags` per their respective tools

## Anti-Pattern: Confirmation Between Steps

Pausing for user approval between mapping, auto-memory, BM, and Obsidian
breaks the wrap-up promise: a single command persists everything. The
user has already invoked the skill — that is the confirmation. Run all
steps and report at the end.

## Anti-Pattern: Mixing Note Formats

Basic Memory and Obsidian have different syntaxes — BM uses
`[brackets]` for observations and typed verbs for relations; Obsidian
uses `#hashtags` and `## Relations` typed edges. Cross-pollinating the
formats produces invalid notes in both systems. Each tool gets its own
format, end of story.

## Anti-Pattern: Re-Reading the Session Handoff

The session handoff is read once during the Load phase and shared via
working context with downstream references. Re-reading the file in
bm-notes or obsidian-notes wastes I/O and risks divergence if the file
changes mid-flow. Load once, share, then ask before clearing.
