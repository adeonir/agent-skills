# TDD -- Technical Design Document

## When to Use

When creating a technical design document before implementation.

## Workflow

```
discovery --> analysis --> drafting
```

3-phase workflow. TDDs are deep technical documents that plan system design before implementation.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns and critical posture.

Never assume context. Discovery is adaptive -- deepen topics based on the quality of answers and available context, not a fixed script.

### Step 1: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and extract product context as starting input for discovery.

| PRD Section | Feeds TDD |
|-------------|-----------|
| Problem Statement | Overview |
| Goals & Metrics | Goals |
| Scope (MoSCoW) | Functional requirements |
| User Journeys | Data flow, API design, components |
| Business Rules | Key algorithms/logic, constraints |
| Edge Cases | Failure modes & recovery |
| NFRs | Performance, security targets |
| Milestones | Scope of this TDD (which milestone?) |

When PRD exists, ask the user which milestone or scope this TDD covers -- a TDD may cover the full PRD or a single milestone.

If no PRD exists: start discovery from scratch.

### Step 2: Interview

Each topic evaluates what context already exists (from PRD or user input) against its sufficiency criteria. If criteria are already met, move on. If gaps exist, deepen.

#### Topic 1: Requirements

**When PRD exists:** Evaluate PRD sections (problem, scope, NFRs) against sufficiency criteria below. Deepen only where PRD is vague or incomplete for technical purposes.

**Opening questions (when no PRD):**
- What is being built? (high-level overview)
- What must it do? (functional requirements)
- What are the quality constraints? (performance, scalability, security)

**Deepen when:**
- Only functional requirements → "What about performance, security, reliability?"
- Requirements are vague → "What does 'fast' mean? What numbers are acceptable?"
- Missing boundaries → "What does this NOT need to do?"
- PRD NFRs lack technical specificity → "Page load < 2s -- what's the JS budget? CDN strategy? Caching approach?"
- PRD edge cases lack technical detail → "The PRD says 'handle gracefully' -- what does that mean technically? Retry? Queue? Fallback?"

**Sufficient when:**
- Functional requirements are concrete and enumerable
- Non-functional requirements have measurable targets with technical specificity
- Scope boundaries are defined

#### Topic 2: Constraints & Dependencies

**Opening questions:**
- What technical constraints exist? (stack, infrastructure, existing systems)
- What does this integrate with?
- Are there related ADRs or RFCs?

**Deepen when:**
- "Standard stack" → "Which specific versions, frameworks, infrastructure?"
- No dependencies mentioned → "Does this read from or write to any existing system?"
- Ignoring prior decisions → "Are there architectural decisions that constrain this?"

**Sufficient when:**
- Stack and infrastructure constraints are concrete
- Integration points identified
- Prior architectural decisions accounted for

#### Topic 3: Architecture Preferences

**Opening questions:**
- Are there architectural patterns to follow?
- How should this scale?
- What are the critical failure scenarios?

**Deepen when:**
- No pattern preference → "How does the rest of the system handle similar problems?"
- Scalability hand-waved → "What's the expected load? What happens at 10x?"
- Failure modes ignored → "What happens when [dependency] goes down?"

**Sufficient when:**
- Architectural direction is clear (or explicitly open for exploration in analysis)
- Scale expectations have concrete numbers
- Critical failure scenarios identified

## Phase 2: Analysis

Synthesize discovery (and PRD context if available) into technical analysis:

1. Identify system boundaries and interfaces
2. Evaluate architectural options
3. Map data flows and state management
4. Identify technical risks and unknowns
5. Present analysis to user for feedback before drafting

### Architecture Evaluation

For key architectural decisions, consider:

- Complexity vs. maintainability
- Performance vs. development speed
- Flexibility vs. simplicity
- Build vs. buy

Reference existing ADRs when decisions have already been recorded.

## Phase 3: Drafting

**USE TEMPLATE:** `templates/tdd.md`

Generate the TDD using the schema below. Present draft to user for review.

## TDD Schema

16 sections matching `templates/tdd.md`:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Overview | What is being solved, scope, audience | Topic 1 (or PRD) |
| 2. Context & Background | Existing system, history, motivation | Topic 1 (or PRD) |
| 3. Goals / Non-Goals | Technical objectives and explicit exclusions | Topic 1 (or PRD) |
| 4. Scope of Impact | Blast radius, affected systems, teams, dependencies | Topic 2 + Analysis |
| 5. Architecture | High-level design, system context, components, data flow | Topic 3 + Analysis |
| 6. Technical Design | Data model, API design, state management, key logic | Analysis |
| 7. Tech Stack & Dependencies | Framework choices with justification | Topic 2 |
| 8. Failure Modes & Recovery | System-level failures, detection, recovery, user impact | Topic 3 (or PRD edge cases) |
| 9. Performance Considerations | Budgets, caching, bundle size, lazy loading | Topic 1 NFRs |
| 10. Security Considerations | Auth, input validation, access control | Topic 1 NFRs |
| 11. Observability & Monitoring | Metrics, dashboards, alerts, health model, rollback signals | Topic 3 + Analysis |
| 12. Testing Strategy | Unit, integration, E2E coverage and tools | Analysis |
| 13. Migration / Rollout Plan | Deployment steps, feature flags, rollback triggers | Analysis |
| 14. Alternatives Considered | Do Nothing + options with pros, cons, rejection reason | Analysis |
| 15. Open Questions | Items requiring further investigation | All phases |
| 16. References | Related ADRs, RFCs, documentation | All phases |

## Guidelines

- TDDs should be written before implementation, not after
- Focus on the "why" behind design choices, not just the "what"
- Include concrete examples (API payloads, data schemas) when possible
- Reference ADRs for architectural decisions rather than duplicating rationale
- Keep diagrams text-based (ASCII or Mermaid) for version control friendliness
- Mark unknowns as TBD -- don't invent solutions for problems not yet understood
- When PRD exists, don't duplicate product-level content -- reference it

## Output

Save to: `.artifacts/docs/tdd.md`
