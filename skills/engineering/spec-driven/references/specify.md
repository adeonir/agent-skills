# Specify Feature

Create a new feature specification with adaptive depth. Load
[status-workflow.md](status-workflow.md) for correct status management.

## When to Use

When creating a new feature spec or modifying an existing one.

## Content Separation (CRITICAL)

Each artifact has a distinct purpose. Never mix these concerns.

| File | Purpose |
|------|---------|
| spec.md | WHAT to build (requirements, acceptance criteria) |
| decisions.md | WHY certain decisions were made (discuss output, gray areas) |
| design.md | HOW to build (architecture, files, implementation) |
| tasks.md | WHEN to build (ordered tasks with dependencies) |

### spec.md MUST contain ONLY:

- Goals (measurable outcomes)
- Non-goals (explicit exclusions)
- Glossary (domain terms used in ACs, defined behaviorally; "None" when empty)
- User stories with acceptance criteria inline (AC-N IDs, EARS-lite shape 1:1 (no compound), status starts as `` `pending` ``)
- Edge cases (boundary conditions, error scenarios)
- Success criteria (measurable outcomes)
- For brownfield: current behavior description (high-level, no code)

### spec.md MUST NOT contain:

- Code snippets, identifiers, or field/enum names from the codebase (e.g., `mode: 'create'`, `reason: 'validation_error'`, `discountType === 'fixed'`)
- Component, hook, function, or class names (e.g., `PlanFormDrawer`, `usePlans`, `DangerZone`)
- File paths or directory structures (e.g., `src/components/ui/`)
- Technology or library choices (e.g., React, TanStack Form, shadcn, Radix)
- Implementation approaches (e.g., `useTransition`, `router.refresh()`, server actions)
- Database schemas or API designs
- Architecture decisions
- Milestones, epics, sprints, release names, or roadmap references (e.g., "part of Q2 epic", "blocked by milestone 3", "planned for v2")

These apply to ALL sections -- Overview, Goals, Non-Goals, Glossary, Stories, ACs, Edge Cases, Success Criteria, Operational Follow-ups, Notes, Baseline. Behavior always trumps symbols.

These belong in design.md, created during the `design` phase.

## Arguments

- `[description]` - Feature description
- `[@file.md]` - Path to PRD/Design Doc file
- Greenfield: "create new feature for..."
- Brownfield: "modify feature...", "improve..."

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Track each step as it completes — mark it done before moving to the next.
In Claude Code, create a task list at phase start (TaskCreate) and update
each step as it completes (TaskUpdate).

### Step 1: Assess Scope

Before anything else, determine complexity to auto-size the pipeline:

| Signal | Scope | Pipeline |
|--------|-------|----------|
| Mechanical change, zero decisions, outcome obvious from the description | **Small** | Redirect to [quick-mode.md](quick-mode.md) |
| Canonical pattern already in the codebase, no new abstraction needed | **Medium** | Specify -> Implement (skip Design, Tasks) |
| ≥1 load-bearing decision new to the codebase (reviewer cannot predict approach from description) | **Large** | Specify -> Design -> Tasks -> Implement |
| Ambiguity in the problem itself, solution space open | **Complex** | Specify (+ Discuss) -> Design -> Tasks -> Implement (+ UAT) |

If **Small**: redirect to [quick-mode.md](quick-mode.md) and stop here.

Record the assessed scope in spec.md frontmatter as `scope: medium|large|complex`.
Small never reaches this file -- it redirects to quick-mode above, so `small`
is not a valid spec.md scope value.

### Step 2: Check Project Context

Load whatever project context exists:

| Context Found | Action |
|---------------|--------|
| `CLAUDE.md` exists | Use `## Project` and `## Architecture` as context for discovery |
| `.artifacts/codebase/{area}.md` cache exists | Use for brownfield pattern matching in that area |
| Neither exists (greenfield) | Proceed without — project context is optional for new projects |
| Neither exists (brownfield) | Scan a few representative files when discovery needs codebase context |

### Step 3: Ensure Project Structure

Check if `.artifacts/features/` parent exists. If not:

```bash
mkdir -p .artifacts/features
```

### Step 4: Generate Feature ID

Scan `.artifacts/features/` for highest ID:

```bash
ls .artifacts/features/ | sort -V | tail -1
```

