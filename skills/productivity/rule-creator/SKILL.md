---
name: rule-creator
description: "Creates and manages Claude Code rules in .claude/rules/ and ~/.claude/rules/, at project or user level. Use when adding a coding convention or standing preference as a rule, listing, editing, or deleting rules, or splitting an oversized CLAUDE.md or AGENTS.md into rule files. Not for linter rules such as ESLint, procedural workflows, lifecycle hooks, one-off task instructions, or edits that keep the text in CLAUDE.md."
---

# Rule Creator

Creates rules at project or user level and manages the rule set at both.

## Triggers

| Signal in input | Load |
|-----------------|------|
| "create / add / new rule", "convention", "standard", or a declarative description with no verb | [create.md](instructions/create.md) |
| "list / show rules", "what rules exist" | [list.md](instructions/list.md) |
| "edit / update / change rule X" | [edit.md](instructions/edit.md) |
| "extract / split / move from AGENTS.md / CLAUDE.md", "AGENTS.md / CLAUDE.md is too big" | [extract.md](instructions/extract.md) |
| "delete / remove rule X" | [delete.md](instructions/delete.md) |

## Workflow

```text
trigger → dispatch → classify → context → destination → render → write
              |              |
              v              v
           list/edit     refuse (procedural / lifecycle / one-off)
           extract/del
```

## References

- [classify-and-context.md](references/classify-and-context.md) - classifier, context check, and destination decision; loaded by create, edit, and extract
- [rule-format.md](references/rule-format.md) - rule template and verifiability checklist; loaded by create, edit, and extract
