---
paths:
  - "skills/**/*.md"
---

## Strip Upstream Scope From Output

**Impact: MEDIUM**

When a skill's workflow reads an upstream artifact (a PRD, brief, parent epic, prior spec, or sibling output), the read step states that the source's own tokens never cross into the produced artifact. Strip forward-phase IDs, sibling-artifact names, downstream task or release references, milestones, and roadmap language — reading is for context, and the output carries only its own concern. The one exception is backward provenance: a skill may carry upstream requirement IDs (`FR/BR/EC/NFR`) for downstream traceability — an epic's `## Requirements` declares the set it owns, and a story links each AC to the requirement it operationalizes on a `**Satisfies**` line — never into prose. `ADR-NNN` is a decision dependency, not a carried requirement; it lives in References.

**Incorrect:**

```markdown
## Read step

Read the parent epic for context, then write the spec.
```

**Correct:**

```markdown
## Read step

Read the parent epic for context only. Its tokens never cross into the story:
strip epic IDs, milestones, sibling-story names, and release references. The
epic declares the requirements it owns in `## Requirements`; link each AC to the
one it operationalizes on a `**Satisfies**` line — backward provenance, never in
prose.
```

## Contain Forbidden References in Templates

**Impact: MEDIUM**

Where a skill ships an output template, the template carries an explicit MUST-NOT list of the forward, sibling, and downstream references that may not appear. The read-step warning and the template list are two halves of one guard; a template without the list lets stripped tokens leak back in.

**Incorrect:**

```markdown
## Epic template

## Requirements
{{the FR/BR/EC/NFR the epic owns}}
```

**Correct:**

```markdown
## Epic template

## Requirements
{{the FR/BR/EC/NFR the epic owns}}

MUST NOT contain: §x.x section numbers, sibling names, milestones, roadmap refs, ADR-NNN.
```
