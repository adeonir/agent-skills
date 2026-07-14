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

**Translate, don't replicate.** The PRD stays the source of requirements; its tokens never cross verbatim into the roadmap. Strip section numbers and PRD framing — the roadmap names epics and their flow in plain language. The one exception is backward provenance: each entry records the requirement IDs (`FR/BR/EC/NFR`) that epic will own, in its `Requirements` field, never in prose. `DEP-N` is an external dependency, not an owned requirement — it informs sequencing and may surface as an `external-dependency` tag, never as a requirement ID.

Read the PRD as a claim, not authority. Where its scope leaves a requirement no epic can plausibly own, or two requirements contradict each other, surface the disagreement instead of forcing a partition around it.

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

### 3. Partition the requirements

Assign every PRD requirement ID in scope (`FR/BR/EC/NFR`) to exactly one epic. This is the partition the epics inherit — it is decided once here, with the whole PRD in view, rather than re-derived epic by epic.

Check the partition before writing:

- **No orphans.** Every requirement in Must and Should scope belongs to some epic. Flag any that does not and ask the user to place it, add an epic, or confirm the omission.
- **No duplicates.** A requirement claimed by two epics means the epic boundaries are wrong, not that the requirement is shared. Resolve the boundary.
- **Could scope is optional.** Assign `Could` requirements only when an epic genuinely carries them; leave the rest unassigned.

An epic with no requirements is legitimate — enabling or validation work often derives from no PRD line. Leave its `Requirements` field off rather than inventing a mapping.

When no PRD exists, skip this step; the roadmap carries no requirement IDs.

### 4. Reconcile on re-run

When `docs/ROADMAP.md` already exists, read it as input. Compare it against the current PRD and any new context, then propose only the delta:

- Epics added because the PRD scope grew
- Epics dropped because scope was cut or moved to Won't Have
- Reordering because dependencies, risks, or external blockers changed
- Phase renaming or merging as the flow evolves
- Requirement IDs added, moved between epics, or dropped as PRD scope shifted

Re-run the partition check from step 3 against the current PRD: a requirement added upstream since the last write is an orphan until it is placed, and a requirement the PRD dropped still sits on an epic until it is removed.

Preserve the existing structure for untouched parts. Update in place — never duplicate.

### 5. Write docs/ROADMAP.md

Write the ordered flow to `docs/ROADMAP.md`. Update it in place on re-run — the roadmap is a living plan; never duplicate it. Whether to commit it is the user's call. The roadmap lists its epics; it does not create them (that is [decompose.md](decompose.md)).

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

1. **{{Epic Title}}** — {{one-line capability the epic delivers}} — _Driven by: {{journey, rule, or goal that motivates this epic}}_ — _Requirements: {{FR/BR/EC/NFR IDs this epic owns — omit the field when the epic derives from no PRD}}_ — {{optional tag: foundation | validation | high-risk | external-dependency}}
2. **{{Epic Title}}** — {{one-line capability}} — _Driven by: {{journey, rule, or goal}}_ — _Requirements: {{IDs}}_
````

MUST NOT contain, in any entry: deadlines or dates, per-story detail, section numbers, `DEP-N`, `ADR-NNN`, or implementation specifics. The frontmatter's `updated` is the only permitted date. Requirement IDs (`FR/BR/EC/NFR`) appear only in the `Requirements` field, never in the capability line or any prose. Tags are short signals only; they never replace the capability description or introduce scheduling.

## Guidelines

- Read the PRD for context; author the flow in plain language, independent of PRD framing
- Consider the full PRD when ordering: scope, journeys, personas, business rules, NFRs, Definition of Done, external dependencies, risks, and open questions
- Partition the PRD requirements across the epics once, with the whole PRD in view — every Must and Should requirement lands on exactly one epic, or its omission is confirmed
- Keep requirement IDs in the `Requirements` field; the capability line stays plain language
- Name epics as capabilities, never UI or technology
- Sequence by flow, not deadline — a roadmap orders work, it does not schedule it
- Keep it one living doc; update in place, never duplicate
- The roadmap references its epics; epics never point back at it — they stay self-contained
- Organizing is not creating — materialize epics via [decompose.md](decompose.md)
- Mark the roadmap provisional when the PRD is missing or known to be unstable
- Populate frontmatter `updated`, `status`, and `sources` on every write
- Use tags sparingly: `foundation`, `validation`, `high-risk`, `external-dependency` — never as a substitute for the capability description
