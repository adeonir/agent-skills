ALWAYS use this exact template structure:

````markdown
## Question

{{The question this spike must answer. One question, phrased so the answer is a decision, a measurement, or a recommendation.}}

MUST NOT contain: a proposed answer, conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, `§x.x` section numbers, sibling artifact names, or roadmap language.

## Why

{{Why the answer is needed now and which work it unblocks.}}

MUST NOT contain: a proposed answer, conversation narrative, or decision history.

## Scope

{{What will be investigated: the options to compare, the systems to read, the constraints to respect.}}

## Out of Scope

{Keep this section when an exclusion was decided. Remove it when none was.}

- {{What this spike does not investigate or implement, in this spike's own terms.}}

MUST NOT contain: sibling artifact names — state each boundary in terms of what this spike does not cover, never where the excluded work lives.

## Exit Criteria

- [ ] {{The main question is answered, with the evidence behind the answer.}}
- [ ] {{The relevant alternatives, trade-offs, and risks are recorded.}}
- [ ] {{The resulting decision or recommendation is documented.}}
- [ ] {{The follow-up work is identified. Omit when the answer needs none.}}

{Adapt each line to this spike, and add a line for any condition the answer must meet, such as a measured threshold. Each line is one verifiable condition. See [ac-validation.md](../references/ac-validation.md) for the contract.}

MUST NOT contain: a condition that presumes the answer, a condition no output of this spike can show, or a requirement link.

## Expected Deliverable

{{Where the answer is recorded and in what form: an ADR, a decision in the spec, a throwaway prototype, a benchmark, a report.}}

## References

{Durable pointers to what the tracker does not model, chosen for what
matters to this spike. The parent epic and every dependency are tracker
relations, not lines here. Remove the section when there is nothing to
point at; a line saying "None" states nothing and rots the same as a
stale link.

A doc link (a file in a repo, like a Design Doc) is an absolute URL or a
repo-relative path. A relative path resolves only when the tracker and the
file share a host; across hosts, use an absolute URL.}

- {{A pointer relevant to this spike: a doc, a link, material the investigation starts from.}}

MUST NOT contain: the parent epic or a dependency (tracker relations).
````

This is the tracker description; the dispatch inputs (title, epic id, `blocked_by`, `priority`, `estimate`) travel as metadata alongside it. The body opens at `## Question` — the tracker renders the title above the description, so no title heading belongs in the body.
