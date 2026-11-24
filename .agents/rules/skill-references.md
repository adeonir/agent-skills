---
paths:
  - "skills/**/*.md"
---

## Shared Constraint Loaded as a Step

**Impact: HIGH**

A constraint two instructions need lives in one `references/` file, and each instruction loads it as a step, before the work that needs it. A prose mention is not the mechanism — an agent working through an instruction applies what a step tells it to load, and reads a bare cross-link as background it may skip. Never cite by name a term the instruction does not define and does not load.

The threshold is size. A constraint that fits in one sentence stays inline in each instruction that needs it; the duplication costs less than a file load. A constraint that needs a block of its own earns the reference.

**Incorrect:**

```markdown
<!-- instructions/create-pull-request.md -->
**Summary — glanceable.** 1-3 short sentences at the plain-prose bar.
```

**Correct:**

```markdown
<!-- instructions/create-pull-request.md -->
4. **Load [message-sourcing.md](../references/message-sourcing.md)** — the diction bar and the sourcing rule for the body.
5. **Write the summary** — 1-3 short sentences at that bar.
```

## Flat References, One Grouping Level

**Impact: MEDIUM**

Reference and instruction files live directly under `references/` or `instructions/`, with no nested tree. A skill with more than eight references may group them into one topic subdirectory (`references/<topic>/<file>.md`); that single grouping level keeps the list scannable without inviting the partial reads (e.g. `head -100`) that miss content in deeper files.

**Incorrect:**

```text
references/auth/login.md
```

**Correct:**

```text
references/auth-login.md
```

## Required Header

**Impact: MEDIUM**

Every reference opens with an H1 title, a one-line description, and a `## When to Use` section before any free sections — the header tells the agent what loading the file buys. Every instruction opens with an H1 title, a one-line description, and the step that loads what it needs before doing the job. An instruction may also carry `## When to Use` when its job has operational entry conditions, phase or state gates, or optionality that must be applied after routing. Keep trigger routing in `SKILL.md`; do not use the section to duplicate the routing table.

**Incorrect:**

```markdown
## Workflow

1. Stage the files
```

**Correct:**

```markdown
# Commit

Create a conventional commit from the actual changes.

## Load first

Read [message-sourcing.md](../references/message-sourcing.md) — where the words come from and the diction bar.

## Staging

Stage by name the files that belong to this change.
```

## No Fan-Forward Sections

**Impact: MEDIUM**

An instruction ends where its job ends; it never carries a `## Next Steps` section or prose like "Proceed to X" that pushes the agent into a downstream trigger. Loading a reference from inside a step is not fan-forward — it pulls in what this job needs, rather than handing the agent the next job.

**Incorrect:**

```markdown
## Next Steps

After generating the spec, run the design phase.
```

**Correct:**

```markdown
2. **Load [acceptance-criteria.md](../references/acceptance-criteria.md)** — the contract the criteria below must satisfy.
```
