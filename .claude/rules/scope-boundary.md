---
paths:
  - "skills/**/*.md"
---

## Strip Upstream Scope From Output

**Impact: MEDIUM**

When a skill's workflow reads an upstream artifact (a PRD, brief, parent epic,
prior spec, or sibling output), the read step states that the source's own
tokens never cross into the produced artifact. Strip forward-phase IDs,
sibling-artifact names, downstream task or release references, milestones, and
roadmap language — reading is for context, and the output carries only its own
concern.

**Incorrect:**

```markdown
## Read step

Read the parent epic for context, then write the spec.
```

**Correct:**

```markdown
## Read step

Read the parent epic for context only. Its tokens never cross into the spec:
strip epic IDs, milestones, sibling-story names, and release references.
```

## Contain Forbidden References in Templates

**Impact: MEDIUM**

Where a skill ships an output template, the template carries an explicit
MUST-NOT list of the forward, sibling, and downstream references that may not
appear. The read-step warning and the template list are two halves of one
guard; a template without the list lets stripped tokens leak back in.

**Incorrect:**

```markdown
## Spec template

## Requirements
{{the requirements}}
```

**Correct:**

```markdown
## Spec template

## Requirements
{{the requirements}}

MUST NOT contain: milestones, epics, sprints, release names, roadmap refs.
```
