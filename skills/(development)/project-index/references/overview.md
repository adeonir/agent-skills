# Overview

Generate project context for AI agents.

## When to Use

- First time working on a project
- Need to document what the project is and who it's for
- `.agents/project.md` doesn't exist or needs refresh

## Workflow

### Step 1: Check Existing

If `.agents/project.md` exists:
- Ask if refresh needed
- If no: skip to Step 4

### Step 2: Gather Context

Read available sources in priority order:

1. **Existing docs-writer artifacts** (`.artifacts/docs/`): richest source when available

   | File | What to extract |
   |------|-----------------|
   | `brief.md` | What/why/who, scope, success metrics, risks |
   | `prd.md` | Problem, personas, goals, requirements, journeys, milestones, constraints |
   | `design.md` | Context, goals/non-goals, design overview, trade-offs |
   | `pitch.md` | Problem narrative, user-facing solution, scope, rabbit holes |
   | `scope.md` | Work slice description, boundaries |

   Read whichever exist. PRD is the richest single source -- if it exists, it likely covers most of what project.md needs.

2. **Project Metadata**: package.json, pyproject.toml, go.mod, Cargo.toml, or equivalent
3. **Documentation**: README.md, CLAUDE.md, AGENTS.md, CONTRIBUTING.md
4. **Configuration**: tsconfig.json, .env.example, docker-compose.yml

Extract:
- Project name and purpose
- Type of application (web app, API, CLI, library, etc.)
- Primary and secondary users
- Core features/capabilities
- Goals and constraints
- External services and integrations
- Initial technology stack

### Step 3: Generate project.md

**USE TEMPLATE:** [templates/project.md](../templates/project.md)

Create `.agents/project.md` using the template structure:
- Project metadata (name, type, purpose)
- Users (primary and secondary)
- Key features and goals
- Constraints and integration points
- Technology stack

### Step 4: Update AGENTS.md

Load [root-agents.md](root-agents.md) and generate/update `AGENTS.md` at the project root.

### Step 5: Report

Inform user:
- Created: `.agents/project.md`
- Updated: `AGENTS.md`

## Guidelines

- Keep project.md focused on WHAT and WHO, not HOW (implementation)
- One paragraph for purpose, not a wall of text
- Integration points should list external services, not internal modules
- Stack section is a quick reference, not an exhaustive dependency list

## Error Handling

- No documentation found: Ask user for project context directly
- Multiple READMEs: Use root-level README
