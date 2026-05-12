# Initialize Project

Set up the `.agents/` directory with project context and codebase analysis.

## When to Use

- Starting work on a new or existing project
- First time running project-index
- `.agents/` does not exist yet

## Workflow

### Step 1: Check Existing Structure

Check if `.agents/` already exists:

```bash
ls -la .agents/ 2>/dev/null
```

If exists:

- Update existing files, merging new findings
- Never overwrite blindly

### Step 2: Create Directory

```bash
mkdir -p .agents
```

### Step 3: Generate Overview

Load [overview.md](overview.md) and generate `.agents/project.md`.

### Step 4: Detect Brownfield

A project is brownfield if ANY of these conditions is true:

| Signal | Examples |
|--------|----------|
| Has a project manifest | `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Gemfile`, `pom.xml`, `build.gradle`, `composer.json` |
| Has source code directories | `src/`, `app/`, `lib/`, `cmd/`, `internal/`, `pkg/`, `packages/` |
| Has multiple source files | More than 5 files with code extensions (`.ts`, `.js`, `.py`, `.go`, `.rs`, `.java`, `.rb`, `.php`) |

If brownfield: dispatch the codebase summary fan-out (see SKILL.md).

If none of the above: skip summary, project is greenfield.

### Step 4b: Detect Vertical Slicing

Before dispatch, check whether the brownfield project is vertically
sliced. The `features` sub-agent is added to the fan-out only when it
is. See [features.md](features.md) Detection Gate for the full signal
list. Quick check:

| Signal | Examples |
|--------|----------|
| Feature directories | `features/<name>/`, `modules/<name>/`, `apps/<name>/`, `domains/<name>/` |
| Co-located slice files | Handler + view + test + schema share one directory per capability |
| Domain-prefixed routes | `/billing/*`, `/auth/*`, `/inbox/*` each with its own handler tree |
| Per-feature workspace packages | Monorepo `packages/<feature>` with no shared `src/services/` layer |

If detection is ambiguous (some signals present, layer-oriented
elsewhere), ask the user once: "Vertical slicing detected? (y/n)" Skip
the `features` sub-agent on `n`.

If layer-oriented: skip `features`, dispatch the standard 6.

### Step 5: Report

Inform user:

- Created `.agents/` with `project.md`
- If brownfield: also created `.agents/codebase/` with fan-out docs +
  `review.md` (6 docs, plus `features.md` when vertical slicing
  detected)
- Next steps:
  - Re-run codebase mapping later: "map codebase" or "summary"
  - Re-run overview later: "overview"

## Guidelines

- Keep `project.md` focused on context, not implementation
- Initialize once per project, not per feature

## Error Handling

- Directory already exists: ask before overwriting
- Permission denied: inform user to check permissions
- Git not initialized: suggest `git init`
