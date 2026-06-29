# Design Doc

A Google-style design doc: the technical design and the trade-offs behind it —
lean and focused.

## When to Use

When authoring or updating the technical design doc for a software project — the
source of truth for technical strategy: how the system is built, why those
choices were made, and which decisions have been formalized as ADRs. Write one
when there are real technical decisions to weigh; keep it as short as the design
allows.

**Boundary with PRD:** the design doc never reframes the product. Context recaps
the project in 1-2 paragraphs and links to the PRD. Goals/Non-Goals are technical
(latency, throughput, isolation), not product (DAU, conversion, NPS).

**Boundary with ADR:** the design doc carries the design and the trade-offs
behind it. ADRs carry the immutable record of individual accepted decisions. Both
coexist and reference each other.

## When NOT to Write a Design Doc

- The work is a trivial bug fix or single-line change
- No meaningful technical decisions exist (no trade-offs, no architecture choices)
- The project is too early to commit to any technical direction — capture as PRD
  discovery, return when there is a technical stance to record

## Workflow

```text
discovery → analysis → drafting
```

Discovery covers four lean topics — context, the design, the trade-offs, and
cross-cutting concerns. Analysis synthesizes findings and prepares the Record
column for ADR linkage. Drafting loads quality gates before presenting.

### Phase 1: Discovery

Load [discovery.md](discovery.md) for shared interview patterns and critical
posture.

**Check Existing Context:**

Look for an existing PRD at `docs/product/PRD.md` and ADRs at `docs/adr/`. Read
them for context only — their tokens never cross verbatim into the design doc.
Context recaps and links to the PRD; existing ADRs seed the Alternatives
Considered Record column.

| PRD Section | Feeds Design Doc |
|-------------|------------------|
| Problem Statement | Context (1-2 paragraph recap, link to PRD) |
| Goals & Non-Goals | Goals/Non-Goals (technical translation only) |
| Scope | Scope hint for Context (link, do not duplicate) |
| NFRs | Goals (measurable targets) and cross-cutting concerns where they shape the design |

If no PRD: open discovery with nothing to seed it.

#### Topic 1: Context & Goals

**Opening questions:**

- What is being built, and what problem on the technical side does it solve?
- What constraints shape the design? (technical, business, regulatory, team)
- What are the technical goals — and the explicit non-goals?

**Deepen when:**

- Scope vague → "Where does this system stop?"
- No constraints → "What limits the design — stack, team, regulation?"
- Goals product-shaped → "What's the technical target behind that KPI?"

**Sufficient when:** clear technical framing with measurable goals and explicit
non-goals.

#### Topic 2: The Design

**Opening questions:**

- What is the high-level shape — components, boundaries, and how they fit the
  surrounding system?
- What are the key pieces the design hinges on (data, interfaces, flows)?

**Deepen when:**

- Components ungrouped → "What does this own?"
- The design is a list of tech with no shape → "How do the pieces relate?"

**Sufficient when:** the design can be drawn (a component / system-context
sketch) and its key pieces are named to the depth the decisions require — no more.

#### Topic 3: Alternatives & Trade-offs

**Opening questions:**

- What were the real decisions, and what was weighed for each?
- What was chosen, what was rejected, and why?

**Deepen when:**

- A choice has no alternative → "Was anything else considered, or is this forced?"
- Reasoning thin → "What's the trade-off you're accepting?"

**Sufficient when:** each significant decision has its chosen / rejected /
reasoning captured.

#### Topic 4: Cross-cutting Concerns

**Opening questions:**

- Which cross-cutting concerns actually shape this design — security/privacy,
  observability, operations, testing?

**Deepen when:**

- A concern is named but has no design impact → drop it
- A concern clearly matters but is hand-waved → "How does it change the design?"

**Sufficient when:** the concerns that affect the design are addressed; the rest
are left out (not marked N/A).

### Phase 2: Analysis

Synthesize discovery into the design:

1. Draft the system-context / component sketch
2. Identify the key decisions and the trade-offs behind each
3. For each alternative, set the `Record` column to `—` or `ADR-NNNN`
4. Present analysis to the user before drafting

For key decisions, weigh axes like complexity vs. maintainability, performance
vs. development speed, flexibility vs. simplicity, build vs. buy, lock-in vs.
managed services.

### Phase 3: Drafting

Use the template below. Load [quality.md](quality.md) before presenting the draft.

**Drafting notes:**

- Context is 1-2 paragraphs plus the PRD link — never recap Problem Statement,
  Personas, or Journeys.
- Goals are technical; translate product KPIs into technical targets ("support
  10k concurrent users", not "grow DAU 30%").
- The design describes itself to the depth the decisions need — no exhaustive
  coverage checklist.
- Alternatives Considered is the heart; the Record column defaults to `—` until
  an ADR is created.
- Mark unknowns as Open Questions rather than inventing technical answers.

## Design Doc Template

ALWAYS use this exact template structure:

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
sources: []
---

# Design Doc: {{Project Name}}

## 1. Context & Scope

{{One or two paragraphs: what is being built, why it matters, and the
surrounding system landscape. Keep it succinct — the reader follows the PRD link
for product depth.}}

> See PRD: `docs/product/PRD.md`

## 2. Goals & Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable technical objective — latency, throughput,
  isolation guarantee, zero-downtime target, etc.}}

### Non-Goals

