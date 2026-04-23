---
name: epic-tracker
description: >-
  Manage the delivery lifecycle from epic planning through story tracking
  to implementation handoff. 4 artifact types (Epic, Story, Bug, Release).
  Use when planning epics, creating stories, reporting bugs, tracking
  delivery status, or preparing handoff to spec-driven.
when_to_use: >-
  Triggers on "create epic", "new epic", "create story", "new story",
  "add story", "report bug", "bug report", "create release", "new release",
  "update status", "mark done", "show roadmap", "list epics", "epic status",
  "handoff to spec-driven". Not for implementing a named story with an
  existing spec (use spec-driven "implement story S###"), project-wide
  overview (use project-index), or feature status within a spec (use
  spec-driven "show feature status").
---

# Epic Tracker

Manage the delivery lifecycle with markdown artifacts. Plan epics, track
stories, report bugs, group releases, and hand off to spec-driven.

## Workflow

```
discover --> create --> track --> handoff
```

Discover checks for existing docs (PRD, brief). Create generates the
artifact. Track updates status in frontmatter. Handoff suggests
spec-driven or tracker sync as next steps.

## Context Loading Strategy

Load only the reference matching the current trigger. Never load multiple
references simultaneously unless explicitly noted.

**Base load:**
- Current epic folder contents (when working within an epic)

**On-demand:**
- `.artifacts/docs/prd.md` (discover phase, if exists)
- `.artifacts/docs/brief.md` (discover phase, if exists)

**Never simultaneous:**
- Multiple epic folders
- Reference files for different artifact types

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Create epic, new epic | [epic.md](references/epic.md) |
| Create story, new story, add story | [story.md](references/story.md) |
| Create bug, report bug, bug report | [bug.md](references/bug.md) |
| Create release, new release | [release.md](references/release.md) |
| Status, update status, mark done | [status.md](references/status.md) |
| Show roadmap, list epics, overview | [status.md](references/status.md) |
| Handoff, implement story, start story | [handoff.md](references/handoff.md) |

Notes:

- `status.md` covers both status updates and overview reads.
- `handoff.md` suggests spec-driven or tracker sync -- it does not
  auto-trigger other skills.

## Cross-References

```
docs-writer -------> epic-tracker  (PRD/brief feed epic discovery)
epic.md -----------> story.md      (epic contains stories)
epic.md -----------> bug.md        (bugs can belong to an epic)
story.md ----------> handoff.md    (story hands off to spec-driven)
bug.md ------------> handoff.md    (bug hands off to spec-driven)
release.md --------> status.md     (release groups stories by status)
epic-tracker ------> spec-driven   (handoff feeds implementation)
```

## Guidelines

**DO:**
- Check for existing PRD/brief before creating an epic (discover phase)
- Use status in frontmatter for all artifacts (planned, in-progress, done, blocked)
- Keep each file to a single artifact type in its proper folder
- Use kebab-case for all artifact and folder names
- Present the artifact for user review before saving
- Suggest spec-driven as the next step; let the user invoke it
- Structure artifacts so a future tracker sync stays possible
- Read artifacts directly when composing an overview; sizing stays with spec-driven

**DON'T:**
- Skip the discover phase (contrasts: check for existing PRD/brief first)
- Auto-trigger spec-driven (contrasts: suggest, let user invoke)
- Implement tracker sync now (contrasts: structure for future compatibility)
- Create an index file or add size fields (contrasts: read artifacts directly; spec-driven handles sizing)
- Mix artifact types in a single file (contrasts: single type per file in its folder)

## Output

All artifacts save to `.artifacts/epics/`. Create the directory structure
as needed.

```
.artifacts/epics/
├── epic-name/
│   ├── epic.md
│   ├── story-name.md
│   └── bug-name.md
├── standalone/
│   └── bug-name.md
└── releases/
    └── release-name.md
```

| Type | Location |
|------|----------|
| Epic | `.artifacts/epics/{epic-name}/epic.md` |
| Story | `.artifacts/epics/{epic-name}/{story-name}.md` |
| Bug (with epic) | `.artifacts/epics/{epic-name}/{bug-name}.md` |
| Bug (standalone) | `.artifacts/epics/standalone/{bug-name}.md` |
| Release | `.artifacts/epics/releases/{release-name}.md` |

## Error Handling

- No `.artifacts/epics/`: create the directory
- Epic not found: list available epics
- Ambiguous trigger: ask which artifact type to create
- Story without epic: ask which epic it belongs to or create one
- Bug without epic: place in standalone/
- Conflicting status update: show current status, ask for confirmation
- PRD/brief not found during discover: ask user for context directly
