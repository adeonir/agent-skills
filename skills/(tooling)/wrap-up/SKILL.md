---
name: wrap-up
description: >-
  End-of-session command that updates auto-memory, writes session and
  debrief notes to Basic Memory, and creates session and daily notes
  in Obsidian. Use when finishing a work session, saving progress
  before clearing context, or documenting what was accomplished.
  Triggers on "wrap up", "end session", "finish up", "close session",
  "wrap-up".
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
depend on the resolved project, BM project, and Obsidian folder.

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
mapping.md -------> bm-notes.md      (provides BM project and prefix)
mapping.md -------> obsidian-notes.md (provides Obsidian folder)
bm-notes.md -----> memory-notes      (uses BM skill for write_note)
obsidian-notes.md > session-notes     (uses Obsidian skill for write/patch)
```

## Guidelines

**DO:**
- Execute all steps in order without confirmation
- Skip auto-memory and BM when mapping returns `--` for BM project
- Skip Obsidian session note when mapping returns `--` for Obsidian session
- Always create/update Obsidian daily note, regardless of mapping values
- Be concise in auto-memory, detailed in BM debrief
- Use past tense and natural language in Obsidian notes

**DON'T:**
- Ask for confirmation between steps
- Create duplicate notes -- search first
- Write changelog-style content in Obsidian notes
- Skip auto-memory even for trivial sessions
- Mix BM format ([brackets]) with Obsidian format (#hashtags)

## Error Handling

- Project not detected from path: ask user for project name and category
- BM tools unavailable: skip BM step, warn user
- Obsidian/MCPVault unavailable: skip Obsidian step, warn user
- Session note already exists in BM: append with edit_note, do not overwrite
- Daily note already exists in Obsidian: update with patch_note
- No meaningful session content: skip BM and Obsidian session, still update daily
