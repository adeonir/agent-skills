# Linear Adapter

Translate generic epic-tracker operations into Linear primitives. Loaded by [sync.md](../instructions/sync.md) when `epic-tracker.kind: linear`.

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
| Story | Issue + label `story` | Sub-issue of an Epic, or standalone |
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

## Milestone

Milestone is a Linear Project Milestone, scoped to `epic-tracker.project` — the same project every artifact lives in. It carries only a name here; never set a target date, so the materialized milestone stays dateless (a user may add a date in the UI; leave it untouched).

Resolve a milestone name by reading before writing: list the project's milestones and reuse the one with that exact name, including one a user created in the UI. Match on the name itself, not semantically — the milestone name is the phase name. When none has that name, create it in the project with no target date. Then associate the Issue with it.

Any artifact can carry a milestone: the caller supplies it on `create_epic`, on `create_story` / `create_bug` / `create_task`, or on `set_milestone`. The adapter associates whatever Issue it is given with the resolved milestone, regardless of type — `sync.md` decides which milestone a child carries (its parent epic's). When the caller supplies no milestone, leave the Issue's milestone unset; when `set_milestone` is given none, clear the association.

## Priority Mapping

Priority is a native Issue field in Linear, not a label. Map the generic value to it:

| Generic | Linear priority |
| ------- | --------------- |
| urgent | Urgent |
| high | High |
| medium | Medium |
| low | Low |
| none supplied | No priority |

Any artifact can carry a priority — the caller supplies it on `create_epic`, on `create_story` / `create_bug` / `create_task`, or on `update_artifact`. When the caller supplies none, leave the field at No priority; the adapter never derives one.

## Estimate

Estimate is the native `estimate` field on the Issue, a number. The team picks how that number renders — Fibonacci, exponential, linear, t-shirt — and the adapter writes the number it is given without touching the scale.

A story, bug, or task carries one when the caller supplies it; an epic never does, so `create_epic` takes no estimate. When the caller supplies none, leave the field unset.

Estimates are a per-team setting in Linear. When `epic-tracker.team` has them disabled, the field cannot be written: tell the user the team has estimates off, and create or update the Issue without it rather than failing the dispatch.

## Operations

### create_epic

1. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`, with label `epic` and no parent issue.
2. Inputs: `title` -> Issue title, `body` -> Issue description.
3. When `milestone` is supplied, resolve it per Milestone above and associate the Issue with it.
4. When `priority` is supplied, set the native priority field per Priority Mapping above.
5. The native sub-issue panel is the source of truth for child hierarchy; the body carries no child list.
6. Return Issue id and url.

### create_story / create_bug / create_task

1. Create an Issue in `epic-tracker.team`, placed in `epic-tracker.project`. `epic_id` is optional on all three: with one, the Issue is a sub-issue of that epic; without one, it is a standalone Issue in the project.
2. Inputs: `title` -> Issue title, `body` -> Issue description (include acceptance criteria for stories, repro steps for bugs, plain description for tasks). For stories, the body must include the validated `### AC-N` Given/When/Then blocks verbatim -- adapters do not transform AC structure, so a downstream consumer can parse these blocks back to structured AC. See [ac-validation.md](ac-validation.md) for the contract.
3. Apply the type label: `story`, `bug`, or `task`. For `create_bug`, add `severity:{level}` when severity is provided.
4. When `milestone` is supplied, resolve it per Milestone above and associate the Issue with it.
5. When `priority` is supplied, set the native priority field per Priority Mapping above.
6. When `estimate` is supplied, set the native estimate field per Estimate above.
7. Return Issue id and url.

### update_artifact

Rewrites an existing Issue's body. `sync.md` refetches immediately before calling this and confirms with the user when the Issue changed underneath — this adapter performs the write it is given.

1. Update the Issue's title and description.
2. When a severity is supplied, re-map the severity label: remove the previous `severity:{level}` and apply the new one.
3. When a priority is supplied, set the native priority field per Priority Mapping above, replacing the previous value.
4. When an estimate is supplied, set the native estimate field per Estimate above, replacing the previous value.
5. Return success.

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

### set_milestone

1. Inputs: `tracker_id` and `milestone` (a name, or none to clear).
2. When a name is given, resolve it per Milestone above and associate the Issue with it, replacing any previous one. When none is given, remove any existing milestone association.
3. Return success.

### fetch_artifact

1. Fetch the Issue by id.
2. Return: type (`epic`, `story`, `bug`, or `task`, read back from the artifact-type label per Primitive Mapping), status (read back from the state's `type` per the Status Mapping table), title, body (the Issue description), severity (from the `severity:{level}` label, when present), priority (read back from the native field per the Priority Mapping table; none when the field is No priority), estimate (the native estimate field's number, when set), parent, blocked-by relations, blocking relations (the inverse side Linear maintains), milestone (the associated project milestone's name, when present), url.

### list_artifacts

1. Query the project's issues matching the filter — type maps to the label (`epic`, `story`, `bug`, `task`), epic maps to the parent issue, status maps to the state types the Status Mapping table reads it back from.
2. Return summaries with id, title, status, and url.

## Error Handling

- Linear MCP server unavailable: surface the error; the caller holds the draft
- `epic-tracker.project` unset or project not found: ask the user to name an existing project or create one, then persist the key
- Parent epic id not found: ask whether to create the epic first or attach to a different one
- Label missing in the team: tell the user, then create it
- No state of the needed type in the team: surface it, and ask which state to use
- Estimates disabled for the team: tell the user, then write the Issue without the estimate
- API rate limit: surface the error, suggest waiting a minute before retry
- Auth error: route the user to Linear MCP auth setup
