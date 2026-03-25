# Status and Overview

Update artifact status or show a delivery overview by reading all
artifacts in `.artifacts/epics/`.

## When to Use

- User says "status", "update status", "mark done"
- User says "show roadmap", "list epics", "overview"
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
planned --> in-progress --> done
planned --> blocked --> in-progress --> done
```

Releases use `released` instead of `done`.

### Update Process

1. Identify the artifact to update (ask if ambiguous)
2. Read the current frontmatter
3. Update the `status` field
4. Save the file
5. If marking a story as "done", check if the parent epic's stories
   are all done -- if so, suggest marking the epic as done too

## Overview

### Reading Artifacts

No index file. Read all artifacts directly:

1. List directories in `.artifacts/epics/`
2. For each epic directory, read `epic.md` frontmatter (status, title)
3. List story and bug files, read their frontmatter
4. Read `.artifacts/epics/standalone/` for standalone bugs
5. Read `.artifacts/epics/releases/` for releases

### Display Format

Present as a structured summary:

```
## Epic: {title} [{status}] (2/4 stories done)
  - [x] story-name (done)
  - [x] story-name (done)
  - [ ] story-name (in-progress)
  - [ ] bug-name [bug] (planned)

## Standalone Bugs
  - [ ] bug-name (planned)

## Releases
  - release-name (planned): 3/5 stories done
```

Use checkmarks for done, empty boxes for other statuses. Always show
completion ratio for epics (`N/M stories done`) and releases.

## Guidelines

**DO:**
- Always read current status before updating
- Suggest cascading updates (all stories done -> suggest epic done)
- Show completion ratios for epics and releases
- Group output by epic for readability

**DON'T:**
- Auto-update parent status -- always suggest, let user confirm
- Show file paths in the overview -- use names and titles
- Skip standalone bugs in the overview
- Update status without user confirmation

## Error Handling

- No artifacts found: suggest creating an epic first
- Invalid status transition (e.g., done -> planned): warn the user,
  allow if they confirm
- Artifact file is malformed: report the issue, suggest manual fix
