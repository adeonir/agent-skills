---
name: project-index
description: Generate project context and codebase documentation for AI agents.
  Creates .agents/ directory with project overview and deep codebase analysis.
  Use when starting work on a project, onboarding to an existing codebase,
  generating project documentation for agents, or mapping codebase patterns and
  conventions. Triggers on "initialize project", "setup project", "overview",
  "summary", "map codebase", "index project", "analyze codebase".
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
    ├── workflows.md
    └── concerns.md          # Optional: tech debt, risks (only when issues detected)

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
| Concerns | [concerns.md](templates/concerns.md) |

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
overview.md ------> root-agents.md (auto-update AGENTS.md)
summary.md -------> root-agents.md (auto-update AGENTS.md)
```

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple references simultaneously.

## Output Size Budget

Keep generated docs concise. Agents load these into context -- every line costs tokens.

| Document | Target | Max |
|----------|--------|-----|
| project.md | ~30 lines | 50 |
| stack.md | ~20 lines | 40 |
| architecture.md | ~50 lines | 80 |
| conventions.md | ~30 lines | 50 |
| testing.md | ~30 lines | 50 |
| integrations.md | ~15 lines | 30 |
| commands.md | ~20 lines | 30 |
| checklist.md | ~15 lines | 20 |
| workflows.md | ~30 lines | 50 |
| concerns.md | ~15 lines | 30 |
| AGENTS.md | ~60 lines | 100 |

**Total target:** ~300 lines / ~12k tokens. Tables max 10 rows, lists max 7 items.

## Integration with Other Skills

```
docs-writer (.artifacts/docs/) --> project-index (overview) consumes as context source
spec-driven (plan phase)       --> may add discoveries to .agents/codebase/
project-index (summary)        --> preserves spec-driven additions when re-running
```

- **docs-writer**: Overview checks `.artifacts/docs/` for existing briefs, PRDs, design docs, pitches, and scopes. When found, uses them as primary context for generating project.md.
- **spec-driven**: Summary preserves discoveries added during planning. More specific context (from feature planning) takes precedence over general analysis.

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
