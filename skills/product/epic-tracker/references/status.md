# Status and Overview

Update artifact status or show a delivery overview by reading all
artifacts in `.artifacts/epics/`.

## When to Use

- User says "status", "update status", "mark done"
- User says "list epics", "overview"
- User wants to see delivery progress at a glance

## Status Updates

### Valid Statuses

| Artifact | Statuses |
|----------|----------|
| Epic | planned, in-progress, done, blocked |
| Story | planned, in-progress, done, blocked |
| Bug | planned, in-progress, done, blocked |
| Release | planned, in-progress, released |

### Status Transitions

```
planned → in-progress → done
planned → blocked → in-progress → done
```

Releases use `released` instead of `done`.

### Update Process

1. Identify the artifact to update (ask if ambiguous)
2. Read the current frontmatter
3. Detect tracker integration:
   - If `tracker.id` is present in the artifact's frontmatter, the tracker is the source of truth -- delegate to [sync.md](sync.md) which dispatches to the matching adapter to update the tracker; on success, update the local frontmatter `status` and `tracker.last_synced` as a cache
   - Otherwise, update the `status` field directly in markdown frontmatter
4. Save the file
5. If marking a story as "done", check if the parent epic's stories
   are all done -- if so, suggest marking the epic as done too

## Overview

### Reading Artifacts

Source depends on tracker config:

**Without tracker (or `epic-tracker.kind: none`):** read markdown directly.

1. List directories in `.artifacts/epics/`
2. For each epic directory, read `epic.md` frontmatter (status, title)
3. List story and bug files, read their frontmatter
4. Read `.artifacts/epics/standalone/` for standalone bugs
5. Read `.artifacts/epics/releases/` for releases

**With tracker configured:** delegate to [sync.md](sync.md) `list_artifacts`
which fetches current state from the tracker. Use markdown only as a cache
when the tracker MCP is unavailable; warn the user that the view is stale.

### Display Format

Present as a structured summary:

```
## Epic: {title} [{status}] (2/4 stories done)
  - [x] story-name (done)
  - [x] story-name (done)
  - [ ] story-name (in-progress)
  - [ ] story-name (planned, blocked by other-epic/api-story)
  - [ ] bug-name [bug] (planned)

## Standalone Bugs
  - [ ] bug-name (planned)

## Releases
  - release-name (planned): 3/5 stories done
```

Use checkmarks for done, empty boxes for other statuses. Always show
completion ratio for epics (`N/M stories done`) and releases. When an
artifact lists `blocked_by`, append `blocked by {paths}` so the reader
sees what gates it.

## Guidelines

**DO:**
- Always read current status before updating
- Detect `tracker.id` in frontmatter to decide source of truth (tracker vs markdown)
- Delegate to `sync.md` for tracker reads/writes; never call MCPs directly from this ref
- Suggest cascading updates (all stories done -> suggest epic done)
- Show completion ratios for epics and releases
- Surface unmet `blocked_by` dependencies in the overview so the reader
  knows what is gated
- Group output by epic for readability
- Warn the user when overview falls back to markdown cache because tracker MCP is unavailable

**DON'T:**
- Auto-update parent status -- always suggest, let user confirm
- Show file paths in the overview -- use names and titles
- Skip standalone bugs in the overview
- Update status without user confirmation
- Read or write the tracker directly -- delegate to `sync.md`

## Error Handling

- No artifacts found: suggest creating an epic first
- Invalid status transition (e.g., done -> planned): warn the user,
  allow if they confirm
- Artifact file is malformed: report the issue, suggest manual fix
