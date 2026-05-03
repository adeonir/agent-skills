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

## Issue Types vs Labels

GitHub has two distinct classification mechanisms with different scopes:

- **Issue types**: configured at the **org level** — shared across all
  repos in the organization. When the org has issue types, every repo
  has them consistently. Bootstrap detects once; no per-repo variation.
- **Labels**: configured at the **repo level** — each repository defines
  its own label set. Never hardcode label names or colors; always query
  the repo's existing labels before assigning (see Label Matching below).

## Label Matching

Labels are repo-specific. Before assigning any label, always fetch the
repo's label list:

```
GET /repos/{owner}/{repo}/labels
```

Match semantically against the needed concept (severity, status). If no
match is found, surface the available labels to the user and ask which
to use (or skip). Never create labels automatically.

Concepts that use labels:

| Concept | Match strategy |
|---------|---------------|
| Severity | Look for labels containing the severity word (e.g., `high`, `critical`, `severity-high`) |
| Status (in-progress) | Look for labels containing `progress` or `wip` |
| Status (blocked) | Look for labels containing `blocked` or `on-hold` |

## Primitive Mapping

### github-issues mode

| Artifact | Primitive |
|----------|-----------|
| Epic     | Milestone |
| Story    | Issue `issuetype: Story` (linked to Milestone) |
| Bug      | Issue `issuetype: Bug` (linked to Milestone) |
| Issue    | Issue `issuetype: Task` (linked to Milestone when epic provided) |
| Release  | Release tag (semver-style; created against a commit) |

### github-projects mode (sub-issues)

| Artifact | Primitive |
|----------|-----------|
| Epic     | Issue `issuetype: Epic` (parent), added to Project |
| Story    | Issue `issuetype: Story` (sub-issue under Epic) |
| Bug      | Issue `issuetype: Bug` (sub-issue) |
| Issue    | Issue `issuetype: Task` (sub-issue when epic provided, else standalone) |
| Release  | Release tag |

### github-projects mode (classic)

| Artifact | Primitive |
|----------|-----------|
| Epic     | Project board (one per Epic) |
| Story    | Issue `issuetype: Story`, added to Project |
| Bug      | Issue `issuetype: Bug`, added to Project |
| Issue    | Issue `issuetype: Task`, added to Project |
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

### Bootstrap: Issue Type Detection

During bootstrap, detect whether the org has custom issue types configured:

1. Query the org's issue types via MCP or `gh api orgs/{org}/issue-types`.
2. If types are found, store the detected names in config:
   ```yaml
   issue_types:
     epic: Epic
     story: Story
     bug: Bug
     task: Task
   ```
   Names may differ from defaults (e.g., the org may use "Chore" instead
   of "Task"). Store whatever name the org configured.
3. If no types found or query fails: set `issue_types: {}` in config.
   Artifact classification relies on semantic matching at the type level
   (no types = plain Issues, no automatic classification).

Re-detect on demand via "configure tracker".

### create_epic

**github-issues mode:**

1. Create a Milestone in the configured `repo`.
2. Inputs: `name` -> Milestone title, `body` -> Milestone description, optional due date.
3. Return Milestone number and url.

**github-projects sub-issues:**

1. Create a parent Issue in the configured `repo`.
2. If `issue_types: true`: set `issue_type: Epic`.
   Otherwise: add label `epic`.
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
4. Set `issue_type` using the name stored in config under `issue_types`
   (e.g., `issue_types.story`, `issue_types.bug`, `issue_types.task`).
   If `issue_types` is empty, no type is set — Issue is created plain.
5. For `create_bug` with a severity: fetch repo labels, match semantically
   to find a severity label (see Label Matching). Assign if found; skip
   with a note to the user if not.
6. Return Issue number and url.

**github-projects sub-issues:**

1. Create an Issue in the `repo`.
2. Attach as sub-issue under the parent Epic Issue (when `epic_id` provided).
3. Add to the Project (`project_number`).
4. Apply issue type per the same rules as github-issues mode above.
5. Return Issue number and url.

**github-projects classic:**

Same as github-issues mode; additionally add the Issue to the Project as an item.

### create_release

1. Create a Release in the `repo` against the target commit (default: current HEAD or `main`).
2. Inputs: `name` -> tag name (e.g., `v1.2.0`), `title` -> release title, `body` -> release notes (auto-generate from linked Issues when possible), `target_date` -> draft/scheduled release.
3. Link Issues to the Release via release notes.
4. Return Release id and url.

### update_status

1. Map generic status to GitHub state via the table above.
2. For `done`: close Issue with reason `completed`.
3. For `planned` -> `in-progress`: fetch repo labels, match semantically
   (look for `progress` or `wip`); assign if found, skip with note if not.
   In Projects mode, prefer setting the Project Status field instead.
4. For `blocked`: fetch repo labels, match semantically (look for `blocked`
   or `on-hold`); assign if found, skip with note if not.

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
- Issue type not found in org (type was deleted or renamed after bootstrap): warn user,
  suggest re-running "configure tracker" to re-detect; create Issue without type
- Severity or status label not found in repo: surface available labels to user, ask
  which to use or confirm to skip; never create labels automatically
- Release tag already exists: ask user whether to overwrite, append, or change the tag name
- API rate limit: surface the error, suggest waiting before retry
