# Build the Roadmap

Organize the project's epics into an ordered flow, derived from the PRD, in `docs/ROADMAP.md`. The roadmap references its epics; the epics never reference the roadmap.

## When to Use

- User says "create roadmap", "plan the roadmap", "organize epics", "roadmap the PRD"
- The delivery needs an ordered plan of epics before or alongside creating them
- Not for creating the epics themselves — that is materialization, see [decompose.md](decompose.md)

## Workflow

### 1. Read the PRD

Look for `docs/product/PRD.md`. If it exists, read:

- **Scope** (Must/Should/Could) for the boundary of work
- **Goals & Non-Goals** for outcomes and constraints
- **User Journeys** for the main flows to support
- **User Personas** for actors that may shape epic grouping
- **Business Rules** for cross-cutting constraints that may become their own epics
- **Non-Functional Requirements** for quality targets that may need dedicated work
- **Definition of Done** for readiness criteria that may require a validation epic
- **External Dependencies** for blockers that should influence sequencing
- **Risks and Open Questions** for uncertainties to address early

If absent, derive the epics from the user directly — the roadmap never depends on the PRD existing. When the PRD is missing, mark the roadmap as provisional in its intro line: this plan assumes a PRD will confirm scope and priorities.

**Translate, don't replicate.** The PRD stays the source of requirements; its tokens never cross verbatim into the roadmap. Strip PRD IDs (FR-N, BR-N, EC-N, NFR-N, DEP-N) and section numbers — the roadmap names epics and their flow in plain language.

### 2. Organize the epic flow

Lay the epics out in delivery order. Each entry is a capability-level epic — a name plus a one-line intent — sequenced by how the work should flow, not by deadline.

**Phasing heuristics.** Use these to decide order and grouping:

- **Dependencies first.** Epics that unblock others come earlier.
- **Risk early.** High-uncertainty epics move earlier so unknowns surface before they block the plan.
- **Value incrementally.** When a slice delivers user value on its own, prefer it over a big-bang phase.
- **Foundation before experience.** Core product plumbing (identity, data model, permissions) typically precedes user-facing features that rely on it.
- **External dependencies shape timing.** Items blocked by outside parties may start earlier or wait, depending on lead time.
- **Readiness last.** If the PRD's Definition of Done requires post-ship validation, include a final validation or readiness epic.

Group into phases only when the flow has natural stages; a flat ordered list is fine.

**Capabilities, not specs.** An entry names a capability or objective, never a UI widget, field, endpoint, or technology. Each epic's own scope and stories are decided later when it is materialized, not here.

Present the proposed flow; let the user reorder, add, drop, merge, or split. Settle the flow before writing.

### 3. Reconcile on re-run

When `docs/ROADMAP.md` already exists, read it as input. Compare it against the current PRD and any new context, then propose only the delta:

- Epics added because the PRD scope grew
- Epics dropped because scope was cut or moved to Won't Have
- Reordering because dependencies, risks, or external blockers changed
- Phase renaming or merging as the flow evolves

Preserve the existing structure for untouched parts. Update in place — never duplicate.

### 4. Write docs/ROADMAP.md

Write the ordered flow to `docs/ROADMAP.md` (committed). Update it in place on re-run — the roadmap is a living plan; never duplicate it. The roadmap lists its epics; it does not create them (that is [decompose.md](decompose.md)).

## Template

Here is a sensible default format, but use your best judgment — phase headings when the flow has stages, a single ordered list when it does not:

````markdown
---
updated: {{YYYY-MM-DD}}
status: {{draft | stable | provisional}}
sources:
  - PRD: {{link to docs/product/PRD.md or "None"}}
  - PRODUCT: {{link to docs/product/PRODUCT.md or "None"}}
---

# Roadmap: {{Project Name}}

{{One line on what this roadmap sequences and why.}}
{{When the PRD is missing or provisional, add a note: "This roadmap is provisional until a PRD confirms scope and priorities."}}

## {{Phase name, or omit the heading for a flat flow}}

1. **{{epic-name}}** — {{one-line capability the epic delivers}} — _Driven by: {{journey, rule, or goal that motivates this epic}}_ — {{optional tag: foundation | validation | high-risk | external-dependency}}
2. **{{epic-name}}** — {{one-line capability}} — _Driven by: {{journey, rule, or goal}}_
````

MUST NOT contain: deadlines or dates, per-story detail, PRD IDs (FR-N, BR-N, EC-N, NFR-N, DEP-N), section numbers, or implementation specifics. Tags are short signals only; they never replace the capability description or introduce scheduling.

## Guidelines

- Read the PRD for context; author the flow in plain language, independent of PRD framing
- Consider the full PRD when ordering: scope, journeys, personas, business rules, NFRs, Definition of Done, external dependencies, risks, and open questions
- Name epics as capabilities, never UI or technology
- Sequence by flow, not deadline — a roadmap orders work, it does not schedule it
- Keep it one living doc; update in place, never duplicate
- The roadmap references its epics; epics never point back at it — they stay self-contained
- Organizing is not creating — materialize epics via [decompose.md](decompose.md)
- Mark the roadmap provisional when the PRD is missing or known to be unstable
- Populate frontmatter `updated`, `status`, and `sources` on every write
- Use tags sparingly: `foundation`, `validation`, `high-risk`, `external-dependency` — never as a substitute for the capability description
