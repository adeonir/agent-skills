# PRD — Product Requirements Document

Capture product requirements: problem, users, scope, journeys, business rules, and success metrics.

## When to Use

When creating a PRD, defining product requirements, or writing product specifications.

## Scope

Product requirements only. Never carries implementation content — no architecture, tech stack, UI components, API endpoints, or code-level decisions — nor strategic positioning (brand personality, anti-references). The former belongs to the Design Doc or ADR; positioning belongs to PRODUCT.

## Workflow

```text
check disk
├ PRD absent  → discovery → validation → summary → drafting
└ PRD present → update requested parts (reconcile.md)
```

Check whether `docs/product/PRD.md` exists; see [discovery.md](discovery.md) `## Discovery or Update by Document State`. If absent, run the four discovery phases below and use any confirmed earlier direction as input. If present, update only the requested parts by following [reconcile.md](reconcile.md). Handle PRODUCT independently based on whether it exists.

### Phase 1: Discovery

Load [discovery.md](discovery.md) for the shared interview method and critical review.

Run these four phases when no PRD exists. Never assume context. Use the answers to choose follow-up questions. Each topic defines opening questions, reasons to ask a follow-up, and completion criteria.

#### Read an Earlier Direction

Apply [discovery.md](discovery.md) `## Reading Project Files`, then check `docs/product/brainstorm.md` before interviewing. If absent, run full discovery. If present, confirm its claims and ask only for missing PRD information.

| Upstream section | Supplies | Behavior |
|---|---|---|
| Context | Topic 1 — problem, motivation, current state | confirm; ask follow-ups only for evidence gaps |
| Constraints | Topic 5 constraints, Business Rule candidates | confirm |
| Success Criteria | Goals & metrics | confirm |
| Alternatives Considered + Decision | Topic 3 (when it runs), chosen-approach rationale | confirm |
| Trade-offs Accepted | Non-Goals; Risks when a trade-off rests on a fragile assumption | confirm |
| Key Assumption | Assumptions | carry |
| Open Questions | Open Questions | carry |

Present each supplied topic as an interpretation for the user to confirm or correct. Do not repeat its opening questions. Run full discovery for information the upstream document does not contain: Users, Journeys, scope levels and FR IDs, Business Rules, Edge Cases, and NFRs.

Do not copy rejected alternatives, Revision History, or the direction's name into the PRD. Carry only the confirmed problem, constraints, and criteria, expressed as product requirements.

The earlier direction supplies product intent. Codebase inspection supplies facts about current behavior. Each source is optional and independent.

#### Topic 1: Problem

**Opening questions:**

- What problem are you solving?
- How do you know this problem exists? (evidence, data, user feedback)
- What is the cost of not solving it?

**Ask follow-up when:**

- User describes symptoms, not root cause → "Why does this happen? What causes it?"
- No evidence → "What would convince you this is real? Have you talked to users?"
- Multiple problems mixed → "These sound like separate problems. Which one is primary?"
- User starts with solution → "What problem does this solution address? Let's start there."

**Complete when:**

- Problem can be stated in one clear sentence
- Evidence exists or is explicitly marked as hypothesis
- Single primary problem identified (secondary problems noted separately)

#### Topic 2: Users

**Opening questions:**

- Who specifically has this problem?
- What are they trying to accomplish? (job to be done)
- Why would they use this over the status quo?

**Ask follow-up when:**

- "Everyone" or too broad → "Who is the *most* affected? Describe one specific person."
- Multiple user types → "Which persona is primary? What happens when their needs conflict?"
- Vague motivation → "Walk me through a concrete scenario. What does their day look like?"
- Can't articulate why they'd switch → "What would they have to give up? What's the switching cost?"

**Complete when:**

- At least one concrete persona with clear motivation
- Job to be done is specific enough to derive features from
- If multiple personas, priority between them is understood

#### Topic 3: Market & Differentiation

**Used by PRODUCT, not the PRD** — run this topic only when writing PRODUCT in the same run. Skip it for a PRD-only run. Its answers can also help with scope and validation.

