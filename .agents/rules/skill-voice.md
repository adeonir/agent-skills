---
paths:
  - "skills/**/*.md"
---

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

## Declarative Facts, Not Narrated Reasoning

**Impact: MEDIUM**

Skill content states a standing fact, never the discovery, reasoning, or process behind it. A because-clause, a "so we changed it" explanation, or a recounting of what was found narrates the authoring session the consumer never reads; only the fact drives the agent. Assert what holds now and drop the account of how it came to be known — this catches explanatory prose the marker phrases above miss.

**Incorrect:**

```markdown
Because rendering the title twice looked wrong, the adapter strips a leading
H1 that repeats the title.
```

**Correct:**

```markdown
The adapter strips a leading H1 that repeats the title.
```
