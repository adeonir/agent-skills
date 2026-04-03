---
name: project-index
description: >-
  Generate project context and codebase documentation for AI agents.
  Creates .agents/ directory with project overview and deep codebase analysis.
  Use when starting work on a project, onboarding to an existing codebase,
  generating project documentation for agents, or mapping codebase patterns and
  conventions. Triggers on "initialize project", "setup project", "overview",
  "summary", "map codebase", "index project", "analyze codebase".
---

# Project Index

Generate project context and codebase documentation for AI agents.

## Workflow

```
initialize --> overview + summary
```

Each command can be used independently or chained via initialize.

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple references simultaneously.

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

## Output Structure

```
.agents/
├── project.md              # Project context, purpose, scope
└── codebase/               # Deep codebase analysis
    ├── stack.md            # Framework, runtime, all dependencies with purpose
    ├── architecture.md     # Mermaid diagrams, component map, layers, data flows, interfaces
    ├── conventions.md      # Observed patterns with code snippets, abstractions, custom hooks
    ├── testing.md          # Patterns from actual tests, mocking, fixtures, coverage gaps
    ├── integrations.md     # External services, env vars, config details
    ├── commands.md         # All available scripts with descriptions
    ├── checklist.md        # Validation steps after completing a task
    ├── workflows.md        # Mermaid flowcharts for user and dev workflows
    ├── review-notes.md     # Self-assessment: consistency, completeness, gaps
    └── concerns.md         # Optional: tech debt, risks (only when detected)

AGENTS.md                   # Concise entry point pointing to .agents/codebase/
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
| Review Notes | [review-notes.md](templates/review-notes.md) |
| Concerns | [concerns.md](templates/concerns.md) |

## Output Size Guidelines

These docs are loaded on-demand (research, implementation), not always in context.
Be thorough -- document patterns with real code examples and file references.
Avoid redundancy across files, but do not sacrifice depth for brevity.

| Document | Guideline |
|----------|-----------|
| project.md | Concise overview (~30 lines) |
| stack.md | All meaningful dependencies with purpose |
| architecture.md | Structure, patterns, data flows with code examples |
| conventions.md | Every observed pattern with code snippets and file references |
| testing.md | Patterns with example test structure from actual tests |
| integrations.md | All external touchpoints with config details |
| commands.md | All available commands with descriptions |
| checklist.md | Concise validation steps (~15 lines) |
| workflows.md | Core flows with step-by-step detail |
| concerns.md | Only real issues with evidence |
| AGENTS.md | Concise entry point (~60 lines) pointing to .agents/codebase/ |

## Integration with Other Skills

```
docs-writer (.artifacts/docs/) --> project-index (overview) consumes as context source
spec-driven (plan phase)       --> may add discoveries to .agents/codebase/
spec-driven (design/implement) --> owns .agents/knowledge.md (accumulates decisions)
project-index (summary)        --> preserves spec-driven additions when re-running
project-index                  --> reads .agents/knowledge.md but never writes it
```

- **docs-writer**: Overview checks `.artifacts/docs/` for existing briefs, PRDs, design docs, epics, and issues. When found, uses them as primary context for generating project.md.
- **spec-driven**: Summary preserves discoveries added during planning. More specific context (from feature planning) takes precedence over general analysis.
- **knowledge.md**: Owned by spec-driven. Contains cross-feature decisions, gotchas, and patterns not derivable from code. project-index reads it for context when generating docs but never overwrites or regenerates it. When re-running summary, preserve knowledge.md as-is.

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
