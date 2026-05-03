# Linear Adapter

Translate generic epic-tracker operations into Linear primitives via the
Linear MCP. Loaded by [../sync.md](../sync.md) when `tracker.kind: linear`.

## Primitive Mapping

| Artifact | Linear primitive | Notes |
|----------|------------------|-------|
| Epic     | Project | Linear's Project is a thematic container for related issues |
| Story    | Issue | Standard work unit |
| Bug      | Issue + label `bug` | Same primitive as Story; `bug` label distinguishes type |
| Issue    | Issue + label `task` | Same primitive as Story; `task` label distinguishes internal work |
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

1. Create a Linear Project in the configured `workspace`.
2. Inputs: `name` -> Project slug, `title` -> Project name, `body` -> Project description.
3. Return Project id and url.

### create_story / create_bug / create_issue

1. Create a Linear Issue in the project (when `epic_id` provided) or in
   the team backlog (when not).
2. Inputs: `title` -> Issue title, `body` -> Issue description (include
   acceptance criteria for stories, repro steps for bugs, plain
   description for issues).
3. For `create_bug`: add label `bug`. Add `severity:{level}` label when
   severity is provided.
4. For `create_issue`: add label `task`.
5. Return Issue id and url.

### create_release

1. Create a Linear Cycle in the workspace's active team.
2. Inputs: `name` -> Cycle name, `title` -> Cycle description, `target_date` -> Cycle end date.
3. Add stories to the Cycle by updating each Issue's `cycle` field via MCP.
4. Return Cycle id and url.

### update_status

1. Map generic status to Linear state via the table above.
2. Update the Issue's `state` field via MCP.

### fetch_artifact

1. Fetch the Project, Issue, or Cycle by id via MCP.
2. Return: status (mapped from Linear state), title, description, labels, url.

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

Linear supports sub-issues. Use them when a Story needs explicit breakdown
that doesn't justify spec-driven (rare). Spec-driven owns implementation
breakdown; sub-issues here are for tracker-level grouping only.

## Error Handling

- Workspace not found: ask user to verify config; offer to re-run bootstrap
- Project not found by id: ask user whether to create a new Project or attach to an existing one
- State name not found in workspace: fall back to closest standard name with a warning
- API rate limit: surface the error, suggest waiting a minute before retry
- Auth error: route user to Linear MCP setup
