# Decompose

Materialize one level of the delivery hierarchy: turn a plan into real
artifacts. Point it at the roadmap to create epics, or at an epic to create its
stories and tasks.

## When to Use

- User says "decompose", "break down the roadmap", "break this epic into
  stories", "materialize the epics"
- A roadmap lists epics that do not exist yet, or an epic needs its stories and
  tasks created
- Not for organizing the flow (that is [roadmap.md](roadmap.md)) or for a single
  artifact (create it directly via its ref)

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Identify the level

- **From the roadmap** (`docs/ROADMAP.md`): the parent is the roadmap; the
  children are epics, each created via [epic.md](epic.md).
- **From an epic** (`.artifacts/epics/{epic-name}/epic.md` or its tracker
  entity): the parent is the epic; the children are stories (via
  [story.md](story.md)) and tasks (via [task.md](task.md)).

Read the parent for context only — **translate, don't replicate**: its tokens
never cross verbatim into a child.

### 2. Propose the set

From the parent, propose the children:

- From the roadmap — the epics it lists.
- From an epic — candidate stories (user-value slices) and tasks (enabling work)
  implied by its scope and its stories checklist.

Idempotent: check which children already exist and propose only the missing
ones; never recreate or overwrite. Present the proposed set; let the user add,
drop, merge, split, or rename. Settle the set before creating.

### 3. Create each child

For each confirmed child, run its create ref — [epic.md](epic.md),
[story.md](story.md), or [task.md](task.md). Each child is drafted to its own
canonical template and validated by its own flow (a story's AC through
ac-validation). Decompose never bypasses the create ref — no auto-generated,
unvalidated artifacts.

Sync is inherited, not added here: each create ref carries its own save-or-push,
governed by `epic-tracker.kind` (see [sync.md](sync.md)). Decompose performs no
sync of its own.

## Guidelines

- Materialize one level per run — roadmap → epics, or epic → stories and tasks
- Propose from the parent, confirm with the user, create via the child's create
  ref
- Idempotent: create only the missing children; never recreate or overwrite
- Delegate every artifact to its create ref — canonical shape and validation are
  non-negotiable
- Route cross-cutting concerns by domain, not by order — a foundational decision
  spanning stories, and a domain-specific trap, each belong to the artifact that
  owns them, never parked on whichever story is created first
- Offer to go deeper (a created epic → its stories) but never auto-create the
  next level

## Error Handling

- Roadmap absent when decomposing the roadmap: route to [roadmap.md](roadmap.md)
  to organize the flow first, or create epics directly via [epic.md](epic.md)
- Epic has no scope or stories checklist to imply children: ask the user to
  outline the stories, or derive candidates from the epic's scope and confirm
  before creating
- A child name conflicts with an existing artifact: defer to the create ref's
  conflict handling (suggest an alternative or confirm overwrite)
