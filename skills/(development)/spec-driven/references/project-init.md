# Project Initialization

Initialize the .specs/ directory structure for a new project.

## When to Use

- Starting a new project
- Setting up spec-driven workflow for existing project
- First time running spec-driven commands

## Process

### Step 1: Check Existing Structure

Check if .specs/ already exists:

```bash
ls -la .specs/ 2>/dev/null
```

If exists, skip to Step 4 (update check).

### Step 2: Create Directory Structure

Create base directories:

```bash
mkdir -p .specs/project
mkdir -p .specs/features
```

### Step 3: Generate PROJECT.md

Create `.specs/project/PROJECT.md`:

```markdown
---
name: {project-name}
created: {YYYY-MM-DD}
---

# Project: {Name}

## Vision

{What we're building and why}

## Goals

- Goal 1
- Goal 2

## Constraints

- Technical constraints
- Business constraints

## Stack (Initial)

- Framework: {framework}
- Language: {language}
- Database: {database}
```

### Step 4: Generate ROADMAP.md

Create `.specs/project/ROADMAP.md`:

```markdown
# Roadmap

## Current Sprint

| Feature | Status | Priority |
|---------|--------|----------|
| {name} | planned | P1 |

## Backlog

| Feature | Priority |
|---------|----------|
| {name} | P2 |
```

### Step 5: Generate CHANGELOG.md

Create `.specs/project/CHANGELOG.md`:

```markdown
# Changelog

## [Unreleased]

### Added
- 

## [Version] - YYYY-MM-DD

### Added
- Feature: {name}
```

### Step 6: Generate STATE.md

Create `.specs/project/STATE.md`:

```markdown
# State

## Decisions

| Date | Decision | Context |
|------|----------|---------|
| | | |

## Blockers

| Date | Blocker | Status |
|------|---------|--------|
| | | |

## Learnings

| Date | Learning | Source |
|------|----------|--------|
| | | |
```

### Step 7: Load Existing Context

If persistent storage is available (memory files, project context, prior session data):
- Load existing context
- Populate STATE.md with relevant decisions and learnings
- Keep STATE.md as the canonical local source

### Step 8: Report

Inform user:
- Created .specs/ structure
- Project initialized with PROJECT.md, ROADMAP.md, CHANGELOG.md, STATE.md
- Next steps:
  - Create features: "create new feature for..."
  - Map existing codebase: "map codebase" (if brownfield)

## Error Handling

- Directory already exists: Update files instead of overwrite
- Permission denied: Inform user to check permissions
- Git not initialized: Suggest git init
