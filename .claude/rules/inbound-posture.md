---
paths:
  - "skills/**/*.md"
---

## Upstream Artifact Is a Claim, Not Authority

**Impact: MEDIUM**

When a skill's read step ingests an upstream artifact — a parent spec, an inherited acceptance criterion, a prior decision — it states that the artifact enters as a claim to check, not as authority to inherit. Name what is rebuttable and what happens when a rebuttal holds: surface the disagreement, or emit a finding. Reading for context never makes the source's assertions true, and a skill that conforms to an upstream artifact silently has no way to catch a defect the source introduced.

**Incorrect:**

```markdown
## Read step

Read the parent spec; it is the source of truth for the acceptance criteria.
Conform the story's AC to it.
```

**Correct:**

```markdown
## Read step

Read the parent spec as a claim, not authority. Where an inherited AC asserts more
than the story's benefit requires, surface the disagreement rather than carrying
it; reading for context never makes the source's assertions true.
```
