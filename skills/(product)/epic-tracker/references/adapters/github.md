# GitHub Adapter

Translate generic epic-tracker operations into GitHub primitives via the
GitHub MCP (or `gh` CLI when MCP is unavailable). Loaded by
[../sync.md](../sync.md) when `tracker.kind: github-issues` or
`tracker.kind: github-projects`.

## Two Modes

| Mode | When to use | Detection |
|------|-------------|-----------|
| **github-issues** | Repository uses Issues + Milestones, no Projects v2 | Bootstrap defaults here when no Project number is provided |
| **github-projects** | Repository uses Projects v2 with sub-issues | Bootstrap defaults here when a Project number is supplied; sub-issues mode chosen by default within Projects |

`projects_mode` config field selects sub-modes within github-projects:

- `sub-issues` (default): Epic = parent Issue, Story/Bug = sub-issues
- `classic`: Epic = Project board itself, Story/Bug = Issues added to the board (legacy fallback)

## Primitive Mapping

### github-issues mode

| Artifact | GitHub primitive |
|----------|------------------|
| Epic     | Milestone |
| Story    | Issue (linked to Milestone via `milestone` field) |
| Bug      | Issue + label `bug` (linked to Milestone) |
| Issue    | Issue (linked to Milestone when epic provided; label `task` optional) |
| Release  | Release tag (semver-style; created against a commit) |

### github-projects mode (sub-issues)

| Artifact | GitHub primitive |
|----------|------------------|
| Epic     | Issue (parent), added to the Project; sub-issues feature enabled |
| Story    | Issue (sub-issue under the parent Epic), added to the Project |
| Bug      | Issue (sub-issue) + label `bug`, added to the Project |
| Issue    | Issue (sub-issue when epic provided, else standalone) + label `task` |
| Release  | Release tag (same as github-issues mode; Project Iterations are sprint-level, not release-level) |

### github-projects mode (classic)

| Artifact | GitHub primitive |
|----------|------------------|
| Epic     | Project board (one Project per Epic) |
| Story    | Issue added as item to the Project |
| Bug      | Issue + label `bug`, added to the Project |
| Issue    | Issue + label `task`, added to the Project |
| Release  | Release tag |

Sub-issues mode is preferred -- it nests work naturally and keeps a single
Project board for the whole repository. Classic mode is supported for
legacy projects.

## Status Mapping

GitHub Issues have an `open` / `closed` state plus optional state reason
(`completed`, `not_planned`). Map generic status:

| Generic | GitHub state |
|---------|--------------|
| planned | open (no reason) |
| in-progress | open + label `in-progress` (or Project field "In Progress" when Projects mode) |
| done | closed + reason `completed` |
| blocked | open + label `blocked` |

In `github-projects` mode, prefer Project custom fields for status when
the project has a Status field; fall back to labels otherwise.

## Operations

### create_epic

**github-issues mode:**

1. Create a Milestone in the configured `repo`.
2. Inputs: `name` -> Milestone title, `body` -> Milestone description, optional due date.
3. Return Milestone number and url.

**github-projects sub-issues:**

1. Create a parent Issue in the configured `repo`.
2. Add label `epic` to mark it semantically.
3. Add the Issue to the Project (`project_number`).
4. Return Issue number and url.

**github-projects classic:**

1. Create a new Project board (or use `project_number` if pointing at one).
2. Return Project number and url.

### create_story / create_bug / create_issue

**github-issues mode:**

1. Create an Issue in the `repo`.
2. Set `milestone` to the parent Epic (when `epic_id` provided).
3. Set body with title/description and acceptance criteria (story),
   repro steps (bug), or plain description (issue).
4. For `create_bug`: add label `bug`. Add `severity:{level}` label when
   provided.
5. For `create_issue`: add label `task` (creates it in the repo on first
   use; color: blue, description: "Internal or infrastructure work").
6. Return Issue number and url.

**github-projects sub-issues:**

1. Create an Issue in the `repo`.
2. Attach as sub-issue under the parent Epic Issue (when `epic_id`
   provided).
3. Add to the Project (`project_number`).
4. For `create_bug`: add label `bug` and severity label.
5. For `create_issue`: add label `task`.
6. Return Issue number and url.

**github-projects classic:**

Same as github-issues mode; additionally add to the Project as an item.

### create_release

1. Create a Release in the `repo` against the target commit (default: current HEAD or `main`).
2. Inputs: `name` -> tag name (e.g., `v1.2.0`), `title` -> release title, `body` -> release notes (auto-generate from linked Issues when possible), `target_date` -> draft/scheduled release.
3. Link Issues to the Release via release notes.
4. Return Release id and url.

### update_status

1. Map generic status to GitHub state via the table above.
2. For `done`: close Issue with reason `completed`.
3. For `planned` -> `in-progress`: add `in-progress` label, optionally set Project Status field.
4. For `blocked`: keep open, add `blocked` label.

### fetch_artifact

1. Fetch the Issue, Milestone, or Release by id/number via MCP.
2. Return: state (mapped from open/closed + labels), title, body, labels, url.

### list_artifacts

1. Query GitHub for items matching the filter (milestone, state, label, project).
2. Return summaries with id, title, state, url.

## Release Strategy

GitHub Release tags are semver-style and tied to a commit. They're the
right primitive when releases ship code. Project Iterations are sprint-
level (1-2 weeks) and don't map to ship-together semantics here.

When the user creates a Release without a current commit (planning ahead):

1. Create a draft Release with the tag and notes.
2. Mark `tracker.draft: true` in markdown frontmatter.
3. User publishes the Release later when the code is ready.

## Sub-Issues Detection

When `tracker.kind: github-projects` and `projects_mode: sub-issues`,
verify the Project has the sub-issues feature enabled (Projects v2 with
sub-issue support). If unavailable:

1. Warn the user.
2. Offer to fall back to `classic` mode (Project + Issues, no parent/child relation).
3. Persist the choice in config.

## Error Handling

- Repo not accessible: route to GitHub MCP auth setup
- Milestone or Project not found: ask user to verify config or offer to create
- Sub-issues feature disabled: fall back to classic mode after user confirmation
- Label `bug` doesn't exist in repo: create it during first push (color: red, description: "Something isn't working")
- Release tag already exists: ask user whether to overwrite, append, or change the tag name
- API rate limit: surface the error, suggest waiting before retry
