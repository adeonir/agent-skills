---
name: project-index
description: >-
  Generates project context and codebase documentation for AI agents.
  Creates `.agents/` directory with project overview and deep codebase
  analysis (architecture, conventions, testing, integrations, checklist,
  workflows, features when vertical slicing detected, review). Use when
  starting work on a project, onboarding to an existing codebase,
  generating project documentation for agents, mapping codebase
  patterns, or incrementally refreshing the index from recent git
  changes. Triggers: "initialize .agents", "setup project index",
  "index project", "map codebase", "analyze codebase", "project
  overview", "codebase summary", "onboarding to this repo", "integrate
  feedback", "sync knowledge", "refresh codebase", "sync codebase",
  "patch index". Not for feature work, Obsidian session notes, or dev
  tooling setup like prettier or eslint.
---

# Project Index

Generate project context and codebase documentation for AI agents.

## Workflow

```
initialize --> overview + (codebase fan-out + review when brownfield)
refresh    --> git diff range --> subset fan-out + review
                                     (fallback: full fan-out)
```

`initialize` is the entrypoint for first-time setup. It always runs
`overview`. If the project is brownfield (has source code), it
dispatches the codebase fan-out: 6 sub-agents in parallel
(architecture, conventions, testing, integrations, checklist,
workflows), plus a 7th (features) when vertical slicing is detected,
then the main agent runs `review` with the fan-out outputs as context.

`refresh` is the cheaper re-run path once `.agents/codebase/` exists.
It diffs `git` from the last sync marker, routes changed paths to the
sub-agents whose domain was touched, and dispatches only that subset.
Falls back to the full fan-out when thresholds (file count, manifest
churn, entry-point change) indicate a broad refactor.

## Triggers

- **One-time setup** ("initialize", "setup project index", "index
  project") → [initialize.md](references/initialize.md)
- **Project context** ("overview", "project context", "refresh project")
  → [overview.md](references/overview.md)
- **Codebase summary** ("map codebase", "analyze codebase", "summary")
  → dispatch the 6 codebase refs in parallel via sub-agent fan-out, then
  run [review.md](references/review.md) with the outputs as context
- **Incremental refresh** ("refresh codebase", "sync codebase", "patch
  index") → [refresh.md](references/refresh.md)
- **Architecture** (single doc refresh) →
  [architecture.md](references/architecture.md)
- **Conventions** (single doc refresh) →
  [conventions.md](references/conventions.md)
- **Testing** (single doc refresh) →
  [testing.md](references/testing.md)
- **Integrations** (single doc refresh) →
  [integrations.md](references/integrations.md)
- **Checklist** (single doc refresh) →
  [checklist.md](references/checklist.md)
- **Workflows** (single doc refresh) →
  [workflows.md](references/workflows.md)
- **Features** (single doc refresh, vertically sliced projects only) →
  [features.md](references/features.md)
- **Self-assessment** (post fan-out) → [review.md](references/review.md)
- **Integrate feedback** ("integrate feedback", "sync knowledge",
  "integrate discoveries") →
  [integrate-feedback.md](references/integrate-feedback.md)
- **Merge policy** (loaded by any ref on re-run) →
  [merge-policy.md](references/merge-policy.md)

## Codebase Fan-Out

When mapping the full codebase (initialize on brownfield, or "summary"
trigger), dispatch all 6 codebase refs as **independent sub-agents in
the same turn**. A 7th sub-agent (`features`) is dispatched only when
the project shows vertical slicing (see [features.md](references/features.md) Detection Gate).

| Sub-agent | Reads | Writes | Gate |
|-----------|-------|--------|------|
| architecture | Entry points, dir tree, layer boundaries | `.agents/codebase/architecture.md` | always |
| conventions | Representative source files | `.agents/codebase/conventions.md` | always |
| testing | Test files, test config | `.agents/codebase/testing.md` | always |
| integrations | API clients, DB models, env files | `.agents/codebase/integrations.md` | always |
| checklist | Scripts (`package.json` / `Makefile`), pre-commit config | `.agents/codebase/checklist.md` | always |
| workflows | Entry points to traced data flows | `.agents/codebase/workflows.md` | always |
| features | Vertical slice dirs, route prefixes, co-located test/handler/view | `.agents/codebase/features.md` | vertical slicing detected |

Each sub-agent reads only what its domain needs. Outputs land on disk —
sub-agents do not return findings through context.

After all sub-agents finish, the main agent runs `review.md` with all
outputs as context. Review cannot be split across sub-agents — the main
agent owns this synthesis.

## Guidelines

- Read actual code files to extract patterns, not just list them
- Document conventions as observed, not as prescribed
- Focus on stable patterns and interfaces, not volatile implementation details
- Update existing docs when re-running (merge, never overwrite)
- Be thorough in `.agents/codebase/*.md` — these load on demand, not
  always in context

## Anti-Pattern: Source Boundary Leak

`.agents/codebase/*.md` captures only **current observable state**.
Never read `.artifacts/` (briefs, PRDs, design docs, epics, roadmaps) as
a source of codebase facts. Forward-looking content (`(planned)`,
`(TBD)`, milestone tags, feature IDs, "shipped through feature X")
belongs to planning artifacts, not the codebase map. If a module, route,
or dependency is described in `.artifacts/` but absent from the
filesystem right now, it does not exist.

## Anti-Pattern: Convention by Dependency Name

Documenting conventions based on what's listed in `package.json` is
guessing. Read the actual config files and source code to understand
how the project uses (or extends, or overrides) each library. The
project's actual values matter, not the framework's defaults.
