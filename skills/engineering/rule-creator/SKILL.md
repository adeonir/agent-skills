---
name: rule-creator
description: >-
  Creates and manages Claude Code rules in .claude/rules/ with the
  Incorrect/Correct template, classifies the input before writing, and
  decides scope, location, and frontmatter from signals in the request.
  Supports create, list, edit, extract from oversized AGENTS.md / CLAUDE.md, delete,
  and refusal with redirect when the input belongs to a skill or hook.
  Use this skill whenever the user defines a coding convention, team standard,
  or constraint Claude should enforce — even when the user does not explicitly
  say "rule". Also use for creating, listing, editing, or deleting a rule,
  scoping a rule to specific paths, splitting a growing AGENTS.md / CLAUDE.md into rule
  files, or auditing existing rules. Not for procedural workflows, lifecycle
  hooks, or one-off task instructions.
---

# Rule Creator

Creates well-scoped rules in `.claude/rules/` and manages the rule set.

## Triggers and dispatch

| Signal in input | Mode | Load |
|-----------------|------|------|
| "create / add / new rule", "convention", "standard", or a declarative description with no verb | create | [classify-and-context.md](references/classify-and-context.md), then [rule-format.md](references/rule-format.md) |
| "list / show rules", "what rules exist" | list | [modes.md](references/modes.md) |
| "edit / update / change rule X" | edit | [modes.md](references/modes.md), [rule-format.md](references/rule-format.md) |
| "extract / split / move from AGENTS.md / CLAUDE.md", "AGENTS.md / CLAUDE.md is too big" | extract | [modes.md](references/modes.md) |
| "delete / remove rule X" | delete | [modes.md](references/modes.md) |

Scope is project only: rules land in `.claude/rules/`. User-level rules (`~/.claude/rules/`) are out of scope.

## Workflow

```text
trigger → dispatch → classify → context → render → write
              |              |
              v              v
           list/edit     refuse (procedural / lifecycle / one-off)
           extract/del
```

Dispatch picks the mode from verb signals. Create runs the classifier and project context check before rendering the template. Other modes skip classification.

## Create gates (run in order)

1. **Classify input.** Procedural multi-step → refuse and recommend authoring a skill instead. Lifecycle event → refuse and recommend a hook. One-off task → refuse, suggest doing it directly. Declarative convention → proceed. See [classify-and-context.md](references/classify-and-context.md).
2. **Context check.** Stack mismatch, duplicate topic, contradiction with AGENTS.md / CLAUDE.md, or rule too vague to verify → flag and ask before writing. Same reference.
3. **Scope decision.** Path signals (extension, directory, framework name) → path-scoped `paths:` frontmatter. Otherwise global. Same reference.
4. **Render.** Apply the Incorrect/Correct template strictly. See [rule-format.md](references/rule-format.md).
5. **Verifiability checklist.** Action verb? Specific tool or syntax? Reviewer can say "violated"? Fail any → rewrite before saving.
6. **Write.** New topic → new file. Existing topic without conflict → append H2. Existing topic with conflict → ask user.

## Guidelines

- Default scope to path-scoped when the input names an extension, a directory, or a framework; global only for universal conventions
- One topic per file; multiple rules in the same topic become H2 sections inside that file
- Filenames are kebab-case, descriptive nouns (`testing.md`, `api-design.md`, not `rules.md` or `misc.md`)
- Sanitize the filename: lowercase, ASCII, hyphens only
- Refuse procedural input — recommend authoring a skill instead of compressing the steps into a weak rule

## Anti-Pattern: Rule as Workflow

A rule that reads like a procedure ("first do A, then B, then C") fails as a rule. Claude reads rules as standing constraints, not playbooks. Multi-step content belongs in a skill. When the input is sequenced and conditional, refuse and recommend authoring a skill instead of compressing the steps into bullets.

## Anti-Pattern: Vague Conventions

"Format code properly" and "write good tests" cannot be checked. The verifiability gate exists to catch these. If the rule has no action verb, no specific tool or syntax, and no observable behavior, it is decoration. Rewrite it concretely or drop it.
