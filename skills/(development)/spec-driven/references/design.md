# Technical Design

Create technical design from specification. ultrathink

**Recommended effort:** xhigh — architectural decisions and contract
enumeration are intelligence-sensitive. Lower effort risks shallow design.

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

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

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

### Step 4: Load Architecture Context

Load each of the following if it exists. Skip silently if absent.

**Project root:**
- `CLAUDE.md` — project conventions and agent constraints
- `AGENTS.md` — agent instructions

**Project intelligence (only if `.agents/` exists):**
- `.agents/project.md` — project context
- Every `.md` file in `.agents/codebase/` — list the directory and read
  each file present (architecture, conventions, integrations, concerns,
  plus any others project-index has generated). Do not hardcode names —
  enumerate the directory and read what is there.
- `.agents/baselines/` — load only the baseline matching the area this
  feature touches, if any

`.agents/knowledge.md` is already loaded in Step 3 — do not re-read.

`.agents/` may not exist (greenfield, or project-index never run).
Greenfield projects may have only `CLAUDE.md`. Never block on a missing
file — load what's there. If nothing exists in either location, proceed
with spec.md only.

### Step 5: Research Phase

Check for new technologies in spec:

- APIs mentioned
- Libraries not in codebase
- External services

For each new tech:
- Check `.artifacts/research/{topic}.md`
- If exists: use cached research
- If not: research and create cache (follow [research.md](research.md) trust boundary rules)

If multiple unknown technologies, dispatch one research subagent per topic in
a single turn -- emit multiple dispatch calls in one message, never
sequentially. Each subagent follows research.md and writes to
`.artifacts/research/{topic}.md`. Output is the cache file; main agent reads
results from disk after dispatch completes.

Single-turn dispatch shape (three unknown techs):

```
Turn N (one message):
  - dispatch subagent for {topic-1}, brief = {research.md + topic-1 + spec context}
  - dispatch subagent for {topic-2}, brief = {research.md + topic-2 + spec context}
  - dispatch subagent for {topic-3}, brief = {research.md + topic-3 + spec context}
Turn N+1: read .artifacts/research/{topic-N}.md for each, validate against spec.
```

Map this shape to the subagent dispatch primitive available in the harness.
Single unknown tech: research inline, no dispatch needed.

