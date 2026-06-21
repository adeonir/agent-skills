---
paths:
  - "skills/**/*.md"
---

## No Dates or Version Pins

**Impact: MEDIUM**

Skill content stays timeless: no absolute dates, no mutable version pins, no
ephemeral product state, no "soon we will" language. When legacy and current
content must coexist, mark the old one under a collapsed `<details>` block
rather than dating it.

**Incorrect:**

```markdown
As of January 2026, use the v2 endpoint (v3 ships next quarter).
```

**Correct:**

```markdown
Use the v2 endpoint: `api.example.com/v2/messages`.
```

## One Term Per Concept

**Impact: MEDIUM**

Choose one term per concept and keep it across SKILL.md, references, and
templates within a skill. Mixing synonyms ("field" / "box" / "element", or
"extract" / "pull" / "get") forces the model to re-map them and weakens
matching.

**Incorrect:**

```markdown
Extract the fields. Then pull each box and retrieve its element value.
```

**Correct:**

```markdown
Extract the fields. Then extract each field and read its value.
```
