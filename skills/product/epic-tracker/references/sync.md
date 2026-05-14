# Sync

Orchestrate push and pull between markdown artifacts and an external
tracker. Detect the configured tracker, dispatch to the matching adapter,
surface conflicts, update frontmatter on success.

Conflict resolution and adapter dispatch deserve careful reasoning — a
wrong push can clobber tracker state that other people rely on.

## When to Use

- Direct trigger: "sync to tracker", "push to {linear,github,jira}", "pull from tracker", "configure tracker"
- Auto-loaded by core refs (epic, story, bug, release) after the artifact is saved when config has `tracker.kind != none`
- Auto-loaded by `status.md` to read overview state from the tracker when configured

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Primitive Mapping

| Artifact | Linear | GitHub | Jira |
|----------|--------|--------|------|
| Epic     | Project | Issue (parent) | Epic |
| Story    | Issue | Issue (sub-issue of Epic) | Story |
| Bug      | Issue + label `bug` | Issue (sub-issue of Epic/Story or standalone) | Bug |
| Issue    | Issue | Issue (sub-issue of Epic/Story or standalone) | Task |
| Release  | Cycle | Release tag | Fix Version |

GitHub uses sub-issues as the hierarchy primitive. Milestones and
Projects v2 are orthogonal opt-in layers (date grouping, custom
fields/views) — neither encodes Epic→Story. See
[adapters/github.md](adapters/github.md) for details.

Release uses the closest native primitive each tracker offers — no forced
single concept across trackers.

## Config

Path: `<project-root>/.artifacts/epics/.config.yml`

Schema:

```yaml
tracker:
  kind: linear | github | jira | none

  # Linear
  workspace: my-team

  # GitHub
  repo: owner/name
  project_number: 5          # optional — enables Projects v2 enrichment (boards, custom fields)
  use_milestones: true       # optional — enables Milestone field as date-bound grouping
  sub_issues: enabled | disabled  # detected during bootstrap; required for hierarchy
  issue_types:               # detected during bootstrap
    epic: Epic               # org-configured type names; empty object if org has none
    story: Story
    bug: Bug
    task: Task

  # Jira
  base_url: https://company.atlassian.net
  project_key: PROJ
```

When `kind: none`, the skill skips all tracker operations; markdown is the
sole source of truth.

## Bootstrap (first-time setup)

Runs when an operation requires a tracker but config is missing or
`kind` is unset.

1. Read `<project-root>/.artifacts/epics/.config.yml`. If valid, skip bootstrap.
2. Detect available integration methods for each tracker:
   - MCP: check if the tracker's MCP server is active in the session
   - CLI: check if the tracker's CLI is installed (`gh`, `linear`, `jira`)
   - MCP is always preferred; CLI is the fallback when MCP is missing
     or fails at runtime
3. Present detected options plus "none (markdown only)" to the user.
4. Ask the user to pick one.
5. Collect tracker-specific fields one question at a time:
   - Linear: workspace.
   - GitHub: repo (`owner/name`); optional `project_number` (Projects v2);
     optional `use_milestones` (Milestone field).
   - Jira: base_url, project_key.
6. For GitHub, probe whether the repo has the sub-issues feature
   available (`addSubIssue` on GraphQL). Store result as
   `sub_issues: enabled | disabled`. When disabled, warn the user that
   Stories will be standalone (no Epic→Story link) and ask whether to
   proceed or abort.
7. For GitHub, detect whether the org has custom Issue Types configured
   (Story, Bug, Task, Epic); store names under `issue_types` (empty
   object when none). See adapter for detection details and label
   fallback rules.
8. Write the config to `.artifacts/epics/.config.yml` including the
   integration method chosen (`via: mcp | cli`).

Bootstrap runs at most once per project. Re-run on demand by triggering
"configure tracker".

## Per-Session Cache

The push question ("push this to the tracker?") is asked once per session,
not per artifact. Cache the user's answer in memory:

- **always push**: subsequent creates push without re-asking
- **always ask**: re-ask on every create (default if user is unsure)
- **never push for this session**: skip pushes until next session

Cache is in-memory only. Next session resets to "always ask" unless the
user updates the cache mid-session.

## Push Direction (draft or markdown → tracker)

1. Read artifact content: use the draft data directly when invoked
   immediately after create (no markdown file exists); read from the saved
   markdown file when invoked standalone (e.g., "sync to tracker").
2. Validate config: `tracker.kind` must be set and not `none`. Otherwise
   fall back to markdown-only and inform the user.
3. Load the adapter matching `tracker.kind`:
   - `linear` → [adapters/linear.md](adapters/linear.md)
   - `github` → [adapters/github.md](adapters/github.md)
   - `jira` → [adapters/jira.md](adapters/jira.md)
4. Adapter creates or updates the entity. Always attempt MCP first; if
   MCP is unavailable or fails (auth, server down, tool missing), fall
   back to the tracker's CLI (`gh`, `linear`, `jira`). The `via` value
   stored at bootstrap is a preference, not a lock — runtime probing
   wins.