Next ID = highest + 1 (padded: 001, 002...)

### Step 5: Determine Type (Greenfield vs Brownfield)

**Greenfield triggers:**
- "create new feature"
- "new feature"
- "implement from scratch"

**Brownfield triggers:**
- "modify feature"
- "improve"
- "refactor"
- "extend"

If ambiguous, ask user.

### Step 6: Process Input

**If input is a file (@file.md):**

Extraction is **transformation**, not copying. Source documents define
product-level or system-level requirements; the spec defines feature-level,
implementation-ready requirements. Every item must be narrowed to feature
scope and refined with implementation detail.

| Source (PRD/Design Doc) | spec.md |
|-------------------------|---------|
| Product-wide user stories | Feature-scoped stories prioritized by implementation order (P1/P2/P3) |
| Directional requirements (must/should/could) | Implementable FRs with measurable criteria |
| High-level acceptance criteria | Testable ACs in EARS-lite shape (1:1, no compound) |
| Product KPIs and success metrics | Feature-specific success criteria (demo-able) |
| No edge cases | Edge cases (boundaries, errors, invalid inputs) |

1. If path is a directory, list all files: `find {path} -type f -name "*.md"`
2. Read each file completely -- extract rules ("must", "cannot", "always"),
   constraints ("only if", "when", "unless"), and examples
3. Filter each item: relevant → transform; not relevant → note WHY in Notes;
   partially relevant → extract only the applicable part
4. Transform (never copy verbatim): narrow broad stories to feature scope, make
   ACs testable (EARS-lite shape, 1:1), add missing edge cases and success criteria
   derived from requirements
5. Output extraction summary in Notes section before generating spec -- the
   "Transformed To" column must show the refined version, not a copy

**If input is text:**
- Use as feature description

**If input is empty:**
- Ask user for feature description

**Record sources:**

`sources:` is the spec's list of durable external references it points to
instead of duplicating their content -- input file paths (`@file.md`, a PRD
or Design Doc path), tracker ticket IDs or URLs, design-artifact paths. One
entry per source. A clean session follows these to recover context the spec
deliberately did not copy, so they are the pointer half of the handoff
(`## Session Context` holds what has no durable source). Record every input
that defined this spec here as you process it; leave `[]` only when nothing
durable defines the work -- the content lived only in conversation and must
go to `## Session Context` instead.

**Detect defect origin:**

The spec captures WHAT to build, including for fixes. When the input
originates from a defect, the spec must be framed around the correct
behavior (the root), not the absence of a symptom.

Defect signals (apply when any match):
- Input file is a bug or issue ticket artifact (e.g.,
  `.artifacts/epics/.../bugs/`, `.artifacts/epics/.../issues/`)
- Input file frontmatter has `type: bug` or `type: issue`
- Description contains defect keywords: `fix`, `bug`, `error`,
  `broken`, `regression`, `crash`, `falha`, `quebrou`,
  `não funciona`, "stopped working", "throws", "fails"

When defect signals match:
- Set frontmatter `origin: defect` (default `origin: feature`)
- Frame Goals around the correct behavior, not the absence of a
  symptom. Prefer "Token expiry check accepts boundary timestamp" over
  "Users no longer see login errors at boundary times". The first
  defines the root; the second defines the symptom.
- Each AC asserts the correct behavior, including for the case that
  used to fail. Symptom-only ACs ("no 500 in logs", "no toast appears")
  are insufficient on their own -- pair with a behavior AC.

Investigation of the cause is NOT performed in specify -- that work
belongs to design (Large/Complex) or to Step 6 Diagnose in quick-mode
(Small). Specify captures the problem and the success behavior; the
how comes later.

### Step 7: Feature Discovery

Load [discovery.md](discovery.md) and conduct feature discovery. If input came
from a file (@file.md), pass the extracted content as starting context so
discovery can skip questions already answered by the document.

### Step 8: Baseline Discovery (Brownfield)

If type is `brownfield`:

1. **Analyze current behavior from user perspective** (not implementation details):
   - What users can currently do
   - Current workflows and limitations
   - What needs to change

2. **Behavior only -- no file paths, no component/hook names:**

   | Include | Exclude |
   |---------|---------|
   | What users can do | File paths |
   | Current limitations | Function names |
   | Behavior gaps | Code snippets |
   | User-facing issues | Technical implementation |