- {{A choice deliberately excluded — e.g. "ACID compliance" considered and not
  pursued. Not a negated goal like "shouldn't crash".}}

## 3. Design

{{The technical design: a high-level architecture and system-context (Mermaid
diagrams as needed), the key components and their responsibilities, and the
data/interfaces the design hinges on — to the depth the decisions require.
Describe the design; do not pad with exhaustive coverage of every axis.}}

```mermaid
{{System-context or component diagram}}
```

## 4. Alternatives Considered & Trade-offs

| Decision | Chosen | Rejected | Reasoning | Record |
|----------|--------|----------|-----------|--------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{trade-offs, why this choice}} | {{— or ADR-NNNN}} |

`—` = the design doc is the only record of this decision. `ADR-NNNN` = the
decision is formalized as an ADR; the row is then frozen (reversals create a
superseding ADR and a new row, never an edit).

## 5. Cross-cutting Concerns

{{Brief prose on the concerns that shape this design — security/privacy,
observability, operations, testing. Cover only what affects the design; leave
the rest out.}}

## 6. Open Questions

- [ ] {{Question or uncertainty to resolve before implementation can proceed}}

## 7. References

- {{Link to PRD}}
- {{Links to ADRs that record extracted decisions}}
- {{External documentation, RFCs, prior art}}
````

MUST NOT contain: product KPIs, personas, journey walkthroughs, requirement IDs,
or restated PRD prose — recap in 1-2 lines and link the PRD instead.

## Design Doc Schema

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Context & Scope | Project recap + PRD link | Topic 1 |
| 2. Goals & Non-Goals | Technical objectives and exclusions | Topic 1 |
| 3. Design | Architecture, components, key data/interfaces | Topic 2 |
| 4. Alternatives Considered & Trade-offs | Decisions, trade-offs, ADR refs | Topic 3 + Analysis |
| 5. Cross-cutting Concerns | Security, observability, ops, testing — where they shape the design | Topic 4 |
| 6. Open Questions | Unresolved technical TBDs | All phases |
| 7. References | PRD, ADRs, external | All phases |

## Sizing

No tier-based sizing — Google's informal guidance: as long as the design needs,
as short as it allows. A few decisions on a small service is a one-pager; a
multi-service system with many trade-offs runs longer. The doc grows with the
decisions, never with a section checklist.

## Guidelines

- Lead with the technical decisions and their trade-offs — that is the doc's value
- Keep Context succinct; never duplicate PRD prose
- Goals are technical, measurable, verifiable
- Use Mermaid for diagrams — version-control friendly
- Cover cross-cutting concerns only where they shape the design
- Track ADR linkage via the Record column
- Update the doc when implementation reveals new structure or new decisions

**On diagrams:** Mermaid throughout; a system-context diagram is highly
recommended; ER or sequence diagrams when relationships or flows are non-trivial.

## ADR Linkage

When a decision in the Alternatives Considered table matures — the team commits
to it, it has stakeholders beyond the authors, or future engineers will need it
without re-reading the design doc — extract it into an ADR.

Process:

1. Create the ADR (see [adr.md](adr.md)). Number sequentially.
2. Update the design doc row: set `Record` to `ADR-NNNN`.
3. The ADR's References section links back to the design doc's Alternatives
   Considered section.
4. The row is now frozen. Reversals create a superseding ADR and a new row,
   never an edit to the original.

Rows with `Record = —` remain editable — design-doc-only records of trade-offs
explored along the way.

## Updating an Existing Design Doc

The design doc is a living document: once it exists, you revise it in place rather
than regenerate it. There is no fresh-versus-rerun mode decision — every touch after
the first is an update.

Read the existing doc as input and scope the change to what actually moved: a new
decision, a new component, a resolved open question, or structure that drifted from
the implementation. Work that delta and leave the settled prose alone — an update is
not a rewrite, and it never pads the doc.

Respect what is frozen. Alternatives Considered rows recorded as an ADR (`Record =
ADR-NNNN`) are immutable — reverse them with a superseding ADR and a new row, never
an in-place edit (see the `## ADR Linkage` section above). The editable surface is
the design prose, rows with `Record = —`, and Open Questions.

Before presenting, re-run the gates in [quality.md](quality.md) against the result
and bump `updated` in the frontmatter, preserving `created`. The thing to catch is a
change that contradicts a frozen decision or an untouched section.

## Anti-Pattern: Implementation Manual Without Trade-offs

A design doc that says "this is how we implement it" without alternatives,
trade-offs, or rationale is not a design doc — it is a task list. The value is
the reasoning behind each choice. If a decision has no meaningful trade-off,
leave it out of Alternatives Considered; if no decision in the project has
trade-offs, the project does not need a design doc.

## Anti-Pattern: Product Prose in Technical Sections

Context recaps the project in 1-2 paragraphs and links to the PRD — it does not
restate the Problem Statement, list Personas, or walk through Journeys. Goals
translate product NFRs into technical targets; they do not echo product KPIs. If
a reviewer cannot tell whether they are reading the PRD or the design doc, cut
and link.

## Anti-Pattern: Exhaustive Coverage

A design doc is not a technical spec that fills every axis — testing strategy,
deployment pipeline, observability dashboards, backup posture — whether or not
the design hinges on them. Cover a concern only where it shapes the design or
carries a real trade-off. Padding the doc with sections that have no decision
behind them turns it back into the TDD this skill deliberately is not.

## Output

Save to: `docs/tech/design-doc.md`.
