# PRD — Product Requirements Document

Capture product requirements: problem, audience, scope, phases, and success metrics.

## Scope

Product requirements only: problem, audience, scope, phases, success metrics. Never carries implementation content — no architecture, tech stack, UI components, API endpoints, or code-level decisions — nor strategic positioning (brand personality, anti-references). Architecture and implementation details belong to the Design Doc or ADR; positioning belongs to PRODUCT.

A section is a technical decision in disguise when it presents two implementation options and asks the reader to choose — microservices vs monolith, SQL vs NoSQL, REST vs GraphQL, framework choice, deployment topology. Move that decision to the Design Doc or an ADR and leave a reference here.

## Workflow

```text
check disk
├ PRD absent  → discovery → validation → drafting
└ PRD present → update requested parts (reconcile.md)
```

Check whether `docs/product/PRD.md` exists; see [discovery.md](../references/discovery.md) `## Discovery or Update by Document State`. If absent, run the three phases below and use any confirmed earlier direction as input. If present, update only the requested parts by following [reconcile.md](../references/reconcile.md). Handle PRODUCT independently based on whether it exists.

### Phase 1: Discovery

Load [discovery.md](../references/discovery.md) for the shared interview method and critical review.

Run these three phases when no PRD exists. Never assume context. Each topic defines two or three opening questions, reasons to ask a follow-up, and completion criteria.

#### Read an Earlier Direction

Apply [discovery.md](../references/discovery.md) `## Reading Project Files`, then check `docs/product/brainstorm.md` before interviewing. If absent, run full discovery. If present, confirm its claims and ask only for missing PRD information.

| Upstream section | Supplies | Behavior |
|---|---|---|
| Context | Topic 1 — problem, motivation, current state | confirm; ask follow-ups only for evidence gaps |
| Constraints | Assumptions & Risks | confirm |
| Success Criteria | Goals & metrics | confirm |
| Alternatives Considered + Decision | Topic 3 (when it runs), chosen-approach rationale | confirm |
| Trade-offs Accepted | Out of Scope; Risks when a trade-off rests on a fragile assumption | confirm |
| Key Assumption | Assumptions | carry |
| Open Questions | Open Questions | carry |

Present each supplied topic as an interpretation for the user to confirm or correct. Do not repeat its opening questions. Run discovery for information the upstream document does not contain: audience, scope levels and FR IDs, phases, and NFRs.

Do not copy rejected alternatives, Revision History, or the direction's name into the PRD. Carry only the confirmed problem, constraints, and criteria, expressed as product requirements.

The earlier direction supplies product intent. Codebase inspection supplies facts about current behavior. Each source is optional and independent.

#### Topic 1: Problem

**Opening questions:**

- What problem are you solving, and who has it?
- What evidence shows the problem exists?
- Why is it worth solving now?

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

- Who uses this, and in what situation?
- What are the main things they need to do with it?

**Ask follow-up when:**

- "Everyone" or too broad → "Who is the *most* affected? Describe one specific person."
- Multiple user types → "Which profile is primary? What happens when their needs conflict?"
- Vague use cases → "Walk me through a concrete scenario."

**Complete when:**

- One to three concrete user profiles
- Main use cases are specific enough to derive requirements from

#### Topic 3: Market & Differentiation

**Used by PRODUCT, not the PRD** — run this topic only when writing PRODUCT in the same run. Skip it for a PRD-only run.

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

#### Topic 4: Scope & Phases

**Opening questions:**

- What must exist at launch, and what can wait?
- What does the product deliberately not do?
- What defines success, and what could invalidate the project?

**Ask follow-up when:**

- Everything is "must have" → "If you could only ship 3 features, which 3?"
- Scope keeps expanding → "We started with X, now it's X+Y+Z. Should we narrow down?"
- Features without clear user connection → "Which user profile needs this? What problem does it solve for them?"
- No success measure → "What single metric would tell you this worked?"
- Quality needs (performance, security, accessibility, privacy) not mentioned → "Does the product have quality requirements beyond its features?"

**Complete when:**

