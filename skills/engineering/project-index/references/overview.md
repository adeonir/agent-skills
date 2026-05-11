# Overview

Generate `.agents/project.md` — project context for AI agents.

## When to Use

- First time working on a project
- `.agents/project.md` does not exist or needs refresh
- User says "overview", "project context", "refresh project"

## Workflow

### Step 1: Check Existing

If `.agents/project.md` exists, update it — merge new findings, never overwrite blindly.

### Step 2: Gather Context

Read available sources in priority order:

1. **Existing planning artifacts** (`.artifacts/docs/`): richest source when available

   | File | What to extract |
   |------|-----------------|
   | `brief.md` | What/why/who, scope, success metrics, risks |
   | `prd.md` | Problem, personas, goals, requirements, journeys, milestones, constraints |
   | `design.md` | Context, goals/non-goals, design overview, trade-offs |
   | `epic.md` | Problem narrative, user-facing solution, scope, rabbit holes |
   | `issue.md` | Work item description, context, boundaries |

   Read whichever exist. PRD is the richest single source — if it exists, it likely covers most of what `project.md` needs.

2. **Project metadata**: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, or equivalent
3. **Documentation**: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`
4. **Configuration**: `tsconfig.json`, `.env.example`, `docker-compose.yml`

Extract:

- Project name and purpose
- Type of application (web app, API, CLI, library, etc.)
- Primary and secondary users
- Core features and capabilities
- Goals and constraints
- External services and integrations
- Technology stack: framework version, key dependencies, dev tools

### Step 3: Generate project.md

Compose `.agents/project.md` using the template below.

### Step 4: Report

Inform user:

- Created: `.agents/project.md`

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources: []
---

# Project: {{Project Name}}

## Purpose

{{What the project does and why it exists — one paragraph}}

## Type

{{Web app | API | CLI | Library | Mobile app | etc.}}

## Users

- Primary: {{Who uses this and what they do}}
- Secondary: {{Other user groups, if any}}

## Key Features

- {{Core capability 1}}
- {{Core capability 2}}
- {{Core capability 3}}

## Goals

- {{Goal 1}}
- {{Goal 2}}

## Constraints

- {{Technical constraints}}
- {{Business constraints}}

## Integration Points

| Service | Purpose |
|---------|---------|
| {{service}} | {{what it does}} |

## Stack

### Framework

- {{name}}: {{version}}

### Key Dependencies

- {{package}}: {{purpose}}

### Dev Tools

- {{tool}}: {{purpose}}
````

## Guidelines

- Keep `project.md` focused on WHAT and WHO, not HOW (implementation)
- Use one paragraph for purpose
- List external services in Integration Points; do not list internal modules
- Keep the stack section as a quick reference, not an exhaustive dependency list

## Error Handling

- No documentation found: ask user for project context directly
- Multiple READMEs: use root-level README
