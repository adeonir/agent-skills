# PRD — Product Requirements Document

Capture product requirements: problem, users, scope, journeys, business
rules, and success metrics.

## When to Use

When creating a PRD, defining product requirements, or writing product
specifications.

## Scope

Product requirements only. Never carries implementation content — no
architecture, tech stack, UI components, API endpoints, or code-level
decisions. Those belong to Design Doc, ADR, or visual design artifacts.

## Workflow

```text
discovery → validation → synthesis → drafting
```

4 sequential phases. Never skip discovery — always interview the user
first.

### Phase 1: Discovery

Load [discovery.md](discovery.md) for shared interview patterns and
critical posture.

Never assume context. Discovery is adaptive — deepen topics based on
the quality of answers, not a fixed script. Each topic has opening
questions, signals for when to probe further, and criteria for when to
move on.

#### Topic 1: Problem

**Opening questions:**

- What problem are you solving?
- How do you know this problem exists? (evidence, data, user feedback)
- What is the cost of not solving it?

**Deepen when:**

- User describes symptoms, not root cause → "Why does this happen? What causes it?"
- No evidence → "What would convince you this is real? Have you talked to users?"
- Multiple problems mixed → "These sound like separate problems. Which one is primary?"
- User starts with solution → "What problem does this solution address? Let's start there."

**Sufficient when:**

- Problem can be stated in one clear sentence
- Evidence exists or is explicitly marked as hypothesis
- Single primary problem identified (secondary problems noted separately)

#### Topic 2: Users

**Opening questions:**

- Who specifically has this problem?
- What are they trying to accomplish? (job to be done)
- Why would they use this over the status quo?

**Deepen when:**

- "Everyone" or too broad → "Who is the *most* affected? Describe one specific person."
- Multiple user types → "Which persona is primary? What happens when their needs conflict?"
- Vague motivation → "Walk me through a concrete scenario. What does their day look like?"
- Can't articulate why they'd switch → "What would they have to give up? What's the switching cost?"

**Sufficient when:**

- At least one concrete persona with clear motivation
- Job to be done is specific enough to derive features from
- If multiple personas, priority between them is understood

#### Topic 3: Market & Differentiation

**Opening questions:**

- How do people solve this today? (existing tools, workarounds, competitors)
- What makes your approach different or better?
- Why hasn't this been solved yet? (timing, technology, market gap)

**Deepen when:**

- "Nothing like this exists" → "How do people cope today? Even manual workarounds count."
- Crowded market → "With X, Y, Z already out there, why would someone switch to this?"
- Weak differentiator → "If a competitor copied this feature tomorrow, what would you still have?"
- Unaware of alternatives → surface known alternatives and ask how this compares

**Sufficient when:**

- Clear picture of how the problem is currently solved
- Differentiator is articulated beyond feature comparison
- User understands the competitive context

**Note:** Market & differentiation feeds PRODUCT, not the PRD. Still
essential discovery — it informs scope decisions and validation.

#### Topic 4: Value & Scope

**Opening questions:**

- What type of thing is this? (product, feature, internal tool, platform)
- How does it generate value? (monetization, cost reduction, efficiency)
- What must exist at launch vs. what can wait?

**Deepen when:**

- Everything is "must have" → "If you could only ship 3 features, which 3?"
- Scope keeps expanding → "We started with X, now it's X+Y+Z. Should we narrow down?"
- Features without clear user connection → "Which persona needs this? What problem does it solve for them?"
- No clear value model → "Who pays? How? What justifies the cost?"

**Sufficient when:**

- Clear must/should/could prioritization
- Each must-have connects to the primary problem and persona
- Value generation model is understood or marked as TBD
- Boundaries are defined (what is explicitly out of scope)

#### Topic 5: Journeys & Constraints

**Opening questions:**

- Walk me through the main flow: what does the user do from start to finish?
- Are there rules or constraints the product must enforce? (limits, permissions, conditions)
- What can go wrong? What happens when it does?

**Deepen when:**

- Only happy path described → "What if the user makes a mistake? What if data is missing?"
- No constraints mentioned → "Are there limits? Who can do what? Any conditions that must be met?"
- Single journey for multiple personas → "Does the admin go through the same flow? What's different?"
- Vague error handling → "When X fails, what should the user see? Can they retry?"

**Sufficient when:**

- At least the primary journey is described end-to-end (pre-conditions → steps → post-conditions)
- Key business rules are identified (even if details are TBD)
- Critical edge cases are surfaced (at least "what if it fails?" for each major action)
- Alternative flows are acknowledged for the main journey

### Phase 2: Validation

Challenge what was learned. This phase exists to prevent building the
wrong thing.

1. **Challenge viability**: Point out risks and weak spots identified during discovery
2. **Question scope**: Is the scope realistic for a first version? If not, push back
3. **Suggest simplifications**: Propose cuts when scope is ambitious. "Do you need X for launch, or can it wait?"
4. **Propose pivots**: If the idea seems fragile after discovery, suggest alternative approaches
5. **Define scope**: Categorize features into must/should/could priorities
6. **Identify hypotheses**: What assumptions need evidence before or during implementation?
7. **Validate journeys**: Do the described flows cover all must-have features? Are there gaps?
8. **Confirm with user**: Present validation findings and get explicit agreement before proceeding

Do not proceed to synthesis until the user confirms scope and priorities.

### Phase 3: Synthesis

Synthesize everything from discovery and validation into a structured summary.

1. Summarize what was learned across all discovery topics
2. Present the agreed scope (must/should/could)
3. List user journeys with main and alternative flows
4. List business rules and edge cases identified
5. List risks and hypotheses identified during validation
6. Identify gaps and mark as TBD
7. Surface assumptions made (distinguish from validated facts)
8. Present synthesis to user for confirmation
9. Only proceed to drafting after user confirms

