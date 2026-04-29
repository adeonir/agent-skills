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
detect-project --> auto-memory --> bm-notes --> obsidian-notes --> spec-delta
```

Detect project from current working directory, then execute four steps
in sequence. No confirmation between steps. The final step is silent
unless a structural delta is detected.

## Context Loading

Load [mapping.md](references/mapping.md) first -- all subsequent steps
depend on the resolved project name, BM project and path, Obsidian path,
and base tags.

Then load each reference in order as each step executes:
1. [auto-memory.md](references/auto-memory.md)
2. [bm-notes.md](references/bm-notes.md)
3. [obsidian-notes.md](references/obsidian-notes.md)
4. [spec-delta.md](references/spec-delta.md)

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wrap up, wrap-up, end session, finish up, close session | All references in sequence |

Notes:

- `mapping.md` is not a direct trigger. It is loaded automatically before
  all other references.
- `spec-delta.md` runs last, only emits output when a spec-driven
  session-dump is present and a structural delta is detected.

## Cross-References

```
mapping.md -------> bm-notes.md        (provides BM project, path, base tags)
mapping.md -------> obsidian-notes.md  (provides Obsidian path, base tags)
bm-notes.md -----> BM MCP              (direct tool calls, no skill indirection)
obsidian-notes.md -> MCPVault MCP      (direct tool calls, no skill indirection)
spec-delta.md ----> spec-driven        (reads .artifacts/.session-dump.md, latest phase block)
spec-delta.md ----> project-index      (suggests /project-index re-index when delta detected)
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
- Run spec-delta last; surface the re-index suggestion only when a session-dump exists and either keyword scan or structural diff fires

**DON'T:**
- Ask for confirmation between steps
- Create duplicate notes without searching first
- Skip auto-memory for trivial sessions
- Write changelog-style content or git metadata in Obsidian notes
- Mix BM `[brackets]` with Obsidian `#hashtags` across tools

## Error Handling

- `.notes/wrap-up.yml` missing: auto link from `~/.config/wrap-up/vault` if present, otherwise run vault bootstrap and ask for vault path once
- Repo not registered in `wrap-up.yml`: run project bootstrap, append entry
- BM tools unavailable: skip BM step, warn user
- Obsidian/MCPVault unavailable: skip Obsidian step, warn user
- Session note already exists in BM: append with edit_note, do not overwrite
- Daily note already exists in Obsidian: update with patch_note
- No meaningful session content: keep session brief, still update daily
- No spec-driven session-dump found: spec-delta step emits nothing
- Not in a git repo: spec-delta skips the structural diff and uses the session-dump keyword scan only
