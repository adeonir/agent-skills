---
paths:
  - "skills/**/*.md"
---

## No Dates or Version Pins

**Impact: MEDIUM**

Skill content stays timeless: no absolute dates, no mutable version pins, no ephemeral product state, no "soon we will" language. When legacy and current content must coexist, mark the old one under a collapsed `<details>` block rather than dating it.

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

Choose one term per concept and keep it across SKILL.md, references, and templates within a skill. Mixing synonyms ("field" / "box" / "element", or "extract" / "pull" / "get") forces the model to re-map them and weakens matching.

**Incorrect:**

```markdown
Extract the fields. Then pull each box and retrieve its element value.
```

**Correct:**

```markdown
Extract the fields. Then extract each field and read its value.
```

## No Authoring-Chat Rationale

**Impact: MEDIUM**

A decision made in the authoring conversation lands in the file as the decision, never as its history. Strip any trace of the exchange that produced it — "as discussed", "we decided", "this used to be X", "now any pair works". The consumer never sees that conversation, so a file arguing with a revision it cannot read spends tokens on a comparison it cannot make; git history carries the why. Superseded content that must stay visible is a `<details>` block, not a sentence narrating the change.

**Incorrect:**

```markdown
Epics used to map to a Project, but that broke cross-level dependencies, so we
moved them to Issues — now any pair is expressible.
```

**Correct:**

```markdown
Every artifact is an Issue. A dependency between any two of them has a native
form; see `set_dependencies`.
```
