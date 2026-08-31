---
name: epic-tracker
description: "Roadmap and delivery artifact management in Linear or GitHub. Use when creating, editing, decomposing, moving, or updating roadmaps, epics, stories, bugs, or tasks. Not for implementing a named story, feature status in a spec, project overviews, or quick fixes."
---

# Epic Tracker

Manages the delivery lifecycle in an external tracker. Plan epics, track stories, report bugs, and file tasks — every artifact lives in Linear or GitHub, which is the single source of truth.

## Triggers

- **Plan / decompose** ("create roadmap", "plan the roadmap", "organize epics", "roadmap the PRD", "decompose", "break down the roadmap", "break this epic into stories", "materialize the epics") → [decompose.md](instructions/decompose.md)
- **Epic** ("create epic", "new epic", "edit epic") → [epic.md](instructions/epic.md)
- **Story** ("create story", "new story", "add story", "edit story", "update story", "change story") → [story.md](instructions/story.md)
- **Bug** ("create bug", "report bug", "bug report", "edit bug") → [bug.md](instructions/bug.md)
- **Task / Chore** ("create task", "new task", "add task", "create chore", "edit task") → [task.md](instructions/task.md)
- **Status / overview** ("mark done", "cancel this", "won't fix", "list epics", "what's in progress", "update status") → [sync.md](instructions/sync.md)
- **Reparent** ("move this to epic X", "reparent this story", "change the parent epic") → [sync.md](instructions/sync.md)
- **Dependencies** ("block this on X", "unblock this", "this depends on X") → [sync.md](instructions/sync.md)
- **Configure tracker** ("configure tracker") → [sync.md](instructions/sync.md)

## Workflow

```text
create ref → tracker → the tracker      every artifact takes this path
    ↑
    ├ user brings the plan               the usual input
    └ decompose (optional): derives the plan from a PRD, feeds the ref
```

Every artifact takes the same path: a create ref drafts it and dispatches it to the tracker. The plan usually comes from the user directly. `decompose` is the optional ceremony in front — it derives the plan from a PRD, records it in the roadmap, and confirms before materializing; a declined checkpoint leaves the roadmap written and nothing created. A tracker is required: without one configured, the bootstrap runs first and nothing is created until it completes.
