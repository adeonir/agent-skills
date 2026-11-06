ALWAYS use this exact template structure:

````markdown
## Summary

{{What this unit delivers and why. One to three sentences, one outcome.}}

MUST NOT contain: conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, `§x.x` section numbers, sibling task names, roadmap language, or implementation details. Requirement IDs (`FR/NFR`) belong at the end of a condition, never the Summary; `ADR-NNN` belongs in References.

## Acceptance Criteria

- [ ] {{Verifiable condition on what this task delivers.}} — {{FR-3}}
- [ ] {{Another condition. Omit the id when it maps to no requirement.}}

{Each line is one condition, one outcome. The ` — FR-3` ending names one parent-epic requirement (`FR/NFR`) and is optional. See [ac-validation.md](../references/ac-validation.md) for the contract.}

MUST NOT contain: a condition observed on a surface a sibling task owns (relocate it to that task), a condition satisfied by something no artifact here builds — platform, runtime, service, or library behavior nobody implements and nobody can fail — a condition that restates a sibling's deliverable or anything listed in Out of Scope, or a condition per error path, edge case, or message the source leaves open (move it to Open Questions).

## Out of Scope

{Keep this section when an exclusion was decided — work cut, a capability
deferred, a boundary settled against a neighbour. Remove it when none was;
a task nobody drew a line around has no boundary to state.}

- {{What this task explicitly does not cover — stated in this task's own terms, never naming the sibling that covers it. Example: "Email-based password reset" not "the reset-via-SMS task"}}

MUST NOT contain: sibling task names — state each boundary in terms of what this task does not cover, never where the excluded work lives.

## Open Questions

{Remove this section if nothing is undecided. Capture what is open so a
fresh session knows what to ask, not re-decide.}

- {{Unknown to resolve. A cross-cutting foundational decision may be marked blocked and suggest an ADR to settle it — never generate the ADR here.}}

MUST NOT contain: an unknown that gates no condition in this task (move it to the task whose domain it gates), or an authored ADR (suggest one, never generate it).

## References

{Durable pointers to what the tracker does not model, chosen for what
matters to this task. The parent epic and every dependency are tracker
relations, not lines here. Remove the section when there is nothing to
point at; a line saying "None" states nothing and rots the same as a
stale link.

A doc link (a file in a repo, like a Design Doc) is an absolute URL or a
repo-relative path. A relative path resolves only when the tracker and the
file share a host — a GitHub tracker linking a file in the same GitHub repo;
across hosts (a Linear tracker pointing at a GitHub repo), use an absolute
URL.

A feature source never enters this section; the body carries the translated
facts it needs.}

- {{A pointer relevant to this task: a design doc, a UI design, an ADR-NNN it depends on, a source link.}}

MUST NOT contain: the parent epic or a dependency (tracker relations), or a feature source.
````

This is the tracker description; the dispatch inputs (title, epic id, `blocked_by`, `priority`, `estimate`) travel as metadata alongside it. The body opens at `## Summary` — the tracker renders the title above the description, so no title heading belongs in the body.
