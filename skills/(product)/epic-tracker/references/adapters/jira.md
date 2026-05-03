# Jira Adapter

Translate generic epic-tracker operations into Jira primitives via the
Jira MCP (or Jira Cloud REST API when MCP is unavailable). Loaded by
[../sync.md](../sync.md) when `tracker.kind: jira`.

## Primitive Mapping

| Artifact | Jira primitive | Notes |
|----------|----------------|-------|
| Epic     | Epic (issue type) | Native Jira primitive |
| Story    | Story (issue type) | Native; linked to Epic via `Epic Link` field |
| Bug      | Bug (issue type) | Native; first-class type, no label needed |
| Issue    | Task (issue type) | Native Jira Task; linked to Epic via `Epic Link` when provided |
| Release  | Fix Version | Jira's native release primitive; Stories, Tasks, and Bugs link via `fixVersions` |

Unlike Linear and GitHub, Jira has dedicated types for every artifact in
this skill. No label workarounds needed.

## Status Mapping

Jira workflow varies per project. Use the project's default workflow
states; map to standard names:

| Generic | Jira default workflow |
|---------|----------------------|
| planned | To Do (or "Backlog" when present) |
| in-progress | In Progress |
| done | Done |
| blocked | Blocked (when workflow has it) or "On Hold" or "To Do" + comment |

Detect the project's workflow via MCP before pushing. Fall back to the
nearest standard name with a warning when an exact match isn't found.

## Operations

### create_epic

1. Create an Issue with `issuetype: Epic` in the configured `project_key`.
2. Inputs: `name` -> Epic Name field (Jira's custom field), `title` -> Summary, `body` -> Description.
3. Return Epic key (e.g., `PROJ-123`) and url.

### create_story / create_bug / create_issue

1. Create an Issue with `issuetype: Story`, `Bug`, or `Task` in the
   `project_key`.
2. Inputs: `title` -> Summary, `body` -> Description (acceptance criteria
   for Story, repro steps for Bug, plain description for Task).
3. Set `Epic Link` to `epic_id` when provided.
4. For `create_bug`: set `Priority` from severity
   (critical/high/medium/low -> Highest/High/Medium/Low).
5. Return Issue key and url.

### create_release

1. Create a Fix Version in the `project_key`.
2. Inputs: `name` -> Version name (e.g., "v1.2.0"), `title` -> Description, `target_date` -> Release date.
3. Link Issues to the Fix Version: for each Story/Bug in `story_ids`, set its `fixVersions` field to include the new version.
4. Return Fix Version id and url.

### update_status

1. Map generic status to Jira workflow state via the table above.
2. Transition the Issue using Jira's transition API (states are not directly settable; transitions move them).
3. If the target state isn't reachable from the current state via the workflow, warn the user and offer the closest reachable transition.

### fetch_artifact

1. Fetch the Issue by key via MCP.
2. Return: status (mapped from Jira workflow state), title (Summary), body (Description), labels, fixVersions, url.

### list_artifacts

1. JQL query for items matching the filter:
   - Epics: `project = {key} AND issuetype = Epic`
   - Stories under Epic: `project = {key} AND "Epic Link" = {epic_key}`
   - Bugs: `project = {key} AND issuetype = Bug`
   - By Fix Version: `project = {key} AND fixVersion = "{name}"`
2. Return summaries with key, title, status, url.

## Release Strategy

Jira Fix Version is the canonical release primitive. Use it directly:

- Create Fix Version per Release artifact in markdown
- Link all Stories/Bugs to it via `fixVersions`
- Mark Fix Version as released when all linked Issues are Done

Released Fix Versions become read-only in Jira. To modify after release,
the user must un-release in Jira UI; the skill warns when attempting an
update on a released version.

## Custom Fields

Jira projects often have custom fields (Story Points, Sprint, Epic Color).
The skill does not write to custom fields by default. When the user wants
them populated:

1. Bootstrap asks whether to discover and map custom fields.
2. If yes, fetch the project's screen schema via MCP.
3. Persist mapping in config under `tracker.custom_fields`.

Without explicit mapping, custom fields stay empty after sync; the user
fills them in Jira UI.

## Error Handling

- Project not found: ask user to verify `project_key`; offer to re-run bootstrap
- Issue type unavailable in project (e.g., "Bug" or "Task" disabled): fall back to Story with appropriate label (`bug` or `task`), warn user
- Workflow transition not reachable: list the legal transitions and ask user to pick or fix the workflow in Jira
- Auth error: route to Jira MCP setup
- Released Fix Version: warn user; refuse update unless explicitly confirmed
- API rate limit: surface error, suggest waiting before retry