Follow the [Knowledge Verification Chain](../SKILL.md#knowledge-verification-chain) for all research.

When incorporating research into the design, validate findings against the spec's requirements.
Research informs decisions but the spec remains the single source of truth for what to build.

### Step 6: Codebase Exploration

Load [codebase-exploration.md](codebase-exploration.md).

Focus areas:
- Similar existing features
- Reusable components
- Patterns to follow
- Integration points

**Sub-agent dispatch:** Codebase exploration is context-heavy (multi-phase
workflow with exhaustive member enumeration). Dispatch as a single subagent
that owns the entire exploration end to end and writes findings to disk per
`templates/exploration.md`. Main agent reads the artifact, never the raw
file content.

Subagent brief:
- Paths to spec.md, codebase-exploration.md, templates/exploration.md
- Path to `.agents/codebase/` (if it exists)
- "Follow codebase-exploration.md end to end. Write findings per the
  template. Anchor every claim with file:line. Member enumeration must be
  exhaustive, not sampled."

**Discovery batch:** Step 5 research subagents and this exploration
subagent are independent. Dispatch all in a single turn -- emit multiple
dispatch calls in one message:

```
Turn N (one message):
  - dispatch research subagent for {topic-1}
  - dispatch research subagent for {topic-2}
  - dispatch codebase-exploration subagent
Turn N+1: read .artifacts/research/*.md and exploration artifact from disk,
          advance to Data Model.
```

Map this shape to the subagent dispatch primitive available in the harness.

### Step 6a: Exploration Depth Gate

Before proceeding to the design generation phase (Steps 10-13), verify the exploration artifact's `Touched Types -- Member Enumeration` table is populated for every entity, projection, or contract the feature will read or modify.

**Exit criterion (all must hold):**

- Every touched type named in the spec or data flow has at least one row in the enumeration table
- Every row cites a real `file:line`
- Every absence claim in the Absence Claims table has a `file:line` anchor
- No row has a blank Member cell or TBD `file:line`

If any criterion fails, return to [codebase-exploration.md](codebase-exploration.md) Phase 4 before continuing.

### Step 7: Check Concerns

If `.agents/codebase/concerns.md` exists, read it before designing.

Any component flagged as fragile, carrying tech debt, or having test coverage gaps requires extra care. Document in the Considerations section how the design mitigates those concerns.

If concerns.md does not exist, skip this step.

### Step 8: Queue Codebase Discoveries

Load [knowledge.md](knowledge.md) for format.

Append to `.agents/knowledge.md`:

1. **Cross-feature decisions** -> `## Decisions`, with rationale
2. **Gotchas** -> `## Gotchas`, with context
3. **Codebase discoveries** -> `## Codebase Feedback` with target tag (`conventions`, `architecture`, `testing`, `integrations`, `workflows`, `concerns`)

Never write to `.agents/codebase/*.md` -- those are owned by project-index.

If `.agents/knowledge.md` doesn't exist, create it with the three empty section headers (`## Decisions`, `## Gotchas`, `## Codebase Feedback`).

After appending, always report the `## Codebase Feedback` state to the user -- even when nothing was added. Count by target and prompt:

> N discoveries queued in knowledge.md (X conventions, Y architecture, Z testing, W integrations). Run `/project-index integrate feedback` now? (y/n)

If N is 0, say "No new codebase discoveries this run" and skip the prompt. Never silently proceed to Step 9 without reporting -- this step is mandatory and user-facing.

Do not auto-invoke project-index -- the user controls integration timing.

### Step 9: Check Visual References

Check if the spec includes a `designs/` folder with visual references:

1. Look for `.artifacts/features/{ID}-{name}/designs/`
2. If images exist (screenshots, mockups, wireframes):
   - Review each image to understand visual requirements
   - Note UI/UX patterns, layout, components shown
   - Consider these in component design and implementation
3. If no designs folder: proceed without visual context

### Step 9a: Mid-Phase Context Checkpoint

Discovery is complete. Write a partial snapshot to disk before the
context-heavy design generation steps (11-13). Do not wait for user
confirmation — write immediately and continue.

- If `.artifacts/.session-dump.md` does not exist, create it with
  `# Session Dump` as the H1
- Append a partial block (use `templates/session-dump.md` shape):
  - Phase: `design (in progress — entering data model)`
  - Feature: ID and name
  - Decisions: open architectural decisions entering the design generation phase
  - Discoveries: key findings from research and exploration not captured
    in their respective cache files (e.g. a constraint that affects
    data model shape)
  - Blockers: anything flagged during exploration that may affect design
  - Open items: questions for the data model or component design steps
  - Next phase: `design (continuing — data model and generation)`
- Confirm the checkpoint was written, then continue immediately

This checkpoint is partial and automatic. The end-of-phase dump
(Step 16) remains opt-in and captures the completed phase in full.
If autocompact fires during Steps 11-13, this checkpoint plus the
artifacts on disk provide enough context to resume.

### Step 10: Dispatch Design Plan subagent

Steps 11-13 are owned by a Plan subagent. Main agent dispatches once,
receives structured slot fillers, composes design.md per
`templates/design.md`, then runs the closing checklist against the
artifact before advancing to Step 14.

Why dispatched: Steps 11-13 are intelligence-sensitive (member
enumeration with file:line cites, dependency inversion, traceability
expansion). Isolating them in a Plan subagent keeps main context clean
for the user-visible checklist and approval gate. Plan is read-only by
harness contract (Edit/Write/NotebookEdit excluded), so it returns
structured slot fillers; main composes the artifact via the canonical
template (pattern A1: Plan returns slots, main fills template).

Skip dispatch when subagent support is unavailable; main agent executes
Steps 11-13 directly in that case.

Subagent brief:

- Inputs (paths only -- Plan reads from disk):
  - `.artifacts/features/{ID}-{name}/spec.md`
  - `.artifacts/features/{ID}-{name}/decisions.md` (if exists)
  - Exploration artifact path (from Step 6)
  - `.artifacts/research/*.md` (cached topics from Step 5)
  - `.agents/knowledge.md` (if exists)
  - Every `.md` file in `.agents/codebase/` (if exists; enumerate the
    directory, do not hardcode names)
  - `.agents/baselines/` matching the feature's area (if any)
  - `.agents/project.md`, `CLAUDE.md`, `AGENTS.md` (project root, if
    exist)
  - `.artifacts/features/{ID}-{name}/designs/` (if exists)
- Reference: `templates/design.md` -- return chunks matching the
  template section order and table shapes exactly
- Process: follow Step 11 (Data Model, including its closing checklist
  criteria internally), Step 12 (Dependency Inversion -- silent
  reasoning, never echoed into chunks), Step 13 prep (organize chunks
  per template section). Anchor every claim about an existing type
  with `file:line` from the exploration's Member Enumeration. Resolve
  any internal `[fail]` against Step 11's checklist criteria before
  returning.
- Return shape (structured slot fillers per template section, no
  surrounding prose):
  - Scope: in-scope, out-of-scope bullets
  - Research Summary: bullets per cached topic (or empty)
  - Patterns & Reuse: Conventions rows, Existing Code rows,
    Integration Points rows
  - Data Model: Entities rows; per-entity Member Enumeration blocks
    (member, type, file:line); Relationships text or mermaid; API
    Contracts rows; Currently Exposed Fields rows (one per AC-named
    field when ACs enumerate output, display, response, or persisted
    fields)
  - Decisions: rows (decision, choice, rationale)
  - Component Design: rows (component, file, action, responsibility)
  - Visual Design Considerations: bullets (only when designs/ exists)
  - Data Flow: numbered steps or mermaid
  - Requirements Traceability: rows (requirement, component, file,
    status); expand to one row per field for multi-field ACs
  - Test Strategy: Infrastructure, Reference Tests, New Tests rows
  - Considerations: Error Handling rows, Security bullets
  - Open Questions: checklist items
- Do NOT return: prose narration, process logs, dependency-inversion
  reasoning (silent per Step 12), Gotcha subsections (design-level
  gotchas with rationale go to Decisions; cross-feature gotchas go to
  `.agents/knowledge.md`)

Main agent composes `design.md` by writing Plan's chunks into
`templates/design.md` slots. Preserve template section order and table
shapes exactly. After writing, run Step 11's closing checklist against
the composed artifact -- display each item as `[pass]` or `[fail]`. If
any item fails, re-dispatch Plan with the failure list as additional
brief context.

Main agent also updates spec.md status tags per Step 13 (change each
AC mapped in Requirements Traceability from `pending` to `in-design`).
Plan cannot perform this update because it is read-only; the write is
always main's responsibility regardless of dispatch.

_Steps 11-13 below describe the process Plan follows. Read them as
Plan's substeps when dispatched, or as main agent's process when
dispatch is skipped._

### Step 11: Data Model Definition

Define the data model before component design. Every statement about an existing type must cite `file:line` from the exploration's Member Enumeration.

- **Entities**: Every member the feature reads or writes, cited to `file:line`. Not "attributes" in the abstract -- the actual exposed members in source
- **Relationships**: How entities relate (one-to-many, many-to-many), with `file:line` for each referenced foreign key or join
- **Contracts**: Every member of every request, response, or projection the feature touches, cited to `file:line`. Not "shapes" -- enumerated members
- **Currently Exposed Fields**: If any acceptance criterion names specific output or display fields, fill the `Currently Exposed Fields` table in the design template (one row per AC-named field)

**Closing checklist — display each item as `[pass]` or `[fail]` before writing
design.md. Fix all `[fail]` items first. Do not run this check silently.**

- [ ] Every field named in any acceptance criterion has a row in `Currently Exposed Fields`
- [ ] Every Source cell cites a real `file:line`
- [ ] No Gap cell is blank (use "none" explicitly if no gap)
- [ ] Every "no change required" / "already returns" / "contract unchanged" claim in this section cites a `file:line` from the exploration's Member Enumeration
- [ ] Every type listed under Entities or Contracts matches a row in the exploration's Member Enumeration

### Step 12: Dependency Inversion Check (implicit)

Reason about this silently before writing design.md. Do not echo this check
into the artifact -- the design stays focused on the design, not on a process
log.

For each component, module, type, or primitive you are placing into a story:

- Identify which story *owns* it (the story that introduces it)
- Identify every story that *consumes* it
- The owning story must be numbered ≤ the earliest consuming story

If inverted -- owning story has a higher number than a consuming story --
resolve before writing, by picking one:

- **Relocate ownership**: move the component into the earliest consuming
  story. Often the right answer for shared primitives that were mentally
  "grouped with their caller"
- **Reorder stories**: if the primitive is conceptually a prerequisite, move
  its story earlier in spec.md. Remember to keep Story IDs aligned with the
  new order
- **Inline then refactor**: leave the earlier story shipping an inline
  implementation, and let the later story's scope explicitly include the
  refactor to a shared primitive. Record this decision in Decisions so tasks
  can plan the refactor as an explicit task

Never let the design leave an inversion implicit. An inverted design produces
tasks whose commits do not stand alone, which breaks the per-story
commit-boundary contract that spec-driven relies on.

### Step 13: Generate design.md

**LOAD ORDER:** Load this template before reading any existing design in `.artifacts/features/`. Existing designs may be stale -- template wins on structure.

**USE TEMPLATE:** `templates/design.md`

Generate the design following the template structure:
- Scope (what is in scope and out of scope)
- Research Summary (if applicable)
- Patterns & Reuse (conventions to follow + existing code to reuse + integration points with existing systems)
- Data Model (Entities, Relationships, API Contracts, Currently Exposed Fields when ACs enumerate fields)
- Decisions (architecture approach + secondary decisions)
- Component Design (component, file, action, responsibility)
- Data Flow (use mermaid for complex flows)
- Requirements Traceability (AC -> Component -> File; ACs enumerating N fields expand to N rows: field -> source file:line)
- Test Strategy
- Considerations (Error Handling, Security, Concerns mitigation -- no Gotcha subsections)
- Open Questions

After generating design.md, update spec.md: for each AC mapped in Requirements Traceability,
change its status tag from `` `pending` `` to `` `in-design` ``.

### Step 14: Update Status

Set spec.md frontmatter: `status: ready`

### Step 15: Approval Gate

Present a summary:

```
Design ready: `.artifacts/features/{ID}-{name}/design.md`
Decisions: {count} | Open questions: {count or "none"}

Approve to proceed, or describe changes.
```

Whether to stop here depends on the user's original request (see Specify Step 14 for the same rule):

- User asked only for design (rare): stop and wait.
- User asked for the full planning bundle ("plan and break into tasks", "turn this into a spec for us to implement", "figure this out and spec it", etc.): present this as a waypoint, then continue into `tasks`. Collect approval once at the end of planning.

If changes are requested: update design.md, then continue.

Do not start code-producing phases (`implement`) without explicit user approval regardless of the original phrasing.

### Step 16: Suggest Session Dump

Phase complete. Suggest to the user that this is a good moment to dump
session context and clear the window before the next phase:

> Phase complete. Append a phase summary to `.artifacts/.session-dump.md`
> and clear the context for the next phase? (y/n)

If the user accepts:

- If `.artifacts/.session-dump.md` does not exist, create it with
  `# Session Dump` as the H1
- Append one block using `templates/session-dump.md` -- record only what
  an artifact does not already capture (unstated decisions, blockers,
  follow-ups for the next phase). Do not duplicate spec.md / design.md /
  tasks.md content
- Confirm the dump was written; the user clears the window manually

If the user declines or skips: continue in the current window without dumping.

The dump is ephemeral cross-phase memory -- wrap-up reads it at end of
session, then the file is disposable.

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
- Add `### Gotcha` subsections to Considerations -- design-level gotchas with rationale go to Decisions; cross-feature gotchas go to `.agents/knowledge.md ## Gotchas`
- Substitute the Entities table for prose or bullets -- the table is the index; member enumeration goes in sub-blocks below

## Error Handling

- Spec not found: Suggest `specify`
- Open questions blocking architecture: Suggest `discuss`
- Codebase unclear: Ask for guidance
