# Product — Strategic Positioning

Author the product's strategic positioning in `PRODUCT.md`: what the product is
and what it stands for, as prose. Distinct from the PRD, which captures what the
product does.

## When to Use

Generated alongside the PRD by default during drafting. Also authored standalone
to create or update positioning when strategy shifts, independent of any PRD
revision.

## Scope

`PRODUCT.md` is identity, not requirements. It carries the product's posture,
audience relationship, personality, what it refuses to be, and the principles
that drive design and copy — all as prose. The PRD remains the specification.

Distinction test: two products with an identical feature list must have different
`PRODUCT.md` files. Content that survives the same feature list is positioning;
content that does not is a requirement and belongs in the PRD.

Three boundary zones to keep clean — the PRD owns the other side of each:

- **Audience** — here: who the product relates to and how (posture, the
  relationship). PRD: the user as a requirement (job to be done).
- **The "nots"** — here: the aesthetics and postures the product refuses
  (anti-references). PRD: features ruled out of scope.
- **The "why"** — here: differentiation and positioning. PRD: the problem and
  its evidence.

## Content Source

Positioning prose, drawn from discovery. Each section maps to a discovery topic:

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
name: {{document-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
---

# Product: {{Product Name}}

## Register

{{`brand` or `product` — the product's dominant posture. brand: the experience
is the product (landing, campaign, marketing). product: the experience serves a
task (app, dashboard, tool). State one value plus a line on why. Surfaces that
diverge from this default are resolved downstream, not here.}}

## Users

{{One paragraph: who the product is for and the relationship it wants with them —
expert-to-expert, premium, approachable. Posture, not a backlog of jobs to be
done (that is the PRD).}}

## Product Purpose

{{One paragraph: what the product is and what it stands for — its identity, not
its measurable targets (those live in the PRD).}}

## Brand Personality

{{One paragraph: the product's character and voice. Three adjectives plus the
tone they imply (e.g., direct, specific, no hedging).}}

## Anti-references

{{What the product refuses to be — the aesthetics, clichés, and postures it
rejects, as prose. The negative space of the identity.}}

## Design Principles

{{The handful of principles that drive design and copy decisions — what the
product always does, stated as commitments.}}
````

MUST NOT contain: requirements, scope or feature lists, success metrics, user
journeys, business rules, accessibility targets, or design tokens — those belong
to the PRD or to downstream design artifacts.

## Guidelines

- Write every section as prose, not symbol lists — downstream design skills
  translate this positioning into their own vocabularies.
- State the register as a single dominant value; let downstream resolve
  per-surface exceptions.
- Keep identity here and requirements in the PRD — when a line could pass the
  distinction test either way, it is positioning.
- Omit a section with no signal from discovery rather than writing TBD.

## Output

Saved to `docs/product/PRODUCT.md`.
