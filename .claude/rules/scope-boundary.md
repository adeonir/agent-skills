---
paths:
  - "skills/**/*.md"
---

## Strip Upstream Scope From Output

**Impact: MEDIUM**

When a skill's workflow reads an upstream artifact (a PRD, brief, parent epic, prior spec, or sibling output), the read step states that the source's own tokens never cross into the produced artifact. Strip forward-phase IDs, sibling-artifact names, downstream task or release references, milestones, and roadmap language — reading is for context, and the output carries only its own concern. The one exception is backward provenance: a skill may carry upstream requirements (`FR/BR/EC/NFR`) for downstream traceability, always in a dedicated field and never in prose. Each artifact in the chain carries the set it owns — a roadmap entry's `Requirements` field partitions the IDs across epics, an epic's `## Requirements` declares the set it owns as `ID — statement`, and a story links each AC to the requirement it operationalizes on a `**Satisfies**` line. `ADR-NNN` is a decision dependency, not a carried requirement; it lives in References. `DEP-N` is an external dependency, not a carried requirement; it shapes sequencing, never a requirement field.

A requirement statement is the norm itself, so the field that carries it is translated in form only: strip the source's framing (section numbers, doc-internal codes, upstream voice), and keep the modal, the actor, the object, and every bound (timing, count, threshold) exactly as strong as the source states them. Reword the frame, never the demand — a statement that lands looser or stricter than its source is a mistranslation, and where no rewording preserves the demand, the source's wording carries over verbatim.

**Incorrect:**

```markdown
## Read step

Read the parent epic for context, then write the spec.
```

**Correct:**

```markdown
## Read step

Read the PRD for context only. Its tokens never cross into the epic: strip
`§x.x` section numbers, doc-internal codes, and PRD framing. The one exception
is backward provenance: the requirements this epic owns are recorded in
`## Requirements` as `ID — statement`, never in prose. Translate each statement
in form, never in norm — the modal, the actor, the object, and every bound carry
over unchanged.
```

## Contain Forbidden References in Templates

**Impact: MEDIUM**

Where a skill ships an output template, the template carries an explicit MUST-NOT list of the forward, sibling, and downstream references that may not appear. The read-step warning and the template list are two halves of one guard; a template without the list lets stripped tokens leak back in.

**Incorrect:**

```markdown
## Epic template

## Requirements
{{ID — statement, one per FR/BR/EC/NFR the epic owns}}
```

**Correct:**

```markdown
## Epic template

## Requirements
{{ID — statement, one per FR/BR/EC/NFR the epic owns}}

MUST NOT contain: a statement looser or stricter than the source's, §x.x section
numbers, sibling names, milestones, roadmap refs, ADR-NNN.
```
