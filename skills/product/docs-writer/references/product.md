# Product — Strategic Positioning

Author the product's strategic positioning in `PRODUCT.md`: what the product is and what it stands for, as prose. Distinct from the PRD, which captures what the product does.

## When to Use

Load this reference to write or update `PRODUCT.md`; see [discovery.md](discovery.md) `## Discovery or Update by Document State`. If `docs/product/PRODUCT.md` is absent, write it during discovery and use confirmed PRD facts when available. If it exists, update only the requested parts by following [reconcile.md](reconcile.md). A positioning change can update PRODUCT without changing the PRD.

## Scope

`PRODUCT.md` is identity, not requirements. It carries the product's posture, audience relationship, personality, what it refuses to be, and the principles that drive design and copy — all as prose. The PRD remains the specification.

Distinction test: two products with an identical feature list must have different `PRODUCT.md` files. Content that survives the same feature list is positioning; content that does not is a requirement and belongs in the PRD.

Three boundary zones to keep clean — the PRD owns the other side of each:

- **Audience** — here: who the product relates to and how (posture, the relationship). PRD: the user as a requirement (job to be done).
- **The "nots"** — here: the aesthetics and postures the product refuses (anti-references). PRD: features ruled out of scope.
- **The "why"** — here: differentiation and positioning. PRD: the problem and its evidence.

## Discovery

Apply [discovery.md](discovery.md) `## Reading Project Files` before reading a PRD or upstream direction. PRODUCT uses one Positioning topic. When writing PRODUCT with a new PRD, use the Users and Market & Differentiation answers instead of asking the same questions again. When writing PRODUCT alone, use confirmed PRD facts as input.

Check `docs/product/brainstorm.md` for an earlier direction. PRODUCT does not depend on this file. If it is absent, run discovery. If it exists, confirm its claims instead of repeating its questions.

| Earlier section | Supplies | Behavior |
|---|---|---|
| Context | Product Purpose — identity, not metrics | confirm |
| Alternatives Considered + Decision | Anti-references — differentiation and rejected styles | confirm |

Use the rejected directions and the reason for rejecting the strongest option to write Anti-references. Ask about register, brand personality, design principles, and audience relationship when the upstream document does not contain them. Do not copy the list of rejected options or Revision History. Write positioning prose, not requirements.

Load [discovery.md](discovery.md) for the shared interview method and critical review.

### Topic: Positioning

**Opening questions:**

- Is the experience itself the product (a landing page, a campaign), or does it serve a task (an app, a dashboard, a tool)? — the register
- Who is this for, and what relationship does it want with them — expert-to-expert, premium, approachable?
- In three words, what is the product's character, and what tone do they imply?
- What does the product refuse to be — the aesthetics, clichés, or postures it rejects?
- What handful of principles drive its design and copy decisions?

**Ask follow-up when:**

- Register is unclear ("a bit of both") → "Which value is the default? Later design work can handle exceptions."
- Personality is generic ("clean, modern, simple") → "Those fit most products. What is specific to this one?"
- No anti-references → "Name a product in this space whose style is wrong for you. What exactly is wrong?"
- Principles restate features → "That is a requirement. What conviction sits behind it?"

**Complete when:**

- Register is a single dominant value (`brand` or `product`) with a reason
- The audience relationship is stated as posture, not a job to be done
- Personality has three adjectives and the tone they imply
- At least one anti-reference and one design principle are captured

## Content Source

Use discovery answers to write positioning prose. When updating `PRODUCT.md`, read it as a source and change only the requested parts. Each section maps to a discovery topic:

| Section | Discovery Source |
|---------|-----------------|
| Register | Positioning topic (the dominant posture) |
| Users | Topic 2: Users (as relationship/posture, not job to be done) |
| Product Purpose | Topic 1: Problem + Positioning topic (identity, not metrics) |
| Brand Personality | Positioning topic |
| Anti-references | Positioning topic + Topic 3: Market & Differentiation |
| Design Principles | Positioning topic |

## Template

ALWAYS use this exact template structure:

````markdown
---
name: [document-name]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: draft
sources: []
---

# Product: [Product Name]

## Register

[`brand` or `product` — the product's dominant posture. brand: the experience is the product (landing, campaign, marketing). product: the experience serves a task (app, dashboard, tool). State one default value and explain why. Later design work handles exceptions.]

## Users

[One paragraph: who the product is for and the relationship it wants with them — expert-to-expert, premium, approachable. Posture, not a backlog of jobs to be done (that is the PRD).]

## Product Purpose

[One paragraph: what the product is and what it stands for — its identity, not its measurable targets (those live in the PRD).]

## Brand Personality

[One paragraph: the product's character and voice. Three adjectives plus the tone they imply (for example, direct, specific, no hedging).]

## Anti-references

[Describe the aesthetics, clichés, and postures that the product rejects.]

## Design Principles

[The handful of principles that drive design and copy decisions — what the product always does, stated as commitments.]
````

MUST NOT contain: requirements, scope or feature lists, success metrics, user journeys, business rules, or accessibility targets — those belong to the PRD.

## Guidelines

- Write every section as prose, not symbol lists. Later design work translates this positioning into its own terms.
- State one default register. Let later design work handle exceptions for specific surfaces.
- Keep identity here and requirements in the PRD — when a line could pass the distinction test either way, it is positioning.
- Omit a section with no signal from discovery rather than writing TBD.

## Output

Write to `docs/product/PRODUCT.md` directly, then report a brief prose summary in chat (up to 2-3 paragraphs) — the register and the identity. Do not paste the full document.