**Opening questions:**

- How do people solve this today? (existing tools, workarounds, competitors)
- What makes your approach different or better?
- Why hasn't this been solved yet? (timing, technology, market gap)

**Ask follow-up when:**

- "Nothing like this exists" → "How do people cope today? Even manual workarounds count."
- Crowded market → "With X, Y, Z already out there, why would someone switch to this?"
- Weak differentiator → "If a competitor copied this feature tomorrow, what would you still have?"
- Unaware of alternatives → name known alternatives and ask how the proposal compares

**Complete when:**

- Clear picture of how the problem is currently solved
- Differentiator is articulated beyond feature comparison
- User understands the competitive context

#### Topic 4: Value & Scope

**Opening questions:**

- What type of thing is this? (product, feature, internal tool, platform)
- How does it generate value? (monetization, cost reduction, efficiency)
- What must exist at launch vs. what can wait?

**Ask follow-up when:**

- Everything is "must have" → "If you could only ship 3 features, which 3?"
- Scope keeps expanding → "We started with X, now it's X+Y+Z. Should we narrow down?"
- Features without clear user connection → "Which persona needs this? What problem does it solve for them?"
- No clear value model → "Who pays? How? What justifies the cost?"

**Complete when:**

- Clear must/should/could prioritization
- Each must-have connects to the primary problem and persona
- Value generation model is understood or marked as TBD
- Boundaries are defined (what is explicitly out of scope)

#### Topic 5: Journeys & Constraints

**Opening questions:**

- Walk me through the main flow: what does the user do from start to finish?
- Are there rules or constraints the product must enforce? (limits, permissions, conditions)
- What can go wrong? What happens when it does?

**Codebase trigger:** If the journey touches existing features, systems, or flows, explore the codebase to map the current flow before asking the user to describe it. Carry the flow's shape into the journey, not the code.

**Ask follow-up when:**

- Only happy path described → "What if the user makes a mistake? What if data is missing?"
- No constraints mentioned → "Are there limits? Who can do what? Any conditions that must be met?"
- Single journey for multiple personas → "Does the admin go through the same flow? What's different?"
- Vague error handling → "When X fails, what should the user see? Can they retry?"

**Complete when:**

- At least the primary journey is described end-to-end (pre-conditions → steps → post-conditions)
- Key business rules are identified (even if details are TBD)
- Critical edge cases are identified (at least "what if it fails?" for each major action)
- Alternative flows are acknowledged for the main journey

### Phase 2: Validation

Challenge what was learned. This phase exists to prevent building the wrong thing.

1. **Challenge viability**: Point out risks and weak spots identified during discovery
2. **Question scope**: Is the scope realistic for a first version? If not, push back
3. **Suggest simplifications**: Propose cuts when scope is ambitious. "Do you need X for launch, or can it wait?"
4. **Flag a fragile direction**: If the direction itself seems fragile after discovery, say so and recommend reopening the direction decision before specifying — the PRD does not generate or choose alternatives
5. **Define scope**: Categorize features into must/should/could priorities
6. **Identify hypotheses**: What assumptions need evidence before or during implementation?
7. **Validate journeys**: Do the described flows cover all must-have features? Are there gaps?
8. **Confirm with user**: Present validation findings and get explicit agreement before proceeding

Do not write the summary until the user confirms scope and priorities.

### Phase 3: Summary

Summarize the confirmed discovery and validation results.

1. Summarize what was learned across all discovery topics
2. Present the agreed scope (must/should/could)
3. List user journeys with main and alternative flows
4. List business rules and edge cases identified
5. List open questions and hypotheses identified during validation (risks too, when material)
6. Identify gaps and mark as TBD
7. Surface assumptions made (distinguish from validated facts)
8. Ask the user to confirm the summary
9. Only proceed to drafting after user confirms

### Phase 4: Drafting

