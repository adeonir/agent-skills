# Technical Design Document (TDD)

Prescriptive technical plan for a component, service, or feature. Bundles Domain, Use Cases, System Flows, and Architecture into one consolidated artifact with cross-section coherence checks. Sized core/medium/large by project complexity — sizing dimensions depth, never skips sections.

## When to Use

When creating a prescriptive technical plan for a specific component, service, or feature before implementation. TDDs list concrete technical choices alongside the domain model, user journeys (as Cockburn-style use cases), and system-initiated flows, with structured sections that scale by project size.

**Key distinction from Design Doc:** Design Docs are informal documents focused on trade-offs and decision-making for ambiguous problems. TDDs are prescriptive — they tell the team exactly what to build, with what entities, through which use cases, and on what architecture. A project can have both: a Design Doc for ambiguous decisions and a TDD for the prescriptive plan.

## When NOT to Write a TDD

- The implementation is trivial with no architectural decisions
- A Design Doc already covers the technical plan in sufficient detail
- The component has no cross-cutting concerns (security, deployment, monitoring)
- The work is a bug fix or minor enhancement

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

```
Phase 0: Context & Sizing
  --> Phase 1: Domain
    --> Phase 2: Use Cases + System Flows
      --> Phase 3: Architecture
        --> Phase 4: Coherence Pass
          --> load quality.md --> present draft
```

Phase 4 can back-edge to any earlier phase when a coherence gap is mechanically fixable by re-running scoped discovery. Resolutions happen before the TDD is presented; no audit-trail section is written to the output.

Load [discovery.md](discovery.md) at the start of every phase for adaptive deepening, critical posture, and sufficiency gating.

### Phase 0: Context & Sizing

**Check existing context.**

Look for existing PRD at `.artifacts/docs/prd.md` and Design Doc at `.artifacts/docs/design.md`.

If PRD found: extract product context as starting input.
If Design Doc found: extract architectural context and decisions.

| PRD Section | Feeds TDD |
|-------------|-----------|
| Problem Statement | Overview |
| Goals & Metrics | Goals / Non-Goals |
| Scope (MoSCoW) | Scope |
| User Journeys | Use Cases (UC-N) |
| Business Rules | Domain invariants, UC steps |
| NFRs | Architecture (Security, Monitoring, Testing) |

| Design Doc Section | Feeds TDD |
|--------------------|-----------|
| Context & Scope | Overview |
| Design | Architecture |
| Cross-Cutting Concerns | Architecture (Security, Monitoring) |
| Alternatives Considered | Alternatives Considered |

When existing docs are found, ask which component this TDD covers.

If no existing docs: open discovery from scratch.

**Size the project.**

Determine project size from PRD signals and Phase 0 answers. If unclear, ask the user directly. Sizing dimensions section depth — every section in the template is always present, regardless of tier.

| Signal | Size |
|--------|------|
| Single service, few integrations, small team, 1-3 entities | Core |
| Multiple integrations, data modeling needed, security concerns, 4-10 entities | Medium |
| Cross-team, production-critical, migration, compliance, 10+ entities | Large |

**Critical section promotion.**

Some sub-sections promote regardless of tier:

| Project Type | Promoted Sub-Sections |
|--------------|----------------------|
| Payment / Auth / PII | 7.6 Security & Compliance |
| Production service | 7.7 Deployment & Rollback, 9 Monitoring & Observability |
| Migration | 11 Risks, 7.7 Deployment & Rollback |
| Infrastructure | 9 Monitoring & Observability, 11 Risks |

**Design Doc detection.**