- Clear must/should/could prioritization, with a reason for each cut
- Each must-have connects to the primary problem and a user profile
- A primary metric exists or is marked TBD
- MVP and what follows are separated
- Assumptions and risks are named

### Phase 2: Validation

Challenge what was learned. This phase exists to prevent building the wrong thing.

1. **Challenge viability**: Point out risks and weak spots identified during discovery
2. **Question scope**: Is the scope realistic for a first version? If not, push back
3. **Suggest simplifications**: Propose cuts when scope is ambitious. "Do you need X for launch, or can it wait?"
4. **Flag a fragile direction**: If the direction itself seems fragile after discovery, say so and recommend reopening the direction decision before specifying — the PRD does not generate or choose alternatives
5. **Define scope**: Categorize features into must/should/could/won't priorities
6. **Identify hypotheses**: What assumptions need evidence before or during implementation?

### Phase 3: Drafting

1. Use the PRD template below.
2. Handle PRODUCT by following [product.md](product.md). If `PRODUCT.md` is absent, write it from the confirmed discovery facts. If it exists, update it by following [reconcile.md](../references/reconcile.md). Do not replace supported positioning without new evidence.
3. Run [quality.md](../references/quality.md).
4. Write each document to its path, then reread each per [quality.md](../references/quality.md) `## Reread`.
5. **Report.** Report each path, what each document holds in one to three sentences — the must/should/could scope and the primary metric for the PRD — and any open question or TBD each carries. Never paste the documents.

**Drafting notes:**

- Market & differentiation content goes to PRODUCT, not PRD
- Value proposition content goes to PRODUCT, not PRD
- Out of Scope lists outcome-level exclusions; capabilities cut from the release go to Scope → Won't Have
- Won't Have must record the reason for exclusion so future revisits have context
- NFRs state the requirement without prescribing the mechanism ("search stays responsive on mobile networks", not "use Redis caching"). Add a number only when the user supplies one; otherwise keep the requirement in words
- Phases name what ships in the MVP and what follows, each with the criterion to advance
- Assumptions & Risks is a flat list; each risk carries its mitigation
- Out-of-team blockers enter Assumptions & Risks; technical dependencies belong in the Design Doc

## PRD Template

For a new document, read `<this-skill>/assets/prd.template.md`, copy its exact structure, remove every comment, and replace every square-bracket slot. For an existing document, follow [reconcile.md](../references/reconcile.md); use the template only to check structure and never copy it over unchanged content.

## PRD Schema

9 numbered sections matching the template:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| 1. Problem | The pain, who is affected, evidence, why it is worth solving | Topic 1: Problem |
| 2. Audience | User profiles and main use cases | Topic 2: Users |
| 3. Goals & Metrics | Goals with metrics and one primary metric | Topic 1: Problem, Topic 4: Scope & Phases |
| 4. Scope | Must/Should/Could/Won't (FR-1...) plus Out of Scope | Topic 4: Scope & Phases |
| 5. Non-Functional Requirements | Quality requirements (NFR-1...) in words or with a supplied number | Topic 4: Scope & Phases |
| 6. Phases | MVP and what follows, with the criterion to advance | Topic 4: Scope & Phases |
| 7. Assumptions & Risks | What is assumed and what could invalidate the project, with mitigations | Validation phase |
| 8. Open Questions | Unresolved questions as a checklist | Validation phase |
| 9. References | Typed references to related documents that exist | All phases |

Topic 3 (Market & Differentiation) supplies PRODUCT, not the PRD.

## Guidelines

- Complete discovery before writing a new PRD. For an existing PRD, update only the requested parts.
- Challenge weak claims during discovery, validation, and updates.
- Write the PRD to its path directly, reread it per [quality.md](../references/quality.md) `## Reread`, then report as Phase 3 step 5 states
- Mark unknowns as TBD rather than inventing constraints or numbers
- Discover PRODUCT if absent. Update only the requested parts if present.
- Record a reason for exclusion on every Won't Have item
- Reference only documents that exist; omit a reference rather than writing "None"

## Output

- PRD: `docs/product/PRD.md`
- PRODUCT: `PRODUCT.md`
