# GitHub Adapter

Map generic issue operations to GitHub MCP or the authenticated gh CLI.

## When to Use

Load after resolving a GitHub destination and primary/fallback channels.

## Channels and capabilities

Use the configured repository explicitly for every operation; do not rely on the CLI's working-directory inference. With MCP, discover fully qualified tool names and inspect their input contracts. With CLI, inspect installed `gh` command help before relying on flags or JSON fields. Use the CLI's supported issue/project operations; where installed gh exposes a needed capability through its authenticated API command, inspect its documentation before using it. Do not introduce a separate REST client, SDK, or credential store.

Probe repository read access and any configured Project before writes. Preflight support for sub-issues, dependencies, issue types, and Project fields individually. A missing capability may use only the configured fallback; apply the shared unknown-write reconciliation rule before switching after a submitted write.

## Classification and metadata

Use native organization issue types when the active channel exposes them. Otherwise use existing repository labels matched to the supplied type. A generic issue without type needs no classification. Query labels before assigning; ask when matching is ambiguous or a new label is needed. Preserve unrelated labels. Keep severity, priority, and status concepts distinct even when their level words overlap.

When a Project is configured, add the issue to it before setting fields on the Project item. Resolve the Project by owner and number and retain its native ID and item ID. Prefer an existing single-select Priority field for priority; otherwise use an existing priority label. Match urgent/high/medium/low to actual options or labels, asking when ambiguous. Never create Project fields or options silently.

Write a numeric estimate only to an existing Project number field representing estimate/size/points. Without a suitable field, report the limitation before a partial write; never encode the estimate as a label. An omitted priority or estimate remains unchanged on update and is not inferred on creation.

Apply explicit clearing from the operation contract: null priority clears its mapped Project field or priority labels; null severity removes only mapped severity labels; null estimate clears the mapped Project number field rather than writing zero. Parent or milestone null removes only the association. Confirm that the selected channel supports each clear before writing. Empty body means an empty description, and empty blocked_by means no blockers.

## Status mapping

| Generic | GitHub state and metadata |
|---------|---------------------------|
| planned | Open; mapped planned/backlog Project status or no progress label |
| in-progress | Open; mapped active Project status or existing progress label |
| done | Closed, completed reason |
| cancelled | Closed, not-planned reason |

Prefer a configured Project's Status field when available. Resolve actual option names instead of assuming them. Keep the issue's open/closed state consistent with the requested generic status. On reads, distinguish closed reasons and use Project status or progress labels for open issues; surface conflicting or unmapped states rather than silently normalizing them. Treat a legacy closed issue with no reason as done only when no conflicting metadata exists.

## Operation mapping

| Operation | MCP or CLI action |
|-----------|-------------------|
| create_issue and typed creates | Create in the explicit repository, preserving body; apply requested type, Project membership, fields, and relations |
| fetch_artifact | Read issue, revision marker, type/labels, state/reason, Project fields, parent, dependencies, milestone, and URL |
| list_artifacts | List/search repository issues, excluding pull requests; apply type/status/parent filters and paginate |
| update_artifact | Edit only supplied fields after refetch and concurrency comparison |
| update_status | Reopen/close as required and reconcile mapped Project status or progress labels |
| set_parent | Attach to the requested parent, replacing an old link only when explicitly requested; null removes it |
| set_dependencies | Read current blockers, then add missing and remove omitted blockers |
| set_milestone | Resolve and assign a repository milestone, or clear it |

Keep issue numbers, native issue IDs, and Project item IDs distinct; use the identifier the selected tool requires. Validate hierarchy and dependency scope with the channel before writing; do not assume cross-repository support. A typed epic is an issue without a parent, not a Project.

Resolve milestones by exact title and obtain approval before creating one that is missing. Do not assign or erase due dates. Read normalized fields from their actual storage surface; an absent capability is not an absent relation.

## Failure handling

Return permission, auth, rate-limit, mapping, and capability errors with the resolved destination. Report any created issue ID/URL if later Project or relation writes fail. Do not create a second issue to repair failed metadata. Use the configured fallback only when it reaches the same repository and identity scope; if neither channel supports the operation, report it as unsupported.
