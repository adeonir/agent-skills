# TDD -- Technical Design Document

## When to Use

When creating a technical design document before implementation.

## Workflow

```
discovery --> analysis --> drafting
```

3-phase workflow. TDDs plan system design before implementation.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns and critical posture.

Never assume context. Discovery is adaptive -- deepen topics based on the quality of answers and available context, not a fixed script.

### Step 1: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and extract product context as starting input for discovery.

| PRD Section | Feeds TDD |
|-------------|-----------|
| Problem Statement | Overview |
| Goals & Metrics | Goals / Non-Goals |
| Scope (MoSCoW) | Functional requirements for architecture |
| User Journeys | Data flow diagrams |
| Business Rules | Architecture constraints |
| Edge Cases | Security & Compliance |
| NFRs | Goals (performance, security targets) |

When PRD exists, ask the user which milestone or scope this TDD covers -- a TDD may cover the full PRD or a single milestone.

If no PRD exists: start discovery from scratch.

### Step 2: Interview

Each topic evaluates what context already exists (from PRD or user input) against its sufficiency criteria. If criteria are already met, move on. If gaps exist, deepen.

#### Topic 1: Requirements & Stack

**When PRD exists:** Evaluate PRD sections against sufficiency criteria below. Deepen only where PRD is vague or incomplete for technical purposes.

**Opening questions (when no PRD):**
- What is being built? (high-level overview and the problem it solves)
- What is the tech stack? (frameworks, languages, databases, hosting)
- What are the quality constraints? (performance, scalability, security)
- What are the non-goals? (explicit exclusions)

**Deepen when:**
- Only functional requirements --> "What about performance, security, reliability?"
- Requirements are vague --> "What does 'fast' mean? What numbers are acceptable?"
- Stack is vague --> "Which specific frameworks, versions, infrastructure?"
- Missing boundaries --> "What does this NOT need to do?"
- PRD NFRs lack technical specificity --> "Page load < 2s -- what's the JS budget? CDN strategy?"

**Sufficient when:**
- Product overview is clear with problem context
- Tech stack choices are concrete
- Goals are measurable and non-goals are explicit
- Scope boundaries are defined

#### Topic 2: Architecture & Integrations

**Opening questions:**
- What external services does this integrate with? (auth providers, APIs, payments, etc.)
- Are there architectural patterns to follow?
- How should data flow through the system for key scenarios?
- Are there related ADRs or RFCs?

**Deepen when:**
- No integration points mentioned --> "Does this read from or write to any existing system?"
- Architecture is hand-waved --> "How does the rest of the system handle similar problems?"
- Data flow unclear --> "Walk me through the main user scenario end-to-end"

**Sufficient when:**
- External services and integrations are identified
- Architectural direction is clear
- Key data flows can be diagrammed
- Prior architectural decisions accounted for

#### Topic 3: Security, Compliance & Testing

**Opening questions:**
- What security concerns exist? (auth, data protection, input validation)
- Are there regulatory requirements? (LGPD, GDPR, HIPAA, etc.)
- What testing approach is planned? (unit, integration, E2E)
- What are the critical failure scenarios?

**Deepen when:**
- Security ignored --> "How is authentication handled? What about data at rest?"
- Compliance hand-waved --> "What specific regulations apply? What data handling is required?"
- Testing vague --> "What are the critical flows that need E2E coverage?"

**Sufficient when:**
- Security approach is defined (auth, encryption, input validation)
- Compliance requirements are identified (or explicitly none)
- Testing strategy covers critical paths
- Key alternatives are noted for the Alternatives section

## Phase 2: Analysis

Synthesize discovery (and PRD context if available) into technical analysis:

1. Map system boundaries and external integrations
2. Design architecture diagrams (high-level, system context, data flow)
3. Evaluate key technical decisions for the Alternatives section
4. Identify security and compliance requirements
5. Present analysis to user for feedback before drafting

### Architecture Evaluation

For key decisions, consider:

- Complexity vs. maintainability
- Performance vs. development speed
- Flexibility vs. simplicity
- Build vs. buy
- Vendor lock-in vs. managed services

Reference existing ADRs when decisions have already been recorded.

## Phase 3: Drafting

**USE TEMPLATE:** `templates/tdd.md`

Generate the TDD using the schema below. Present draft to user for review.

## TDD Schema

9 sections matching `templates/tdd.md`:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Overview | What is being built, why, problem context | Topic 1 (or PRD) |
| 2. Goals / Non-Goals | Measurable objectives and explicit exclusions | Topic 1 (or PRD) |
| 3. Tech Stack | Framework choices by category (frontend, backend, shared) | Topic 1 |
| 4. Architecture | High-level design, system context, data flow (all Mermaid) | Topic 2 + Analysis |
| 5. Security & Compliance | Auth, encryption, input validation, regulatory requirements | Topic 3 |
| 6. Testing | Coverage by type with tools | Topic 3 |
| 7. Alternatives Considered | Decision, choice, rejected option, reasoning | Analysis |
| 8. Open Questions | Items requiring further investigation | All phases |
| 9. References | Related docs, ADRs, RFCs, external links | All phases |

## Guidelines

- TDDs should be written before implementation, not after
- Focus on the "why" behind design choices, not just the "what"
- Architecture section must include Mermaid diagrams (high-level, system context, data flow)
- Tech Stack tables list choices without justification -- use Alternatives Considered for decision rationale
- Keep diagrams text-based (Mermaid) for version control friendliness
- Mark unknowns as TBD -- don't invent solutions for problems not yet understood
- When PRD exists, don't duplicate product-level content -- reference it
- Reference ADRs for architectural decisions rather than duplicating rationale

## Output

Save to: `.artifacts/docs/tdd.md`
