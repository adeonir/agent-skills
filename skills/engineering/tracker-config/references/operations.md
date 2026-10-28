# Tracker Operations

Generic issue and relationship contracts independent of content authoring.

## When to Use

Load before executing tracker reads or writes.

## Operations

| Operation | Required inputs | Optional inputs | Result |
|-----------|-----------------|-----------------|--------|
| create_issue | title, body | type, parent_id, blocked_by, severity, priority, estimate, milestone | id, url, revision, applied fields |
| create_epic | title, body | priority, milestone | create_issue with type epic and no parent |
| create_story / create_bug / create_task | title, body | parent_id, blocked_by, severity for bug, priority, estimate, milestone | create_issue with named type |
| fetch_artifact | id or URL | none | normalized issue |
| list_artifacts | destination | type, parent_id, status, query, pagination cursor | summaries and next cursor |
| update_artifact | id, changed fields | title, body, severity, priority, estimate | verified changed fields |
| update_status | id, status | none | normalized status |
| set_parent | id, parent_id or null | none | parent ID or null |
| set_dependencies | id, blocked_by list | none | reconciled blocker IDs |
| set_milestone | id, milestone or null | none | milestone or null |

Accept `epic_id` as an alias for parent_id on typed creates; reject conflicting values. A bare intent or another issue type can use create_issue without classification. Do not impose an issue-body template or transform supplied Markdown.

## Normalized fields

Return destination, id, title, body, type, status, parent_id, blocked_by, blocking, severity, priority, estimate, milestone, revision, and url when available. Summaries contain id, title, status, and url. Use null for an absent supported field; report unsupported or unreadable fields explicitly rather than treating them as absent. Keep service-native IDs alongside display identifiers where required for writes.

Statuses: planned, in-progress, done, cancelled. Priorities: urgent, high, medium, low. Priority, severity, and estimate are independent and never inferred from each other or from issue position. Estimates are supplied numbers in the existing team scale; typed epics take no estimate. Preserve existing unspecified metadata. Ask when a native state or label mapping is ambiguous.

## Field values and clearing

Validate supplied fields before any write. Omission leaves an existing field unchanged; on creation it leaves the field to the tracker default. Reject fields outside the selected operation's contract. Do not convert null, an empty string, or an empty list into one another.

| Field | Accepted value | Explicit clearing |
|-------|----------------|-------------------|
| title | Nonempty string | Not supported; reject null, empty or whitespace-only strings, and lists |
| body | String, preserved verbatim | Empty string clears the description; reject null and lists |
| type | Nonempty classification string on creation | Omit for an unclassified issue; reject null, empty strings, and lists |
| status | One of the generic statuses | Not supported; reject null, empty strings, and lists |
| priority | One of the generic priorities, or null | Null removes the mapped priority value; never substitute low |
| severity | Nonempty severity string, or null | Null removes only mapped severity metadata |
| estimate | Finite number, or null; booleans are not numbers | Null clears the estimate; zero is a supplied value, not a clearing instruction |
| parent_id | Resolvable issue ID/URL, or null | Null removes the parent association without deleting the parent issue |
| milestone | Nonempty milestone name/ID, or null | Null removes the association without deleting the milestone |
| blocked_by | List of resolvable issue IDs/URLs | Empty list clears blockers; reject null and strings |

Only the fields explicitly accepting null above accept it; reject empty strings and lists for those fields unless their row permits them. On creation, null for a nullable field requests no value or association. Check whether the active channel can express the requested clearing operation; if it cannot, apply the unsupported-capability handling before writing instead of substituting an empty string, zero, or another value. Refetch to verify both clears and retained unspecified fields.

## Relations and write outcomes

Read the existing relation set before modifying it. set_dependencies adds requested missing blockers and removes only blockers omitted from the explicitly supplied complete list; an empty list clears them. Repeated writes converge on the same set. Reject self-links and known hierarchy/dependency cycles. Resolve all referenced issues before writing; never silently drop a missing blocker.

Obtain the revision marker and a snapshot of affected fields from the initial fetch; these are internal execution metadata, not required caller inputs. If the caller supplies a revision, treat it as an expected-revision precondition and compare it with the initial fetch before proceeding. Immediately before each write, refetch and compare with the snapshot; preserve unrelated changes and return overlapping conflicts to the caller for redrafting or user resolution. Use a conditional write when supported. Without an atomic precondition or revision marker, compare the affected fields immediately before writing and report that concurrency protection is best-effort. Refresh the snapshot after each verified write in a multi-part operation.

Classify outcomes as succeeded, failed-before-write, partial, or unknown. Return the created issue's ID and URL even when a later relationship write fails. A retry resumes incomplete work; it never creates a second issue to repair a relation. A failed read or incomplete page is not evidence that an issue does not exist.
