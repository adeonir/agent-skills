# Technical Design Document (TDD)

Prescriptive technical plan for a component, service, or feature, sized
core/medium/large by project complexity.

## When to Use

When creating a prescriptive technical plan for a specific component,
service, or feature before implementation. TDDs list concrete technical
choices with structured sections that scale by project size.

**Key distinction from Design Doc:** Design Docs are informal documents
focused on trade-offs and decision-making for ambiguous problems. TDDs
are prescriptive documents focused on listing technical choices with
structure — they tell the team exactly what to build, with what, and
how to deploy it. A project can have both: a Design Doc for system-level
decisions and TDDs for component-level technical planning.

## When NOT to Write a TDD

- The implementation is trivial with no architectural decisions
- A Design Doc already covers the technical plan in sufficient detail
- The component has no cross-cutting concerns (security, deployment, monitoring)
- The work is a bug fix or minor enhancement

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

```
discovery --> analysis --> drafting
```

### Phase 1: Discovery

Load [discovery.md](discovery.md) for shared interview patterns and
critical posture.

**Check Existing Context:**

Look for existing PRD at `.artifacts/docs/prd.md` and Design Doc at
`.artifacts/docs/design.md`.

If PRD found: extract product context as starting input.
If Design Doc found: extract architectural context and decisions.

| PRD Section | Feeds TDD |
|-------------|-----------|
| Problem Statement | Overview |
| Goals & Metrics | Goals / Non-Goals |
| Scope (MoSCoW) | Scope |
| User Journeys | Data flow, APIs |
| NFRs | Security, monitoring, testing |

| Design Doc Section | Feeds TDD |
|--------------------|-----------|
| Context & Scope | Overview |
| Design | Architecture, APIs, Data Model |
| Cross-Cutting Concerns | Security, Monitoring |
| Alternatives Considered | Alternatives Considered |

When existing docs are found, ask which component this TDD covers.

If no existing docs: start discovery from scratch.

**Discovery Topics:**

#### Topic 1: Requirements & Stack

**Opening questions:**

- What is the component/service being built?
- What problem does it solve and what are the success criteria?
- What tech stack is being used or considered? (languages, frameworks, infra)
- What is explicitly out of scope?

**Deepen when:**

- No success criteria → "How will you measure if this works?"
- Stack is hand-waved → "What specific frameworks? What versions?"
- No constraints mentioned → "Are there performance requirements? Team expertise constraints?"

**Sufficient when:**

- Clear overview of what is being built
- Success criteria are measurable
- Tech stack is specified
- Scope boundaries are defined

#### Topic 2: Architecture & Integrations

**Opening questions:**

- What is the high-level architecture of this component?
- How does it integrate with existing systems?
- What data does it store, read, or transform?
- What APIs or interfaces does it expose or consume?

**Deepen when:**

- No integration points → "Does this read from or write to any existing system?"
- Data model unclear → "What are the key entities and relationships?"
- No API surface → "How do other systems interact with this component?"

**Sufficient when:**

- Architecture can be diagrammed
- Integration points are identified
- Data model is understood
- API surface is defined

#### Topic 3: Operations & Risk

**Opening questions:**

- What security concerns exist? (auth, encryption, PII, compliance)
- How will this be deployed? (CI/CD, rollback strategy)
- How will you know if it is working in production? (metrics, logs, alerts)
- What testing approach is planned?

**Deepen when:**

- Security ignored → "How is authentication handled? What about data at rest?"
- No deployment plan → "How does your team typically deploy? Any phased rollout needs?"
- Observability missing → "How will you detect failures? What metrics matter?"
- Testing vague → "What types of tests? What coverage target?"

**Sufficient when:**

- Security approach is defined or explicitly not applicable
- Deployment strategy is clear
- Monitoring approach is defined
- Testing strategy is clear

### Auto-Sizing

Determine project size from discovery answers. If unclear, ask the user
directly.

