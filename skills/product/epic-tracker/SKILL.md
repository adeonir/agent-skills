---
name: epic-tracker
description: >-
  Manages the delivery lifecycle from roadmap and epic planning through story
  tracking, across 5 artifact types (Epic, Story, Bug, Task, Release) plus a
  roadmap. Use when creating or editing an epic, story, task, bug,
  release, or roadmap; decomposing a
  roadmap into epics or an epic into stories; updating or listing delivery status; or
  syncing artifacts to or from Linear or GitHub. Not for implementing a named
  story with an existing spec, project-wide overview, feature status within a
  spec, or quick fixes.
---

# Epic Tracker

Manages the delivery lifecycle with tracker-first integration and
markdown fallback. Plan epics, track stories, report bugs, file tasks,
group releases, and push to a tracker (via MCP or CLI) when configured.

## Triggers

- **Epic** ("create epic", "new epic") → [epic.md](references/epic.md)
- **Roadmap** ("create roadmap", "plan the roadmap", "organize epics",
  "roadmap the PRD") → [roadmap.md](references/roadmap.md)
- **Decompose** ("decompose", "break down the roadmap", "break this epic
  into stories", "materialize the epics") →
  [decompose.md](references/decompose.md)
- **Story** ("create story", "new story", "add story", "edit story",
  "update story", "change story") → [story.md](references/story.md)
- **Bug** ("create bug", "report bug", "bug report") →
  [bug.md](references/bug.md)
- **Task / Chore** ("create task", "new task", "add task",
  "create chore") → [task.md](references/task.md)
- **Release** ("create release", "new release") →
  [release.md](references/release.md)
- **Sync** ("sync to tracker", "push to linear/github", "pull from
  tracker", "configure tracker") → [sync.md](references/sync.md)
- **Linear adapter** (auto-loaded by sync) →
  [adapter-linear.md](references/adapter-linear.md)
- **GitHub adapter** (auto-loaded by sync) →
  [adapter-github.md](references/adapter-github.md)

`epic.md` opens with context discovery — reads `docs/product/PRD.md`,
`docs/ROADMAP.md`, and `docs/product/PRODUCT.md` before
prompting; falls back to direct questions when none exist.

`roadmap.md` organizes the project's epics into an ordered flow derived
from the PRD and writes the living plan to `docs/ROADMAP.md` (committed,
local — no tracker mirror); it does not create epics. `decompose.md`
materializes a level: point it at the roadmap to create its epics, or at
an epic to create its stories and tasks — composing `epic.md`, `story.md`,
and `task.md` and staying idempotent.

`sync.md` is also auto-loaded by core refs (epic, story, task, bug, release)
after the artifact is saved when `epic-tracker.kind` is set and not `none`.

`adapter-{linear,github}.md` are loaded by `sync.md` based on
`epic-tracker.kind`. Not direct triggers.

`ac-validation.md` is auto-loaded by `story.md` on create and on edits
that change AC text. Not a direct trigger.

`discriminator.md` owns the Bug/Story/Task type rule — loaded when a trigger
does not name the type, and referenced by the create refs on type disputes.
Not a direct trigger.

## Workflow

```text
discover → create → sync*
                    ^__|  (sync is optional, gated by config)
```

Tracker-first when configured — artifacts go directly to the tracker.
Falls back to markdown when not. Status and overview happen directly — on
the tracker when configured, else the markdown files; no dedicated ref.

## Guidelines

- Use kebab-case for all artifact and folder names
- Keep each file to a single artifact type in its proper folder
- Save or push immediately after the draft step — no separate preview gate
- Route tracker operations through `sync.md` — core artifact refs stay
  tracker-agnostic
- Validate Story AC against ac-validation rules V1-V9 on create and on
  edits that change AC text
- Capture cross-artifact order with `blocked_by`; sync maps it to the
  tracker's native dependency relation
- Decompose the roadmap into its epics (or an epic into its stories and
  tasks) with `decompose.md`
- Delegate sizing to the implementation phase
- Status values: `planned`, `in-progress`, `done`, `blocked` (releases use `released`)
- Create and edit both conform the artifact to its canonical template — structure and MUST-NOT boundaries hold either way, never a free-form write

## Anti-Pattern: Tracker Operations in Core Refs

Embedding `gh issue create` or Linear MCP calls inside `epic.md`,
`story.md`, etc. couples each ref to a specific tracker. Route tracker
operations through `sync.md` instead — core refs build the artifact, sync
dispatches to the right adapter. Adding a new tracker becomes a new
adapter, not a rewrite of every artifact ref.

## Anti-Pattern: AC Validation on Reads

Validating Acceptance Criteria during pull or status reads breaks
legacy artifacts that predate the Given/When/Then enforcement. Validate
on **write paths only** — story create and edit-when-AC-text-changes —
and let read paths tolerate legacy AC. The implementation consumer
decides how to handle non-conforming AC.

## Anti-Pattern: Mixed Artifact Files

A single file holding both a story and the bugs it spawned, or an epic
mixed with its release plan, makes status updates and tracker pushes
ambiguous. One file = one artifact type. Bugs go to their own file (in
the epic folder or `standalone/`); releases go to `releases/`.
