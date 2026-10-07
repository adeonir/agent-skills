---
name: rule-creator
description: "Claude Code rule management at project and user level. Use when defining conventions, scoping, listing, editing, extracting, or deleting rules. Not for procedural workflows, lifecycle hooks, or one-off task instructions."
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

Create runs the classifier and context check before rendering the template. The other modes skip classification.
