# Technical Design

Create technical design from specification.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

- Scope is **Large** or **Complex** (check `scope:` in spec.md frontmatter)
- Spec is complete (no open questions blocking progress)
- Ready to define HOW to build

Start with a clean context window. Load artifacts from disk (spec.md, decisions.md),
not from a previous phase's conversation context. See SKILL.md Phase Transitions.

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

### Step 3: Load Project Knowledge

If `.agents/knowledge.md` exists, read it before designing. It contains
cross-feature decisions, gotchas, and patterns accumulated from previous
features. Use it to:

- Avoid repeating past mistakes
- Follow established architectural patterns
- Respect decisions already made for the project

If it doesn't exist, skip this step.

### Step 4: Research Phase

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

### Step 5: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

### Step 5a: Exploration Depth Gate

Before proceeding to Step 9 (Data Model), verify the exploration artifact's `Touched Types -- Member Enumeration` table is populated for every entity, projection, or contract the feature will read or modify.

**Exit criterion (all must hold):**

- Every touched type named in the spec or data flow has at least one row in the enumeration table
- Every row cites a real `file:line`
- Every absence claim in the Absence Claims table has a `file:line` anchor
- No row has a blank Member cell or TBD `file:line`

If any criterion fails, return to [codebase-exploration.md](codebase-exploration.md) Phase 4 before continuing.

### Step 6: Check Concerns

If `.agents/codebase/concerns.md` exists, read it before designing.

Any component flagged as fragile, carrying tech debt, or having test coverage gaps requires extra care. Document in the Considerations section how the design mitigates those concerns.

If concerns.md does not exist, skip this step.

### Step 7: Persist Codebase Discoveries

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

After persisting codebase discoveries, also feed `.agents/knowledge.md` with
any project-level architectural decisions made during this design. Append new
entries -- never overwrite existing content. If the file doesn't exist, create
it. See format below:

```markdown
## Architecture
- {decision + rationale} (YYYY-MM-DD, feature {ID})

## Gotchas
- {gotcha + context} (YYYY-MM-DD, feature {ID})

## Patterns
- {pattern + why it emerged} (YYYY-MM-DD, feature {ID})
```

### Step 8: Check Visual References

Check if the spec includes a `designs/` folder with visual references:

1. Look for `.artifacts/features/{ID}-{name}/designs/`
2. If images exist (screenshots, mockups, wireframes):
   - Review each image to understand visual requirements
   - Note UI/UX patterns, layout, components shown
   - Consider these in component design and implementation
3. If no designs folder: proceed without visual context

### Step 9: Data Model Definition

Define the data model before component design. Every statement about an existing type must cite `file:line` from the exploration's Member Enumeration.

- **Entities**: Every member the feature reads or writes, cited to `file:line`. Not "attributes" in the abstract -- the actual exposed members in source
- **Relationships**: How entities relate (one-to-many, many-to-many), with `file:line` for each referenced foreign key or join
- **Contracts**: Every member of every request, response, or projection the feature touches, cited to `file:line`. Not "shapes" -- enumerated members
- **Currently Exposed Fields**: If any acceptance criterion names specific output or display fields, fill the `Currently Exposed Fields` table in the design template (one row per AC-named field)

**Closing checklist -- all must pass before Step 10:**

- [ ] Every field named in any acceptance criterion has a row in `Currently Exposed Fields`
- [ ] Every Source cell cites a real `file:line`
- [ ] No Gap cell is blank (use "none" explicitly if no gap)
- [ ] Every "no change required" / "already returns" / "contract unchanged" claim in this section cites a `file:line` from the exploration's Member Enumeration
- [ ] Every type listed under Entities or Contracts matches a row in the exploration's Member Enumeration

### Step 10: Generate design.md

**LOAD ORDER:** Load this template before reading any existing design in `.artifacts/features/`. Existing designs may be stale -- template wins on structure.

**USE TEMPLATE:** `templates/design.md`

Generate the design following the template structure:
- Scope (what is in scope and out of scope)
- Research Summary (if applicable)
- Patterns & Reuse (conventions to follow + existing code to reuse)
- Data Model (Entities, Relationships, API Contracts, Currently Exposed Fields when ACs enumerate fields)
- Decisions (architecture approach + secondary decisions)
- Component Design (component, file, action, responsibility)
- Data Flow (use mermaid for complex flows)
- Requirements Traceability (AC -> Component -> File; ACs enumerating N fields expand to N rows: field -> source file:line)
- Test Strategy
- Considerations (Error Handling, Security, Concerns mitigation)
- Open Questions

### Step 11: Update Status

Set spec.md frontmatter: `status: ready`

### Step 12: Report

Inform user:
- Created: `design.md`
- Research cached: {topics}
- Codebase docs updated: {files updated in .agents/codebase/, if it existed}
- Knowledge updated: {entries added to .agents/knowledge.md, if any}
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
- Enumerate every member of every type the feature reads or writes, cited to file:line
- Cite file:line from the exploration's Member Enumeration for every claim about an existing type
- Expand multi-field acceptance criteria into one traceability row per field

**DON'T:**
- Start designing with unresolved open questions in the spec
- Fabricate APIs or patterns -- verify first
- Over-architect beyond the feature scope
- Sample touched types -- enumerate them
- Claim "already returns X" / "no additional join" / "contract unchanged" without a file:line anchor
- Collapse multi-field ACs into a single traceability row

## Error Handling

- Spec not found: Suggest `specify`
- Open questions blocking architecture: Suggest `discuss`
- Codebase unclear: Ask for guidance
