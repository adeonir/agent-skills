# Linear Adapter

Translate generic epic-tracker operations into Linear primitives. Loaded by [sync.md](sync.md) when `epic-tracker.kind: linear`.

## When to Use

Loaded by `sync.md` when `epic-tracker.kind` is `linear`. Not a direct trigger.

## Integration Channel

MCP is the only channel. Every operation below runs through the Linear MCP server. When the server is unavailable, surface the failure to the caller.

Take each tool name from the connected server's own tool list and call it qualified (`Linear:tool_name`).

## Config

| Key | Description |
| --- | ----------- |
| `epic-tracker.team` | Linear team the issues belong to |
| `epic-tracker.project` | Linear project that holds every artifact |

Both are required. Every Issue is created in `epic-tracker.team` and placed in `epic-tracker.project`. When either is unset, ask the user to name an existing one or create it, then persist with `git config --local`.

## Primitive Mapping

Every artifact is a Linear Issue, created in `epic-tracker.team` and placed in `epic-tracker.project`. The label carries the type; the parent issue carries the hierarchy.

| Artifact | Linear primitive | Notes |
| -------- | ---------------- | ----- |
| Epic | Issue + label `epic` | No parent issue |
| Story | Issue + label `story` | Sub-issue of its Epic |
| Bug | Issue + label `bug` | Sub-issue of an Epic, or standalone |
| Task | Issue + label `task` | Sub-issue of an Epic, or standalone |

The adapter derives the label from the artifact type; the caller never passes it. Match semantically against the labels `epic-tracker.team` already defines — `story` matches an existing `feature`, `task` an existing `chore`. When nothing matches, tell the user which label is missing and create it.

Severity is the one label built from a value rather than matched: `severity:{level}`. Create it the same way — after telling the user.

## Status Mapping

Linear's workflow states are defined per team. Match on the state's `type`, never its name.

| Generic | Write to a state of type | Read back from type |
| ------- | ------------------------ | ------------------- |
| planned | `unstarted`, or `backlog` when the team has no `unstarted` state | `triage`, `backlog`, `unstarted` |
| in-progress | `started` | `started` |
| done | `completed` | `completed` |
| cancelled | `canceled` | `canceled` |

A create sets no state; the team's default applies.

Detect the team's available states before pushing. When the team defines no state of the type a write needs, surface it and ask which state to use.

## Body Normalization

Linear renders the Issue title above the description; a leading H1 that repeats the title would render twice. On every write (`create_epic`, `create_story` / `create_bug` / `create_task`, `update_artifact`), strip a leading H1 matching the Issue title before sending the body as the description. Leave any other heading intact.

## Operations

### create_epic

1. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`, with label `epic` and no parent issue.
2. Inputs: `title` -> Issue title, `body` -> Issue description.
3. The native sub-issue panel is the source of truth for child hierarchy; the body carries no child list.
4. Return Issue id and url.

### create_story / create_bug / create_task

1. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`. `create_story` requires `epic_id`: the Issue is a sub-issue of the epic it names, and a dispatch without it is an error to surface, never a top-level Issue to create. On `create_bug` / `create_task`, `epic_id` is optional: with one, the Issue is a sub-issue of that epic; without one, it is a standalone Issue in the project.
2. Inputs: `title` -> Issue title, `body` -> Issue description (include acceptance criteria for stories, repro steps for bugs, plain description for tasks). For stories, the body must include the validated `### AC-N` Given/When/Then blocks verbatim -- adapters do not transform AC structure, so a downstream consumer can parse these blocks back to structured AC. See [ac-validation.md](ac-validation.md) for the contract.
3. Apply the type label: `story`, `bug`, or `task`. For `create_bug`, add `severity:{level}` when severity is provided.
4. Return Issue id and url.

### update_artifact

Rewrites an existing Issue's body. `sync.md` refetches immediately before calling this and confirms with the user when the Issue changed underneath — this adapter performs the write it is given.

1. Update the Issue's title and description.
2. When a severity is supplied, re-map the severity label: remove the previous `severity:{level}` and apply the new one.
3. Return success.

### update_status

1. Map generic status to the Linear state whose `type` the table above names.
2. Update the Issue's `state` field.

### set_parent

1. Inputs: `tracker_id` and the target `epic_id`.
2. Set the Issue's parent to the epic named by `epic_id`, replacing the previous one.
3. Return success.

### set_dependencies

1. Inputs: `tracker_id` and a list of blocker ids (sync.md supplies them directly — they are already tracker ids).
2. Create a native issue relation of type `blocked by` for each blocker. Linear maintains both directions.
3. Remove relations no longer listed.
4. Return success.

### fetch_artifact

1. Fetch the Issue by id.
2. Return: status (read back from the state's `type` per the Status Mapping table), title, body (the Issue description), severity (from the `severity:{level}` label, when present), parent, blocked-by relations, url.

### list_artifacts

1. Query the project's issues matching the filter — type maps to the label (`epic`, `story`, `bug`, `task`), epic maps to the parent issue, status maps to the state types the Status Mapping table reads it back from.
2. Return summaries with id, title, status, and url — the url is what a child artifact records in its `## References`.

## Error Handling

- Linear MCP server unavailable: surface the error; the caller holds the draft
- `epic-tracker.project` unset or project not found: ask the user to name an existing project or create one, then persist the key
- Parent epic id not found: ask whether to create the epic first or attach to a different one
- Label missing in the team: tell the user, then create it
- No state of the needed type in the team: surface it, and ask which state to use
- API rate limit: surface the error, suggest waiting a minute before retry
- Auth error: route the user to Linear MCP auth setup
