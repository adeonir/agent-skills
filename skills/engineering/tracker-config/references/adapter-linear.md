# Linear Adapter

Map generic issue operations to the connected Linear MCP tools.

## When to Use

Load after resolving a Linear destination.

## Channel and capabilities

Use MCP only. Discover the connected server and its fully qualified tool names from the host catalog; inspect each tool's input contract before calling it. Do not assume tool names or a REST/SDK alternative. Probe the configured team and project with read-only calls. Check support for each requested field and relation before writing. If the MCP lacks a needed operation, return that limitation; do not change trackers or discard fields.

## Destination and issue fields

Every issue belongs to the configured team and project. Keep the supplied body verbatim. A generic create_issue has no forced type label; a supplied type uses an existing team label matched to the intended concept. Prefer exact label matches, and ask when multiple labels fit. List labels before assigning; obtain approval before creating missing labels. Severity uses a separate severity label and never determines priority.

Use a parent issue for hierarchy, not a project or milestone. Preserve native IDs and display identifiers separately. Read and write parent, dependency, and milestone relations through tools that explicitly support them. Keep unrelated labels and relations intact.

## Status and priority

Read the team's workflow states and map their native types, not display names:

| Generic status | Write target type | Read types |
|----------------|-------------------|------------|
| planned | unstarted; backlog when unstarted is absent | triage, backlog, unstarted |
| in-progress | started | started |
| done | completed | completed |
| cancelled | canceled | canceled |

When a target type is missing or has multiple suitable states, ask which state to use. Creation leaves the team's default state unless an explicit status operation follows.

Map urgent, high, medium, and low to the native priority field. Leave unspecified priority unchanged on update and at the team's default on creation. Set an estimate only when supplied, numeric, and enabled for the team. If estimates are disabled, report the limitation before a planned partial write. Do not change the team's estimate scale.

Apply explicit clearing from the operation contract: null priority selects the native no-priority value; null estimate clears the native estimate; null severity removes only mapped severity labels. For parent or milestone null, clear the association. Discover the MCP's actual clearing arguments; if unsupported, report the limitation before writing. Empty body means an empty description, and empty blocked_by means no blockers.

## Operation mapping

| Operation | MCP action |
|-----------|------------|
| create_issue and typed creates | Create an issue with title, description, team, project, and supported supplied fields; apply requested relations |
| fetch_artifact | Read issue fields, revision marker, parent, both dependency directions, and milestone |
| list_artifacts | Query within the configured project; map type, status, parent, and search filters; paginate completely |
| update_artifact | Update only supplied fields after the concurrency check |
| update_status | Set the resolved team workflow state |
| set_parent | Replace or clear the native parent link |
| set_dependencies | Compare native blocker relations and add/remove only the difference |
| set_milestone | Associate or clear a project milestone in the configured project |

For milestones, list the project's milestones and reuse an exact name. Obtain approval before creating a missing milestone; leave target dates untouched. No supplied milestone means no association change. Relation orientation must match the MCP tool contract; read back both sides rather than guessing which issue blocks which.

## Failure handling

Preserve the draft and report auth, rate-limit, missing-object, or capability errors. After partial creation, return the existing ID and URL with missing relations or metadata. Use the shared operation contract for revision conflicts, retries, and unknown write outcomes. Never fall back outside MCP.
