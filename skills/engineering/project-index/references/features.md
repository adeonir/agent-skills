# Features

Generate `.agents/codebase/features.md` — user-facing capabilities grouped as vertical slices, listing the files that compose each feature and the cross-feature reuse observed.

## When to Use

- Sub-agent dispatched during codebase summary fan-out **only when vertical slicing is detected** (see below)
- User explicitly asks to refresh `features.md` after a feature is added, removed, or restructured

## Detection Gate

Run this ref only when the codebase shows vertical slicing. Otherwise skip — a layer-oriented project does not benefit from `features.md`, and forcing the grouping invents structure that does not exist.

A project is vertically sliced when **any** of these conditions is true:

| Signal | Examples |
|--------|----------|
| Dedicated feature directories | `features/<name>/`, `modules/<name>/`, `apps/<name>/`, `domains/<name>/`, `bounded-contexts/<name>/` |
| Co-located slice files | Same directory holds handler + view + test + schema for one capability (not split into `controllers/`, `views/`, `tests/` at the top level) |
| Domain-prefixed routes with handler tree | `/billing/*`, `/auth/*`, `/inbox/*` each backed by a directory or module that owns its full stack |
| Workspace packages per feature | `packages/<feature>` in a monorepo with no shared `src/services/` layer |

If none apply, document features implicitly via `architecture.md` Entry Points and `workflows.md`. Do not create `features.md`.

The `initialize` step performs this detection before dispatching the sub-agent. If detection is ambiguous, the main agent asks once.

## Scope

Group code by **user-facing capability**, not by technical layer. A feature is observable when the codebase makes the slice explicit — through a dedicated directory, a routed entry point with handler + view + tests, or a domain term that recurs across files.

Two passes:

- **Feature catalog**: list every observable feature with its entry point and primary files
- **Cross-feature reuse**: shared modules each feature depends on (auth, billing, telemetry, design tokens)

Do not include capabilities described in `.artifacts/` (briefs, PRDs, epics) but absent from the filesystem. Do not propose unification or consolidation — that belongs to refactor-time analysis, not the codebase map.

## Reading Priorities

1. Vertical slice directories (`features/<name>/`, `modules/<name>/`, `apps/<name>/`)
2. Routes table from `architecture.md` — group routes that share a domain prefix or handler tree
3. Test directory structure — co-located feature tests reveal slice boundaries
4. Shared/common directories (`lib/`, `shared/`, `core/`) — feed the cross-feature reuse section
5. Sample 1-2 files per feature to confirm responsibility

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning slice files larger than 300 lines.

## Source Boundary

A feature exists when its code exists. A feature flagged off but wired in code counts as present (flag state is volatile; the slice is not). A feature mentioned in a roadmap but with zero source files does not.

If `.agents/codebase/architecture.md` lists a route or component, `features.md` may reference it — these are sibling outputs of the same fan-out and read each other freely. Never read `.artifacts/`.

## Output

Save to `.agents/codebase/features.md`. On re-run, follow [merge-policy.md](merge-policy.md). Features no longer present go through the standard stale-flag cycle, not silent removal.

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources:
  - {{file-path-actually-read}}
  - {{file-path-actually-read}}
---

# Features

## Feature Catalog

| Feature | Entry Point | Directory | Status |
|---------|-------------|-----------|--------|
| {{feature}} | {{route or trigger}} | {{path}} | {{active/flagged/deprecated}} |

## {{Feature Name}}

**Entry**: {{route, command, screen, or trigger}}

**Files**:

| File | Role |
|------|------|
| {{file-path}} | {{handler/view/test/schema/etc.}} |

**Depends on**: {{shared modules from cross-feature reuse}}

**Notable**: {{one or two sentences on what distinguishes this feature in the codebase — pattern reused, integration touched, edge handled}}

{{Repeat per feature}}

## Cross-Feature Reuse

| Shared Module | Consumed By | Surface |
|---------------|-------------|---------|
| {{module}} | {{feature-a, feature-b}} | {{exported function/class/component}} |
````

## Guidelines

- A feature with one file is still a feature — do not collapse small slices into "misc"
- Status field reflects observable state only: `active` (wired and reachable), `flagged` (gated by feature flag in source), `deprecated` (kept for backward compat with `@deprecated` or equivalent marker)
- Cross-feature reuse documents the **consumer relationship**, not architectural intent — list what is imported, not what should be shared
- If detection fails mid-run (initialize dispatched but vertical slicing turns out shallow), abort and leave `features.md` absent — do not write a half-features doc that contradicts `architecture.md`
- Populate `sources:` with every file actually read; empty list is not acceptable
