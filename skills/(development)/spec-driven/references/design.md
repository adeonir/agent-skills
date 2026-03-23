# Technical Design

Create technical design from specification.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

- Scope is **Large** or **Complex** (check `scope:` in spec.md frontmatter)
- Spec is complete (no open questions blocking progress)
- Ready to define HOW to build

## When to Skip

- Scope is **Medium**: straightforward change, no architectural decisions, no new patterns
- When skipped, implement handles a lightweight codebase scan inline (see [implement.md](implement.md))

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Spec

Read `.artifacts/features/{ID}-{name}/spec.md`.

If spec has critical open questions that block architecture decisions:
- List items
- Suggest running [discuss](discuss.md) to resolve them
- Exit

If decisions.md exists, load it for resolved gray areas.

### Step 3: Research Phase

Check for new technologies in spec:

- APIs mentioned
- Libraries not in codebase
- External services

For each new tech:
- Check `.artifacts/research/{topic}.md`
- If exists: use cached research
- If not: research and create cache (follow [research.md](research.md) trust boundary rules)

Follow the [Knowledge Verification Chain](../SKILL.md#knowledge-verification-chain) for all research.

When incorporating research into the design, validate findings against the spec's requirements.
Research informs decisions but the spec remains the single source of truth for what to build.

### Step 4: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

### Step 5: Check Concerns

If `.agents/codebase/concerns.md` exists, read it before designing.

Any component flagged as fragile, carrying tech debt, or having test coverage gaps requires extra care. Document in the Considerations section how the design mitigates those concerns.

If concerns.md does not exist, skip this step.

### Step 6: Persist Codebase Discoveries

After exploration, feed new findings back to project-level docs:

1. If `.agents/codebase/` doesn't exist: skip (project-index hasn't been run yet, keep discoveries in design.md only)
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

### Step 7: Check Visual References

Check if the spec includes a `designs/` folder with visual references:

1. Look for `.artifacts/features/{ID}-{name}/designs/`
2. If images exist (screenshots, mockups, wireframes):
   - Review each image to understand visual requirements
   - Note UI/UX patterns, layout, components shown
   - Consider these in component design and implementation
3. If no designs folder: proceed without visual context

### Step 8: Data Model Definition

Define the data model before component design:

- **Entities**: Key domain objects and their attributes
- **Relationships**: How entities relate (one-to-many, many-to-many)
- **API contracts**: Request/response shapes for new endpoints

### Step 9: Generate design.md

**USE TEMPLATE:** `templates/design.md`

Generate the design following the template structure:
- Scope (what is in scope and out of scope)
- Research Summary (if applicable)
- Patterns & Reuse (conventions to follow + existing code to reuse)
- Data Model (Entities, Relationships, API Contracts)
- Decisions (architecture approach + secondary decisions)
- Component Design (component, file, action, responsibility)
- Data Flow (use mermaid for complex flows)
- Requirements Traceability (AC -> Component -> File)
- Test Strategy
- Considerations (Error Handling, Security, Concerns mitigation)
- Open Questions

### Step 10: Update Status

Set spec.md frontmatter: `status: ready`

### Step 11: Report

Inform user:
- Created: `design.md`
- Research cached: {topics}
- Codebase docs updated: {files updated in .agents/codebase/, if it existed}
- Key decisions: {count}
- Visual references considered: {count} (if designs/ exists)
- Next: Run `tasks`

## Guidelines

**DO:**
- Resolve open questions in the spec before designing
- Keep architecture decisions scoped to the feature
- Research unfamiliar technologies before committing to them
- Reference existing codebase patterns when available
- Follow Knowledge Verification Chain for all technical decisions

**DON'T:**
- Start designing with unresolved open questions in the spec
- Fabricate APIs or patterns -- verify first
- Over-architect beyond the feature scope

## Error Handling

- Spec not found: Suggest `specify`
- Open questions blocking architecture: Suggest `discuss`
- Codebase unclear: Ask for guidance
