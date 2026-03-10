---
name: project-index
description: Generate project context and codebase documentation for AI agents. Creates .agents/ directory with project overview and deep codebase analysis. Use when starting work on a project, onboarding to an existing codebase, generating project documentation for agents, or mapping codebase patterns and conventions. Triggers on "initialize project", "setup project", "overview", "summary", "map codebase", "index project", "analyze codebase".
metadata:
  author: Adeonir Kohl
  version: "1.0.0"
---

# Project Index

Generate project context and codebase documentation for AI agents.

## Workflow

```
initialize --> overview + summary
```

Each command can be used independently or chained via initialize.

## Output Structure

```
.agents/
├── project.md              # Project context (overview)
└── codebase/               # Codebase analysis (summary)
    ├── stack.md
    ├── architecture.md
    ├── conventions.md
    ├── testing.md
    ├── integrations.md
    ├── commands.md
    ├── checklist.md
    └── workflows.md

AGENTS.md                   # Root file (auto-generated)
```

## Templates

| Document | Template |
|----------|----------|
| Project overview | [project.md](templates/project.md) |
| Stack | [stack.md](templates/stack.md) |
| Architecture | [architecture.md](templates/architecture.md) |
| Conventions | [conventions.md](templates/conventions.md) |
| Testing | [testing.md](templates/testing.md) |
| Integrations | [integrations.md](templates/integrations.md) |
| Commands | [commands.md](templates/commands.md) |
| Checklist | [checklist.md](templates/checklist.md) |
| Workflows | [workflows.md](templates/workflows.md) |

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Initialize project, setup project, index project | [initialize.md](references/initialize.md) |
| Overview, project context | [overview.md](references/overview.md) |
| Summary, map codebase, analyze codebase | [summary.md](references/summary.md) |

## Cross-References

```
initialize.md ----> overview.md
initialize.md ----> summary.md (if brownfield)
overview.md ------> AGENTS.md (auto-update)
summary.md -------> AGENTS.md (auto-update)
```

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple references simultaneously.

## Guidelines

**DO:**
- Read actual code files to extract patterns, not just list them
- Keep all outputs concise and scannable
- Document conventions as observed, not as prescribed
- Update existing docs when re-running (merge, never overwrite)

**DON'T:**
- Generate exhaustive catalogs of every component/file
- Include implementation details that change frequently
- Duplicate information across output files
- Create outputs without reading representative source files

## Error Handling

- No source code found: Inform this is for existing projects
- Empty project: Skip summary, generate overview only
- `.agents/` already exists: Ask if refresh needed
