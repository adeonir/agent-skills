# Linear Adapter

Translate generic epic-tracker operations into Linear primitives via the
Linear MCP (or `linear` CLI when MCP is unavailable). Loaded by
[sync.md](sync.md) when `epic-tracker.kind: linear`.

## When to Use

Loaded by `sync.md` when `epic-tracker.kind` is `linear`. Not a direct trigger.

## Primitive Mapping

| Artifact | Linear primitive | Notes |
|----------|------------------|-------|
| Epic     | Project | Linear's Project is a thematic container for related issues |
| Story    | Issue | Standard work unit |
| Bug      | Issue + label `bug` | Same primitive as Story; `bug` label distinguishes type |
| Task     | Issue + label `task` | Same primitive as Story; `task` label distinguishes non-story work |
| Release  | Cycle | Linear has no first-class Release; Cycle is the closest native primitive (sprint-like, but used here as the ship-together grouping) |

## Status Mapping

Linear's workflow states vary per workspace. Use the team's default state
group when present; otherwise map to standard names:

| Generic | Linear default state |
|---------|---------------------|
| planned | Backlog |
| in-progress | In Progress |
| done | Done |
| blocked | Cancelled (with comment marking as blocked) or custom "Blocked" state if the workspace has one |

Detect available states from the workspace via MCP before pushing. If
"Blocked" doesn't exist as a state, fall back to a comment plus a label
`blocked`.

## Operations

### create_epic

1. Strip the `## Stories` section from the body before push. The
   section is local-only — Linear's native sub-issue panel under the
   Project is the source of truth for child hierarchy. Drop the
   heading and all bullets up to (but not including) the next `##`
   heading.
2. Create a Linear Project in the workspace (from `epic-tracker.workspace`) with the
   stripped body.
3. Inputs: `name` -> Project slug, `title` -> Project name, `body` -> Project description.
4. Return Project id and url.

### create_story / create_bug / create_task

1. Create a Linear Issue in the project (when `epic_id` provided) or in
   the team backlog (when not).
2. Inputs: `title` -> Issue title, `body` -> Issue description (include
   acceptance criteria for stories, repro steps for bugs, plain
   description for tasks). For stories, the body must include the
   validated `### AC-N` Given/When/Then blocks verbatim -- adapters do
   not transform AC structure, so a downstream consumer can parse these
   blocks back to structured AC. See
   [ac-validation.md](ac-validation.md) for the contract.
3. For `create_bug`: add label `bug`. Add `severity:{level}` label when
   severity is provided.
4. For `create_task`: add label `task`.
5. Return Issue id and url.

### create_release

1. Create a Linear Cycle in the workspace's active team.
2. Inputs: `name` -> Cycle name, `title` -> Cycle description, `target_date` -> Cycle end date.
3. Add stories to the Cycle by updating each Issue's `cycle` field via MCP.
4. Return Cycle id and url.

### update_status

1. Map generic status to Linear state via the table above.
2. Update the Issue's `state` field via MCP.

### set_dependencies

1. Inputs: the entity id and a list of blocker ids (resolved from paths by
   sync.md).
2. Issue-level blockers (Story, Bug, Issue → Linear Issues): create a
   native issue relation of type `blocked by` via MCP for each blocker.
   Linear maintains both directions.
3. Epic-level blockers (Epic → Linear Project): use a Project relation
   when both endpoints are Projects. A dependency mixing a Project and an
   Issue has no native Linear form — keep it in markdown `blocked_by` and
   warn the user it is not mirrored in the tracker.
4. Remove relations no longer listed.
5. Return success.

### fetch_artifact

1. Fetch the Project, Issue, or Cycle by id via MCP.
2. Return: status (mapped from Linear state), title, description, labels,
   blocked-by relations (issue relations, or project relations for Epics),
   url.

### list_artifacts

1. Query Linear for items matching the filter (project, state, label, cycle).
2. Return summaries with id, title, status, url.

## Release Strategy

Linear Cycles are typically 1-2 week sprints, semantically narrower than
"Release" in other trackers. Inform the user when bootstrapping that
Linear Releases are represented as Cycles. Users who want true ship-together
groupings beyond a sprint window can additionally use a label like
`ships-{name}`.

When the user creates a Release in Linear:

1. Ask whether to create a Cycle (sprint-style) or use a label-only approach (`ships-{name}`).
2. Default to Cycle (matches "closest native primitive" principle).
3. If label-only, skip Cycle creation and store the label name in markdown frontmatter `tracker.label`.

## Sub-issues

Linear supports sub-issues. Use them when a Story needs explicit
breakdown that does not justify a full implementation spec (rare).
Implementation specs own the task-level breakdown; Linear sub-issues
here are for tracker-level grouping only.

## Error Handling

- Workspace not found: ask user to verify `epic-tracker.workspace`; offer to re-run bootstrap
- Project not found by id: ask user whether to create a new Project or attach to an existing one
- State name not found in workspace: fall back to closest standard name with a warning
- API rate limit: surface the error, suggest waiting a minute before retry
- Auth error: route user to Linear MCP setup