### Phase 4: Drafting

Use the PRD template below. Generate PRODUCT alongside using
[product.md](product.md) — create it when absent, never overwrite existing
positioning. Load [quality.md](quality.md) before presenting the drafts to
the user.

**Drafting notes:**

- Market & differentiation content goes to PRODUCT, not PRD
- Value proposition content goes to PRODUCT, not PRD
- Journeys should be product-level (actor, goal, flow, conditions) — no UI components, endpoints, or implementation details
- Business rules use IDs (BR-1) for traceability
- Edge cases use IDs (EC-1) for traceability

## PRD Template

ALWAYS use this exact template structure:

````markdown
---
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
---

# PRD: {{Product Name}}

## Executive Summary

{{One short paragraph for a quick scan of the spec: the problem, who it is for, the must-have scope, and the primary success metric. Requirements digest only — positioning (what the product is and stands for) lives in PRODUCT, never here.}}

## 1. Problem Statement

{{Describe the problem being solved. What pain point exists? Who is affected? What evidence supports this?}}

## 2. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| {{goal}} | {{how it will be measured}} | {{concrete number or threshold}} |

## 3. User Personas

### {{Persona Name}}

- **Role:** {{role or job title}}
- **Pain Point:** {{primary frustration or problem}}
- **Goal:** {{what they want to achieve with this product}}

## 4. Scope Definition

### Must Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-1 | {{core capability required for launch}} | |
| FR-2 | {{another core capability}} | |

### Should Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-3 | {{important but not launch-blocking}} | |

### Could Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-4 | {{nice-to-have for future iteration}} | |

### Won't Have

| ID | Requirement | Notes |
|----|------------|-------|
| FR-N | {{feature considered and explicitly excluded}} | {{reason for exclusion}} |

### Non-Goals

- {{What is explicitly out of scope and why}}

## 5. User Journeys

### {{Journey Name}}

**Actor:** {{persona}}
**Goal:** {{what the user is trying to accomplish}}

**Pre-conditions:**

- {{what must be true before this journey starts}}

**Main Flow:**

1. {{user action}} → {{system behavior}}
2. {{user action}} → {{system behavior}}
3. {{user action}} → {{system behavior}}

**Alternative Flows:**

- {{step}}a. {{condition}} → {{what happens instead}}

**Post-conditions:**

- {{what is true after the journey completes}}

## 6. Business Rules

| ID | Rule | Scope |
|----|------|-------|
| BR-1 | {{functional constraint that applies across features}} | {{which features/journeys it affects}} |
| BR-2 | {{another business rule}} | {{scope}} |

## 7. Edge Cases

| ID | Scenario | Expected Behavior |
|----|----------|-------------------|
| EC-1 | {{what goes wrong or what unusual situation occurs}} | {{how the product should respond}} |
| EC-2 | {{another exception scenario}} | {{expected behavior}} |

## 8. Non-Functional Requirements

| ID | Requirement | Target |
|----|------------|--------|
| NFR-1 | Performance | {{e.g., page load < 2s}} |
| NFR-2 | Accessibility | {{e.g., WCAG 2.1 AA}} |

## 9. Assumptions

- {{Assumption that, if wrong, would change the plan}}

## 10. Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| {{what could go wrong}} | High | Medium | {{how to address}} |

## 11. Hypotheses to Validate

- [ ] {{Hypothesis to be tested and validated with data or user research}}

## 12. Unknowns

- [ ] TBD: {{Question that needs answering before implementation}}

## 13. References

- {{Link to designs, research, prior art, or related documents}}
````

## PRD Schema

A lead Executive Summary plus 13 numbered sections matching the template:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| Executive Summary | Requirements digest for a quick scan — problem, audience, must-have scope, primary metric (no positioning) | Synthesis of Topics 1, 2, 4 |
| 1. Problem Statement | What problem exists, for whom, with evidence | Topic 1: Problem |
| 2. Goals & Success Metrics | Measurable KPIs (concrete numbers, not vague goals) | Topic 1: Problem |
| 3. User Personas | Who uses this, role, pain point, goal | Topic 2: Users |
| 4. Scope Definition | Must/Should/Could/Won't have, non-goals (FR-1...) | Topic 4: Value & Scope |
| 5. User Journeys | End-to-end flows per persona with pre/post-conditions | Topic 5: Journeys & Constraints |
| 6. Business Rules | Functional constraints across features (BR-1...) | Topic 5: Journeys & Constraints |
| 7. Edge Cases | Exception scenarios and expected behavior (EC-1...) | Topic 5: Journeys & Constraints |
| 8. Non-Functional Requirements | Performance, accessibility, security targets | Topic 4: Value & Scope |
| 9. Assumptions | What we believe to be true that underpins the plan | Validation phase |
| 10. Risks | What could go wrong and how to address it | Validation phase |
| 11. Hypotheses to Validate | Assumptions that need evidence before implementation | Validation phase |
| 12. Unknowns | Questions that need answering before implementation (TBD) | Validation phase |
| 13. References | Links to designs, research, related documents | All phases |

Topic 3 (Market & Differentiation) feeds PRODUCT, not the PRD.

## Guidelines

- Always complete discovery before drafting
- Challenge ideas during discovery and validation — do not be a yes-man
- Present draft for user feedback
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Generate PRODUCT alongside PRD during drafting
- Keep journeys at product level — describe what happens, not how it's built
- Assign IDs to business rules and edge cases for traceability

## Output

- PRD: `docs/product/prd.md`
- PRODUCT: `docs/product/PRODUCT.md`
