---
name: epic-tracker
description: >-
  Manage the delivery lifecycle from epic planning through story tracking
  to implementation handoff. 5 artifact types (Epic, Story, Bug, Issue,
  Release). Tracker-first when configured (Linear, GitHub Issues/Projects,
  Jira) via MCP or CLI — artifacts go directly to the tracker with no local
  files. Falls back to markdown as source of truth when no tracker is
  configured.
when_to_use: >-
  Triggers on "create epic", "new epic", "create story", "new story",
  "add story", "create issue", "new issue", "add issue", "report bug",
  "bug report", "create release", "new release", "update status", "mark
  done", "show roadmap", "list epics", "epic status", "sync to tracker",
  "push to linear", "push to github", "push to jira", "pull from tracker",
  "configure tracker", "handoff to spec-driven". Not for implementing a
  named story with an existing spec (use spec-driven "implement story
  S###"), project-wide overview (use project-index), feature status
  within a spec (use spec-driven "show feature status"), or quick fixes
  and small changes (use spec-driven "quick task", "quick fix").
---

# Epic Tracker

Manage the delivery lifecycle with tracker-first integration and markdown
fallback. Plan epics, track stories, report bugs, file issues, group
releases, push to a tracker (via MCP or CLI) when configured, and hand
off to spec-driven.

## Workflow

```
discover --> create --> sync* --> track --> handoff
                          ^_______|  (sync is optional, gated by config)
```

Tracker-first when configured — artifacts go directly to the tracker;
falls back to markdown when not.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Create epic, new epic | [epic.md](references/epic.md) |
| Create story, new story, add story | [story.md](references/story.md) |
| Create bug, report bug, bug report | [bug.md](references/bug.md) |
| Create issue, new issue, add issue, create chore, create task, add task | [issue.md](references/issue.md) |
| Create release, new release | [release.md](references/release.md) |
| Status, update status, mark done | [status.md](references/status.md) |
| Show roadmap, list epics, overview | [status.md](references/status.md) |
| Sync to tracker, push to linear, push to github, push to jira, pull from tracker, configure tracker | [sync.md](references/sync.md) |
| Handoff, implement story, start story | [handoff.md](references/handoff.md) |

Notes:

- `status.md` covers both status updates and overview reads.
- `handoff.md` suggests spec-driven and surfaces tracker URLs -- it does not
  auto-trigger other skills.
- `sync.md` is also auto-loaded by core refs (epic, story, bug, release)
  after the artifact is saved when tracker config is present and `kind`
  is not `none`.
- `adapters/{linear,github,jira}.md` are not direct triggers. They are
  loaded by `sync.md` based on `tracker.kind` from config.

## Cross-References

```
docs-writer -------> epic-tracker      (PRD/brief feed epic discovery)
epic.md -----------> story.md          (epic contains stories)
epic.md -----------> bug.md            (bugs can belong to an epic)
epic.md -----------> issue.md          (issues can belong to an epic)
epic.md -----------> sync.md           (push on create when tracker configured)
story.md ----------> sync.md           (push on create when tracker configured)
bug.md ------------> sync.md           (push on create when tracker configured)
issue.md ----------> sync.md           (push on create when tracker configured)
release.md --------> sync.md           (push on create when tracker configured)
release.md --------> status.md         (release groups stories by status)
sync.md -----------> adapters/linear   (when tracker.kind = linear)
sync.md -----------> adapters/github   (when tracker.kind = github-issues or github-projects)
sync.md -----------> adapters/jira     (when tracker.kind = jira)
status.md ---------> sync.md           (overview reads from tracker when configured)
story.md ----------> handoff.md        (story hands off to spec-driven)
bug.md ------------> handoff.md        (bug hands off to spec-driven)
issue.md ----------> handoff.md        (issue can hand off to spec-driven)
epic-tracker ------> spec-driven       (handoff feeds implementation)
```

## Guidelines

**DO:**
- Use kebab-case for all artifact and folder names
- Keep each file to a single artifact type in its proper folder
- Present the artifact for user review before saving or pushing
- Route tracker operations through `sync.md` — core artifact refs stay tracker-agnostic
- Delegate sizing to spec-driven

**DON'T:**
- Mix artifact types in a single file (contrasts: single type per file in its folder)
- Handle tracker push/pull directly in core refs (contrasts: route through sync.md)
- Create an index file or add size fields (contrasts: delegate sizing to spec-driven)

## Output

All artifacts save to `.artifacts/epics/`. Create the directory structure
as needed.

Markdown files are created only when no tracker is configured, or when
the user declines to push on a per-artifact basis.

```
.artifacts/epics/
├── epic-name/
│   ├── epic.md
│   ├── story-name.md
│   ├── bug-name.md
│   └── issue-name.md
├── standalone/
│   ├── bug-name.md
│   └── issue-name.md
└── releases/
    └── release-name.md
```

| Type | Location |
|------|----------|
| Epic | `.artifacts/epics/{epic-name}/epic.md` |
| Story | `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md` |
| Bug (with epic) | `.artifacts/epics/{epic-name}/{bug-name}.md` |
| Bug (standalone) | `.artifacts/epics/standalone/{bug-name}.md` |
| Issue (with epic) | `.artifacts/epics/{epic-name}/{issue-name}.md` |
| Issue (standalone) | `.artifacts/epics/standalone/{issue-name}.md` |
| Release | `.artifacts/epics/releases/{release-name}.md` |

## Error Handling

- No `.artifacts/epics/`: create the directory
- Epic not found: list available epics
- Ambiguous trigger: ask which artifact type to create
- Story without epic: ask which epic it belongs to or create one
- Bug without epic: place in standalone/
- Conflicting status update: show current status, ask for confirmation
- PRD/brief not found during discover: ask user for context directly
