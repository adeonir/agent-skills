# GitHub Adapter

Translate generic epic-tracker operations into GitHub primitives. Loaded by [sync.md](sync.md) when `epic-tracker.kind: github`. The sync ref decides whether to use MCP or CLI for each call (`epic-tracker.method` and `epic-tracker.fallback`); this adapter implements each operation through both channels.

## When to Use

Loaded by `sync.md` when `epic-tracker.kind` is `github`. Not a direct trigger.

## Model

Every artifact is an Issue. Artifact type is carried by org-level Issue Types when available, or by a label fallback. Hierarchy is always expressed via Issue sub-issue parent links — never Projects.

| Artifact | Issue type / label | Sub-issue role |
| -------- | ------------------ | -------------- |
| Epic | `Epic` | always parent |
| Story | `Story` | always child of an Epic |
| Bug | `Bug` | optional child of Epic or Story; may be standalone |
| Task | `Task` (or org default) | optional child of Epic; may be standalone |

Bug and Task are distinct artifacts with different purpose/body (severity + repro steps vs. plain description); both have optional parent linkage.

Sub-issues are a native Issues feature (GraphQL `addSubIssue`) — independent of Projects v2, available to anyone with triage permission on the repository.

## Orthogonal Layers

One opt-in layer wraps the same Issue substrate, independent of hierarchy.

| Layer | What it adds | Activation |
| ----- | ------------ | ---------- |
| **Projects v2** | Board/roadmap views and custom fields (status, priority, sprint). Issues are added as Project items. Does not encode Epic→Story. | `git config epic-tracker.project-number <n>` |

This layer does not change how Issues are created or how parent/child links are formed. Issue creation flow is identical with or without it.

## Integration Channel

Each operation below is implemented for both MCP and CLI. The caller (`sync.md`) selects the channel based on `epic-tracker.method` and `epic-tracker.fallback`. When an operation specifies an MCP call, the CLI equivalent is used when the CLI channel is active. If a capability is unavailable in one channel, surface it and let the caller decide whether to try the other channel.

## Issue Types vs Labels

GitHub has two classification mechanisms with different scopes:

- **Issue types**: configured at the **org level** — shared across all repos in the organization. When the org has issue types, every repo has them consistently. Bootstrap detects once; no per-repo variation.
- **Labels**: configured at the **repo level** — each repository defines its own label set. Never hardcode label names or colors; always query the repo's existing labels before assigning (see Label Matching below).

Issue Types are an **org-only feature**. Personal/user-owned repos (`github.com/{user}/{repo}` where `{user}` is an account, not an org) do not have access to Issue Types under any circumstance. For these repos the adapter skips Issue Type detection at bootstrap and operates in **labels-only mode** — every artifact is classified by repo labels.

When org issue types are unavailable (or repo is user-owned), the adapter falls back to artifact labels (`epic`, `story`, `bug`, `task`) matched semantically against the repo's existing labels, never created automatically.

## Label Matching

Labels are repo-specific. Before assigning any label, always fetch the repo's label list:

```text
GET /repos/{owner}/{repo}/labels
```

Match semantically against the needed concept (artifact type, severity, status). If no match is found, surface the available labels to the user and ask which to use (or skip). Never create labels automatically.

Concepts that use labels:

| Concept | Match strategy |
|---------|---------------|
| Artifact type: Epic | Labels containing `epic` |
| Artifact type: Story | Labels containing `story`, `feature`, `user-story` |
| Artifact type: Bug | Labels containing `bug`, `defect`, `fix` |
| Artifact type: Task | Labels containing `task`, `chore`, `enhancement`, `work`, `maintenance` |
| Severity | Labels containing the severity word (e.g., `high`, `critical`, `severity-high`) |
| Status (in-progress) | Labels containing `progress` or `wip` |
| Status (blocked) | Labels containing `blocked` or `on-hold` |

## Status Mapping

GitHub Issues have an `open` / `closed` state plus optional state reason (`completed`, `not_planned`). Map generic status:

| Generic | GitHub state |
| ------- | ------------ |
| planned | open (no reason) |
| in-progress | open + label `in-progress` (or Project Status field "In Progress" when `epic-tracker.project-number` is set) |
| done | closed + reason `completed` |
| blocked | open + label `blocked` |

When `epic-tracker.project-number` is set and the Project has a Status field, prefer the Project field over labels.

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

Re-detect on demand via "configure tracker".

