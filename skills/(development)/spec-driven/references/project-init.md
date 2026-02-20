# Project Initialization

Initialize the .artifacts/ directory structure for a new project.

## When to Use

- Starting a new project
- Setting up spec-driven workflow for existing project
- First time running spec-driven commands

## Process

### Step 1: Check Existing Structure

Check if .artifacts/ already exists:

```bash
ls -la .artifacts/ 2>/dev/null
```

If exists, skip to Step 4 (update check).

### Step 2: Create Directory Structure

Create base directories:

```bash
mkdir -p .artifacts/project
mkdir -p .artifacts/features
```

### Step 3: Generate PROJECT.md

**USE TEMPLATE:** `templates/PROJECT.md`

Generate PROJECT.md following the template structure with project name, vision, goals, constraints, and tech stack.

### Step 4: Generate ROADMAP.md

**USE TEMPLATE:** `templates/ROADMAP.md`

Generate ROADMAP.md following the template structure with Current Sprint and Backlog tables.

### Step 5: Generate CHANGELOG.md

**USE TEMPLATE:** `templates/CHANGELOG.md`

Generate CHANGELOG.md following the template structure with Unreleased and versioned sections (Added, Changed, Fixed).

### Step 6: Report

Inform user:
- Created .artifacts/ structure
- Project initialized with PROJECT.md, ROADMAP.md, CHANGELOG.md
- Next steps:
  - Create features: "create new feature for..."
  - Map existing codebase: "map codebase" (if brownfield)

## Error Handling

- Directory already exists: Update files instead of overwrite
- Permission denied: Inform user to check permissions
- Git not initialized: Suggest git init
