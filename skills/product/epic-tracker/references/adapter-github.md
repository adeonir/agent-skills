# GitHub Adapter

Translate generic epic-tracker operations into GitHub primitives. Loaded by [sync.md](sync.md) when `epic-tracker.kind: github`.

## When to Use

Loaded by `sync.md` when `epic-tracker.kind` is `github`. Not a direct trigger.

## Config

| Key | Description |
| --- | ----------- |
| `epic-tracker.channel` | `mcp` or `cli` — primary integration channel |
| `epic-tracker.fallback` | `mcp`, `cli`, or `none` — secondary channel when the primary fails |
| `epic-tracker.project` | Projects v2 number (optional) |

The repo is inferred from `git remote get-url origin`, never configured. `epic-tracker.project` activates the Projects v2 layer; when it is unset, the adapter operates on Issues alone.

## Model

Every artifact is an Issue. Artifact type is carried by org-level Issue Types when available, or by a label fallback. Hierarchy is expressed via Issue sub-issue parent links.

| Artifact | Issue type / label | Sub-issue role |
| -------- | ------------------ | -------------- |
| Epic | `Epic` | always parent |
| Story | `Story` | always child of an Epic |
| Bug | `Bug` | optional child of an Epic; may be standalone |
| Task | `Task` (or org default) | optional child of an Epic; may be standalone |

Sub-issues are a native Issues feature (GraphQL `addSubIssue`), available to anyone with triage permission on the repository.

## Orthogonal Layers

One opt-in layer wraps the same Issue substrate, independent of hierarchy.

| Layer | What it adds | Activation |
| ----- | ------------ | ---------- |
| **Projects v2** | Board/roadmap views and custom fields (status, priority, sprint). Issues are added as Project items. | `git config epic-tracker.project {n}` — the Projects v2 number |

## Integration Channel

MCP and the `gh` CLI are both channels. The caller (`sync.md`) selects the active one from `epic-tracker.channel` and `epic-tracker.fallback`; every operation below runs through whichever is active. When a capability is missing from the active channel, surface it and let the caller decide whether to try the other.

Take each MCP tool name from the connected server's own tool list and call it qualified (`GitHub:tool_name`).

## Issue Types vs Labels

Issue types are org-level; a user-owned repo has none. Labels are repo-level. Never hardcode a label name or color — query the repo's labels before assigning (see Label Matching).

When the session cache holds no issue type, classify by artifact label (`epic`, `story`, `bug`, `task`) matched semantically against the repo's labels.

## Label Matching

Labels are repo-specific. Before assigning any label, always fetch the repo's label list:

```text
GET /repos/{owner}/{repo}/labels
```

Match semantically against the needed concept (artifact type, severity, status). When nothing matches, tell the user which label is missing and create it, then assign it.

Concepts that use labels:

| Concept | Match strategy |
|---------|---------------|
| Artifact type: Epic | Labels containing `epic` |
| Artifact type: Story | Labels containing `story`, `feature`, `user-story` |
| Artifact type: Bug | Labels containing `bug`, `defect`, `fix` |
| Artifact type: Task | Labels containing `task`, `chore`, `enhancement`, `work`, `maintenance` |
| Severity | Labels containing the severity word (e.g., `high`, `critical`, `severity-high`) |
| Status (in-progress) | Labels containing `progress` or `wip` |

## Status Mapping

GitHub Issues have an `open` / `closed` state plus optional state reason (`completed`, `not_planned`). Map generic status:

| Generic | Write | Read back from |
| ------- | ----- | -------------- |
| planned | open, no `in-progress` label | open, no `in-progress` label |
| in-progress | open + label `in-progress` (or Project Status field "In Progress" when `epic-tracker.project` is set) | open + label `in-progress` (or the Project Status field) |
| done | closed + reason `completed` | closed + reason `completed`, or closed with no reason |
| cancelled | closed + reason `not_planned` | closed + reason `not_planned` |

When `epic-tracker.project` is set and the Project has a Status field, prefer the Project field over labels.

## Milestone

Milestone is a native repo-level GitHub Milestone, independent of the Projects v2 layer. It carries only a title here; never set a due date, so the materialized milestone stays dateless (a user may add one in the UI; leave it untouched).

Resolve a milestone name by reading before writing: fetch the repo's milestones and reuse the one whose title is exactly that name, including one a user created in the UI. Match on the name itself, not semantically — the milestone name is the phase name. When none has that title, create it in the repo with no due date. Then set it on the Issue.

Only an epic carries a milestone; the caller supplies it on `create_epic` or `set_milestone` and never on a story, bug, or task.

## Operations

### Issue Type Detection (runtime)

Detected once per session and cached in memory. Run before the first operation that assigns an artifact type.

1. Infer repo from `git remote get-url origin` (extract `owner/name`).
2. Determine repo owner kind via the active channel (`gh api repos/{owner}/{repo}` when CLI is active, or equivalent MCP call):
   - `owner.type == "User"`: personal/user-owned repo — Issue Types unavailable. Cache `issue_types: {}` and fall back to Label Matching.
   - `owner.type == "Organization"`: continue to step 3.
3. Query the org's issue types via the active channel (`gh api orgs/{org}/issue-types` when CLI is active, or equivalent MCP call).
4. If types are found, cache detected names in memory (keys: `epic`, `story`, `bug`, `task` → org-configured names; may differ from defaults, e.g., "Chore" instead of "Task").
5. If no types found or query fails: cache `issue_types: {}` and fall back to Label Matching.

The cache lives for the session; a new session re-detects.

### create_epic

