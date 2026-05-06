---
name: project-index
description: >-
  Generate project context and codebase documentation for AI agents.
  Creates .agents/ directory with project overview and deep codebase analysis.
  Use when starting work on a project, onboarding to an existing codebase,
  generating project documentation for agents, or mapping codebase patterns
  and conventions.
when_to_use: >-
  Triggers on "initialize .agents", "setup project index", "index project",
  "map codebase", "analyze codebase", "project overview",
  "codebase summary", "onboarding to this repo". Not for feature work
  (use spec-driven), session notes in Obsidian (use session-notes), or
  dev tooling setup like prettier/eslint (out of scope for all skills).
effort: high
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

## Triggers

| Trigger Pattern                                           | Reference                                                 |
| --------------------------------------------------------- | --------------------------------------------------------- |
| Initialize project, setup project, index project          | [initialize.md](references/initialize.md)                 |
| Overview, project context                                 | [overview.md](references/overview.md)                     |
| Summary, map codebase, analyze codebase                   | [summary.md](references/summary.md)                       |
| Integrate feedback, integrate discoveries, sync knowledge | [integrate-feedback.md](references/integrate-feedback.md) |

Notes:

- `summary.md` parallelizes doc generation via sub-agent fan-out (see Step 3).

## Cross-References

```
initialize.md ----> overview.md
initialize.md ----> summary.md (if brownfield)
spec-driven -------> integrate-feedback.md (consumes knowledge.md Codebase Feedback)
integrate-feedback.md --> knowledge.md (clears Codebase Feedback only)
```

- docs-writer (`.artifacts/docs/`) feeds overview.md as context source for project.md
- spec-driven queues codebase discoveries to `.agents/knowledge.md` `## Codebase Feedback`; integrate-feedback merges them into `codebase/*.md` on demand
- spec-driven owns `.agents/knowledge.md` (Decisions, Gotchas, Codebase Feedback); project-index reads it but never modifies Decisions or Gotchas
- project-index is sole writer to `.agents/project.md` and `.agents/codebase/*.md`

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

## Output

```
.agents/
├── project.md              # Project context, purpose, scope, stack
└── codebase/               # Deep codebase analysis
    ├── architecture.md     # Mermaid diagrams, component map, layers, data flows, interfaces
    ├── conventions.md      # Observed patterns with code snippets, abstractions, custom hooks
    ├── testing.md          # Patterns from actual tests, mocking, fixtures, coverage gaps
    ├── integrations.md     # External services, env vars, config details
    ├── checklist.md        # Validation steps after completing a task
    ├── workflows.md        # Mermaid flowcharts for user and dev workflows
    └── review.md           # Self-assessment: consistency, completeness, concerns if any
```

## Error Handling

- No source code found: inform this is for existing projects
- Empty project: skip summary, generate overview only
- `.agents/` already exists: update existing files, never overwrite blindly — merge new findings
