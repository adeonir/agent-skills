# Design Doc

Single project-wide living technical document. Captures high-level
strategy, trade-offs, and a prescriptive plan for the system — domain,
conventions, architecture, security, observability, testing, and
deployment — alongside the alternatives considered along the way.

## When to Use

When authoring or updating the technical document for a software
project. The Design Doc is the source of truth for technical strategy:
how the system is built, why those choices were made, and which
decisions have been formalized as ADRs.

One Design Doc per project. The doc lives through the project's
lifecycle, evolving from greenfield draft to shipped baseline to
historical record. Significant decisions extracted from its
Alternatives Considered table become ADRs while the row remains in
the design doc with an `ADR-NNNN` reference, preserving narrative
history.

**Boundary with PRD:** the Design Doc never reframes the product. The
Context section recaps the project in 1-2 paragraphs and links to the
PRD. Goals/Non-Goals are technical (latency, throughput, isolation),
not product (DAU, conversion, NPS).

**Boundary with ADR:** the Design Doc carries the living narrative of
trade-offs. ADRs carry the immutable record of accepted decisions.
Both coexist; they reference each other.

## When NOT to Write a Design Doc

- The work is a trivial bug fix or single-line change
- No meaningful technical decisions exist (no trade-offs, no
  architecture choices)
- The project is too early to commit to any technical direction —
  capture as PRD discovery, return when there is a technical stance
  to record

## Workflow

```text
discovery --> analysis --> drafting
```

Discovery expands into 5 topics covering the full surface of the
project. Analysis synthesizes findings, gates the trade-off
discussion, and prepares the Record column for ADR linkage. Drafting
loads quality gates before presenting.

### Phase 1: Discovery

Load [discovery.md](discovery.md) for shared interview patterns and
critical posture.

**Check Existing Context:**

Look for existing PRD at `docs/product/prd.md` and ADRs at
`docs/adr/`.

If PRD found: read and extract product context as input. The Design
Doc Context section will recap and link, never copy paragraphs
verbatim.

If ADRs found: list them; existing decisions seed the Alternatives
Considered Record column.

| PRD Section | Feeds Design Doc |
|-------------|------------------|
| Problem Statement | Context (1-2 paragraph recap, link to PRD) |
| Goals & Metrics | Goals/Non-Goals (technical translation only) |
| Scope (MoSCoW) | Scope hint for Context (link, do not duplicate) |
| User Journeys | Domain entity transitions and Architecture API surface |
| NFRs | Goals (measurable targets) and 3.5-3.8 cross-cutting |

If no PRD: open discovery from scratch.

#### Topic 1: System Overview

**Opening questions:**

- What is being built at a high level?
- What constraints shape the design? (technical, business, regulatory)
- What is explicitly out of scope technically?
- What system landscape surrounds this — upstream services,
  downstream consumers, neighboring teams?

**Deepen when:**

- Scope is vague → "What are the technical boundaries of this
  system? Where does it stop?"
- No constraints mentioned → "Are there technical limitations? Team
  size constraints? Regulatory requirements?"
- Missing context → "How does this fit into the existing landscape?"

**Sufficient when:**

- Clear technical overview with explicit boundaries
- Constraints identified
- Surrounding system context understood

#### Topic 2: Domain & Data

**Opening questions:**

- What are the core entities the system manipulates?
- What invariants must always hold? (rules the system cannot violate)
- Are there bounded contexts (sub-models with different rules)?
- How is data stored, accessed, and retained?

**Deepen when:**

- Entities described only by name → "What attributes? What identifies
  this entity uniquely?"
- Invariants implicit → "What must always be true? What can never
  happen?"
- Storage hand-waved → "Which engine? Read/write pattern? Retention?"
- Lifecycle vague → "What states can this entity be in? Which
  transitions are valid?"

**Sufficient when:**

- Each core entity has a purpose statement and key invariants
- Each entity has a storage decision (engine, access pattern,
  retention)
- Bounded contexts surfaced when relevant
- Business rules captured

#### Topic 3: Architecture & Conventions

**Opening questions:**

- What is the high-level component breakdown?
- What tech stack (languages, frameworks, infra)?
- What APIs/interfaces are exposed or consumed?
- What conventions govern the codebase — API contract shape, naming,
  versioning?

**Deepen when:**

- Components ungrouped → "Which responsibility does this own? Which
  entity does it serve?"
- API surface implicit → "What endpoints? Auth model? Contract shape?"
- No conventions discussed → "How are errors formatted? How is
  pagination handled? Idempotency keys?"
