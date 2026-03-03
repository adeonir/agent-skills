# Technical Planning

Create technical plan from specification.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

- Spec is complete (no open questions blocking progress)
- Ready to define HOW to build

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Spec

Read `.artifacts/features/{ID}-{name}/spec.md`.

If spec has critical open questions that block architecture decisions:
- List items
- Ask user to resolve them
- Exit

### Step 3: Research Phase

Check for new technologies in spec:

- APIs mentioned
- Libraries not in codebase
- External services

For each new tech:
- Check `.artifacts/research/{topic}.md`
- If exists: use cached research
- If not: research and create cache (follow [research.md](research.md) trust boundary rules)

When incorporating research into the plan, validate findings against the spec's requirements.
Research informs decisions but the spec remains the single source of truth for what to build.

### Step 4: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

### Step 5: Persist Codebase Discoveries

After exploration, feed new findings back to project-level docs:

1. If `.agents/codebase/` doesn't exist: skip (project-index hasn't been run yet, keep discoveries in plan.md only)
2. If it exists: compare findings against current docs and append new discoveries

What to update:
- **conventions.md**: new convention rows, updated file:line refs
- **architecture.md**: new entry points, layers, integration points
- **testing.md**: new test patterns, reference tests

Rules:
- Merge new findings, never overwrite existing content
- Only add patterns confirmed by this exploration (not speculative)
- Use the same table formats already in the codebase docs
- Never create `.agents/codebase/` from scratch (that's project-index's job)

### Step 6: Data Model Definition

Define the data model before component design:

- **Entities**: Key domain objects and their attributes
- **Relationships**: How entities relate (one-to-many, many-to-many)
- **API contracts**: Request/response shapes for new endpoints

### Step 7: Generate plan.md

**USE TEMPLATE:** `templates/plan.md`

Generate the plan following the template structure:
- Context (feature reference)
- Scope (what is in scope and out of scope)
- Research Summary (if applicable)
- Critical Files (Reference, Modify, Create)
- Codebase Patterns
- Data Model (Entities, Relationships, API Contracts)
- Architecture Decision
- Component Design
- Data Flow (use mermaid for complex flows)
- Requirements Traceability
- Test Strategy
- Considerations (Error Handling, Security)
- Decisions
- Open Questions

### Step 8: Update Status

Set spec.md frontmatter: `status: ready`

### Step 9: Report

Inform user:
- Created: `plan.md`
- Research cached: {topics}
- Codebase docs updated: {files updated in .agents/codebase/, if it existed}
- Key decisions: {count}
- Next: Run `tasks`

## Guidelines

- Don't start planning with unresolved open questions in the spec
- Keep architecture decisions scoped to the feature
- Research unfamiliar technologies before committing to them
- Reference existing codebase patterns when available

## Error Handling

- Spec not found: Suggest `initialize`
- Open questions blocking architecture: Ask user to resolve them
- Codebase unclear: Ask for guidance
