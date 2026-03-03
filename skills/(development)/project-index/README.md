# Project Index

Generate project context and codebase documentation for AI agents.

## What It Does

Creates an `.agents/` directory with structured documentation that any AI agent can consume to understand your project.

| Command | What It Generates |
|---------|-------------------|
| **initialize** | Everything (overview + summary if existing code found) |
| **overview** | `.agents/project.md` -- project context, users, features |
| **summary** | `.agents/codebase/` -- 8 docs covering stack, architecture, conventions, testing, integrations, commands, checklist, workflows |

All commands also generate/update `AGENTS.md` at the project root.

## Output Structure

```
.agents/
├── project.md              # What the project is, who it's for
└── codebase/               # How the code works
    ├── stack.md            # Framework, deps, dev tools
    ├── architecture.md     # Patterns, layers, structure, data flow
    ├── conventions.md      # Naming, imports, types, error handling
    ├── testing.md          # Test infra, patterns, reference tests
    ├── integrations.md     # External services and APIs
    ├── commands.md         # Dev, test, build, deploy scripts
    ├── checklist.md        # Post-task validation steps
    └── workflows.md        # User and development flows

AGENTS.md                   # Root summary for AI agents
```

## Usage

```
# Full initialization (recommended for first time)
initialize project

# Just project context
overview

# Just codebase analysis
map codebase
summary
```

## How It Works

### Overview

Reads project metadata (package.json, README, etc.) and generates a concise project context document covering purpose, users, features, constraints, and stack.

### Summary

Deep analysis of the codebase through 4 phases:

1. **Project Discovery** -- metadata, docs, directory structure
2. **Deep Code Analysis** -- reads 5-20 representative files, traces data flows
3. **Testing & Integrations** -- test setup, external services
4. **Convention Extraction** -- synthesizes patterns with evidence

Re-running summary updates existing docs (merge, never overwrite).

## Works With

- **spec-driven** -- spec-driven consumes `.agents/codebase/` for brownfield features and can update it with new discoveries during planning
- **Any AI agent** -- AGENTS.md and `.agents/` follow standard conventions readable by any agent

## Installation

```bash
npx skills add adeonir/agent-skills --skill project-index
```

## Requirements

- Existing project with source code (for summary)
- No dependencies on other skills
