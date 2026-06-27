# Sync

Orchestrate push and pull between markdown artifacts and an external
tracker. Detect the configured tracker, dispatch to the matching adapter,
surface conflicts, update frontmatter on success.

Conflict resolution and adapter dispatch deserve careful reasoning — a
wrong push can clobber tracker state that other people rely on.

## When to Use

- Direct trigger: "sync to tracker", "push to {linear,github}", "pull from tracker", "configure tracker"
- Auto-loaded by core refs (epic, story, bug, release) after the artifact is saved when `epic-tracker.kind` is set and not `none`
- Auto-loaded by `status.md` to read overview state from the tracker when configured

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Primitive Mapping

| Artifact | Linear | GitHub |
|----------|--------|--------|
| Epic     | Project | Issue (parent) |
| Story    | Issue | Issue (sub-issue of Epic) |
| Bug      | Issue + label `bug` | Issue (sub-issue of Epic/Story or standalone) |
| Task     | Issue | Issue (sub-issue of Epic or standalone) |
| Release  | Cycle | Release tag |

GitHub uses sub-issues as the hierarchy primitive. Milestones and
Projects v2 are orthogonal opt-in layers (date grouping, custom
fields/views) — neither encodes Epic→Story. See
[adapters/github.md](adapters/github.md) for details.

Release uses the closest native primitive each tracker offers — no forced
single concept across trackers.

## Config

Read and written via `git config --local`. Keys:

| Key | Trackers | Description |
|-----|----------|-------------|
| `epic-tracker.kind` | all | `linear`, `github`, or `none` |
| `epic-tracker.workspace` | Linear | team workspace slug |
| `epic-tracker.project-number` | GitHub | Projects v2 number (optional) |
| `epic-tracker.milestones` | all | `true` to mirror epic milestones to the tracker's native grouping; unset or `false` keeps them markdown-only |

When `epic-tracker.kind` is `none` or unset, the skill skips all tracker
operations; markdown is the sole source of truth.

## Bootstrap (first-time setup)

Runs when an operation requires a tracker but `epic-tracker.kind` is not
set in git config.

1. Check `git config --get epic-tracker.kind`. If set and not `none`, skip bootstrap.
2. Detect available integration methods for each tracker:
   - MCP: check if the tracker's MCP server is active in the session
   - CLI: check if the tracker's CLI is installed (`gh`, `linear`)
   - MCP is always preferred; CLI is the fallback when MCP is missing
     or fails at runtime
3. Present detected options plus "none (markdown only)" to the user.
4. Ask the user to pick one.
5. Collect tracker-specific fields one question at a time:
   - Linear: workspace.
   - GitHub: optional `project-number` (Projects v2).
6. Persist config with `git config --local`:
   - All trackers: `git config --local epic-tracker.kind {kind}`
   - Linear: `git config --local epic-tracker.workspace {workspace}`
   - GitHub: `git config --local epic-tracker.project-number {n}` (when provided)

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

The artifact body — including `## References` and `## Signals` — travels
into the tracker description, so durable pointers survive the push.
Frontmatter `sources:` is a markdown-only index mirroring those links; it
is not pushed separately. Body is the source of truth, frontmatter mirrors.

1. Read artifact content: use the draft data directly when invoked
   immediately after create (no markdown file exists); read from the saved
   markdown file when invoked standalone (e.g., "sync to tracker").
2. Read `git config --get epic-tracker.kind`; if not set or `none`, fall
   back to markdown-only and inform the user.
3. Load the adapter matching `epic-tracker.kind`:
   - `linear` → [adapters/linear.md](adapters/linear.md)
   - `github` → [adapters/github.md](adapters/github.md)
4. Adapter creates or updates the entity. Always attempt MCP first; if
   MCP is unavailable or fails (auth, server down, tool missing), fall
   back to the tracker's CLI (`gh`, `linear`). Runtime probing
   always wins — MCP is preferred regardless of how the tracker was
   configured.
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
   - If the artifact declares `blocked_by`, resolve the paths to tracker
     ids and call `set_dependencies` (see Dependencies). Missing blockers
     are skipped with a warning, never failing the push.
   - If the epic declares `milestone:` and the milestone mirror is enabled,
     call `set_milestone` (see Milestones). When the mirror is off, skip it
     silently — the milestone stays markdown-only.
6. On failure, surface the error and leave any existing markdown untouched.
   Suggest re-running sync once the issue is resolved.

## Pull Direction (tracker → markdown)

1. Read artifact markdown frontmatter; require `tracker.id` to be present.
2. Load the matching adapter.
3. Adapter fetches the entity from the tracker via MCP.
4. Compare tracker state with local frontmatter and body.
5. Detect conflicts (see below).
6. Update markdown content + frontmatter `tracker.last_synced`, and refresh
   `blocked_by` from the entity's native dependency relations (see
   Dependencies) and `milestone:` from the native grouping when the mirror
   is enabled (see Milestones).

