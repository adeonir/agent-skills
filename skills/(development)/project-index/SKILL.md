---
name: project-index
description: >-
  Generate project context and codebase documentation for AI agents.
  Creates .agents/ directory with project overview and deep codebase analysis.
  Use when starting work on a project, onboarding to an existing codebase,
  generating project documentation for agents, or mapping codebase patterns
  and conventions.
when_to_use: >-
  Triggers on "initialize project", "setup project", "overview", "summary",
  "map codebase", "index project", "analyze codebase".
effort: xhigh
context: fork
agent: general-purpose
---

# Project Index

**Recommended effort:** xhigh for initialize and summary; medium for overview
and integrate-feedback.

Generate project context and codebase documentation for AI agents. Use
ultrathink for initialize and summary phases.

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
| Integrate feedback, integrate discoveries, sync knowledge | [integrate-feedback.md](references/integrate-feedback.md) |

## Cross-References

```
initialize.md ----> overview.md
initialize.md ----> summary.md (if brownfield)
overview.md ------> root-agents.md (auto-update AGENTS.md)
summary.md -------> root-agents.md (auto-update AGENTS.md)
spec-driven ---------------> integrate-feedback.md (consumes knowledge.md Codebase Feedback)
integrate-feedback.md -----> knowledge.md (clears integrated rows only)
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
spec-driven (design/implement) --> queues codebase discoveries to .agents/knowledge.md Codebase Feedback
integrate-feedback             --> merges knowledge.md Codebase Feedback into .agents/codebase/*.md
project-index (summary)        --> preserves knowledge.md as-is when re-running
project-index                  --> sole writer to .agents/codebase/*.md and .agents/project.md
```

- **docs-writer**: Overview checks `.artifacts/docs/` for existing briefs, PRDs, design docs, epics, and issues. When found, uses them as primary context for generating project.md.
- **spec-driven**: queues codebase discoveries to `.agents/knowledge.md` `## Codebase Feedback`; integrate-feedback merges them into `codebase/*.md` on demand. spec-driven never writes directly to `.agents/codebase/*.md`.
- **knowledge.md**: Owned by spec-driven. Contains `## Decisions`, `## Gotchas`, and a `## Codebase Feedback` queue. project-index reads the file for context and consumes the Codebase Feedback queue via `integrate-feedback`, but never modifies Decisions or Gotchas. When re-running summary, preserve the full file.

## Guidelines

**DO:**
- Read actual code files to extract patterns, not just list them
- Keep all outputs concise and scannable
- Document conventions as observed, not as prescribed
- Document stable patterns and interfaces, not volatile implementation details
- Cross-reference between output files rather than duplicating content
- Update existing docs when re-running (merge, never overwrite)

**DON'T:**
- Create outputs without reading representative source files (contrasts: read actual code)
- Generate exhaustive catalogs of every component/file (contrasts: concise and scannable)
- Include implementation details that change frequently (contrasts: stable patterns and interfaces)
- Duplicate information across output files (contrasts: cross-reference between files)

## Error Handling

- No source code found: inform this is for existing projects
- Empty project: skip summary, generate overview only
- `.agents/` already exists: update existing files, never overwrite blindly — merge new findings