3. **Add Baseline section to spec.md:**

   ```markdown
   ## Baseline

   ### Current Behavior
   - Users can currently do X
   - System behaves like Y
   - Limitation: Z

   ### Gaps / Limitations
   - Missing: A
   - Problem: B
   - Improvement needed: C
   ```

If no `.artifacts/codebase/{area}.md` cache exists for the area:
- Scan a few representative files for brownfield context
- Proceed with limited codebase understanding if that is enough

### Step 9: Generate Feature Name

Convert description to kebab-case:
- "Add user authentication" -> `add-user-auth`

### Step 10: Ask About Branch

Default suggestion is a new branch. Record the user's choice in `branch:` frontmatter only — the branch is created at implement start, not here.

```text
Branch for this feature?
1. New branch: feature/{name} (recommended)
2. Current branch ({current-branch})
3. Other (specify name)
```

- Whichever option the user picks, store the resolved branch name in spec.md frontmatter.
- Do not run `git checkout` or `git switch` in this step. Branch creation belongs to implement.md.

### Step 11: Create Feature Directory

```bash
mkdir -p .artifacts/features/{ID}-{name}
```

### Step 12: Include Visual References

Check if the prompt includes images (screenshots, mockups, wireframes, diagrams):

**If images are present:**
1. Create `designs/` subdirectory:
   ```bash
   mkdir -p .artifacts/features/{ID}-{name}/designs
   ```
2. Save each image to the designs folder with descriptive filenames:
   - `{brief-description}.{ext}` (e.g., `login-screen.png`, `user-flow.jpg`)
3. Images will be referenced in spec.md section "Visual References"

**If no images:**
- Skip this step (designs/ folder is optional)

### Step 13: Propose Approaches (Large/Complex only)

Skip for Small and Medium scope.

For **Large** and **Complex** features, before drafting the spec present 2-3 architectural
approaches with trade-offs. Lead with your recommendation and the reason. Keep each
option to 3-4 sentences. Wait for user to choose before proceeding.

Example structure:

```text
**Option A (recommended):** {approach} — {why it fits, trade-off}
**Option B:** {approach} — {why it fits, trade-off}
**Option C:** {approach} — {why it fits, trade-off}
```

Do not draft spec.md until user confirms an approach. Record the chosen approach in
spec.md Notes section.

### Step 14: Generate spec.md

Use the template (below) before reading any existing spec in
`.artifacts/features/`. Existing specs may be stale — template wins on
structure.

