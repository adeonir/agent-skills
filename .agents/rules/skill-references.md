---
paths:
  - "skills/**/*.md"
---

## One Instruction Per Job

**Impact: HIGH**

The unit is the job the skill does, never the number of triggers or the number of files on each side. Count the jobs: a job runs end to end and produces its own outcome. A skill that does one job has no `instructions/` — its SKILL.md is the procedure, and loads what it needs as a step. A skill that does several has one **instruction** per job, and SKILL.md routes to them.

Several triggers entering the same job are one job, not several. A mode that changes only what the procedure returns, an entry state that changes only where the procedure starts, and a phase inside the procedure are all part of one job. A **reference** is what a procedure loads from inside a step: no trigger, never a routing target. `references/` is optional either way, and holds what a procedure loads rather than carries inline.

**Incorrect:**

```text
references/commit.md              # routed by SKILL.md, holds the procedure
references/create-pull-request.md # routed by SKILL.md, holds the procedure
```

**Correct:**

```text
instructions/commit.md            # routed by SKILL.md
instructions/create-pull-request.md
references/message-sourcing.md    # loaded by a step in both
```

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

## References One Level Deep

**Impact: MEDIUM**

Reference and instruction files live one level deep, directly under `references/` or `instructions/`, with no nested subdirectories. A nested tree invites partial reads (e.g. `head -100`) that miss content carried in deeper files.

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

Every reference opens with an H1 title, a one-line description, and a `## When to Use` section before any free sections — the header tells the agent what loading the file buys. Every instruction opens with an H1 title, a one-line description, and the step that loads what it needs before doing the job. An instruction carries no `## When to Use`: SKILL.md already named the condition that routed to it.

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
