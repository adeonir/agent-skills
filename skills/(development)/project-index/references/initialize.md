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
- Check age of files
- Ask if refresh needed
- If no refresh: skip to Step 5 (report)

### Step 2: Create Directory

```bash
mkdir -p .agents
```

### Step 3: Generate Overview

Load [overview.md](overview.md) and generate `.agents/project.md`.

### Step 4: Detect Brownfield

Check if the project has existing source code:

```bash
ls src/ app/ lib/ packages/ 2>/dev/null
ls package.json Cargo.toml go.mod pyproject.toml Gemfile 2>/dev/null
```

If any source code or project manifest is found:
- Load [summary.md](summary.md)
- Run codebase summary as part of initialization
- This generates `.agents/codebase/` with 8 docs

If nothing is found: skip, project is greenfield.

### Step 5: Report

Inform user:
- Created `.agents/` with project.md
- If brownfield: also created `.agents/codebase/` with 8 analysis docs
- Generated AGENTS.md at project root
- Next steps:
  - If using spec-driven: "create feature for..."
  - Re-run summary later: "map codebase" or "summary"
  - Re-run overview later: "overview"

## Guidelines

- Don't overwrite existing `.agents/` structure without confirmation
- Keep project.md focused on context, not implementation
- Initialize once per project, not per feature
- AGENTS.md is always regenerated to reflect current state

## Error Handling

- Directory already exists: Ask before overwriting
- Permission denied: Inform user to check permissions
- Git not initialized: Suggest git init
