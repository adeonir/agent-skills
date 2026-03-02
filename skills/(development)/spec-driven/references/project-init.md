# Project Initialization

Initialize the .artifacts/ directory structure for a new project.

## When to Use

- Starting a new project
- Setting up spec-driven workflow for existing project
- First time running spec-driven commands

## Workflow

### Step 1: Check Existing Structure

Check if .artifacts/ already exists:

```bash
ls -la .artifacts/ 2>/dev/null
```

If exists, skip to Step 5 (report).

### Step 2: Create Directory Structure

Create base directory:

```bash
mkdir -p .artifacts/project
```

Other directories are created on demand:
- `.artifacts/features/` -- created when first feature is initialized
- `.artifacts/research/` -- created when first research is conducted
- `.artifacts/codebase/` -- created during brownfield detection (Step 4) or manual codebase mapping

### Step 3: Generate PROJECT.md

**USE TEMPLATE:** `templates/PROJECT.md`

Generate PROJECT.md following the template structure with project name, vision, goals, constraints, and tech stack.

### Step 4: Detect Brownfield

Check if the project has existing source code:

```bash
ls src/ app/ lib/ packages/ 2>/dev/null
ls package.json Cargo.toml go.mod pyproject.toml Gemfile 2>/dev/null
```

If any source code or project manifest is found:
- Load [codebase-mapping.md](codebase-mapping.md)
- Run codebase mapping as part of initialization
- This generates `.artifacts/codebase/` with 6 docs (STACK, ARCHITECTURE, CONVENTIONS, STRUCTURE, TESTING, INTEGRATIONS)

If nothing is found: skip, project is greenfield.

### Step 5: Report

Inform user:
- Created .artifacts/project/ with PROJECT.md
- If brownfield: also created .artifacts/codebase/ with 6 analysis docs
- Next steps:
  - Create features: "create new feature for..."
  - Map codebase manually: "map codebase" (if greenfield that becomes brownfield later)

### Lazy Artifacts

These files are created when first needed, not at initialization:

| Artifact | Created When |
|----------|-------------|
| ROADMAP.md | User runs "create roadmap" or "plan features" |
| CHANGELOG.md | First feature is archived |
| .artifacts/features/ | First feature is initialized |

## Guidelines

- Don't overwrite existing .artifacts/ structure
- Keep PROJECT.md focused on vision and constraints, not implementation
- Use the provided templates for consistent formatting
- Initialize once per project, not per feature

## Error Handling

- Directory already exists: Update files instead of overwrite
- Permission denied: Inform user to check permissions
- Git not initialized: Suggest git init
