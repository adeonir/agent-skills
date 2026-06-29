---
name: epic-tracker
description: >-
  Manages the delivery lifecycle from milestone and epic planning through
  story tracking to implementation handoff. 5 artifact types (Epic, Story, Bug,
  Task, Release) plus a milestones registry. Tracker-first when configured (Linear, GitHub
  Issues/Projects) via MCP or CLI — artifacts go directly to the
  tracker with no local files. Falls back to markdown as source of
  truth when no tracker is configured. Triggers: "create epic", "new
  epic", "create story", "new story", "edit story", "create task",
  "report bug", "create release", "create milestone", "decompose milestone",
  "update status", "list epics", "sync to tracker", "push to linear",
  "push to github",
  "pull from tracker", "configure tracker", "handoff".
  Not for implementing a named story with an existing spec, project-
  wide overview, feature status within a spec, or quick fixes.
---

# Epic Tracker

Manages the delivery lifecycle with tracker-first integration and
markdown fallback. Plan epics, track stories, report bugs, file tasks,
group releases, push to a tracker (via MCP or CLI) when configured, and
hand off to implementation.

## Workflow

```
discover → create → sync* → track → handoff
                          ^_______|  (sync is optional, gated by config)
```

Tracker-first when configured — artifacts go directly to the tracker.
Falls back to markdown when not.

## Triggers

- **Epic** ("create epic", "new epic") → [epic.md](references/epic.md)
- **Milestone** ("create milestone", "define milestone", "plan
  milestones") → [milestone.md](references/milestone.md)
- **Decompose** ("decompose milestone", "break down milestone", "create
  epics from a milestone") → [decompose.md](references/decompose.md)
- **Story** ("create story", "new story", "add story") →
  [story.md](references/story.md)
- **Edit Story** ("edit story", "update story body", "change story") →
  [update-story.md](references/update-story.md)
- **Bug** ("create bug", "report bug", "bug report") →
  [bug.md](references/bug.md)
- **Task / Chore** ("create task", "new task", "add task",
  "create chore") → [task.md](references/task.md)
- **Release** ("create release", "new release") →
  [release.md](references/release.md)
- **Status** ("status", "update status", "mark done", "list epics",
  "overview") → [status.md](references/status.md)
- **Sync** ("sync to tracker", "push to linear/github", "pull from
  tracker", "configure tracker") → [sync.md](references/sync.md)
- **Handoff** ("handoff", "implement story", "start story") →
  [handoff.md](references/handoff.md)
- **Linear adapter** (auto-loaded by sync) →
  [adapters/linear.md](references/adapters/linear.md)
- **GitHub adapter** (auto-loaded by sync) →
  [adapters/github.md](references/adapters/github.md)

`epic.md` opens with context discovery — reads `docs/product/prd.md`,
`.artifacts/epics/milestones.md`, and `docs/product/PRODUCT.md` before
prompting; falls back to direct questions when none exist.

`milestone.md` records delivery phases in the registry
(`.artifacts/epics/milestones.md`); `decompose.md` reads a chosen milestone
from that registry and creates its epic set, composing `epic.md` (and
optionally `story.md`); the epics it creates carry a `milestone:` pointer to
their parent.

`status.md` covers status updates and the delivery overview.

`sync.md` is also auto-loaded by core refs (epic, story, bug, release)
after the artifact is saved when `epic-tracker.kind` is set and not `none`.

`adapters/{linear,github}.md` are loaded by `sync.md` based on
`epic-tracker.kind`. Not direct triggers.

`ac-validation.md` is auto-loaded by `story.md` (create) and
`update-story.md` (when AC text changes). Not a direct trigger.

## Guidelines

- Use kebab-case for all artifact and folder names
- Keep each file to a single artifact type in its proper folder
- Save or push immediately after the draft step — no separate preview gate
- Route tracker operations through `sync.md` — core artifact refs stay
  tracker-agnostic
- Validate Story AC against ac-validation rules V1-V7 on create and on
  edits that change AC text
- Capture cross-artifact order with `blocked_by`; sync maps it to the
  tracker's native dependency relation
- Decompose a milestone into its epics with `decompose.md`; record the
  `milestone:` parent pointer on each epic
- Delegate sizing to the implementation phase

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