If discovery surfaces a heavy trade-off (signals listed in [Design Doc Detection](#design-doc-detection) below), pause TDD and propose spinning a Design Doc.

**Phase 0 sufficiency:**

- [ ] Overview, problem, success criteria identified
- [ ] Size proposed and confirmed
- [ ] Critical-section promotions noted
- [ ] No unresolved Design Doc triggers

### Phase 1: Domain

Discover the entities, invariants, and bounded contexts that anchor every later section. Every UC step and Architecture decision will cite Domain content, so depth here calibrates the rest of the TDD.

**Opening questions:**

- What are the core entities (nouns the product manipulates)?
- What invariants must always hold (rules the system cannot violate)?
- What state transitions does each entity go through?
- Are there bounded contexts (sub-models with different rules)?

**Deepen when:**

- Entities described only by name → "What attributes? What identifies this entity uniquely?"
- Invariants implicit → "What must always be true about an Order? What can never happen?"
- Lifecycle vague → "What states can Order be in? Which transitions are valid?"
- Contexts blurred → "Does Order mean the same thing in checkout vs fulfilment?"

**Sufficient when:**

- Every PRD business rule (BR) maps to an invariant or UC step (deferred to Phase 4 if UC not yet drafted)
- Every entity has a clear purpose statement
- Lifecycle states are named (Core: bullets; Medium+: explicit transitions)
- Bounded contexts surfaced when relevant (always for Large)

**Output:** populate section `## 4. Domain` per tier depth (see [Tier Depth Matrix](#tier-depth-matrix)).

### Phase 2: Use Cases + System Flows

Trace user journeys (Use Cases, UC-N) and non-user triggers (System Flows, SF-N). Both cite Domain entities and state transitions from Phase 1. UC and SF discovery run in parallel within this phase — they share the same Domain base but answer different questions.

**Use Cases — opening questions:**

- For each PRD journey, what is the actor's goal?
- What is the main success scenario (numbered steps)?
- What extensions / failure paths exist?

**System Flows — opening questions:**

- What system triggers exist (cron, webhooks, scheduled jobs, event handlers)?
- What are the preconditions and effects of each?
- What failure modes need handling?

**Deepen when:**

- UC has no extensions → "What happens if X fails? Are there alternative paths?"
- UC step skips entity transition → "Which state does the Order move to here?"
- SF trigger unclear → "What invokes this? Time? External event? Internal cascade?"
- Background process implied by PRD but not surfaced → "Reconciliation runs daily — let's capture it as SF"

**Sufficient when:**

- Every PRD journey maps to ≥1 UC
- Every non-user trigger maps to ≥1 SF
- UC/SF steps cite Domain entities and state transitions
- Distinct ID ranges used (UC-1, UC-2... and SF-1, SF-2...)

**Output:** populate sections `## 5. Use Cases` and `## 6. System Flows` per tier depth.

### Phase 3: Architecture

Discover components, data, integrations, and operational concerns. Every component must own at least one UC or SF; every entity must have a storage decision; every NFR from the PRD must map to an Architecture choice.

**Opening questions:**

- What is the high-level component breakdown?
- What tech stack (languages, frameworks, infra)?
- How is data stored and accessed?
- What APIs / interfaces are exposed or consumed?
- What security, deployment, monitoring concerns apply?

**Deepen when:**

- Components ungrouped → "Which UC does this serve? Which entity does it own?"
- Storage hand-waved → "Which engine? Read/write pattern? Retention?"
- API surface implicit → "What endpoints? Auth model? Contract shape?"
- Security ignored → "Auth mechanism? Data at rest? PII classification?"
- Deployment absent → "Phased rollout? Rollback triggers? Migration path?"

**Sufficient when:**

- High-level diagram drafted
- Tech stack table populated
- Every UC/SF has an owner component or API
- Every Domain entity has a storage decision
- PRD NFRs map to Architecture decisions

**Output:** populate section `## 7. Architecture` and its sub-sections per tier depth.

### Phase 4: Coherence Pass

Diff the four content sections against each other and against the PRD. Resolve gaps before presenting. No persistent output section — coherence is enforced silently, the TDD ships clean.

**Cross-checks (run in order):**

| # | Check | Critical when | Warning when |
|---|-------|---------------|--------------|
| C1 | Domain ↔ UC entity refs resolve | UC names entity absent from Domain | UC uses entity but omits state transition |
| C2 | Domain ↔ SF entity refs resolve | SF mutates undefined entity | SF skips lifecycle transition |
| C3 | UC ↔ SF classification | UC triggered by system; SF triggered by user; duplicate IDs | Overlapping responsibility |
| C4 | Domain ↔ Architecture storage | Entity has no storage decision | Storage lacks access pattern |
| C5 | UC/SF ↔ Architecture ownership | UC/SF has no owner component or API | Endpoint exists with no UC/SF caller |
| C6 | PRD ↔ Journeys | PRD journey orphaned (no UC) | Journey covered by partial UC |
| C7 | PRD ↔ BR/NFR | BR has no enforcement (invariant or UC step); NFR has no Architecture decision | BR/NFR cited without metric or rule body |

**Gap classification:**

- **critical** → blocks output. Resolved via back-edge to phase or explicit waiver.
- **warning** → noted internally, output proceeds.
- **sizing-drift** → e.g., Core proposed but 8 entities + 6 UCs surfaced → propose promoting to Medium. Opt-in.

**Resolution paths:**

- **Back-edge to phase** — when the fix is mechanical (rename to match Domain, add missing entity, classify trigger). Agent re-enters the responsible phase scoped to the gap; no full discovery re-run.
- **Ask user** — when the fix requires judgment (waive with reason, change classification, restructure UC into SF). Agent surfaces the gap inline and waits.

Sizing drift is always user-confirmed: agent proposes promotion, user accepts or overrides.

**Phase 4 exit:**

- [ ] Zero critical gaps remain
- [ ] Warnings reviewed (kept internal; not written to output)
- [ ] Sizing confirms tier matches content
- [ ] Load [quality.md](quality.md), then present draft

## Design Doc Detection

When discovery surfaces decisions that span comparable options without an obvious winner, pause TDD and propose a Design Doc.

**Signals by phase:**

- **Phase 0:** user phrasing — "we don't know if X or Y", "two approaches we're considering", "trade-off between"
- **Phase 1:** 2+ candidate bounded-context partitions surface, no obvious winner
- **Phase 3:** comparison questions on storage engine, sync vs async, monolith vs services, build vs buy, framework choice
- **Phase 3:** NFR conflict (consistency vs availability, latency vs throughput) with no resolution

**On match, prompt:**

```
This decision space is trade-off heavy: {{summary}}.
Pause TDD and run a Design Doc? [yes | no | inline]
```

- **yes** → suspend TDD, switch to [design.md](design.md) workflow, resume TDD when Design Doc is approved
- **no** → mark trade-off as deferred, continue TDD with user's tentative choice
- **inline** → capture comparison in `## 10. Alternatives Considered` without spawning a separate doc

## TDD Template

ALWAYS use this exact template structure. Every section is always present; sizing controls depth per the [Tier Depth Matrix](#tier-depth-matrix).

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
size: {{core|medium|large}}
---

# TDD: {{Component Name}}

## 1. Overview

{{What is being built and why. Brief description of the component/service, its purpose, and the problem it solves.}}

---

## 2. Goals / Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable objective this component must achieve}}

### Non-Goals

- {{Explicit exclusion — something that could reasonably be a goal but is deliberately not}}

---

## 3. Scope

### In Scope

- {{Feature or responsibility this TDD covers}}

### Out of Scope

- {{What is explicitly excluded and why}}

---

## 4. Domain

### Entities

| Entity | Purpose | Key Invariants |
|--------|---------|----------------|
| {{Entity}} | {{One-line purpose}} | {{Invariant that must always hold}} |

### Bounded Contexts

- **{{Context}}:** {{entities included, why this boundary exists}}

<!-- Medium+: add entity attributes, lifecycle states, context map table, BR→entity coverage matrix -->
<!-- Large: add cross-context relationships diagram and ubiquitous-language glossary -->

---

## 5. Use Cases

| ID | Actor | Goal | PRD Journey |
|----|-------|------|-------------|
| UC-1 | {{Actor}} | {{User goal}} | {{J-N}} |

<!-- Medium+: add full Cockburn block per UC (below) -->
<!-- Large: + Extensions fully expanded, frequency, priority, perf constraints -->

### UC-1: {{Use Case Name}}

- **Trigger:** {{What initiates this use case}}
- **Preconditions:** {{What must be true to start}}
- **Main Success Scenario:**
  1. {{Step — cites Domain entity transition}}
- **Extensions:**
  - {{1a. Alternative path or failure mode}}
- **Postconditions:** {{Resulting state}}
- **Entity Transitions:** {{Entity X: state A → state B}}
- **References:** {{BR-N, EC-N from PRD}}

---

## 6. System Flows

| ID | Trigger | Effect | Source |
|----|---------|--------|--------|
| SF-1 | {{Time / Event / Internal}} | {{Resulting state change}} | {{PRD ref}} |

<!-- Core: one-line table only when non-user triggers exist -->
<!-- Medium+: add full block per SF (below) -->
<!-- Large: + retry/idempotency, sequence diagram, SLO targets -->

### SF-1: {{System Flow Name}}

- **Trigger:** {{Cron schedule / external event / internal cascade}}
- **Preconditions:** {{What must be true to start}}
- **Steps:**
  1. {{Step — cites Domain entity transition}}
- **Effects:** {{State changes, side effects}}
- **Failure Modes:** {{What can go wrong, how it's handled}}

---

## 7. Architecture

### 7.1 Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| {{Language}} | {{e.g. TypeScript 5.x}} | {{Primary language}} |
| {{Framework}} | {{e.g. Next.js 14}} | {{Web framework}} |
| {{Database}} | {{e.g. PostgreSQL 16}} | {{Primary data store}} |

### 7.2 High-Level Design

```mermaid
{{Component diagram showing internal modules and their relationships}}
```

### 7.3 System Context

```mermaid
{{System-context diagram showing this component within the broader system landscape}}
```

### 7.4 Component Interactions

{{How internal modules interact, key flows, request/response patterns. Cite UC-N and SF-N owners.}}

<!-- Medium+ -->

### 7.5 Data Model

```mermaid
erDiagram
    {{Entity relationships and key fields}}
```

- **Engine:** {{e.g. PostgreSQL 16}}
- **Access patterns:** {{Read-heavy, write-heavy, mixed}}
- **Retention:** {{Data lifecycle and retention policy}}

### 7.6 APIs / Interfaces

| Method | Path | Description | Auth | UC/SF |
|--------|------|-------------|------|-------|
| {{GET}} | {{/api/resource}} | {{List resources}} | {{required}} | {{UC-N}} |

{{Key request/response shapes, error formats, pagination strategy.}}

### 7.7 Security & Compliance

- **Auth:** {{Mechanism (JWT, OAuth2, API keys); authorization model (RBAC, ABAC)}}
- **Data Protection:** {{Encryption at rest and in transit; PII handling}}
- **Regulatory:** {{Applicable regulations (LGPD, GDPR, HIPAA, PCI-DSS) and compliance approach}}

<!-- Large -->

### 7.8 Deployment & Rollback

- **CI/CD:** {{Pipeline stages, build and artifact strategy}}
- **Release Strategy:** {{Phased rollout, canary, blue-green, big-bang; feature flags}}
- **Rollback Plan:** {{How to roll back; database migration rollback; trigger conditions}}

---

## 8. Testing

| Type | Scope | Tools | Coverage Target |
|------|-------|-------|-----------------|
| {{Unit}} | {{Business logic, utilities}} | {{e.g. Vitest}} | {{e.g. 80%}} |
| {{Integration}} | {{API endpoints, DB queries}} | {{e.g. Vitest + Testcontainers}} | {{e.g. key paths}} |
| {{E2E}} | {{Critical user flows}} | {{e.g. Playwright}} | {{e.g. happy paths}} |

---

## 9. Monitoring & Observability

### Metrics

- {{Key metric and what it measures}}

### Logging

- {{Logging strategy, structured logging format, log levels}}

### Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| {{Alert name}} | {{Trigger condition}} | {{critical/warning/info}} |

---

## 10. Alternatives Considered

| Decision | Chosen | Rejected | Reasoning |
|----------|--------|----------|-----------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{why this choice}} |

---

## 11. Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {{Risk description}} | {{high/medium/low}} | {{high/medium/low}} | {{Mitigation strategy}} |

---

## 12. Open Questions

- [ ] {{Question or uncertainty that needs resolution}}

---

## 13. References

- {{Link to PRD, if exists}}
- {{Link to Design Doc, if exists}}
- {{Link to relevant ADRs}}
- {{Link to external documentation}}
````

## Tier Depth Matrix

Every section is always present. Tier controls depth.

| Section | Core | Medium | Large |
|---------|------|--------|-------|
| 1. Overview | 1-2 paragraphs | + diagram if helpful | + context narrative |
| 2. Goals / Non-Goals | 3-5 goals | + measurable targets | + explicit non-goals with reasons |
| 3. Scope | Bullets | + rationale | + dependency map |
| 4. Domain | 3-6 entities (name + purpose + key invariants), contexts as bullets | + entity attributes, lifecycle states, context map table, BR→entity coverage matrix | + cross-context relationships diagram, ubiquitous-language glossary |
| 5. Use Cases | 3-5 UCs as one-line table | + full Cockburn block per UC | + Extensions fully expanded, frequency, priority, perf constraints |
| 6. System Flows | 0-3 SFs as one-line table (only when non-user triggers exist) | + full block per SF | + retry/idempotency, sequence diagram, SLO targets |
| 7. Architecture | 7.1-7.4 | + 7.5, 7.6 | + 7.7, 7.8 |
| 8. Testing | Table of types | + targets and tools | + flake handling, perf testing |
| 9. Monitoring & Observability | Metrics + logs | + alerts table | + SLOs + dashboards |
| 10. Alternatives Considered | Omit unless promoted | Required | + ADRs per major decision |
| 11. Risks | Omit unless promoted | Optional | Required |
| 12. Open Questions | Inline TBDs | Inline TBDs | Required dedicated section |
| 13. References | Required | Required | Required |

**Critical section promotion** (Phase 0): sub-sections in Architecture (7.6, 7.7) and top-level sections (9, 10, 11) promote regardless of tier when project type matches Payment/Auth/PII, Production service, Migration, or Infrastructure.

## Guidelines

- Be prescriptive — TDDs tell the team what to build and how
- Cite Domain entities and state transitions in every UC, SF, and Architecture decision
- Use distinct ID ranges (UC-N, SF-N, BR-N) for traceability
- Include concrete tech stack choices with versions when known
- Use Mermaid diagrams for architecture, data flow, and large-tier sequence diagrams
- Scale depth (not section presence) to project size
- Promote critical sub-sections based on project type
- Mark unknowns as TBD rather than inventing answers

## Anti-Pattern: Forcing Detail on Small Work

Even on Core, every section is present — but depth is minimal. A Core TDD with a 3-line Domain, a one-line UC table, and a single Architecture diagram is correct. Padding Medium-tier blocks onto a Core feature creates noise without value.

## Anti-Pattern: Skipping Coherence

Phase 4 is not optional. Cross-section drift (UC cites missing entity, NFR has no Architecture mapping, journey has no UC) silently breaks downstream specs. Run the full pass before presenting, even on Core.

## Anti-Pattern: TDD as Requirements Doc

Listing what users need or what the product should do belongs in the PRD. The TDD prescribes how to build it: Domain, Use Cases, System Flows, Architecture. When a section starts describing user value, link to the PRD instead of duplicating.

## Output

Save to: `.artifacts/docs/tdd.md`.
