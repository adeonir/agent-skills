# GitHub Adapter

Translate generic epic-tracker operations into GitHub primitives via the
GitHub MCP (or `gh` CLI when MCP is unavailable). Loaded by
[../sync.md](../sync.md) when `tracker.kind: github`.

## Model

Every artifact except Release is an Issue. Artifact type is carried by
org-level Issue Types when available, or by a label fallback.
Hierarchy is always expressed via Issue sub-issue parent links —
never Milestones, never Projects.

| Artifact | Issue type / label | Sub-issue role |
|----------|---------------------|----------------|
| Epic     | `Epic`              | always parent |
| Story    | `Story`             | always child of an Epic |
| Bug      | `Bug`               | optional child of Epic or Story; may be standalone |
| Issue    | `Task` (or org default) | optional child of Epic or Story; may be standalone |
| Release  | GitHub Release tag (separate primitive, not an Issue) | n/a |

Bug and Issue are distinct artifacts with different purpose/body
(severity + repro steps vs. plain description); both have optional
parent linkage.

Sub-issues are a native Issues feature (GraphQL `addSubIssue`) —
independent of Projects v2. The Issues source repository must have
sub-issues enabled.

## Orthogonal Layers

Two opt-in layers wrap the same Issue substrate. Both are independent
of hierarchy and of each other.

| Layer | What it adds | Config |
|-------|--------------|--------|
| **Milestones** | Date-bound grouping for releases or campaigns. Issue belongs to at most one Milestone. Does not encode Epic→Story. | `use_milestones: true` |
| **Projects v2** | Board/roadmap views and custom fields (status, priority, sprint). Issues are added as Project items. Does not encode Epic→Story. | `project_number: <n>` |

Neither layer changes how Issues are created or how parent/child links
are formed. Issue creation flow is identical with or without them.

## Issue Types vs Labels

GitHub has two classification mechanisms with different scopes:

- **Issue types**: configured at the **org level** — shared across all
  repos in the organization. When the org has issue types, every repo
  has them consistently. Bootstrap detects once; no per-repo variation.
- **Labels**: configured at the **repo level** — each repository defines
  its own label set. Never hardcode label names or colors; always query
  the repo's existing labels before assigning (see Label Matching below).

Issue Types are an **org-only feature**. Personal/user-owned repos
(`github.com/{user}/{repo}` where `{user}` is an account, not an org)
do not have access to Issue Types under any circumstance. For these
repos the adapter skips Issue Type detection at bootstrap and operates
in **labels-only mode** — every artifact is classified by repo labels.

When org issue types are unavailable (or repo is user-owned), the
adapter falls back to artifact labels (`epic`, `story`, `bug`, `task`)
matched semantically against the repo's existing labels, never created
automatically.

## Label Matching

Labels are repo-specific. Before assigning any label, always fetch the
repo's label list:

```
GET /repos/{owner}/{repo}/labels
```

Match semantically against the needed concept (artifact type, severity,
status). If no match is found, surface the available labels to the user
and ask which to use (or skip). Never create labels automatically.

Concepts that use labels:

| Concept | Match strategy |
|---------|---------------|
| Artifact type: Epic | Labels containing `epic` |
| Artifact type: Story | Labels containing `story`, `feature`, `user-story` |
| Artifact type: Bug | Labels containing `bug`, `defect`, `fix` |
| Artifact type: Issue (generic task) | Labels containing `task`, `chore`, `enhancement`, `work`, `maintenance` |
| Severity | Labels containing the severity word (e.g., `high`, `critical`, `severity-high`) |
| Status (in-progress) | Labels containing `progress` or `wip` |
| Status (blocked) | Labels containing `blocked` or `on-hold` |

## Status Mapping

GitHub Issues have an `open` / `closed` state plus optional state reason
(`completed`, `not_planned`). Map generic status:

| Generic | GitHub state |
|---------|--------------|
| planned | open (no reason) |
| in-progress | open + label `in-progress` (or Project Status field "In Progress" when `project_number` is set) |
| done | closed + reason `completed` |
| blocked | open + label `blocked` |

When `project_number` is set and the Project has a Status field, prefer
the Project field over labels.

## Operations

### Bootstrap: Issue Type Detection

During bootstrap:

1. Determine repo owner kind via MCP or `gh api repos/{owner}/{repo}`:
   - `owner.type == "User"`: personal/user-owned repo. Set
     `issue_types: {}` immediately and skip the rest of this step —
     Issue Types are not available for user-owned repos.
   - `owner.type == "Organization"`: continue to step 2.
2. Query the org's issue types via MCP or
   `gh api orgs/{org}/issue-types`.
3. If types are found, store the detected names in config:
   ```yaml
   issue_types:
     epic: Epic
     story: Story
     bug: Bug
     task: Task
   ```
   Names may differ from defaults (e.g., the org may use "Chore" instead
   of "Task"). Store whatever name the org configured.
4. If no types found or query fails: set `issue_types: {}` in config.
   Adapter falls back to artifact labels via Label Matching.

