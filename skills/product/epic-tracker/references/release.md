# Create Release

Group stories from one or more epics into a cross-cutting delivery slice.

## When to Use

- User wants to plan what ships together
- User says "create release", "new release"
- Multiple stories across epics need to be grouped for a delivery

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Discover

1. If tracker is configured, fetch story summaries via the sync.md
   `list_artifacts` operation; otherwise scan `.artifacts/epics/`
2. List stories by status to help the user choose what to include
3. If no stories exist, suggest creating epics and stories first

### 2. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive (`mvp-launch`, `billing-v2`,
  `q2-release`)
- **Title**: short human-readable release phrase, slug-safe. No
  commands, flags, file paths, parentheses, brackets, or pipes —
  becomes branch name slug downstream.
- **Status**: always starts as `planned` (planned, in-progress,
  released)
- **Prose context**: what this release delivers, why these stories
  were grouped, who benefits
- **Stories**: checklist with `epic-name/story-name` prefix for each
  included story. Can also include entire epics.
- **Release Criteria**: conditions that must be met before shipping
  (not acceptance criteria -- those live on stories)
- **References**: changelog links, milestone links

### 3. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  the adapter maps Release to the closest native primitive (Linear: Cycle,
  GitHub: Release tag, Jira: Fix Version) and links included stories/tasks/
  bugs to the release — no markdown file is created
- If no: save to `.artifacts/epics/releases/{release-name}.md`

**If no tracker configured** (config missing or `kind: none`):
- Save to `.artifacts/epics/releases/{release-name}.md`; create the
  directory if it doesn't exist

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

## Guidelines

**DO:**
- Reference stories with their full path (`epic-name/story-name`)
- Include release criteria that are verifiable pre-ship checks
- Group stories that deliver coherent user value together
- Show story statuses when listing candidates for the release

**DON'T:**
- Include stories that aren't tracked as artifacts yet
- Duplicate acceptance criteria from stories -- release criteria are
  about the release as a whole
- Create a release for a single story in a single epic (just track
  the epic)
- Mark a release as "released" if any included story is not "done"

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{release-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github | jira
#   id: PROJ-123  # Linear Cycle id, GitHub Release tag, or Jira Fix Version id
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Release Title}}

## Summary

{{What this release delivers, why these stories were grouped together, who benefits.}}

## Stories

- [ ] {{epic-name}}/{{story-name}} — {{brief description}}
- [ ] {{epic-name}}/{{story-name}} — {{brief description}}

## Release Criteria

- [ ] {{Condition that must be met before shipping}}
- [ ] {{Another pre-ship check}}

## References

- **Changelog:** {{link or "None"}}
- **Milestone:** {{link or "None"}}
````

## Error Handling

- No stories exist: suggest creating epics and stories first
- Some stories are blocked: flag them, ask if the release should
  proceed without them
- Release name conflicts: suggest alternative or confirm overwrite
