---
name: spec-driven
description: "Spec-driven feature work with traceable requirements, design, tasks, audit, and validation. Use when planning, designing, implementing, or validating a feature. Not for unknown-bug diagnosis, standalone product or technical documents, PR or commit mechanics, or backlog tracking."
argument-hint: "[T-N] | [T-N..T-M] | [S-N] | [S-N..S-M] | [W-N] | [W-N..W-M]"
allowed-tools: Bash(git:*) Bash(python3:*) Read Write Edit Grep Glob Task
---

# Spec-Driven Development

Feature development in phases. Light by default; weight only where the change pays for it.

## Triggers

- **Specify** ("plan feature", "spec this", "from PRD", "modify feature", "discuss how to build") → [specify.md](instructions/specify.md)
- **Design** ("design this feature", "technical design", "plan the build") → [design.md](instructions/design.md)
- **Tasks** ("create tasks", "break into tasks", "task breakdown") → [tasks.md](instructions/tasks.md)
- **Implement** ("implement task T-1", "implement T-1 to T-4", "implement slice S-1", "implement wave W-1", "execute tasks", "implement everything") → [implement.md](instructions/implement.md)
- **Audit** ("audit feature", "validate goals", "verify before PR") → [audit.md](instructions/audit.md)
- **Validate / UAT** ("run UAT", "manual testing", "validate flows") → [validate.md](instructions/validate.md)
- **Archive** ("archive feature", "archive this spec") → [archive.md](instructions/archive.md)

## Workflow

```text
specify → design → tasks → implement → [validate] → [audit] → [archive]
   └────────┴────────┴──────────┴──────────┴ a mechanical change skips all of this: one-liner → branch → implement inline
```

Specify's triage decides the path: a mechanical change with zero load-bearing decisions becomes a one-liner straight to inline implement on its own branch, and a prompt carrying outcomes that ship separately becomes one feature per outcome. Everything else produces the artifacts and runs the phases in turn. Verify is mental, per task, inside implement — never a user phase. Validate and audit are optional. Archive is manual housekeeping for a feature in any state, never automatic or suggested.