| Signal | Size |
|--------|------|
| Single service, few integrations, small team | Core |
| Multiple integrations, data modeling needed, security concerns | Medium |
| Cross-team, production-critical, migration, compliance | Large |

### Critical Sections by Project Type

Some sections are mandatory regardless of size when the project matches
these types:

| Project Type | Mandatory Sections |
|--------------|--------------------|
| Payment / Auth / PII | Security & Compliance |
| Production service | Deployment & Rollback, Monitoring & Observability |
| Migration | Risks, Deployment & Rollback |
| Infrastructure | Monitoring & Observability, Risks |

If a critical section would not be included at the detected size,
promote it.

### Phase 2: Analysis

Synthesize discovery into technical analysis:

1. Map components and integration points
2. Design architecture diagrams
3. Determine sizing (core/medium/large) from discovery signals
4. Check project type for critical section promotion
5. Identify gaps and open questions
6. Present analysis to user for feedback before drafting

### Phase 3: Drafting

Use the template below. Include only sections matching the determined
size plus any promoted critical sections. Load
[quality.md](quality.md) before presenting the draft to the user.

## TDD Template

ALWAYS use this exact template structure (include only sections matching
the determined size):

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

<!-- Core sections (always included) -->

## 1. Overview

{{What is being built and why. Brief description of the component/service, its purpose, and the problem it solves.}}

---

## 2. Goals / Non-Goals

### Goals

- **{{Goal name}}:** {{Measurable objective this component must achieve}}
- **{{Goal name}}:** {{Measurable objective this component must achieve}}

### Non-Goals

- {{Explicit exclusion — something that could reasonably be a goal but is deliberately not}}

---

## 3. Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| {{Language}} | {{e.g. TypeScript 5.x}} | {{Primary language}} |
| {{Framework}} | {{e.g. Next.js 14}} | {{Web framework}} |
| {{Database}} | {{e.g. PostgreSQL 16}} | {{Primary data store}} |
| {{Infrastructure}} | {{e.g. AWS ECS}} | {{Container orchestration}} |
| {{Other}} | {{e.g. Redis 7}} | {{Caching layer}} |

---

## 4. Architecture

### High-Level Design

```mermaid
{{Component diagram showing internal modules and their relationships}}
```

### System Context

```mermaid
{{System-context diagram showing this component within the broader system landscape}}
```

### Component Interactions

{{How internal modules interact, key flows, request/response patterns.}}

---

## 5. Testing

| Type | Scope | Tools | Coverage Target |
|------|-------|-------|-----------------|
| {{Unit}} | {{Business logic, utilities}} | {{e.g. Vitest}} | {{e.g. 80%}} |
| {{Integration}} | {{API endpoints, DB queries}} | {{e.g. Vitest + Testcontainers}} | {{e.g. key paths}} |
| {{E2E}} | {{Critical user flows}} | {{e.g. Playwright}} | {{e.g. happy paths}} |

---

## 6. Monitoring & Observability

### Metrics

- {{Key metric and what it measures}}
- {{Key metric and what it measures}}

### Logging

- {{Logging strategy, structured logging format, log levels}}

### Alerts

| Alert | Condition | Severity |
|-------|-----------|----------|
| {{Alert name}} | {{Trigger condition}} | {{critical/warning/info}} |

---

## 7. References

- {{Link to PRD, if exists}}
- {{Link to Design Doc, if exists}}
- {{Link to relevant ADRs}}
- {{Link to external documentation}}

---

<!-- Medium sections (include for medium and large projects) -->

## 8. Scope

### In Scope

- {{Feature or responsibility this TDD covers}}

### Out of Scope

- {{What is explicitly excluded and why}}

---

## 9. Data Model

### Schema

```mermaid
erDiagram
    {{Entity relationships and key fields}}
```

### Storage

- **Engine:** {{e.g. PostgreSQL 16}}
- **Access patterns:** {{Read-heavy, write-heavy, mixed}}
- **Retention:** {{Data lifecycle and retention policy}}

---

