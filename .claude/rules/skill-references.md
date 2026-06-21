---
paths:
  - "skills/**/*.md"
---

## References One Level Deep

**Impact: MEDIUM**

Reference and instruction files live one level deep, directly under
`references/` or `instructions/`, with no nested subdirectories. A nested tree
invites partial reads (e.g. `head -100`) that miss content carried in deeper
files.

**Incorrect:**

```text
references/auth/login.md
```

**Correct:**

```text
references/auth-login.md
```

## Required Reference Header

**Impact: MEDIUM**

Every reference opens with an H1 title, a one-line description, and a
`## When to Use` section before any free sections. The header tells the agent
when to load the file at all.

**Incorrect:**

```markdown
## Workflow

1. Stage the files
```

**Correct:**

```markdown
# Commit Workflow

Create a conventional commit from staged changes.

## When to Use

When committing staged or unstaged changes.
```

## No Fan-Forward Sections

**Impact: MEDIUM**

A reference ends where its job ends; it never carries a `## Next Steps` section
or prose like "Proceed to X" that pushes the agent into a downstream phase. A
genuine prerequisite is a sibling cross-link in prose, not a closing nudge
forward.

**Incorrect:**

```markdown
## Next Steps

After generating the spec, run the design phase.
```

**Correct:**

```markdown
See [validate.md](validate.md) for the gate this output must pass.
```
