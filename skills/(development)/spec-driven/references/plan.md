# Technical Planning

Create technical plan from specification.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

- Spec is complete (no open questions blocking progress)
- Ready to define HOW to build

## Process

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
- If not: research and create cache

### Step 4: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

### Step 5: Data Model Definition

Define the data model before component design:

- **Entities**: Key domain objects and their attributes
- **Relationships**: How entities relate (one-to-many, many-to-many)
- **API contracts**: Request/response shapes for new endpoints

### Step 6: Generate plan.md

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

### Step 7: Update Status

Set spec.md frontmatter: `status: ready`

### Step 8: Report

Inform user:
- Created: `plan.md`
- Research cached: {topics}
- Key decisions: {count}
- Next: Run `tasks`

## Error Handling

- Spec not found: Suggest `initialize`
- Open questions blocking architecture: Ask user to resolve them
- Codebase unclear: Ask for guidance
