# Design Doc

A Google-style Design Doc: the technical design and the trade-offs behind it — lean and focused.

## Load first

Read [discovery.md](../references/discovery.md) at the start of discovery, and [quality.md](../references/quality.md) before writing to disk. When `docs/tech/design-doc.md` already exists, follow [reconcile.md](../references/reconcile.md) and update only the requested parts.

## Boundaries

The document records how the system is built, why the team chose that design, and which decisions have ADRs. Write one when the project has technical choices with real trade-offs, and keep it as short as the design allows.

**Boundary with PRD:** the Design Doc never reframes the product. Context recaps the project in 1-2 paragraphs and links to the PRD. Goals/Non-Goals are technical (latency, throughput, isolation), not product (DAU, conversion, NPS). It is not visual or UI design, and not an exhaustive technical spec.

**Boundary with ADR:** the Design Doc carries the design and the trade-offs behind it. ADRs record individual decisions. Both coexist and reference each other. When several options remain open, keep the decision here with `Record = —`; when it is final, create the ADR, set `Record` to `ADR-NNN`, and link the ADR back to this section.

## When NOT to Write a Design Doc

- The work is a trivial bug fix or single-line change
- No meaningful technical decisions exist (no trade-offs, no architecture choices)
- The project is too early to commit to any technical direction — capture as PRD discovery, return when there is a technical stance to record

## Workflow

```text
document absent  → discovery → analysis → drafting
document present → update requested parts (reconcile.md)
```

Check whether `docs/tech/design-doc.md` exists. If absent, run discovery, analysis, and drafting. If present, update only the requested parts by following [reconcile.md](../references/reconcile.md). Discovery covers context, design, trade-offs, and cross-cutting concerns. Analysis prepares the `Record` column that links decisions to ADRs. Run the quality checks before writing.

### Phase 1: Discovery

Load [discovery.md](../references/discovery.md) for the shared interview method and critical review.

**Check Existing Context:**

Apply [discovery.md](../references/discovery.md) `## Reading Project Files`, then look for `docs/product/PRD.md` and ADRs under `docs/adr/`. Read them for context only. Summarize the PRD in Context and link to it instead of copying its prose. Use existing ADR IDs in the Alternatives Considered `Record` column.

| PRD Section | Feeds Design Doc |
|-------------|------------------|
| Problem Statement | Context (1-2 paragraph recap, link to PRD) |
| Goals & Non-Goals | Goals/Non-Goals (technical translation only) |
| Scope | Scope hint for Context (link, do not duplicate) |
| NFRs | Goals (measurable targets) and cross-cutting concerns where they shape the design |

If no PRD exists, gather the required context during discovery.

#### Topic 1: Context & Goals

**Opening questions:**

- What is being built, and what problem on the technical side does it solve?
- What constraints shape the design? (technical, business, regulatory, team)
- What are the technical goals — and the explicit non-goals?

**Ask follow-up when:**

- Scope vague → "Where does this system stop?"
- No constraints → "What limits the design — stack, team, regulation?"
- Goals product-shaped → "What's the technical target behind that KPI?"

**Complete when:** clear technical framing with measurable goals and explicit non-goals.

#### Topic 2: The Design

**Opening questions:**

- What is the high-level shape — components, boundaries, and how they fit the surrounding system?
- Which data, interfaces, or flows does the design depend on?

**Ask follow-up when:**

- Components ungrouped → "What does this own?"
- The design is a list of tech with no shape → "How do the pieces relate?"

**Complete when:** the design can be drawn (a component / system-context sketch) and its key pieces are named to the depth the decisions require — no more.

#### Topic 3: Alternatives & Trade-offs

**Opening questions:**

- What were the real decisions, and what was weighed for each?
- What was chosen, what was rejected, and why?

**Ask follow-up when:**

- A choice has no alternative → "Was anything else considered, or is this forced?"
- Reasoning thin → "What's the trade-off you're accepting?"

**Complete when:** each significant decision has its chosen / rejected / reasoning captured.

#### Topic 4: Cross-cutting Concerns

**Opening questions:**

- Which cross-cutting concerns actually shape this design — security/privacy, observability, operations, testing?

**Ask follow-up when:**

