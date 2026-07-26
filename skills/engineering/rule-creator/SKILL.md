---
name: rule-creator
description: >-
  Creates and manages Claude Code rules in project .claude/rules/ and
  user-level rules with the Incorrect/Correct template, classifies the input
  before writing, and decides level, scope, and frontmatter from signals in
  the request. Supports create, list, edit, extract from oversized
  AGENTS.md / CLAUDE.md, delete, and refusal with redirect when the input
  belongs to a skill or hook.
  Use this skill whenever the user defines a coding convention, team standard,
  or constraint Claude should enforce — even when the user does not explicitly
  say "rule". Also use for creating, listing, editing, or deleting a rule,
  writing a rule for one project or for every project, scoping a rule to
  specific paths, or splitting a growing AGENTS.md / CLAUDE.md
  into rule files. Not for procedural workflows, lifecycle
  hooks, or one-off task instructions.
---

# Rule Creator

Creates rules at project or user level and manages the rule set at both.

## Triggers and dispatch

| Signal in input | Mode | Load |
|-----------------|------|------|
| "create / add / new rule", "convention", "standard", or a declarative description with no verb | create | [classify-and-context.md](references/classify-and-context.md), then [rule-format.md](references/rule-format.md) |
| "list / show rules", "what rules exist" | list | [modes.md](references/modes.md) |
| "edit / update / change rule X" | edit | [modes.md](references/modes.md), [rule-format.md](references/rule-format.md) |
| "extract / split / move from AGENTS.md / CLAUDE.md", "AGENTS.md / CLAUDE.md is too big" | extract | [modes.md](references/modes.md) |
| "delete / remove rule X" | delete | [modes.md](references/modes.md) |

A rule has two independent axes:

| Axis | Values | Materializes as |
|------|--------|-----------------|
| Level | user (`~/.claude/rules/`) / project (`.claude/rules/`) | the directory written to |
| Scope | unconditional / path-scoped | absence or presence of `paths:` frontmatter |

Project rules take priority over user rules. `user + path-scoped` is unavailable, so a path signal resolves the level to project.

## Workflow

```text
trigger → dispatch → classify → context → destination → render → write
              |              |
              v              v
           list/edit     refuse (procedural / lifecycle / one-off)
           extract/del
```

Create runs the classifier and context check before rendering the template. Other modes skip classification.

## Create gates (run in order)

1. **Classify input.** Procedural multi-step → refuse and recommend authoring a skill instead. Lifecycle event → refuse and recommend a hook. One-off task → refuse, suggest doing it directly. Declarative convention → proceed. See [classify-and-context.md](references/classify-and-context.md).
2. **Context check.** Stack mismatch, duplicate topic across both levels, or contradiction with a memory file → flag and ask before writing. Same reference.
3. **Destination decision.** Level from explicit signals; no signal → ask. Scope from path signals. Same reference.
4. **Render.** Apply the Incorrect/Correct template strictly. See [rule-format.md](references/rule-format.md).
5. **Verifiability checklist.** Run the three checks in [rule-format.md](references/rule-format.md). Fail any → rewrite before saving.
6. **Write.** New topic → new file under the chosen level's rules directory, named for the topic: kebab-case descriptive noun, lowercase ASCII, hyphens only (`testing.md`, `api-design.md` — never `rules.md` or `misc.md`). Discovery is recursive, so a subdirectory (`frontend/testing.md`) is available when a level accumulates enough topics to group them. Existing topic without conflict → append H2. Existing topic with conflict → ask user.
