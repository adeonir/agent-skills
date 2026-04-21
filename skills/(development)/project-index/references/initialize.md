# Initialize Project

Set up the `.agents/` directory with project context and codebase analysis.

## When to Use

- Starting work on a new or existing project
- First time running project-index commands
- `.agents/` doesn't exist yet

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
|--------|---------|
| Has a project manifest | package.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, pom.xml, build.gradle, composer.json |
| Has source code directories | src/, app/, lib/, cmd/, internal/, pkg/, packages/ |
| Has multiple source files | More than 5 files with code extensions (.ts, .js, .py, .go, .rs, .java, .rb, .php) |

If brownfield:
- Load [summary.md](summary.md)
- Run codebase summary as part of initialization
- This generates `.agents/codebase/` with analysis docs

If none of the above: skip summary, project is greenfield.

### Step 5: Report

Inform user:
- Created `.agents/` with project.md
- If brownfield: also created `.agents/codebase/` with analysis docs
- AGENTS.md: `created` / `updated` / `skipped (CLAUDE.md present)` / `skipped (user declined)` -- mirror the outcome from root-agents.md
- Next steps:
  - If using spec-driven: "create feature for..."
  - Re-run summary later: "map codebase" or "summary"
  - Re-run overview later: "overview"

## Guidelines

**DO:**
- Keep project.md focused on context, not implementation
- Initialize once per project, not per feature
- Regenerate AGENTS.md to reflect current state

**DON'T:**
- Overwrite existing `.agents/` structure without confirmation
- Run initialize per feature -- it is a one-time project setup

## Error Handling

- Directory already exists: Ask before overwriting
- Permission denied: Inform user to check permissions
- Git not initialized: Suggest git init
