# Create Release

Group stories from one or more epics into a cross-cutting delivery slice.

## When to Use

- User wants to plan what ships together
- User says "create release", "new release"
- Multiple stories across epics need to be grouped for a delivery

## Workflow

### 1. Discover

1. Scan `.artifacts/epics/` for existing epics and their stories
2. List stories by status to help the user choose what to include
3. If no stories exist, suggest creating epics and stories first

### 2. Draft

**USE TEMPLATE:** `templates/release.md`

Fill the template:

- **Name**: kebab-case, descriptive (`mvp-launch`, `billing-v2`,
  `q2-release`)
- **Title**: human-readable release title
- **Status**: always starts as `planned` (planned, in-progress,
  released)
- **Prose context**: what this release delivers, why these stories
  were grouped, who benefits
- **Stories**: checklist with `epic-name/story-name` prefix for each
  included story. Can also include entire epics.
- **Release Criteria**: conditions that must be met before shipping
  (not acceptance criteria -- those live on stories)
- **References**: changelog links, milestone links

### 3. Review

Present the draft to the user. Wait for feedback before saving.

### 4. Save

Save to `.artifacts/epics/releases/{release-name}.md`. Create the
directory if it doesn't exist.

### 5. Sync to tracker (optional)

If `.artifacts/epics/.config.yml` exists with `tracker.kind` set and not
`none`, ask the user (per session, cached) whether to push this release to
the tracker. If yes, load [sync.md](sync.md) and dispatch to the matching
adapter; the adapter maps Release to the closest native primitive:

- Linear -> Cycle (sprint-style)
- GitHub Issues / Projects -> Release tag
- Jira -> Fix Version

The adapter also links included stories/bugs to the release primitive
(e.g., setting `cycle` on Linear Issues, `fixVersions` on Jira Issues,
listing Issues in the GitHub Release notes).

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

If `tracker.kind: none` or no matching MCP is available, skip silently --
markdown stays the source of truth.

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

## Error Handling

- No stories exist: suggest creating epics and stories first
- Some stories are blocked: flag them, ask if the release should
  proceed without them
- Release name conflicts: suggest alternative or confirm overwrite
