# Product — Strategic Positioning

Author the product's strategic positioning in `PRODUCT.md`: what the product is
and what it stands for, as prose. Distinct from the PRD, which captures what the
product does.

## When to Use

Loaded by the product-doc flow to author or reconcile `PRODUCT.md`. It resolves by
whether the artifact exists on disk — see [discovery.md](discovery.md)
`## Discovery or Reconcile by Artifact State`. When `docs/product/PRODUCT.md` is
absent, draft it in discovery — possibly seeded by an existing PRD; when it exists,
reconcile only the delta per [reconcile.md](reconcile.md). Positioning shifts
independently of any PRD revision, so a reconcile may touch PRODUCT alone.

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

## Discovery

PRODUCT is drawn from a single Positioning topic. When drafted alongside a new PRD,
it shares that discovery — Users (Topic 2) and Market & Differentiation (Topic 3)
feed positioning directly, so run this topic against what they surfaced rather than
re-asking. When drafted alone (the PRD already exists), run it fresh, seeded by the
PRD.

Seed from an upstream direction when present: check `docs/product/brainstorm.md`. The PRODUCT never depends on it — absent, run discovery as above; present, read it as input and confirm rather than re-ask.

| Upstream section | Seeds | Behavior |
|---|---|---|
| Context | Product Purpose — identity, not metrics | confirm |
| Alternatives Considered + Decision | Anti-references — differentiation and negative space | confirm |

The rejected directions and the deciding factor against the strongest rejected option are what Anti-references captures. Run the rest of the Positioning topic fresh — register, brand personality, design principles, audience posture — which the artifact does not carry. Strip the exploration trail (rejected options as a list, Revision History) and translate to positioning prose, never requirements.

Load [discovery.md](discovery.md) for the shared interview patterns and critical
posture.

### Topic: Positioning

**Opening questions:**

- Is the experience itself the product (a landing page, a campaign), or does it serve
  a task (an app, a dashboard, a tool)? — the register
- Who is this for, and what relationship does it want with them — expert-to-expert,
  premium, approachable?
- In three words, what is the product's character, and what tone do they imply?
- What does the product refuse to be — the aesthetics, clichés, or postures it rejects?
- What handful of principles drive its design and copy decisions?

**Deepen when:**

- Register is hedged ("a bit of both") → "Which dominates? Downstream resolves
  per-surface exceptions; name the default."
- Personality is generic ("clean, modern, simple") → "Those fit most products. What
  is specific to this one?"
- No anti-references → "Name a product in this space whose vibe is wrong for you.
  What exactly is off?"
- Principles restate features → "That is a requirement. What conviction sits behind it?"

**Sufficient when:**

- Register is a single dominant value (`brand` or `product`) with a reason
- The audience relationship is stated as posture, not a job to be done
- Personality has three adjectives and the tone they imply
- At least one anti-reference and one design principle are captured

## Content Source

Positioning prose, drawn from discovery. Under reconcile, the existing `PRODUCT.md`
is itself a source — read as input, with only the delta reworked. Each section maps
to a discovery topic:

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
journeys, business rules, or accessibility targets — those belong to the PRD.

## Guidelines

- Write every section as prose, not symbol lists — downstream design skills
  translate this positioning into their own vocabularies.
- State the register as a single dominant value; let downstream resolve
  per-surface exceptions.
- Keep identity here and requirements in the PRD — when a line could pass the
  distinction test either way, it is positioning.
- Omit a section with no signal from discovery rather than writing TBD.

## Output

Write to `docs/product/PRODUCT.md` directly, then report a brief prose summary in
chat (up to 2-3 paragraphs) — the register and the identity. Do not paste the
full document.
