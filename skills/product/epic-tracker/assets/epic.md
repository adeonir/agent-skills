ALWAYS use this exact template structure:

````markdown
## Outcome

{{The result this epic delivers. One to three sentences.}}

MUST NOT contain: conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, scenario narratives, `§x.x` section numbers, document references, sibling epic names, roadmap language, a list of children, or implementation details. Requirement IDs (`FR/NFR`) belong in `## Requirements`, never the Outcome; `ADR-NNN` belongs in References.

## Why

{{The problem or opportunity that makes this result worth delivering.}}

## Scope

**In:**

- {{What's included, described by what users get}}

**Out:**

- {{What's explicitly excluded — stated in this epic's own terms, never naming the sibling that owns it. Example: "Multi-factor authentication" not "MFA epic"}}

## Success Criteria

{Remove this section when nothing sources one — the PRD's expected outcome, PRODUCT
positioning, or what the user stated. Finding no criterion is a result,
not a gap to fill.}

- {{Observable condition that says the epic delivered, checked after it ships. Example: "Password reset stops appearing among the top support contact reasons" not "FR-3 is satisfied"}}

MUST NOT contain: a restatement of a requirement (`## Requirements` owns what must hold), a metric with no source in the PRD, PRODUCT, or what the user stated, a date or deadline, or a condition phrased as a gate — a criterion is observed after the epic ships and closes nothing, since the epic closes when its children do.

## Requirements

{Remove this section when the epic derives from a feature PRD or feature design doc with no enumerated requirements, or from no PRD.}

- {{ID — statement. One PRD requirement this epic owns, as `FR-3 — <what it demands>`. The children operationalize these, each task condition linking back with its requirement id. Every requirement here must be coverable by a child inside this epic.}}

Example:

```markdown
- FR-3 — A signed-in user must be able to reset their password without contacting support.
- FR-4 — A reset link expires 15 minutes after it is issued.
```

MUST NOT contain: a statement that reads looser or stricter than the PRD's — the modal, the actor, the object, and every bound (timing, count, threshold) carry over unchanged. No `§x.x` section numbers, sibling names, roadmap refs, or `ADR-NNN` (a decision dependency → References).

## Open Questions

{Remove this section if nothing is undecided.}

- {{A decision that can change the scope or how the epic is broken down.}}

## References

{Durable pointers to what the tracker does not model, chosen for what
matters to this epic. Remove the section when there is nothing to point at;
a line saying "None" states nothing and rots the same as a stale link.

A project document link (a file in a repo, like a Design Doc) is an absolute URL or a
repo-relative path. A relative path resolves only when the tracker and the
file share a host — a GitHub tracker linking a file in the same GitHub repo;
across hosts (a Linear tracker pointing at a GitHub repo), use an absolute
URL. A feature source never enters this section; the epic body carries the
translated facts it needs.}

- {{A pointer relevant to this epic: a PRD, a design doc, an ADR, a UI design.}}

MUST NOT contain: a child list, a dependency list, roadmap references, or sibling epic names.
````

This is the tracker description; the dispatch inputs (title, `blocked_by`, `priority`, `milestone`) travel as metadata alongside it. The body opens at `## Outcome` — the tracker renders the title above the description, so no title heading belongs in the body.
