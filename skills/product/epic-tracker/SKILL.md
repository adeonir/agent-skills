---
name: epic-tracker
description: "Roadmap and delivery artifact management in Linear or GitHub. Use when creating, editing, decomposing, moving, or updating roadmaps, epics, stories, bugs, or tasks, including sizing an explicit feature PRD or RFC into an epic, a standalone story, or a standalone task. Not for implementing a named story, feature documents, project overviews, or quick fixes."
---

# Epic Tracker

Manages the delivery lifecycle in an external tracker. Plan epics, track stories, report bugs, and file tasks — every artifact lives in Linear or GitHub, which is the single source of truth.

## Triggers

- **Feature source** ("create from this RFC", "create from this feature PRD", "turn this RFC into issues", "track this feature") → [feature.md](instructions/feature.md)
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
    ├ decompose (optional): derives the plan from the project PRD
    └ feature (optional): sizes a feature PRD/RFC, picks the ref
```

Every artifact takes the same path: a create ref drafts it and dispatches it to the tracker. The plan usually comes from the user directly. Two optional ceremonies sit in front. `decompose` derives the plan from the project PRD, records it in the roadmap, and confirms before materializing; a declined checkpoint leaves the roadmap written and nothing created. `feature` sizes a feature PRD or RFC into an epic, a standalone story, or a standalone task, and writes no roadmap. A tracker is required: without one configured, the bootstrap runs first and nothing is created until it completes.
