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
| Epic | Issue + label `epic` | No parent issue. Optionally assigned to a milestone |
| Story | Issue + label `story` | Sub-issue of its Epic |
| Bug | Issue + label `bug` | Sub-issue of an Epic, or standalone |
| Task | Issue + label `task` | Sub-issue of an Epic, or standalone |

The adapter derives the label from the artifact type; the caller never passes it. Match semantically against the labels the workspace already defines — `story` matches an existing `feature`, `task` an existing `chore`. When nothing matches, tell the user which label is missing and create it.

Severity is the one label built from a value rather than matched: `severity:{level}`. Create it the same way — after telling the user.

## Milestones

Project milestones group epics. They carry no target date — grouping and order only.

Every epic dispatch resolves a milestone. When `epic-tracker.project` defines any, list them alongside "none" and let the user pick; when the user names one in the request, take it and skip the question. Create a milestone only when the user asks for one. A project with no milestones skips the question entirely, and an epic assigned to none stays unassigned.

A story, bug, or task is never assigned to a milestone.

## Status Mapping

Linear's workflow states are defined per team. Use `epic-tracker.team`'s default state group when present; otherwise map to standard names:

| Generic | Linear default state |
| ------- | -------------------- |
| planned | Backlog |
| in-progress | In Progress |
| done | Done |
| blocked | Custom "Blocked" state when the team defines one; otherwise keep the current state and add the label `blocked` plus a comment naming the blocker |

Detect the team's available states before pushing.

## Operations

### create_epic

1. Resolve the milestone (see Milestones) before creating anything — the answer travels with the create, not as a follow-up edit.
2. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`, with label `epic`, no parent issue, and the resolved milestone when there is one.
3. Inputs: `title` -> Issue title, `body` -> Issue description.
4. The native sub-issue panel is the source of truth for child hierarchy; the body carries no child list.
5. Return Issue id and url.

### create_story / create_bug / create_task

1. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`. `create_story` requires `epic_id`: the Issue is a sub-issue of the epic it names, and a dispatch without it is an error to surface, never a top-level Issue to create. On `create_bug` / `create_task`, `epic_id` is optional: with one, the Issue is a sub-issue of that epic; without one, it is a standalone Issue in the project.
2. Inputs: `title` -> Issue title, `body` -> Issue description (include acceptance criteria for stories, repro steps for bugs, plain description for tasks). For stories, the body must include the validated `### AC-N` Given/When/Then blocks verbatim -- adapters do not transform AC structure, so a downstream consumer can parse these blocks back to structured AC. See [ac-validation.md](ac-validation.md) for the contract.
3. Apply the type label: `story`, `bug`, or `task`. For `create_bug`, add `severity:{level}` when severity is provided.
4. Return Issue id and url.

### update_artifact

Rewrites an existing Issue's body and status. `sync.md` refetches immediately before calling this and confirms with the user when the entity changed underneath — this adapter performs the write it is given.

1. Update the Issue's title and description.
2. When a status is supplied, apply it via `update_status` below.
3. When a severity is supplied, re-map the severity label: remove the previous `severity:{level}` and apply the new one.
4. On an epic, re-resolve the milestone (see Milestones) and apply the answer — an edit that leaves it untouched keeps the current one.
5. Return success.

### update_status

1. Map generic status to a Linear state via the table above.
2. Update the Issue's `state` field.

### set_parent

1. Inputs: the Issue id and the target `epic_id`, or none to detach.
2. Set the Issue's parent to the epic named by `epic_id`. With none, clear the parent and leave the Issue standalone in the project.
3. Detaching a story is an error to surface — a story always keeps a parent.
4. Return success.

### set_dependencies

1. Inputs: the entity id and a list of blocker ids (sync.md supplies them directly — they are already tracker ids).
2. Create a native issue relation of type `blocked by` for each blocker. Linear maintains both directions. Any pair is expressible, including Epic and Story.
3. Remove relations no longer listed.
4. Return success.

### fetch_artifact

1. Fetch the Issue by id.
2. Return: status (mapped from the Linear state), title, description, labels, parent issue, milestone, blocked-by relations, url.

### list_artifacts

1. Query the project's issues matching the filter — type maps to the label (`epic`, `story`, `bug`, `task`), epic maps to the parent issue, status maps to the Linear state.
2. Return summaries with id, title, status, and url — the url is what a child artifact records in its `## References`.

## Error Handling

- Linear MCP server unavailable: surface the error; the caller holds the draft
- `epic-tracker.project` unset or project not found: ask the user to name an existing project or create one, then persist the key
- Parent epic id not found: ask whether to create the epic first or attach to a different one
- Label missing in the workspace: tell the user, then create it
- State name not found in the team: fall back to the closest standard name with a warning
- API rate limit: surface the error, suggest waiting a minute before retry
- Auth error: route the user to Linear MCP auth setup
