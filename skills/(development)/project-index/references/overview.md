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

Read available documentation and metadata:

1. **Project Metadata**: package.json, pyproject.toml, go.mod, Cargo.toml, or equivalent
2. **Documentation**: README.md, CLAUDE.md, AGENTS.md, CONTRIBUTING.md
3. **Configuration**: tsconfig.json, .env.example, docker-compose.yml

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

### Step 4: Generate AGENTS.md

Generate or update `AGENTS.md` at the project root. The file should reference the contents of `.agents/` and provide a concise summary of the project for any AI agent.

Content should include:
- Project summary (from project.md)
- Key conventions (from conventions.md, if exists)
- Important commands (from commands.md, if exists)
- Checklist (from checklist.md, if exists)
- References to `.agents/` files for deeper context

If `AGENTS.md` already exists: merge new content, preserve any manual additions.

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