- A concern is named but has no design impact → drop it
- A concern matters but lacks detail → "How does it change the design?"

**Complete when:** the concerns that affect the design are addressed; the rest are left out (not marked N/A).

### Phase 2: Analysis

Synthesize discovery into the design:

1. Draft the system-context / component sketch
2. Identify the key decisions and the trade-offs behind each
3. For each alternative, set the `Record` column to `—` or `ADR-NNN`
4. Present analysis to the user before drafting

For key decisions, weigh axes like complexity vs. maintainability, performance vs. development speed, flexibility vs. simplicity, build vs. buy, lock-in vs. managed services.

### Phase 3: Drafting

Use the template below. Run the checks in [quality.md](../references/quality.md) before writing, then write the Design Doc to its path and report a brief prose summary in chat (up to 2-3 paragraphs) — the path and the key decisions recorded. Do not paste the full document.

**Drafting notes:**

- Context is 1-2 paragraphs plus the PRD link — never recap Problem Statement, Personas, or Journeys.
- Goals are technical; translate product KPIs into technical targets ("support 10k concurrent users", not "grow DAU 30%").
- The design describes itself to the depth the decisions need — no exhaustive coverage checklist.
- Alternatives Considered is the heart; the Record column defaults to `—` until an ADR is created.
- Mark unknowns as Open Questions rather than inventing technical answers.

## Design Doc Template

For a new document, read `<this-skill>/assets/design-doc.template.md`, copy its exact structure, remove every comment, and replace every square-bracket slot. For an existing document, follow [reconcile.md](../references/reconcile.md); use the template only to check structure and never copy it over unchanged content.

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

Do not size the Design Doc by a fixed tier. Keep it as short as the design allows. A small service with a few decisions can use one page. A system with several services and trade-offs needs more detail. Add content only when a decision needs it.

## Guidelines

- Lead with the technical decisions and their trade-offs — that is the doc's value
- Keep Context succinct; never duplicate PRD prose
- Goals are technical, measurable, verifiable
- Use Mermaid for diagrams — version-control friendly
- Cover cross-cutting concerns only where they shape the design
- Track ADR linkage via the Record column
- Update the document when implementation reveals new structure or decisions

**On diagrams:** Mermaid throughout; a system-context diagram is highly recommended; ER or sequence diagrams when relationships or flows are non-trivial.

## ADR Linkage

Create an ADR when the team accepts a decision in the Alternatives Considered table, the decision affects people beyond the authors, or future engineers will need it without reading the full Design Doc.

Process:

First check the row's `Record` column. If it already reads `ADR-NNN`, read that ADR before deciding whether the record needs an update. Otherwise:

1. Create the ADR (see [adr.md](adr.md)). Number sequentially.
2. Update the Design Doc row: set `Record` to `ADR-NNN`.
3. The ADR's References section links back to the Design Doc's Alternatives Considered section.

Rows with `Record = —` are design-doc-only records of trade-offs explored along the way.

## Updating an Existing Design Doc

If `docs/tech/design-doc.md` exists, read it and update only what changed: a decision, component, resolved question, or structure that no longer matches the implementation. Preserve unrelated sections and follow [reconcile.md](../references/reconcile.md).

Set `updated` to the current date and preserve `created`. Report any change that conflicts with a linked ADR or an unchanged section.

## Anti-Pattern: Implementation Manual Without Trade-offs

A Design Doc must explain the alternatives, trade-offs, and reasons behind its choices. A document that only lists implementation steps is a task list. Omit a choice from Alternatives Considered when it has no meaningful trade-off. If the project has no decisions with trade-offs, it does not need a Design Doc.

## Anti-Pattern: Product Prose in Technical Sections

Summarize the project in Context with one or two paragraphs and a PRD link. Do not repeat the Problem Statement, Personas, or Journeys. Translate product NFRs into technical targets instead of repeating product KPIs. Remove repeated product content and link to the PRD.

## Anti-Pattern: Exhaustive Coverage

A Design Doc is not a full technical specification. Include testing, deployment, observability, or backups only when they affect the design or involve a real trade-off. Omit sections that do not explain a decision.

## Output

Save to: `docs/tech/design-doc.md`.