- Naming undefined → "How are entities named? Endpoints? Events?"

**Sufficient when:**

- Component diagram drafted
- Tech stack table populated
- API contracts and conventions defined
- Each component owns explicit responsibility

#### Topic 4: Security & Compliance

**Opening questions:**

- What auth mechanism applies?
- What data classifications exist? (PII, secrets, public)
- What regulations apply? (LGPD, GDPR, HIPAA, PCI-DSS, etc.)
- How are secrets managed?

**Deepen when:**

- Auth ignored → "How is authentication handled? Authorization model?
  RBAC? ABAC?"
- PII not classified → "What personal data flows through? Where is it
  stored? Encrypted?"
- Compliance hand-waved → "Which jurisdictions apply? What does each
  require?"
- Audit absent → "What needs an audit trail? How long is it retained?"

**Sufficient when:**

- Auth and authz approach defined
- PII handling explicit (transport, at rest, in logs)
- Compliance requirements identified or explicitly none
- Audit and secrets management captured

#### Topic 5: Operations

**Opening questions:**

- How is the system observed? (metrics, logs, traces)
- What alerts page someone?
- What is the testing strategy?
- How does code reach production? (CI/CD, rollout, rollback)

**Deepen when:**

- Observability missing → "How will you know if the system is
  working? When it isn't?"
- Testing absent → "What is tested? How? What coverage target?"
- Deployment vague → "How does code reach prod? Phased rollout?
  Migration path? Rollback trigger?"
- Backups not discussed → "What gets backed up? How often? Recovery
  RTO/RPO?"

**Sufficient when:**

- Observability strategy is concrete (specific metrics, log format,
  alert conditions)
- Testing types and CI integration defined
- Deployment pipeline and rollback plan captured
- Backup and recovery posture explicit when stateful

### Phase 2: Analysis

Synthesize discovery into technical analysis:

1. Map system boundaries and external integrations
2. Draft system context and component diagrams
3. Identify key design decisions and evaluate alternatives
4. Document trade-offs explicitly
5. For each alternative considered, set the `Record` column to `—`
   (design-doc-only) or `ADR-NNNN` (already formalized)
6. Confirm coherence: every entity has storage; every component owns
   responsibility; every NFR maps to a section
7. Present analysis to user for feedback before drafting

**Architecture Evaluation:**

For key decisions, consider:

- Complexity vs. maintainability
- Performance vs. development speed
- Flexibility vs. simplicity
- Build vs. buy
- Vendor lock-in vs. managed services

### Phase 3: Drafting

Use the template below. Load [quality.md](quality.md) before
presenting the draft to the user.

**Drafting notes:**

- Context section is 1-2 paragraphs plus PRD link. Resist the urge to
  recap Problem Statement, Personas, or Journeys in full.
- Goals are technical. Translate product KPIs into technical
  derivatives (e.g., "support 10k concurrent users" rather than "grow
  DAU by 30%").
- Sub-sections under section 3 may be omitted when not applicable.
  Note "N/A" explicitly with a one-line reason rather than leaving
  empty placeholders.
- Alternatives Considered Record column is mandatory. Default is `—`
  until an ADR is created.
- Mark unknowns as Open Questions in section 5 rather than inventing
  technical answers.

## Design Doc Template

ALWAYS use this exact template structure. Sub-sections under section
3 may be omitted if not applicable; mark omissions explicitly.

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
---

# Design Doc: {{Project Name}}

## 1. Context & Scope

{{One or two paragraphs: what is being built, why it matters, and
the surrounding system landscape. Keep it succinct — assume the
reader can follow up via the PRD link below for product depth.}}

> See PRD: `docs/product/prd.md`

---

## 2. Goals / Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable technical objective — latency,
  throughput, isolation guarantee, zero-downtime target, etc.}}

### Non-Goals

- {{Thing that could reasonably be a goal but is explicitly chosen
  not to be a goal. Note: non-goals aren't negated goals like "The
  system shouldn't crash"; they are choices like "ACID compliance"
  that were considered and excluded.}}

---

## 3. Architecture

### 3.1 Architecture

```mermaid
{{Component diagram showing internal modules and their relationships}}
```

- **Components:** {{apps, packages, services — list as needed}}
- **Runtime boundaries:** {{processes, deployment units, isolation
  zones}}

### 3.2 System Context

```mermaid
{{System-context diagram showing this project within the broader
technical landscape}}
```