### create_epic

1. Strip the `## Stories` section from the body before push. The section is local-only — GitHub's native Sub-issues panel is the source of truth for child hierarchy. Drop the heading and all bullets up to (but not including) the next `##` heading.
2. Create an Issue in the repo (inferred from `git remote get-url origin`) with the stripped body.
3. Apply artifact type:
   - session cache has `epic` issue type: assign it.
   - otherwise: match repo labels semantically for `epic` and assign; surface available labels and ask if no match.
4. If `epic-tracker.project-number` is set: add the Issue to the Project.
5. Return Issue number and url.

### create_story

1. Create an Issue in the repo (inferred from `git remote get-url origin`) with title, body, and AC. The body must include the validated `### AC-N` Given/When/Then blocks verbatim — adapters do not transform AC structure, so a downstream consumer can parse these blocks back to structured AC. See [ac-validation.md](ac-validation.md) for the contract.
2. Attach the Issue as a sub-issue under the parent Epic (`epic_id` required). Stories are always children of an Epic.
3. Apply artifact type (session cache `story` issue type, or `story` label).
4. If `epic-tracker.project-number` is set: add to the Project.
5. Return Issue number and url.

### create_bug

1. Create an Issue in the repo (inferred from `git remote get-url origin`) with title, repro steps, severity, and any other Bug-specific fields.
2. If `parent_id` is provided: attach as sub-issue under that parent (Epic or Story). Otherwise create as standalone.
3. Apply artifact type (session cache `bug` issue type, or `bug` label).
4. If severity is provided: fetch repo labels, match semantically; assign if found, surface labels and ask otherwise.
5. If `epic-tracker.project-number` is set: add to the Project.
6. Return Issue number and url.

### create_task

Generic task/chore artifact — distinct from Bug (no severity, no repro steps, plain description body).

1. Create an Issue in the repo (inferred from `git remote get-url origin`) with title and body.
2. If `parent_id` is provided: attach as sub-issue under the parent (Epic). Otherwise create as standalone.
3. Apply artifact type (session cache `task` issue type, or `task` label).
4. If `epic-tracker.project-number` is set: add to the Project.
5. Return Issue number and url.

### update_status

1. Map generic status to GitHub state via the Status Mapping table.
2. For `done`: close Issue with reason `completed`.
3. For `planned` -> `in-progress`: prefer Project Status field when `epic-tracker.project-number` is set; otherwise fetch repo labels, match semantically (look for `progress` or `wip`); assign if found, skip with a note if not.
4. For `blocked`: prefer Project Status field when present; otherwise match repo labels semantically (`blocked` or `on-hold`).

### set_dependencies

GitHub has native, typed Issue dependencies (`blocked by` / `blocking`), maintained on both sides automatically. Every artifact is an Issue, so any of them can block any other.

1. Inputs: the Issue number and a list of blocker Issue numbers (resolved from paths by sync.md).
2. For each blocker, add a `blocked by` link via the active channel. When CLI is active: `gh issue edit {n} --add-blocked-by {blocker}`. Setting one side is enough; GitHub records `blocking` on the other.
3. Remove links no longer listed via the active channel. When CLI is active: `gh issue edit {n} --remove-blocked-by {blocker}`.
4. Return success.

Dependencies are Issue-to-Issue within the same repo; cross-repo blocking is not assumed.

### fetch_artifact

1. Fetch the Issue by id/number via the active channel.
2. Return: state (mapped from open/closed + labels or Project fields), title, body, labels, sub-issue parent (when present), blocked-by Issue numbers (via the dependencies endpoints, or `gh issue view --json blockedBy` when CLI is active), url.

### list_artifacts

1. Query GitHub for items matching the filter (parent issue, state, label, project).
2. Return summaries with id, title, state, url.

## Error Handling

- Repo not accessible: route to GitHub auth setup.
- Sub-issue attach fails (permissions, cross-repo restriction): surface the error together with the already-created Issue's number and url, so the user can attach it in the tracker or discard it — the Issue exists even though the attach did not.
- `epic-tracker.project-number` set but Project not found: ask user to verify or offer to create.
- Issue type not found in org (type was deleted or renamed since last detection): warn user, suggest re-running "configure tracker" to re-detect; fall back to label matching for this operation.
- Severity or status label not found in repo: surface available labels to user, ask which to use or confirm to skip; never create labels automatically.
- API rate limit: surface the error, suggest waiting before retry.
