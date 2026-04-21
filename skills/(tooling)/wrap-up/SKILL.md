---
name: wrap-up
description: >-
  End-of-session command that persists context across auto-memory,
  Basic Memory, and Obsidian. Use when finishing a work session,
  saving progress before clearing context, or documenting what was
  accomplished. Triggers on "wrap up", "end session", "finish up",
  "close session", "wrap-up".
---

# Wrap Up Session

End-of-session documentation across auto-memory, Basic Memory, and Obsidian.

## Workflow

```
detect-project --> auto-memory --> bm-notes --> obsidian-notes
```

Detect project from current working directory, then execute three steps
in sequence. No confirmation between steps.

## Context Loading

Load [mapping.md](references/mapping.md) first -- all subsequent steps
depend on the resolved project name, BM project and path, Obsidian path,
and base tags.

Then load each reference in order as each step executes:
1. [auto-memory.md](references/auto-memory.md)
2. [bm-notes.md](references/bm-notes.md)
3. [obsidian-notes.md](references/obsidian-notes.md)

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wrap up, end session, finish up, close session | All references in sequence |

Notes:

- `mapping.md` is not a direct trigger. It is loaded automatically before
  all other references.

## Cross-References

```
mapping.md -------> bm-notes.md        (provides BM project, path, base tags)
mapping.md -------> obsidian-notes.md  (provides Obsidian path, base tags)
bm-notes.md -----> BM MCP              (direct tool calls, no skill indirection)
obsidian-notes.md -> MCPVault MCP        (direct tool calls, no skill indirection)
```

## Guidelines

**DO:**
- Call BM MCP and MCPVault MCP tools directly from bm-notes.md and obsidian-notes.md workflows
- Execute all steps in order without confirmation
- Skip auto-memory and BM when mapping returns `--` for BM project
- Skip Obsidian session note when mapping returns `--` for Obsidian session
- Always create/update Obsidian daily note, regardless of mapping values
- Be concise in auto-memory, detailed in BM session
- Use past tense and natural language in Obsidian notes

**DON'T:**
- Ask for confirmation between steps
- Create duplicate notes -- search first
- Write changelog-style content or git metadata in Obsidian notes
- Skip auto-memory even for trivial sessions
- Mix BM format ([brackets]) with Obsidian format (#hashtags)

## Error Handling

- `.notes/` symlink missing: run vault bootstrap, ask user for vault path
- Repo not registered in `wrap-up.yml`: run project bootstrap, append entry
- BM tools unavailable: skip BM step, warn user
- Obsidian/MCPVault unavailable: skip Obsidian step, warn user
- Session note already exists in BM: append with edit_note, do not overwrite
- Daily note already exists in Obsidian: update with patch_note
- No meaningful session content: keep session brief, skip decision notes, still update daily