- **Actors:** {{users, services, schedulers triggering this system}}
- **External services:** {{upstream and downstream dependencies}}

### 3.3 Conventions

- **API:** {{error format, pagination, idempotency, versioning}}
- **Naming:** {{entities, endpoints, events — capture as patterns
  emerge}}
- **Versioning:** {{strategy — semver, calver, header-based, etc.}}

### 3.4 Domain

- **Bounded Contexts:** {{name + scope of each context}}

| Entity | Purpose | Key Invariants | Storage |
|--------|---------|----------------|---------|
| {{Entity}} | {{One-line purpose}} | {{Invariant}} | {{Engine + pattern}} |

- **Lifecycle states:** {{state transitions per entity}}
- **Business rules:** {{cross-entity rules that anchor decisions}}

```mermaid
erDiagram
    {{Entity relationships and key fields}}
```

- **Ubiquitous glossary:** {{terms shared between code, docs, and
  conversation}}

### 3.5 Security & Compliance

- **Transport and storage:** {{TLS, encryption at rest, key
  management}}
- **PII handling:** {{classification, storage location, redaction
  policy}}
- **Auth:** {{mechanism — JWT, OAuth2, API keys}}
- **Authz:** {{model — RBAC, ABAC, scope-based}}
- **Audit log:** {{what is recorded, retention}}
- **Regulatory:** {{applicable jurisdictions and how compliance is
  met}}

### 3.6 Observability

- **Metrics:** {{key metrics and what they measure}}
- **Logging:** {{format, levels, structured fields}}
- **Alerts:** {{table of alert name, condition, severity}}
- **Dashboards:** {{primary dashboards and audience}}
- **Tracing:** {{when applicable — propagation, sampling}}

### 3.7 Testing

| Type | Scope | Tools | Coverage Target |
|------|-------|-------|-----------------|
| {{Unit}} | {{Business logic}} | {{Framework}} | {{Target}} |
| {{Integration}} | {{APIs, DB}} | {{Framework}} | {{Target}} |
| {{E2E}} | {{Critical flows}} | {{Framework}} | {{Target}} |

- **Test environments:** {{local, preview, staging}}
- **Flake handling:** {{strategy}}
- **CI integration:** {{when tests run, blocking vs reporting}}

### 3.8 Deployment

- **CI/CD:** {{pipeline stages, build and artifact strategy}}
- **Release strategy:** {{phased, canary, blue-green, feature flags}}
- **Migrations:** {{schema/data migration approach, ordering}}
- **Backups:** {{frequency, retention, recovery RTO/RPO}}
- **Rollback plan:** {{trigger conditions, procedure}}
- **Environments:** {{preview, staging, prod parity}}
- **Secrets management:** {{vault, env vars, rotation policy}}

---

## 4. Alternatives Considered

| Decision | Chosen | Rejected | Reasoning | Record |
|----------|--------|----------|-----------|--------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{trade-offs, why this choice}} | {{— or ADR-NNNN}} |

**Record column:**

- `—` means the design doc is the only record of this decision.
- `ADR-NNNN` means the decision has been formalized as an ADR. The
  row is frozen post-acceptance; reversals create a superseding ADR
  and a new row, never an edit to the original row.

---

## 5. Open Questions

- [ ] {{Question or uncertainty that needs resolution before
      implementation can proceed}}

---

## 6. References

- {{Link to PRD}}
- {{Links to ADRs that record extracted decisions}}
- {{External documentation, RFCs, prior art}}
````

## Design Doc Schema

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Context & Scope | Project recap + PRD link | Topic 1 |
| 2. Goals / Non-Goals | Technical objectives and exclusions | Topic 1 (with PRD NFR translation) |
| 3.1 Architecture | Component breakdown, runtime boundaries | Topic 3 |
| 3.2 System Context | External landscape | Topic 1 + Topic 3 |
| 3.3 Conventions | API contract, naming, versioning | Topic 3 |
| 3.4 Domain | Entities, lifecycle, storage, rules | Topic 2 |
| 3.5 Security & Compliance | Auth, PII, regulatory | Topic 4 |
| 3.6 Observability | Metrics, logs, alerts | Topic 5 |
| 3.7 Testing | Strategy, environments, CI | Topic 5 |
| 3.8 Deployment | CI/CD, rollback, backups, secrets | Topic 5 |
| 4. Alternatives Considered | Decisions, trade-offs, ADR refs | Analysis |
| 5. Open Questions | Unresolved technical TBDs | All phases |
| 6. References | PRD, ADRs, external | All phases |