AC validation does not run on pull. Pulled bodies may contain legacy AC
format from before the Given/When/Then enforcement; the planner subagent
decides how to handle them. See [ac-validation.md](ac-validation.md)
"Read-path tolerance" for rationale.

If `tracker.id` is missing, route the user to push first or to manually
attach an existing tracker entity.

## Dependencies

An artifact declares `blocked_by` in frontmatter — the artifacts that must
finish before it proceeds, each referenced by path (`epic-name`,
`epic-name/story-name`, or `standalone/bug-name`). Only this direction is
stored; the inverse (`blocking`) is derivable and each tracker maintains
both sides natively.

Dependencies are structured metadata, not body prose. They never travel in
the description; each adapter maps them to the tracker's native dependency
relation:

| Tracker | Native relation |
|---------|-----------------|
| GitHub  | Issue dependencies (`blocked by` / `blocking`) |
| Linear  | Issue relations (`blocked by`) |

`blocked_by` holds local paths; the native relation needs tracker ids:

- **Push:** after the artifact itself is created, resolve each `blocked_by`
  path to the referenced artifact's frontmatter `tracker.id` and pass the
  ids to the adapter's `set_dependencies`. When a referenced artifact has
  no `tracker.id` yet (not pushed), skip that one link, warn which
  dependency could not be formed, and suggest pushing the referenced
  artifact first then re-syncing. The artifact's own push still succeeds —
  a missing blocker never blocks it.
- **Pull:** the adapter returns native blocked-by relations as tracker ids.
  Resolve each id back to a local path when an artifact carries that
  `tracker.id`; otherwise keep the tracker id so the link is not lost.
  Write the result to `blocked_by`.

`set_dependencies` is idempotent: it adds links present in `blocked_by` and
removes tracker links no longer listed, so re-running sync after editing the
field reconciles both sides. In markdown-only mode no resolution runs — the
field is the source of truth and `status.md` reads it directly.

## Milestones

An epic may carry a `milestone:` pointer (its milestone in the registry, see
[milestone.md](milestone.md) and [epic.md](epic.md)). Mirroring milestones to
the tracker is **opt-in and never forced** — the milestone always works in
markdown (the registry `.artifacts/epics/milestones.md` plus the `milestone:`
pointer on epics); the tracker grouping is an optional layer on top.

| Tracker | Native grouping |
|---------|-----------------|
| GitHub  | Milestone (repo-level; an Issue belongs to at most one) |
| Linear  | Initiative (groups Projects = epics) |

Gate the mirror on two conditions:

1. A tracker is configured (`epic-tracker.kind` set and not `none`).
2. The mirror is enabled (`epic-tracker.milestones` is `true`).

When a tracker is configured but `epic-tracker.milestones` is unset, ask once
— "Mirror epic milestones to the tracker's native grouping?" — and persist
the answer with `git config --local epic-tracker.milestones {true|false}`.
Re-ask only via "configure tracker".

- **Push:** when both gates pass and the epic has a `milestone:`, call the
  adapter's `set_milestone` after the epic is created. The native grouping
  stays thin — the milestone's definition lives in the registry, never copied
  into the tracker. When the mirror is off or no tracker is configured, the
  milestone stays markdown-only; nothing is pushed.
- **Pull:** refresh `milestone:` from the entity's native grouping when the
  mirror is enabled; otherwise leave the markdown pointer untouched.

Stories inherit their epic's milestone grouping where the tracker supports it
(see the adapters).

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
| `create_task` | epic_id (optional), name, title, body, labels | tracker id + url |
| `create_release` | name, title, story_ids, target_date | tracker id + url |
| `update_status` | tracker_id, new_status | success |
| `set_dependencies` | tracker_id, blocked_by_ids | success |
| `set_milestone` | tracker_id, milestone_name | success |
| `fetch_artifact` | tracker_id | full state (status, title, body, labels, blocked_by, milestone) |
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

- `epic-tracker.kind` not set: route to bootstrap
- `epic-tracker.kind` is `none`: skip silently; markdown is the source of truth
- MCP unavailable for the configured tracker: try the tracker's CLI (`gh`, `linear`); if both fail, warn user, fall back to markdown for this operation, suggest re-running bootstrap if MCP environment changed
- Push fails (network, auth, tracker rejection): log error, leave markdown untouched, suggest retry
- Pull fails: log error, keep current markdown state, suggest retry
- `tracker.id` missing on pull: route to push first or ask user to manually attach an existing tracker entity
- Bootstrap user picks "none": `git config --local epic-tracker.kind none`; skill behaves as markdown-only

## Outcomes

- After successful push: artifact lives in the tracker; further status updates flow through the tracker (or via `status.md` which dispatches here)
- After successful pull: frontmatter and body reflect the tracker; user can keep editing the markdown until the next push
- After bootstrap: confirm to the user which tracker is now active and remind them how to override (`configure tracker`)
