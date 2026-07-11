# Decompose

Materialize one level of the delivery hierarchy: turn a plan into real artifacts. Point it at the roadmap to create epics, or at an epic to create its stories and tasks.

## When to Use

- User says "decompose", "break down the roadmap", "break this epic into stories", "materialize the epics"
- A roadmap lists epics that do not exist yet, or an epic needs its stories and tasks created
- Not for organizing the flow (that is [roadmap.md](roadmap.md)) or for a single artifact (create it directly via its ref)

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Identify the level

- **From the roadmap** (`docs/ROADMAP.md`): the parent is the roadmap; the children are epics, each created via [epic.md](epic.md).
- **From an epic** (`.artifacts/epics/{epic-name}/epic.md` or its tracker entity): the parent is the epic; the children are stories (via [story.md](story.md)) and tasks (via [task.md](task.md)).

Read the parent for context only — **translate, don't replicate**: its tokens never cross verbatim into a child.

Epics do not reference the roadmap. The roadmap references epics; the epics carry their own provenance (PRD, PRODUCT, Design Doc) in `## References` and frontmatter `sources:`.

### 2. Propose the set

From the parent, propose the children:

- **From the roadmap** — the epics it lists, in the order they appear. Respect phase grouping and use roadmap tags (`foundation`, `validation`, `high-risk`, `external-dependency`) as signals only — they inform priority or caution, but never alter the epic template.
- **From an epic** — candidate stories (user-value slices) and tasks (enabling work) implied by its scope and its stories checklist.

Each proposed child carries a one-line boundary: the capability it owns, and the adjacent capability it explicitly does not. Boundaries partition the parent's scope — where one child's slice ends, the neighbor's begins; work claimed by two children means the set is wrong, not the boundary.

Idempotent: check which children already exist and propose only the missing ones; never recreate or overwrite. Present the proposed set with its boundaries; let the user add, drop, merge, split, or rename. Settle the set and the boundaries before creating.

### 3. Propose ordering and blockers

When decomposing the roadmap, inspect the proposed epic sequence:

- Suggest `blocked_by` on epics that depend on earlier epics in the same or previous phases.
- Surface roadmap tags that indicate risk or external dependency so the user can confirm order.

When decomposing an epic into stories:

- Order stories so that foundational outcomes come before dependent ones.
- Suggest `blocked_by` when one story's outcome is a precondition for another.

Blockers are suggestions; the user confirms or adjusts them before creation.

### 4. Coverage check

When decomposing an epic into stories, read the epic's `## Requirements` (the PRD requirement IDs it owns: `FR/BR/EC/NFR`).

For each requirement ID, ensure at least one proposed story has an acceptance criterion that links back to it via a `**Satisfies**` line. If a requirement ID is not covered, flag it and ask the user to add a story or confirm the omission. `ADR-NNN` is a decision dependency, not a requirement — it belongs in `## References`, not in coverage.

Stories operationalize requirements; tasks do not carry `Satisfies` lines because they deliver no user-visible outcome.

### 5. Story vs task discrimination

Use [discriminator.md](discriminator.md) when the type is unclear. Default rule:

- **Story:** delivers demonstrable user-visible value. Has acceptance criteria and may carry `Satisfies` lines.
- **Task:** enabling work with no demonstrable user outcome (setup, spike, migration, configuration, plumbing). No `Satisfies` line.

### 6. Granularity gate

Before creating, check that no proposed story is too large:

- More than 3–5 acceptance criteria, or
- Touches multiple unrelated domains, or
- Its summary cannot state a single outcome

When any of these are true, propose splitting the story. Respect the user's decision if they prefer to keep it whole.

### 7. Create each child

For each confirmed child, run its create ref — [epic.md](epic.md), [story.md](story.md), or [task.md](task.md). Each child is drafted to its own canonical template and validated by its own flow (a story's AC through ac-validation). The settled boundary travels into the child: its "does not" half lands in the child's Out of Scope, stated in the child's own terms — never naming the sibling that owns the excluded work. Decompose never bypasses the create ref — no auto-generated, unvalidated artifacts.

Sync is inherited, not added here: each create ref carries its own save-or-push, governed by `epic-tracker.kind` (see [sync.md](sync.md)). Decompose performs no sync of its own.

### 8. Re-run / orphan check

When decomposing a parent that was already decomposed before, identify existing children that no longer fit the parent's current scope or sequence. Do not delete automatically. Surface them as orphans and ask whether to archive, reparent, or keep them.

## Guidelines

- Materialize one level per run — roadmap → epics, or epic → stories and tasks
- Propose from the parent, confirm with the user, create via the child's create ref
- Settle boundaries with the set — every child states what it owns and what it does not before any child is created; the boundary becomes its Out of Scope
- Idempotent: create only the missing children; never recreate or overwrite
- Delegate every artifact to its create ref — canonical shape and validation are non-negotiable
- Route cross-cutting concerns by domain, not by order — a foundational decision spanning stories, and a domain-specific trap, each belong to the artifact that owns them, never parked on whichever story is created first
- Offer to go deeper (a created epic → its stories) but never auto-create the next level
- Respect roadmap order and tags when creating epics; suggest `blocked_by` for dependencies
- Ensure every PRD requirement ID in the epic is covered by a story's `Satisfies` line, or explicitly confirm the omission
- Split oversized stories before creating, or record the user's decision to keep them whole
- Surface orphaned children on re-run rather than deleting them

## Error Handling

- Roadmap absent when decomposing the roadmap: route to [roadmap.md](roadmap.md) to organize the flow first, or create epics directly via [epic.md](epic.md)
- Epic has no scope or stories checklist to imply children: ask the user to outline the stories, or derive candidates from the epic's scope and confirm before creating
- A child name conflicts with an existing artifact: defer to the create ref's conflict handling (suggest an alternative or confirm overwrite)
- Requirement coverage gap: flag the uncovered PRD requirement IDs and ask the user to add a story or confirm the omission