## Sizing

Drop tier-based sizing. Use Google's informal guidance:

- **Mini design doc** (1-3 pages): early-stage project, single
  service, few entities, minimal cross-cutting concerns. Many 3.x
  sub-sections may be marked N/A.
- **Larger design doc** (10-20 pages): multi-service, multi-team, or
  production-critical project. All sub-sections typically populated.

The doc grows organically with the project. Section presence is
"include when applicable", never tier-locked.

## Guidelines

- Focus on the technical strategy and trade-offs — this is the
  primary value of a Design Doc
- Keep Context succinct; never duplicate PRD prose
- Goals are technical, measurable, and verifiable
- Use Mermaid for diagrams — version-control friendly
- Document alternatives with trade-offs; track ADR linkage via the
  Record column
- Omit sub-sections under 3 when not applicable; mark N/A explicitly
  with one-line reason
- Update the doc when implementation reveals new structure or new
  decisions
- One Design Doc per project; major rewrites spawn a new doc
  (`design-doc-v2.md`) and supersede the old via frontmatter

**On Diagrams:**

- Use Mermaid throughout
- System-context diagram is highly recommended
- ER diagrams in 3.4 when entity relationships are non-trivial
- Sequence diagrams under 3.x as needed for complex flows

## ADR Linkage

When a decision in the Alternatives Considered table matures —
because the team committed to it, because it has stakeholders
beyond the immediate authors, or because future engineers will need
to understand it without re-reading the design doc — extract it
into an ADR.

Process:

1. Create the ADR (see [adr.md](adr.md)). Number sequentially.
2. Update the design doc row: set `Record` to `ADR-NNNN`.
3. The ADR's References section links back to the design doc
   section anchor (e.g., `docs/tech/design-doc.md#4-alternatives-considered`).
4. The design doc row is now frozen. Subsequent reversals create a
   superseding ADR and a new row in the design doc, never an edit
   to the original row.

Rows with `Record = —` remain editable; they are design-doc-only
records of trade-offs explored along the way.

## Design Doc Lifecycle

Frontmatter `status` field tracks the doc through the project:

```text
draft --> accepted --> in-progress --> shipped --> superseded
```

- **draft**: Discovery and initial trade-off mapping. Editable
  freely.
- **accepted**: Design approved. Architecture and Conventions stable;
  Alternatives rows being formalized into ADRs.
- **in-progress**: Implementation underway. Doc updated when reality
  reveals structural changes; new decisions append to Alternatives.
- **shipped**: System in production. Doc becomes the historical
  entry point. Incremental updates allowed; major changes spawn
  `design-doc-v2.md`.
- **superseded**: Replaced by a newer Design Doc. Frontmatter
  `superseded-by` populated.

Stages 1-4 mirror Google's design doc lifecycle: Creation and rapid
iteration → Review → Implementation and iteration → Maintenance and
learning. The skill adds an explicit `superseded` terminal state for
major rewrites.

## Anti-Pattern: Implementation Manual Without Trade-offs

A Design Doc that says "this is how we are going to implement it"
without covering alternatives, trade-offs, or decision rationale is
not a Design Doc — it is a task list. The value of the doc is the
reasoning behind each choice. If there are no meaningful trade-offs
for a decision, leave it out of Alternatives Considered; if no
decision in the project has trade-offs, the project does not need a
Design Doc.

## Anti-Pattern: Product Prose in Technical Sections

The Context section recaps the project in 1-2 paragraphs and links
to the PRD. It does not restate the Problem Statement, list
Personas, or walk through Journeys. The Goals section translates
product NFRs into technical targets; it does not echo product KPIs.
If a reviewer cannot tell whether they are reading the PRD or the
Design Doc, the Context section is too long or the Goals are not
technical. Cut and link.

## Anti-Pattern: Empty Sub-Section Padding

Sections 3.1-3.8 cover every common axis of a technical project,
but not every project needs every axis. A read-mostly internal API
may have no migration strategy; a stateless component may have no
backup posture. Mark these "N/A — {{one-line reason}}" or omit the
heading entirely. Leaving the template placeholder behind creates
noise and signals that the project has not been thought through.

## Output

Save to: `docs/tech/design-doc.md`.

The Design Doc is a living document that follows the project
lifecycle. Update it as the project evolves; supersede with a new
Design Doc when the system undergoes a major rewrite.
