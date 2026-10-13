# Design Doc

A lean project Design Doc: the technical foundation of the system and the reasons behind its stack.

## Load first

Read [discovery.md](../references/discovery.md) at the start of discovery, and [quality.md](../references/quality.md) before writing to disk. When `docs/tech/design-doc.md` already exists, follow [reconcile.md](../references/reconcile.md) and update only the requested parts.

## Boundaries

The document records how the system is built and why the stack was chosen. Write one when the project has technical choices worth recording, and keep it as short as the design allows.

**Boundary with PRD:** the Design Doc never reframes the product. It cites the PRD and its NFR IDs and does not restate them. It is not visual or UI design, and not an exhaustive technical spec.

**Boundary with ADR:** the Design Doc carries the foundation with one line of reasoning per stack choice. An ADR records a single decision and its trade-offs in full. When a stack choice has real trade-offs, create the ADR, add `ADR-NNN` to the stack item, and link the ADR back to the Stack section.

## When NOT to Write a Design Doc

- The work is a trivial bug fix or single-line change
- No meaningful technical choices exist (no stack, no architecture decisions)
- The project is too early to commit to any technical direction — capture as PRD discovery, return when there is a technical stance to record

## Workflow

```text
document absent  → discovery → drafting → report
document present → update requested parts (reconcile.md)
```

Check whether `docs/tech/design-doc.md` exists. If absent, run discovery and drafting. If present, update only the requested parts by following [reconcile.md](../references/reconcile.md). Run the quality checks before writing.

### Phase 1: Discovery

Load [discovery.md](../references/discovery.md) for the shared interview method and critical review.

**Check Existing Context:**

Apply [discovery.md](../references/discovery.md) `## Reading Project Files`, then look for `docs/product/PRD.md` and ADRs under `docs/adr/`. Read them for context only. Cite the PRD in References instead of copying its prose, and add the ID of an existing ADR to the stack item it records.

| PRD Section | Feeds Design Doc |
|-------------|------------------|
| Problem, Scope | Overview (a paragraph, no recap) |
| Non-Functional Requirements | Non-Functional Requirements (how each is met) |

If no PRD exists, gather the required context during discovery.

Each topic below uses two or three opening questions.

#### Topic 1: Overview & Stack

**Opening questions:**

- What is being built, and what does the system do in one paragraph?
- Which technologies were chosen for each layer, and why?

**Ask follow-up when:**

- Scope vague → "Where does this system stop?"
- A choice has no reason → "Why this over the alternatives?"
- A choice has real trade-offs → "Should this get its own ADR?"

**Complete when:** the system fits in one paragraph and every stack item has a one-line justification.

#### Topic 2: Architecture, Data & Integrations

**Opening questions:**

- What are the modules or layers, how do they communicate, and where does each responsibility live?
- Which main entities, relationships, and external services does the design depend on?

**Ask follow-up when:**

- Components ungrouped → "What does this own?"
- The design is a list of tech with no shape → "How do the pieces relate?"
- An external service is named → "What happens when it fails?"

**Complete when:** the design can be drawn (a component or system-context sketch) and the main entities and integrations are named to the depth the decisions require, no more.

#### Topic 3: Infra, NFRs & Conventions

**Opening questions:**

- Where does the system run, in which environments, and how does a change reach production?
- Which non-functional requirements shape the design, and how are they met?

**Ask follow-up when:**

- A requirement is named but has no design impact → drop it
- A requirement matters but lacks detail → "How does it change the design?"
- Conventions are not documented elsewhere → ask for the folder structure, code patterns, and testing approach

**Complete when:** hosting, environments, and CI/CD are stated, and each NFR that shapes the design has a way to be met. Leave out the rest instead of marking it N/A.

### Phase 2: Drafting

Use the template below. Run the checks in [quality.md](../references/quality.md) before writing, then write the Design Doc to its path, and reread it per [quality.md](../references/quality.md) `## Reread`.

**Drafting notes:**

- Overview is one paragraph plus the diagram, never a recap of the PRD.
- Each stack item carries one line of justification; the full trade-offs live in the ADR.
- Data Model, External Integrations, and Conventions are optional. Include them only when a decision needs them.
- Non-Functional Requirements cite each NFR by ID and state how the design meets it, never the requirement text.
- Mark unknowns as TBD rather than inventing technical answers.
- `sources` lists the files and URLs the user supplied as input. References lists related documents that exist, such as the PRD and ADRs.

### Phase 3: Report

Report the path, what the document holds in one to three sentences — the stack and architecture recorded, or what changed on an update — and any TBD it carries. Never paste the document.

## Design Doc Template

For a new document, read `<this-skill>/assets/design-doc.template.md`, copy its exact structure, remove every comment, and replace every square-bracket slot. For an existing document, follow [reconcile.md](../references/reconcile.md); use the template only to check structure and never copy it over unchanged content.

## Design Doc Schema

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| Overview | The system in one paragraph plus a high-level diagram | Topic 1 |
| Stack | Technology per layer with a one-line justification and the ADR when one exists | Topic 1 |
| Architecture | Modules or layers, how they communicate, where each responsibility lives | Topic 2 |
| Data Model (optional) | Main entities and relationships | Topic 2 |
| External Integrations (optional) | Third-party services and behavior on failure | Topic 2 |
| Infra & Deploy | Hosting, environments, CI/CD | Topic 3 |
| Non-Functional Requirements | How the design meets each NFR it shapes | Topic 3 |
| Conventions (optional) | Folder structure, code patterns, testing, when not documented elsewhere | Topic 3 |
| References | PRD, ADRs, and other related documents that exist | All phases |

## Sizing

Do not size the Design Doc by a fixed tier. Keep it as short as the design allows. A small service can use one page. Add content only when a decision needs it.

## Guidelines

- Lead with the stack and architecture; that is the doc's value
- Keep Overview to one paragraph; never duplicate PRD prose
- Use Mermaid for diagrams — version-control friendly
- Cover Infra, NFRs, and optional sections only where they shape the design
- Track ADR linkage by adding `ADR-NNN` to the stack item it records
- Update the document when implementation reveals new structure or decisions

**On diagrams:** Mermaid throughout; a system-context diagram in Overview is highly recommended; ER or sequence diagrams when relationships or flows are non-trivial.

## ADR Linkage

Create an ADR when a stack choice has real trade-offs, affects people beyond the authors, or future engineers will need it without reading the full Design Doc.

First check the stack item. If it already names `ADR-NNN`, read that ADR before deciding whether the record needs an update. Otherwise:

1. Create the ADR (see [adr.md](adr.md)). Number sequentially.
2. Add `ADR-NNN` to the stack item.
3. The ADR's References section links back to the Design Doc's Stack section.

Stack items without an ADR are recorded only here, with their one-line justification.

## Updating an Existing Design Doc

If `docs/tech/design-doc.md` exists, read it and update only what changed: a stack choice, component, or structure that no longer matches the implementation. Preserve unrelated sections and follow [reconcile.md](../references/reconcile.md).

Set `updated` to the current date and preserve `created`. Report any change that conflicts with a linked ADR or an unchanged section.

## Anti-Pattern: Product Prose in Technical Sections

Summarize the system in Overview with one paragraph. Do not repeat the PRD's Problem or Audience, and do not restate NFR text. Cite the PRD and the NFR IDs and remove repeated product content.

## Anti-Pattern: Exhaustive Coverage

A Design Doc is not a full technical specification. Include the optional sections, testing, observability, or backups only when they affect the design. Omit sections that do not explain a decision.

## Output

Save to: `docs/tech/design-doc.md`.