Generate the spec following the template structure:
- Frontmatter with ID, feature name, type, scope, status, review, branch, created date
- Greenfield: Overview, Goals, Non-Goals, Glossary, User Stories (with ACs inline), Edge Cases, Success Criteria, Operational Follow-ups, Open Questions, Notes
- Brownfield: Same structure plus Baseline section (Current Behavior, Gaps/Limitations)
- **If images were saved to designs/**: Include Visual References section with markdown image references (e.g., `![Description](designs/filename.png)`)

Each story includes "Why Px" to justify its priority level. P1 stories must be vertical slices -- complete, demo-able features (not just backend or frontend). Each P1 story includes an Independent Test. Acceptance criteria are inline per story with AC-xxx IDs for traceability.

#### Pre-write checklist

Before writing spec.md, display the result of every item below — show `[pass]` or
`[fail]` for each line. Fix all `[fail]` items before writing. Do not run this
check silently.

- [ ] No code identifiers in ACs or Edge Cases (no `mode: 'create'`, no `===`, no field or enum names)
- [ ] No technology or library names anywhere (no React, TanStack, shadcn, Radix)
- [ ] No component, hook, function, or class names from the codebase
- [ ] No file paths or directory names
- [ ] Non-Goals entries describe behavior, not code symbols
- [ ] Notes contains only behavioral context -- no HOW, no libraries, no component names
- [ ] No milestones, epics, sprints, release names, or roadmap references anywhere
- [ ] Every non-functional claim is quantified (e.g. `p95 ≤ 200ms`) or demoted to an Open Question — no vague "fast", "scalable", "responsive"
- [ ] Each story is a commit boundary: no AC depends on work belonging to a later story (move it if so)
- [ ] Baseline (if brownfield) describes user-observable behavior, not code structure
- [ ] If origin=defect: Goals name the correct root behavior, not the absence of a symptom; every defect AC asserts correct behavior (symptom-only ACs are paired with a behavior AC)

If any box fails: rewrite the offending lines behaviorally, or move HOW content to design.md. Never ship a spec that leaks design.

### Section Rules

**Goals:** 2-4 per feature (more signals scope creep). Each goal must map to at least
one Success Criterion. Future-tense observation windows ("for N days after deploy",
"in the period following launch") are not verifiable at audit time -- keep the
architectural/instrumentation claim in Goals and move the observation window to
`## Operational Follow-ups`.

**User Stories:** All stories WILL be implemented. Priorities define implementation
order, not whether something ships. Each story is a commit boundary -- an AC that
requires work from a later story must be moved to that story. Watch for narrative vs
build order inversions: if a story defines a reusable primitive that an earlier-numbered
story consumes, the inversion breaks the commit-boundary contract. Fix by moving the
primitive's story earlier, merging it into the first consumer, or making the earlier
story ship an inline implementation that the later story refactors into the shared
primitive. Never leave the inversion implicit.

**Acceptance Criteria:** Use EARS-lite — one of five clause shapes, 1:1 per AC, no
compound clauses. The shape names how the requirement is triggered; the sentence
states one observable obligation:

```text
Ubiquitous:  The system shall {action}.
Event:       When {trigger}, the system shall {action}.
State:       While {state}, the system shall {action}.
Optional:    Where {feature}, the system shall {action}.
Unwanted:    If {unwanted condition}, then the system shall {mitigation}.
```

One trigger, one outcome per AC. Each shape maps cleanly to a Given/When/Then or
property-based test downstream — that mapping lives in the tests, not the spec.
Happy paths go in ACs; boundary conditions go in Edge Cases. AC IDs are monotonic
and never reused: removing an AC retires its ID with a tombstone entry — status
`removed` plus a one-line reason — instead of renumbering, so existing task and
test references stay stable. When an AC references a third-party audit tool, append
an `Audit-tool measurement` sub-bullet:

```markdown
- [ ] AC-1: When {trigger}, the system shall {observable outcome}
  - **Audit-tool measurement:** {tool name} -- {exact metric the tool reports} -- pass threshold: {numeric or boolean}
```
Required only when the AC references a third-party audit tool. Omit the sub-line otherwise.

**Non-functional criteria:** Any performance, latency, throughput, capacity, or
availability claim must carry a number and the condition it holds under (`p95 ≤ 200ms
under 50 RPS`), or it is not an acceptance criterion — demote it to an Open Question.
Vague adjectives ("fast", "scalable", "responsive") are not testable and never ship as ACs.

**Glossary:** Define every domain term that appears in an AC, behaviorally — no code
identifiers, libraries, or component names. Write "None" when the feature introduces no
domain vocabulary. This is where Spec Review confirms each term is defined.

**Operational Follow-ups:** Plain bullets (no `[ ]` -- the absence of a checkbox makes
the non-gating intent explicit). Use "None" if every criterion is pre-merge verifiable.
Never duplicate items that also appear in Goals or Success Criteria.

**Notes:** Same behavior vs symbol filter as the rest of the spec -- no libraries, no
paths, no component or hook names. Omit the section entirely if there is nothing
behavioral to capture beyond what other sections already cover. Boundary vs Session
Context: Notes holds surrounding evidence (stakeholders, deadlines, prior art);
Session Context holds prompt-only material that *defines* the work (content/copy,
constraints, clarifications, user/source-stated assumptions). If losing it would change
what gets built, it is Session Context, not Notes.

**Decisions and Session Context:** Both sections are always present -- the durable home for
context settled during specify that would otherwise live only in chat. `## Decisions`
captures choices made among alternatives at the specify grain (scope, requirements,
product behavior); `## Session Context` captures content, constraints, clarifications, and user/source-stated assumptions.
Boundary: when design.md runs (Large/Complex), technical and architecture decisions
go in its `## Decisions` instead -- spec.md stays at the specify grain, design.md owns
the implementation grain, no duplication. When discuss.md runs (Complex gray areas),
its resolutions stay there; record only their downstream effect on scope or
requirements here. At Medium, design.md is skipped, so spec.md is the only home --
capture everything implement needs here. Fill from this
conversation, or write "None" when a `sources:` pointer covers it. Never delete either
section -- an explicit "None" asserts nothing was lost; a missing section is an
omission.

### Step 15: Spec Review

After generating spec.md, review the written artifact against the criteria below and
record the verdict in frontmatter `review:`. This is the spec's own review gate —
there is no separate review file. Show `[pass]` or `[fail]` per line.

- [ ] Every AC matches one EARS-lite shape (ubiquitous, event, state, optional, unwanted)
- [ ] Every AC is atomic — one trigger, one outcome, no compound "and"
- [ ] Every AC is testable — a Given/When/Then test is describable without guessing intent
- [ ] Every Goal maps to at least one Success Criterion
- [ ] Every domain term used in an AC is defined (no undefined jargon)
- [ ] Open Questions are each resolved or explicitly deferred with a reason

Set the verdict:

- All pass → `review: pass`
- Any fail → `review: changes`; report the failing lines, fix them, re-run until `pass`

Downstream phases (design, tasks, implement) expect `review: pass`. A spec edited after
review resets to `review: pending` and must be re-reviewed before proceeding.

### Step 16: Handoff Completeness Gate

Before presenting the spec as ready, confirm self-sufficiency:

> Could a clean session implement this from `spec.md` plus its `sources:`
> alone? If anything that bears on implementation was settled only in this
> conversation -- a decision, content/copy, a constraint, a clarification --
> capture it in `## Decisions` or `## Session Context` now. If it lives in a durable
> source the project already tracks, record a `sources:` pointer instead of
> duplicating.

The artifact is the only thing the next session sees. If it is only in
chat, it does not exist.

### Step 17: Approval Gate

Present a summary:

```text
Spec ready: `.artifacts/features/{ID}-{name}/spec.md`
Type: {greenfield|brownfield} | Scope: {medium|large|complex}
Review: {pass|changes} | Open questions: {count or "none"} | Gray areas: {yes/no}

Approve to proceed, or describe changes.
```

Whether to stop here depends on what the user actually asked for. Read the original request:

- **User asked for the spec only** (e.g. "write a spec", "capture the requirements", "draft what this feature should do") -- stop at this gate and wait for approval.
- **User asked for the full planning bundle** (e.g. "plan this out", "plan and break into tasks", "turn this into a spec for us to implement", "design this", "break into tasks", "figure this out and spec it", provides a PRD and asks to "turn this into something we can execute") -- do not stop. Present this summary as a waypoint, then continue the pipeline through the final planning phase the scope requires. Approval is collected once at the end of planning, not at every phase boundary.

Apply the pipeline by scope once you have decided to continue:

- Small: Quick mode handles the whole job -- Specify was not invoked. If you are reading this, the scope assessment was wrong; back out and route through `quick-mode`.
- Medium: Specify finishes, then `implement` waits for user go
- Large: Specify → `design` → `tasks`, then wait for user go before `implement`
- Complex: Specify → (`discuss` if gray areas) → `research` (if new tech) → `design` → `tasks`, then wait for user go before `implement`

The approval gates exist to catch user disagreement, not to impose a phase-by-phase checkpoint when the user has already asked for the whole planning bundle. Stopping prematurely on a phrase like "a spec" when the user clearly meant "the full plan, starting from the spec" forces the user to re-ask for every downstream phase -- that is ceremony, not safety.

If changes are requested at any gate: update the relevant artifact, re-run its pre-write checks, then continue.

Do not start `implement` (code-producing phases) without explicit user approval regardless of the original phrasing.

## Codebase Mapping Note

The `.artifacts/codebase/{area}.md` cache holds reusable area-level
exploration (patterns, integration points) from prior features.
**Baseline in specify** captures specific current behavior relevant to
this feature.

They complement each other:

- Area cache: macro view (the area, reused across features)
- Baseline discovery (Step 8): micro view (this feature only)

## Guidelines

**DO:**
- Validate feature scope before creating the spec
- Mark unclear requirements as TBD rather than inventing constraints
- Keep one feature per spec -- split if scope is too broad
- Auto-size correctly based on actual complexity

**DON'T:**
- Include technical solutions in spec (that belongs in design)
- Force Large pipeline on Medium features
- Invent constraints when requirements are unclear

## Spec Template

ALWAYS use this exact template structure:

````markdown
---
id: {{NNN}}
name: {{name}}
scope: {{medium|large|complex}}
status: draft
review: pending
type: {{greenfield|brownfield}}
origin: {{feature|defect}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
branch: {{branch-name or main}}
sources: []
---

# Feature: {{Title}}

## Overview

{{Problem description: what pain point are we solving, who is affected, why now}}

## Goals

- [ ] {{Primary goal with measurable outcome}}
- [ ] {{Secondary goal with measurable outcome}}

## Non-Goals

| Feature | Reason |
|---------|--------|
| {{feature}} | {{why excluded}} |

## Glossary

{{Domain terms used in the acceptance criteria, defined behaviorally. Write "None"
when the feature introduces no domain vocabulary.}}

- **{{Term}}** — {{definition, no code identifiers, libraries, or component names}}

## User Stories

### S-1 [P1] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P1:** {{why this is critical for MVP}}
- **Independent Test:** {{how to verify this story works alone}}

**Acceptance Criteria:**

- [ ] AC-1 `pending`: When {{trigger}}, the system shall {{observable outcome}}
  - **Audit-tool measurement:** {{tool name}} — {{exact metric}} — pass threshold: {{numeric or boolean}}
- [ ] AC-2 `pending`: While {{state}}, the system shall {{observable outcome}}

### S-2 [P2] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P2:** {{why this matters but is not MVP}}

**Acceptance Criteria:**

- [ ] AC-3 `pending`: The system shall {{observable outcome}}

### S-3 [P3] {{Story Title}}

- As a {{user}}, I want {{goal}} so that {{benefit}}
- **Why P3:** {{why this is nice-to-have}}

**Acceptance Criteria:**

- [ ] AC-4 `pending`: If {{unwanted condition}}, then the system shall {{mitigation}}

{{#if designs}}
## Visual References

{{#each designs}}
![{{description}}](designs/{{filename}})
{{description of what this image shows}}

{{/each}}
{{/if}}

## Edge Cases

- If {{boundary condition}}, then the system shall {{observable handling}}
- If {{error scenario}}, then the system shall {{graceful handling}}
- If {{unexpected input}}, then the system shall {{validation response}}

## Success Criteria

- [ ] {{Measurable outcome — e.g., "User can complete X in under 2 minutes"}}
- [ ] {{Measurable outcome — e.g., "Zero errors in Y scenario"}}

## Operational Follow-ups

Post-deploy observations, monitoring windows, or runbook tasks that
cannot be verified at audit time. Recorded here so the spec captures
intent, but **not audit targets** — audit only checks Goals and Success
Criteria.

- {{Operational item, e.g., "Post-deploy monitoring: zero rejections in payment flow over 7 days"}}
- {{or write "None" if every criterion is pre-merge verifiable}}

## Open Questions

- {{Any unresolved questions, or "None" if all resolved}}

## Decisions

{{Choices settled during this conversation that a clean session could not
reconstruct from the spec or its `sources:`. Omit self-evident rows;
write "None" when every choice is obvious or covered by a `sources:`
pointer. At Large/Complex this is usually "None" -- technical and
architecture choices belong in design.md.}}

| Decision | Choice | Rationale |
|----------|--------|-----------|
| {{what was decided}} | {{what was chosen}} | {{why this over alternatives}} |

## Session Context

{{Material that defines the work but lives only in this conversation, not
in a `sources:` pointer — content/copy to implement, user-stated constraints
and assumptions, clarifications that resolved ambiguity. Write "None" when a
`sources:` entry covers it.}}

- {{captured item, or "None"}}

## Notes

{{additional behavioral context — evidence, stakeholders, deadlines; never technology choices, component names, or file paths}}

{{#if brownfield}}
## Baseline

### Current Behavior

- {{What users observe today — no component names, no code identifiers}}

### Gaps / Limitations

- {{What's missing or problematic, described as user impact}}
{{/if}}
````

## Error Handling

- No project structure: Initialize project first
- ID conflict: Regenerate ID
- Branch exists: Offer to checkout existing
- Scope misjudged: Safety valve in implement catches this
