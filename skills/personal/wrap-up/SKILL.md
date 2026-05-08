---
name: wrap-up
description: >-
  End-of-session command that persists context across auto-memory,
  Basic Memory, and Obsidian. Use when finishing a work session,
  saving progress before clearing context, or documenting what was
  accomplished.
when_to_use: >-
  Triggers on "wrap up", "end session", "finish up", "close session",
  "wrap-up".
effort: medium
---

# Wrap Up Session

End-of-session documentation across auto-memory, Basic Memory, and Obsidian.

## Workflow

```
detect-project --> session-dump:load --> auto-memory --> bm-notes -->
obsidian-notes --> session-dump:detect+cleanup
```

Detect project from current working directory, load the spec-driven
session dump (when present), then execute the four note-writing steps
in sequence. No confirmation between steps. The closing step runs
structural-delta detection — silent unless a delta fires — and then
unconditionally clears the dump file.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wrap up, wrap-up, end session, finish up, close session | All references in sequence |

Notes:

- `mapping.md` is loaded first — all other steps depend on its output.
  It is not a direct trigger.
- Loading order within wrap-up:
  1. [mapping.md](references/mapping.md)
  2. [session-dump.md](references/session-dump.md) (Load phase)
  3. [auto-memory.md](references/auto-memory.md)
  4. [bm-notes.md](references/bm-notes.md)
  5. [obsidian-notes.md](references/obsidian-notes.md)
  6. [session-dump.md](references/session-dump.md) (Detect + Cleanup phases)
- `session-dump.md` is not a direct trigger. Loaded after mapping (Load
  phase) and again after obsidian-notes (Detect + Cleanup phases). Detect
  emits one suggestion line only when a structural delta is detected;
  Cleanup writes empty content to the dump file unconditionally.

## Cross-References

```
mapping.md -------> bm-notes.md        (provides BM project, path, base tags)
mapping.md -------> obsidian-notes.md  (provides Obsidian path, base tags)
mapping.md -------> session-dump.md    (loaded after mapping)
session-dump.md --> bm-notes.md        (provides Discoveries / Decisions / Next Context)
session-dump.md --> obsidian-notes.md  (same)
session-dump.md --> spec-driven        (consumes .artifacts/.session-dump.md, latest phase block)
session-dump.md --> project-index      (suggests /project-index re-index when Detect fires)
session-dump.md --> filesystem         (unconditional clear at end)
auto-memory.md --> filesystem          (reads/writes agent auto-memory files)
bm-notes.md -----> BM MCP              (direct tool calls, no skill indirection)
obsidian-notes.md -> MCPVault MCP      (direct tool calls, no skill indirection)
```

## Guidelines

**DO:**
- Call BM MCP and MCPVault MCP tools directly from bm-notes.md and obsidian-notes.md workflows
- Execute all steps in order without confirmation
- Search existing notes before creating new ones
- Run auto-memory for every session, even trivial ones
- Skip auto-memory and BM when mapping returns `--` for BM project
- Skip Obsidian session note when mapping returns `--` for Obsidian session
- Always create/update Obsidian daily note, regardless of mapping values
- Be concise in auto-memory, detailed in BM session
- Use past tense and natural language in Obsidian notes
- Use BM `[brackets]` tag syntax and Obsidian `#hashtags` per tool
- Load session-dump first so bm-notes and obsidian-notes can fold its content
- Run session-dump cleanup last so the ephemeral file does not linger

**DON'T:**
- Ask for confirmation between steps
- Create duplicate notes without searching first
- Skip auto-memory for trivial sessions
- Write changelog-style content or git metadata in Obsidian notes
- Mix BM `[brackets]` with Obsidian `#hashtags` across tools
- Re-read `.artifacts/.session-dump.md` in downstream refs (contrasts: load once, share via context)
- Prompt before clearing the session-dump (contrasts: cleanup is unconditional)

