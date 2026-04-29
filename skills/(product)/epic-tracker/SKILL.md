---
name: epic-tracker
description: >-
  Manage the delivery lifecycle from epic planning through story tracking
  to implementation handoff. 4 artifact types (Epic, Story, Bug, Release).
  Authors markdown locally; pushes to external tracker (Linear, GitHub
  Issues/Projects, Jira) when MCP is available. Falls back to markdown as
  source of truth when no tracker is configured.
when_to_use: >-
  Triggers on "create epic", "new epic", "create story", "new story",
  "add story", "report bug", "bug report", "create release", "new release",
  "update status", "mark done", "show roadmap", "list epics", "epic status",
  "sync to tracker", "push to linear", "push to github", "push to jira",
  "pull from tracker", "configure tracker", "handoff to spec-driven". Not
  for implementing a named story with an existing spec (use spec-driven
  "implement story S###"), project-wide overview (use project-index), or
  feature status within a spec (use spec-driven "show feature status").
---

# Epic Tracker

Manage the delivery lifecycle with markdown artifacts and optional tracker
integration. Plan epics, track stories, report bugs, group releases, push
to a tracker when MCP is configured, and hand off to spec-driven.

## Workflow

```
discover --> create --> sync* --> track --> handoff
                          ^_______|  (sync is optional, gated by config)
```

Discover checks for existing docs (PRD, brief). Create generates the
artifact in markdown. Sync (optional) pushes to the configured tracker
when an MCP is available; user is asked once per session whether to push.
Track updates status -- in the tracker when configured, in markdown
frontmatter when not. Handoff suggests spec-driven and surfaces tracker
URLs.

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
epic.md -----------> sync.md           (push after save when tracker configured)
story.md ----------> sync.md           (push after save when tracker configured)
bug.md ------------> sync.md           (push after save when tracker configured)
release.md --------> sync.md           (push after save when tracker configured)
release.md --------> status.md         (release groups stories by status)
sync.md -----------> adapters/linear   (when tracker.kind = linear)
sync.md -----------> adapters/github   (when tracker.kind = github-issues or github-projects)
sync.md -----------> adapters/jira     (when tracker.kind = jira)
status.md ---------> sync.md           (overview reads from tracker when configured)
story.md ----------> handoff.md        (story hands off to spec-driven)
bug.md ------------> handoff.md        (bug hands off to spec-driven)
epic-tracker ------> spec-driven       (handoff feeds implementation)
```

## Tracker Integration

Optional and adaptive. When the user has an MCP for a supported tracker
installed, the skill can push markdown artifacts to that tracker and pull
state back. When no MCP is available, markdown stays the source of truth
(current behavior).

Supported trackers and primitive mapping:

| Artifact | Linear | GitHub Issues | GitHub Projects | Jira |
|----------|--------|---------------|-----------------|------|
| Epic     | Project | Milestone | Issue parent (with sub-issues) | Epic |
| Story    | Issue | Issue | Sub-issue | Story |
| Bug      | Issue + label `bug` | Issue + label `bug` | Sub-issue + label `bug` | Bug |
| Release  | Cycle | Release tag | Release tag | Fix Version |

Release uses the closest native primitive each tracker offers; no forced
single concept across trackers.

Config lives at `.artifacts/epics/.config.yml`. First operation that needs
a tracker triggers bootstrap: detect available MCPs, ask user, persist.
Push is asked per session (cached after first ask).

## Guidelines

**DO:**
- Check for existing PRD/brief before creating an epic (discover phase)
- Use status in frontmatter for all artifacts (planned, in-progress, done, blocked) when no tracker is configured
- When tracker is configured, treat tracker as source of truth for status; markdown frontmatter `status` becomes a cache updated on pull
- Keep each file to a single artifact type in its proper folder
- Use kebab-case for all artifact and folder names
- Present the artifact for user review before saving
- After save, ask user once per session whether to push to tracker (cache the answer)
- Suggest spec-driven as the next step; let the user invoke it
- When pulling from tracker, warn the user about any divergence (status, title, body) before resolving
- Read from tracker when composing overview if configured; markdown when not
- Sizing stays with spec-driven

**DON'T:**
- Skip the discover phase (contrasts: check for existing PRD/brief first)
- Auto-trigger spec-driven (contrasts: suggest, let user invoke)
- Push to tracker without asking (contrasts: ask once per session, cache choice)
- Auto-resolve conflicts silently (contrasts: warn user about divergence in pull, default tracker wins, allow override)
- Hardcode tracker primitives in core refs (contrasts: core refs stay tracker-agnostic; adapters own tracker mapping)
- Create an index file or add size fields (contrasts: read artifacts/tracker directly; spec-driven handles sizing)
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