## 10. APIs / Interfaces

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| {{GET}} | {{/api/resource}} | {{List resources}} | {{required}} |
| {{POST}} | {{/api/resource}} | {{Create resource}} | {{required}} |

### Contracts

{{Key request/response shapes, error formats, pagination strategy.}}

---

## 11. Security & Compliance

### Authentication & Authorization

- {{Auth mechanism (e.g. JWT, OAuth2, API keys)}}
- {{Authorization model (e.g. RBAC, ABAC)}}

### Data Protection

- {{Encryption at rest and in transit}}
- {{PII handling and data classification}}

### Regulatory

- {{Applicable regulations (LGPD, GDPR, HIPAA, PCI-DSS)}}
- {{How compliance is achieved}}

---

## 12. Alternatives Considered

| Decision | Chosen | Rejected | Reasoning |
|----------|--------|----------|-----------|
| {{what was decided}} | {{what was chosen}} | {{what was rejected}} | {{why this choice}} |

---

<!-- Large sections (include for large projects only) -->

## 13. Deployment & Rollback

### CI/CD

- {{Pipeline description and stages}}
- {{Build and artifact strategy}}

### Release Strategy

- {{Phased rollout, canary, blue-green, or big-bang}}
- {{Feature flags if applicable}}

### Rollback Plan

- {{How to roll back if deployment fails}}
- {{Database migration rollback strategy}}
- {{Rollback triggers (what conditions trigger rollback)}}

---

## 14. Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| {{Risk description}} | {{high/medium/low}} | {{high/medium/low}} | {{Mitigation strategy}} |

---

## 15. Open Questions

- [ ] {{Question or uncertainty that needs resolution}}
- [ ] {{Decision pending input from another team or stakeholder}}
````

## TDD Schema

15 sections organized by sizing tier:

### Core (always included, 7 sections)

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Overview | What is being built and why | Topic 1 |
| 2. Goals / Non-Goals | Measurable objectives and explicit exclusions | Topic 1 |
| 3. Tech Stack | Frameworks, languages, infrastructure | Topic 1 |
| 4. Architecture | Components, diagrams, interactions | Topic 2 |
| 5. Testing | Test types, coverage targets, tools | Topic 3 |
| 6. Monitoring & Observability | Metrics, logs, alerts | Topic 3 |
| 7. References | Links to PRD, ADRs, Design Doc, external docs | All phases |

### Medium (adds 5 sections)

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 8. Scope | In-scope / out-of-scope | Topic 1 |
| 9. Data Model | Schema, storage, access patterns | Topic 2 |
| 10. APIs / Interfaces | Endpoints, contracts, protocols | Topic 2 |
| 11. Security & Compliance | Auth, encryption, regulatory | Topic 3 |
| 12. Alternatives Considered | Rejected options and reasoning | Analysis |

### Large (adds 3 sections)

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 13. Deployment & Rollback | CI/CD, phased release, rollback strategy | Topic 3 |
| 14. Risks | Impact/probability matrix with mitigations | Analysis |
| 15. Open Questions | Uncertainties and pending decisions | All phases |

## Guidelines

- Be prescriptive — TDDs tell the team what to build and how
- Include concrete tech stack choices with versions when known
- Use Mermaid diagrams for architecture and data flow
- Scale sections to project size (don't force large structure on small projects)
- Promote critical sections based on project type
- Mark unknowns as TBD rather than inventing answers
- Update the TDD when implementation reveals changes

## Anti-Pattern: Forcing Large Structure on Small Work

Including all 15 sections on a small component pads the doc with empty
sections that nobody reads. Use auto-sizing — Core (7), Medium (12),
Large (15) — and only promote critical sections when project type
demands them (Payment/Auth/PII, production service, migration,
infrastructure).

## Anti-Pattern: TDD as Requirements Doc

Listing what users need or what the product should do belongs in the
PRD. The TDD prescribes how to build it: stack, architecture, testing,
deployment. When sections start describing user value, link to the PRD
instead of duplicating.

## Output

Save to: `.artifacts/docs/tdd.md`