Re-detect on demand via "configure tracker".

### create_epic

1. Strip the `## Stories` section from the body before push. The
   section is local-only — GitHub's native Sub-issues panel is the
   source of truth for child hierarchy. Drop the heading and all
   bullets up to (but not including) the next `##` heading.
2. Create an Issue in the configured `repo` with the stripped body.
3. Apply artifact type:
   - `issue_types.epic` set: assign that Issue Type.
   - otherwise: match repo labels semantically for `epic` and assign;
     surface available labels and ask if no match.
4. If `project_number` is set: add the Issue to the Project.
5. If `use_milestones` is true and a milestone is supplied: assign it.
6. Return Issue number and url.

### create_story

1. Create an Issue in the `repo` with title, body, and AC. The body
   must include the validated `### AC-N` Given/When/Then blocks
   verbatim — adapters do not transform AC structure. The planner
   subagent (consumer in a separate repo) parses these blocks back to
   structured AC. See [../ac-validation.md](../ac-validation.md) for
   the contract.
2. Attach the Issue as a sub-issue under the parent Epic (`epic_id`
   required). Stories are always children of an Epic.
3. Apply artifact type (`issue_types.story` or `story` label).
4. If `project_number` is set: add to the Project.
5. If `use_milestones` is true and the Epic has a Milestone: inherit
   it unless overridden.
6. Return Issue number and url.

### create_bug

1. Create an Issue in the `repo` with title, repro steps, severity,
   and any other Bug-specific fields.
2. If `parent_id` is provided: attach as sub-issue under that parent
   (Epic or Story). Otherwise create as standalone.
3. Apply artifact type (`issue_types.bug` or `bug` label).
4. If severity is provided: fetch repo labels, match semantically;
   assign if found, surface labels and ask otherwise.
5. If `project_number` is set: add to the Project.
6. If `use_milestones` is true and a milestone is supplied: assign it.
7. Return Issue number and url.

### create_issue

Generic task/chore artifact — distinct from Bug (no severity, no repro
steps, plain description body).

1. Create an Issue in the `repo` with title and body.
2. If `parent_id` is provided: attach as sub-issue under the parent
   (Epic or Story). Otherwise create as standalone.
3. Apply artifact type (`issue_types.task` or `task` label).
4. If `project_number` is set: add to the Project.
5. If `use_milestones` is true and a milestone is supplied: assign it.
6. Return Issue number and url.

### create_release

1. Create a Release in the `repo` against the target commit (default:
   current HEAD or `main`).
2. Inputs: `name` -> tag name (e.g., `v1.2.0`), `title` -> release title,
   `body` -> release notes (auto-generate from linked Issues when
   possible), `target_date` -> draft/scheduled release.
3. Link Issues to the Release via release notes.
4. Return Release id and url.

Releases are independent of Milestones. A team can use Milestones for
campaign-style grouping and Releases for shipped versions, or either,
or neither.

### update_status

1. Map generic status to GitHub state via the Status Mapping table.
2. For `done`: close Issue with reason `completed`.
3. For `planned` -> `in-progress`: prefer Project Status field when
   `project_number` is set; otherwise fetch repo labels, match
   semantically (look for `progress` or `wip`); assign if found, skip
   with a note if not.
4. For `blocked`: prefer Project Status field when present; otherwise
   match repo labels semantically (`blocked` or `on-hold`).

### fetch_artifact

1. Fetch the Issue, Milestone, or Release by id/number via MCP.
2. Return: state (mapped from open/closed + labels or Project fields),
   title, body, labels, sub-issue parent (when present), url.

### list_artifacts

1. Query GitHub for items matching the filter (parent issue, state,
   label, milestone, project).
2. Return summaries with id, title, state, url.

## Sub-Issues Detection

Hierarchy requires the sub-issues feature on the source repository.
During bootstrap:

1. Probe via GraphQL whether `addSubIssue` is available on the repo.
2. If unavailable: warn the user and ask whether to proceed without
   hierarchy (every artifact is standalone — Stories cannot be linked
   to Epics). Persist the choice in config (`sub_issues: disabled`).

There is no legacy "classic Projects" fallback. When sub-issues are
disabled, Stories are simply created without a parent — the model
flattens, but artifact creation continues.

## Error Handling

- Repo not accessible: route to GitHub MCP auth setup.
- Sub-issues feature disabled: warn user; offer to proceed without
  hierarchy or to abort.
- `project_number` set but Project not found: ask user to verify config
  or offer to create.
- Milestone not found (when `use_milestones` is true and a milestone is
  supplied): ask user to verify or offer to create.
- Issue type not found in org (type was deleted or renamed after
  bootstrap): warn user, suggest re-running "configure tracker" to
  re-detect; fall back to label matching for this operation.
- Severity or status label not found in repo: surface available labels
  to user, ask which to use or confirm to skip; never create labels
  automatically.
- Release tag already exists: ask user whether to overwrite, append,
  or change the tag name.
- API rate limit: surface the error, suggest waiting before retry.
