---
name: handoff
description: >-
  Save current conversation state to disk so a later session resumes with full
  context. Captures focus and next step, plus optional decisions, findings, open
  threads, blockers, and references; appends snapshots newest-at-top. Use when
  ending a session before context loss, checkpointing mid-session, saving,
  loading, or clearing a handoff, or starting a session that should continue
  prior work. Not for end-of-session persistence across memory systems or for
  repository-wide project context.
argument-hint: "[focus]"
---

# Handoff

Capture conversation state to `.artifacts/HANDOFF.md` so a later
session resumes with full context. Three ops: save, load, clear.

## Workflow

```
save  → append snapshot at top of .artifacts/HANDOFF.md
load  → Read .artifacts/HANDOFF.md; latest snapshot at top
clear → overwrite .artifacts/HANDOFF.md with empty content
```

## Triggers

- **Save** ("save context", "dump conversation", "checkpoint this",
  "session handoff", "save handoff") → [save.md](references/save.md)
- **Load** ("resume session", "load handoff", "continue from last") →
  [load.md](references/load.md)
- **Clear** ("clear handoff", "reset handoff") → see Clear below

## Clear

Write empty content to `.artifacts/HANDOFF.md`. Do not delete the
file — an empty file is treated as missing on next load, and writing
avoids a Bash permission prompt. Silent no-op when the file is
already absent.

## Guidelines

- Append snapshot at top, never bottom — most recent always first
- One snapshot per save; do not merge across saves
- Skip ops silently when file is absent (load and clear no-op)
- Save what is not already in committed artifacts — focus, open
  threads, next step, decisions and findings worth carrying

## Anti-Pattern: Restating Artifacts

Snapshots that repeat content already captured in artifacts on disk,
commits, PRs, issues, or documentation waste space. The handoff
carries context that lives only in the conversation: unresolved
threads, decisions made on the fly, where to pick up, which skill to
invoke next. Anything already persisted elsewhere should be referenced
by path or URL, not duplicated.

## Anti-Pattern: Overwriting on Save

Each save prepends a new dated block at the top. Overwriting destroys
prior snapshots that may still hold useful context for older threads.
Append-at-top preserves history while keeping the latest visible first.