Use the PRD template below. Handle PRODUCT by following [product.md](product.md). If `docs/product/PRODUCT.md` is absent, write it during discovery using confirmed PRD facts. If it exists, update it by following [reconcile.md](reconcile.md). Do not replace supported positioning without new evidence. Run [quality.md](quality.md), write the documents to their paths, and report the paths, must/should/could scope, and primary metric in up to three short paragraphs. Do not paste the full documents.

**Drafting notes:**

- Market & differentiation content goes to PRODUCT, not PRD
- Value proposition content goes to PRODUCT, not PRD
- Journeys should be product-level (actor, goal, flow, conditions) — no UI components, endpoints, or implementation details
- Business rules use IDs (BR-1) for traceability
- Edge cases use IDs (EC-1) for traceability
- Non-Goals are outcome-level exclusions; features cut from the release go to Scope → Won't Have
- Won't Have must record the reason for exclusion so future revisits have context
- Definition of Done states product-level readiness criteria, independent of any launch date
- External Dependencies capture out-of-team blockers with owner and status; technical dependencies belong in the Design Doc
- NFRs state measurable targets without prescribing the mechanism ("p95 latency under 200ms", not "use Redis caching")

## PRD Template

ALWAYS use this exact template structure:

````markdown
---
name: [document-name]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: draft
sources: []
---

# PRD: [Product Name]

## 1. Executive Summary

[One short paragraph for a quick scan of the spec: the problem, who it is for, the must-have scope, and the primary success metric. Requirements digest only — positioning (what the product is and stands for) lives in PRODUCT, never here.]

## 2. Problem Statement

[Describe the problem being solved. What pain point exists? Who is affected? What evidence supports this?]

## 3. Goals & Non-Goals

| Goal | Metric | Target |
|------|--------|--------|
| [goal] | [how it will be measured] | [concrete number or threshold, or TBD] |

### Non-Goals