1. Create an Issue in the repo (inferred from `git remote get-url origin`): `title` -> Issue title, `body` -> Issue body. The Sub-issues panel is the source of truth for child hierarchy; the body carries no child list.
2. Apply artifact type:
   - session cache has `epic` issue type: assign it.
   - otherwise: match repo labels semantically for `epic` and assign; when nothing matches, tell the user and create the label.
3. When `milestone` is supplied, resolve it per Milestone below and set it on the Issue.
4. If `epic-tracker.project` is set: add the Issue to the Project.
5. Return Issue number and url.

### create_story

1. Require `epic_id` before creating anything — a story is always a child of an epic, and a dispatch without it is an error to surface, never an Issue to create unlinked.
2. Create an Issue in the repo (inferred from `git remote get-url origin`): `title` -> Issue title, `body` -> Issue body. The body carries the validated `### AC-N` Given/When/Then blocks verbatim — adapters do not transform AC structure, so a downstream consumer can parse these blocks back to structured AC. See [ac-validation.md](ac-validation.md) for the contract.
3. Attach the Issue as a sub-issue under the parent Epic named by `epic_id`.
4. Apply artifact type (session cache `story` issue type, or `story` label).
5. If `epic-tracker.project` is set: add to the Project.
6. Return Issue number and url.

### create_bug

1. Create an Issue in the repo (inferred from `git remote get-url origin`): `title` -> Issue title, `body` -> Issue body. The body carries the repro steps, signals, and workaround the draft holds.
2. If `epic_id` is provided: attach as sub-issue under that Epic. Otherwise create as standalone.
3. Apply artifact type (session cache `bug` issue type, or `bug` label).
4. If severity is provided: fetch repo labels, match semantically; assign the match, or tell the user and create the label when nothing matches.
5. If `epic-tracker.project` is set: add to the Project.
6. Return Issue number and url.

### create_task

1. Create an Issue in the repo (inferred from `git remote get-url origin`): `title` -> Issue title, `body` -> Issue body.
2. If `epic_id` is provided: attach as sub-issue under that Epic. Otherwise create as standalone.
3. Apply artifact type (session cache `task` issue type, or `task` label).
4. If `epic-tracker.project` is set: add to the Project.
5. Return Issue number and url.

### update_artifact

Rewrites an existing Issue's body. `sync.md` refetches immediately before calling this and confirms with the user when the Issue changed underneath — this adapter performs the write it is given.

1. Update the Issue's title and body via the active channel.
2. When a severity is supplied, re-map the severity label: fetch repo labels, match the new level semantically, remove the previously matched severity label and assign the new one. When nothing matches, tell the user and create the label.
3. Return success.

### update_status

1. Map generic status to GitHub state via the Status Mapping table.
2. For `done`: close the Issue with reason `completed`.
3. For `cancelled`: close the Issue with reason `not_planned`.
4. For `in-progress`: reopen the Issue when closed. Prefer the Project Status field when `epic-tracker.project` is set; otherwise fetch repo labels, match semantically (look for `progress` or `wip`); assign the match, or tell the user and create the label when nothing matches.
5. For `planned`: reopen the Issue when closed, and remove the `in-progress` label (or clear the Project Status field).

### set_parent

1. Inputs: `tracker_id` and the target `epic_id`.
2. Attach the Issue as a sub-issue under the epic named by `epic_id`, removing the previous parent link.
3. Return success.

### set_dependencies

GitHub has native, typed Issue dependencies (`blocked by` / `blocking`), maintained on both sides automatically.

1. Inputs: `tracker_id` and a list of blocker ids (sync.md supplies them directly — they are already tracker ids).
2. For each blocker, add a `blocked by` link via the active channel. When CLI is active: `gh issue edit {n} --add-blocked-by {blocker}`. Setting one side is enough; GitHub records `blocking` on the other.
3. Remove links no longer listed via the active channel. When CLI is active: `gh issue edit {n} --remove-blocked-by {blocker}`.
4. Return success.

Dependencies are Issue-to-Issue within the same repo; cross-repo blocking is not assumed.

### set_milestone

1. Inputs: `tracker_id` and `milestone` (a name).
2. Resolve it per Milestone below and set it on the Issue, replacing any previous one.
3. Return success.

### fetch_artifact

1. Fetch the Issue by id/number via the active channel.
2. Return: status (read back per the Status Mapping table), title, body, severity (from the matched severity label, when present), parent (the sub-issue parent, when present), blocked-by Issue numbers (via the dependencies endpoints, or `gh issue view --json blockedBy` when CLI is active), milestone (the Issue's milestone title, when present), url.

### list_artifacts

1. Query GitHub for items matching the filter — type maps to the issue type or its label fallback, epic maps to the sub-issue parent, status maps to the GitHub state via the Status Mapping table. `done` has no direct predicate: GitHub search cannot express "closed with no reason", so filter it as `is:closed -reason:"not planned"`.
2. Return summaries with id, title, status, and url — status is the generic value, never `open` / `closed`. The url is what a child artifact records in its `## References`.

## Error Handling

- Repo not accessible: route to GitHub auth setup.
- Sub-issue attach fails (permissions, cross-repo restriction): surface the error together with the already-created Issue's number and url, so the user can attach it in the tracker or discard it — the Issue exists even though the attach did not.
- `epic-tracker.project` set but Project not found: ask user to verify or offer to create.
- Issue type not found in org (type was deleted or renamed since it was cached): warn the user, drop the cached types, and fall back to label matching for this operation.
- Label missing in the repo: tell the user, then create it.
- API rate limit: surface the error, suggest waiting before retry.