5. On success:
   - If a markdown file exists: patch its frontmatter with tracker info:
     ```yaml
     tracker:
       id: PROJ-123
       url: https://linear.app/.../PROJ-123
       last_synced: 2026-04-29T10:30:00Z
     ```
   - If no markdown file (tracker-native workflow): surface the tracker URL
     to the user; nothing is stored locally.
6. On failure, surface the error and leave any existing markdown untouched.
   Suggest re-running sync once the issue is resolved.

## Pull Direction (tracker → markdown)

1. Read artifact markdown frontmatter; require `tracker.id` to be present.
2. Load the matching adapter.
3. Adapter fetches the entity from the tracker via MCP.
4. Compare tracker state with local frontmatter and body.
5. Detect conflicts (see below).
6. Update markdown content + frontmatter `tracker.last_synced`.

AC validation does not run on pull. Pulled bodies may contain legacy AC
format from before the Given/When/Then enforcement; the planner subagent
decides how to handle them. See [ac-validation.md](ac-validation.md)
"Read-path tolerance" for rationale.

If `tracker.id` is missing, route the user to push first or to manually
attach an existing tracker entity.

## Conflict Detection and Resolution

When pull state differs from local state, surface the conflict before
applying changes:

| Field | What to compare | Default resolution |
|-------|-----------------|--------------------|
| `status` | frontmatter `status` vs tracker status | tracker wins on pull |
| `title` | frontmatter `title` vs tracker title | tracker wins on pull |
| `body` | markdown body vs tracker description | tracker wins on pull |
| labels | frontmatter labels (when present) vs tracker labels | tracker wins on pull |

Conflict report format:

```
Conflict on {artifact-name}:
  status: local=in-progress, tracker=done
  title: local="Auth flow", tracker="Authentication flow"

Defaulting to tracker. Override? [y/N]
```

User can override per-field or choose "keep local" to push back instead.
On override, switch to push direction and treat local as authoritative.

For push, the default is the inverse: markdown wins, tracker is updated
with local content. Conflict warning still fires when pushing over
tracker state that diverged from `last_synced`.

## Operations Summary

The adapter exposes a generic interface. Each tracker adapter implements
these operations using its own MCP calls:

| Operation | Inputs | Output |
|-----------|--------|--------|
| `create_epic` | name, title, body, labels | tracker id + url |
| `create_story` | epic_id (optional), name, title, body, acceptance criteria, labels | tracker id + url |
| `create_bug` | epic_id (optional), name, title, severity, body, repro steps | tracker id + url |
| `create_issue` | epic_id (optional), name, title, body, labels | tracker id + url |
| `create_release` | name, title, story_ids, target_date | tracker id + url |
| `update_status` | tracker_id, new_status | success |
| `fetch_artifact` | tracker_id | full state (status, title, body, labels) |
| `list_artifacts` | filter (epic, status, etc.) | list of summaries |

Status mapping (planned -> in-progress -> done -> blocked) is the
adapter's responsibility; each tracker has its own status enum.

## Guidelines

**DO:**
- Run bootstrap exactly once per project; re-run on demand via "configure tracker"
- Cache the per-session push preference in memory after first ask
- Treat the tracker as source of truth for status when `tracker.id` is set in frontmatter
- Warn the user about every conflict before resolving; never resolve silently
- Update `last_synced` timestamp on every successful sync
- Try MCP first on every operation; fall back to CLI when MCP is missing or fails; fall back to markdown-only when both are unavailable, and warn the user

**DON'T:**
- Push without asking (contrasts: ask once per session, cache the choice)
- Auto-resolve conflicts (contrasts: surface the conflict, let user decide)
- Hardcode tracker primitives in this ref (contrasts: adapters own tracker-specific mapping)
- Modify the tracker entity from this ref directly (contrasts: dispatch to the adapter)
- Skip writing `tracker.last_synced` (contrasts: every successful sync updates it)

## Error Handling

- Config missing: route to bootstrap
- Config has `kind: none`: skip silently; markdown is the source of truth
- MCP unavailable for the configured tracker: try the tracker's CLI (`gh`, `linear`, `jira`); if both fail, warn user, fall back to markdown for this operation, suggest re-running bootstrap if MCP environment changed
- Push fails (network, auth, tracker rejection): log error, leave markdown untouched, suggest retry
- Pull fails: log error, keep current markdown state, suggest retry
- `tracker.id` missing on pull: route to push first or ask user to manually attach an existing tracker entity
- Bootstrap detects multiple MCPs but user picks "none": persist `kind: none`; skill behaves as markdown-only

## Next Steps

- After successful push: artifact lives in the tracker; further status updates flow through the tracker (or via `status.md` which dispatches here)
- After successful pull: frontmatter and body reflect the tracker; user can keep editing the markdown until the next push
- After bootstrap: confirm to the user which tracker is now active and remind them how to override (`configure tracker`)