- [An outcome this product deliberately does not pursue. Distinct from a cut feature — that goes to Scope → Won't Have.]

## 4. User Personas

### [Persona Name]

- **Role:** [role or job title]
- **Pain Point:** [primary frustration or problem]
- **Goal:** [what they want to achieve with this product]

## 5. User Journeys

### [Journey Name]

**Actor:** [persona]
**Goal:** [what the user is trying to accomplish]

**Pre-conditions:**

- [what must be true before this journey starts]

**Main Flow:**

1. [user action] → [system behavior]
2. [user action] → [system behavior]
3. [user action] → [system behavior]

**Alternative Flows:**

- [step]a. [condition] → [what happens instead]

**Post-conditions:**

- [what is true after the journey completes]

## 6. Scope

### Must Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-1 | [core capability required for launch] | |
| FR-2 | [another core capability] | |

### Should Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-3 | [important but not launch-blocking] | |

### Could Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-4 | [nice-to-have for future iteration] | |

### Won't Have

| ID | Requirement | Reason for exclusion |
|----|------------|----------------------|
| FR-N | [feature considered and cut from this release] | [why it is out of scope now — informs future revisit] |

## 7. Business Rules

| ID | Rule | Scope |
|----|------|-------|
| BR-1 | [functional constraint that applies across features] | [which features/journeys it affects] |
| BR-2 | [another business rule] | [scope] |

## 8. Edge Cases (optional)

[Include only when exception scenarios are material to the product.]

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-1 | [what goes wrong or what unusual situation occurs] | [how the product should respond] |
| EC-2 | [another exception scenario] | [expected behavior] |

## 9. Non-Functional Requirements

Non-functional requirements state measurable targets without prescribing the mechanism.

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | Performance | [for example, page load < 2s] |
| NFR-2 | Accessibility | [applicable WCAG conformance level] |

Examples:
- "Use Redis caching" (prescribes mechanism)
- "Search returns results within 200ms" (states measurable target)

## 10. Definition of Done

[Product-level criteria that tell us this is ready to ship. Independent of any calendar; applies whenever launch happens.]

| Criterion | How verified |
|-----------|--------------|
| [for example, all Must Have requirements implemented and validated] | [test/validation method] |
| [for example, primary success metric meeting target for 7 days] | [measurement source] |
| [for example, no critical or blocker defects open] | [issue tracker state] |

## 11. External Dependencies

[Dependencies outside the product team that can block or shape delivery.]

| ID | Dependency | Impact if blocked | Owner / Status |
|----|-----------|-------------------|----------------|
| DEP-1 | [for example, legal approval on terms of use] | [blocks launch] | [Owner — pending] |

## 12. Risks (optional)

[Include only when there are material risks worth tracking.]

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [what could go wrong] | High | Medium | [how to address] |

## 13. Open Questions & Assumptions

### Assumptions

- [Assumption that, if wrong, would change the plan]

### Open Questions

- [ ] [Hypothesis to validate with data or user research, or unknown to resolve before implementation (mark TBD)]

## 14. References

Durable pointers to related documents. Use typed labels so a fresh session knows where to recover context.

- **PRODUCT:** [link to docs/product/PRODUCT.md or "None"]
- **PRD:** [link to this PRD or upstream PRD]
- **Design Doc:** [link to docs/tech/design-doc.md or "None"]
- **Research:** [link to research, interviews, data — or "None"]
- **ADRs:** [link to relevant ADRs or "None"]
````

MUST NOT contain: architecture, tech stack, framework or deployment choices, API contracts, database schema, or UI components — those belong to the Design Doc or ADR; nor strategic positioning (brand personality, anti-references) — that lives in PRODUCT.

## PRD Schema

14 numbered sections matching the template, with Edge Cases and Risks optional:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Executive Summary | Requirements digest for a quick scan — problem, audience, must-have scope, primary metric (no positioning) | Synthesis of Topics 1, 2, 4 |
| 2. Problem Statement | What problem exists, for whom, with evidence | Topic 1: Problem |
| 3. Goals & Non-Goals | Measurable goals (concrete numbers, not vague) plus outcomes deliberately not pursued | Topic 1: Problem (goals/metrics), Topic 4: Value & Scope (non-goals) |
| 4. User Personas | Who uses this, role, pain point, goal | Topic 2: Users |
| 5. User Journeys | End-to-end flows per persona with pre/post-conditions | Topic 5: Journeys & Constraints |
| 6. Scope | Must/Should/Could/Won't have (FR-1...) | Topic 4: Value & Scope |
| 7. Business Rules | Functional constraints across features (BR-1...) | Topic 5: Journeys & Constraints |
| 8. Edge Cases (optional) | Exception scenarios and expected behavior (EC-1...) | Topic 5: Journeys & Constraints |
| 9. Non-Functional Requirements | Performance, accessibility, security targets | Topic 4: Value & Scope |
| 10. Definition of Done | Product-level readiness criteria, independent of calendar | Validation phase, Topic 4 |
| 11. External Dependencies | Dependencies outside the team that can block or shape delivery | Validation phase |
| 12. Risks (optional) | What could go wrong and how to address it | Validation phase |
| 13. Open Questions & Assumptions | Assumptions underpinning the plan plus hypotheses to validate and unknowns to resolve | Validation phase |
| 14. References | Typed links to PRODUCT, Design Doc, research, ADRs | All phases |

Topic 3 (Market & Differentiation) supplies PRODUCT, not the PRD.

## Guidelines

- Complete discovery before writing a new PRD. For an existing PRD, update only the requested parts.
- Challenge weak claims during discovery, validation, and updates.
- Write the PRD to its path directly, then report a brief prose summary in chat (path, scope, primary metric)
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Discover PRODUCT if absent. Update only the requested parts if present.
- Keep journeys at product level — describe what happens, not how it's built
- Assign IDs to business rules and edge cases for traceability
- Edge Cases and Risks are optional — include only when relevant
- Record a reason for exclusion on every Won't Have item
- Keep Definition of Done independent of calendar dates — state readiness criteria, not deadlines
- Track External Dependencies with owner and status; keep technical dependencies in the Design Doc
- Use typed labels in References so later sessions know which document to read

## Output

- PRD: `docs/product/PRD.md`
- PRODUCT: `docs/product/PRODUCT.md`
