# Shared Discovery Patterns

Common interview and discovery patterns used across document types.

## When to Use

Auto-loaded by the product-doc flow (PRD and PRODUCT), Design Doc, and ADR workflows during discovery. Also supplies the discovery-or-reconcile decision and the critical posture that reconcile reuses. Not a direct trigger.

## Core Principle

Never assume context. When no artifact exists yet, ask before drafting (full discovery). When the artifact already exists on disk, read it as input and ask only about the gap or the change (reconcile). The critical posture is always on either way — depth varies, scrutiny does not. Same principle throughout: understand the problem before writing the solution.

## Discovery or Reconcile by Artifact State

Whether a document is discovered fresh or reconciled is not a chosen mode — it follows from whether the artifact already exists on disk. Absent → run full discovery. Present → reconcile: read it as input and work only the gap or the declared change (light discovery on the delta). This holds for the PRD, PRODUCT, and the Design Doc alike.

For the product-doc pair (`docs/product/PRD.md`, `docs/product/PRODUCT.md`), each artifact resolves independently, so a single run can mix the two — discovery for the absent artifact, reconcile for the present one:

| State on disk | Action |
|---|---|
| Neither exists | Discovery on both (the only full-interview case) |
| PRD exists, PRODUCT absent | Reconcile PRD + discovery PRODUCT seeded by the PRD |
| PRODUCT exists, PRD absent | Discovery PRD seeded by PRODUCT + reconcile PRODUCT |
| Both exist | Reconcile both, scoped by declared intent |

The Design Doc resolves the same way against its own artifact (`docs/tech/design-doc.md`): absent → discovery, present → reconcile the delta. It has no sibling to seed it, so it never mixes.

Discovery builds an artifact fresh — its depth is the full topic set minus whatever an existing sibling already supplies. Reconcile reads an existing artifact as input and works only the gap or the declared change. The reconcile procedure lives in [reconcile.md](reconcile.md).

ADRs are the exception: append-only, superseded by a new record and never reconciled, so this check does not apply to them.

## Interview Strategy

Discovery is adaptive, not scripted. Each document type defines topics with opening questions. The agent decides when to deepen and when to move on based on the quality of answers received.

### How It Works

1. Start each topic with its opening questions (2-4 per topic)
2. Evaluate answers against the topic's sufficiency criteria
3. If criteria are not met, deepen -- ask follow-ups targeting the gap
4. If criteria are met, move to the next topic
5. Summarize understanding before advancing

### Adaptive Deepening

Probe further when answers are:

- **Vague**: "users want something better" → ask for specifics
- **Assumed**: stated as fact without evidence → ask for evidence or mark as hypothesis
- **Conflated**: multiple concepts mixed in one answer → separate and explore each
- **Solution-first**: describes what to build before why → redirect to the problem
- **Overly broad**: "everyone", "all cases" → narrow down to the most important

Move on when:

- The topic's sufficiency criteria are met
- The user explicitly says "I don't know" (mark as TBD)
- Further questioning would not yield new information

### Question Principles

- Lead with a proposed interpretation that invites redirect ("sounds like the core problem is X — is that right, or more like Y?") rather than a cold open-ended question; it unsticks vague thinking and, because it offers the alternative, is not a biasing leading question. Scale the POV to the document's altitude — a PRD maps understanding, a Design Doc recommends decisions
- Do not scan the codebase upfront — only when a question about the system's present factual state arises (existing flows, schema, endpoints, current behavior) that the code can answer, read it instead of asking and state what you found before moving on. Motivation, value, and desired future behavior stay with the user — the code answers what is, never why or what should be. Extract the answer at the document's altitude — for a PRD or PRODUCT, current-state facts inform the problem and journeys but code detail never crosses into the artifact; a Design Doc may carry it
- Build follow-ups on what the user actually said, not on a script
- One question at a time -- never batch multiple questions in a single message
- Summarize understanding before moving to the next topic

## Discovery Depth by Type

**Full discovery** (adaptive deepening, sufficiency criteria, critical posture):

| Type | Structure | Focus |
|------|-----------|-------|
| PRD | 5 topics | Problem, users, market, scope, journeys & constraints |
| PRODUCT | 1 topic | Positioning: register, audience posture, personality, anti-references, principles (part of the product-doc pair; depth = full minus what an existing sibling already supplies) |
| Design Doc | 4 topics | Context & goals, the design, alternatives & trade-offs, cross-cutting concerns |
| ADR | 1 topic | The decision: context forces, alternatives, consequences (lightweight) |

Design Doc discovery stays lean and trade-off-focused. See [design.md](design.md) for the topic-by-topic workflow and the ADR linkage pattern that promotes Alternatives rows into formal ADRs.

## Synthesis Pattern

After discovery is complete, synthesize before drafting:

1. Summarize what was learned
2. Identify gaps (mark as TBD)
3. Surface assumptions made
4. Present synthesis to user for confirmation
5. Only proceed to drafting after user confirms

This is the full-discovery gate. When reconciling, the equivalent is the scoped-plan confirmation in [reconcile.md](reconcile.md) — confirm the delta, not a full re-synthesis.

## Critical Posture

Discovery is not a formality. Challenge ideas with respect, but never be a yes-man.

### Principles

- **Ask for evidence.** When the user claims a problem exists, ask: "How do you know this problem exists? What evidence do you have?" Accept anecdotal evidence but distinguish it from data.
- **Challenge weak ideas.** If an idea sounds like a solution looking for a problem, say so. "This sounds like you already decided the solution -- can we go back to the problem?"
- **Flag a fragile direction.** If the problem is real but the proposed approach seems fragile, say so. For a product doc, recommend reopening the direction decision before specifying rather than generating alternatives here; for a Design Doc, weighing technical alternatives is this document's own job. Frame it as a question, not a demand.
- **Flag scope creep.** If the user keeps adding features or expanding scope during discovery, pause and realign. "We started with X -- this is now X + Y + Z. Should we narrow down?"
- **Gate advancement.** Only move from discovery to the next phase when you have confidence that the problem is understood. If something feels off, ask one more question rather than proceeding with uncertainty.

### What This Looks Like

| Situation | Passive Response | Critical Response |
|-----------|-----------------|-------------------|
| User describes vague problem | "Okay, let's proceed" | "Who specifically has this problem? How often?" |
| User jumps to solution | "Got it, I'll include that" | "Before we define the solution -- what problem does this solve?" |
| User adds scope mid-discovery | "I'll add that too" | "This changes the scope significantly. Should we focus on the core first?" |
| User has no evidence | "Noted" | "Without evidence, this is an assumption. Should we mark it as a hypothesis to validate?" |

## Quality Gate

These criteria gate full discovery. When reconciling, the gate is the scoped-plan confirmation in [reconcile.md](reconcile.md), applied to the delta rather than to every topic.

Before moving from discovery to drafting, verify:

- [ ] All topics have met their sufficiency criteria or gaps are marked as TBD
- [ ] Open questions and unknowns are explicitly marked (TBD)
- [ ] User has confirmed the synthesis
- [ ] No critical ambiguity remains (ask if unclear)
- [ ] Problem is understood with evidence or explicitly marked as hypothesis
