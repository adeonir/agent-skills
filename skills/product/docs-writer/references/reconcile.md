# Reconcile an Existing Document

Update an existing PRD, PRODUCT, or Design Doc by reading it as input and scrutinizing only the delta, instead of re-running full discovery or overwriting it.

## When to Use

When `docs/product/PRD.md`, `docs/product/PRODUCT.md`, or `docs/tech/design-doc.md` already exists on disk. A present artifact reconciles while any absent one runs discovery (see [discovery.md](discovery.md) `## Discovery or Reconcile by Artifact State`). Auto-loaded when the target artifact is present; not a direct trigger.

## Procedure

```text
triage → scope → validate delta → declare settled → confirm → draft
```

1. **Triage.** Read the existing artifact(s) as input. Inventory what is already
   captured and evidenced. Nothing here is re-elicited just because the run
   restarted — settled content stays settled.
2. **Scope by intent.** Pin down what the user actually wants to change. The
   reconcile touches only that, plus whatever it provably affects. If the intent
   is vague, ask — a vague change is as unsafe as a vague greenfield brief.
3. **Validate the delta.** Apply the critical posture to the change, not to the
   whole doc — see [discovery.md](discovery.md) `## Critical Posture`. The
   anti-yes-man scrutiny is scoped to the delta: "Why this change? What evidence?",
   "You asked to update X — this is now X + Y + Z, should we narrow?", "The doc
   records this with evidence — what changed to overturn it?". Then check the delta
   against the untouched sections: a changed metric that contradicts a persona, a
   new rule that breaks an existing journey, must surface here.
4. **Declare what is settled.** Before drafting, state plainly what the reconcile
   took as settled and what it scrutinized — e.g. "reconciling the Goals table;
   Personas and Journeys taken as settled". This is the safeguard against silently
   rubber-stamping or silently rewriting; the user can see and correct the boundary.
5. **Confirm the scoped plan.** Get explicit agreement on the scoped change before
   editing. This replaces the greenfield synthesis gate — confirm the delta, not a
   full re-synthesis.
6. **Draft.** Apply the change using the artifact's own template — [prd.md](prd.md)
   for the PRD, [product.md](product.md) for PRODUCT, [design.md](design.md) for the
   Design Doc — preserving every section the scope did not touch. Write the change to
   the artifact's path, then report a brief prose summary of the delta in chat — what
   changed and where. Do not paste the full document.

Some artifacts mark regions immutable. A Design Doc's Alternatives Considered rows
recorded as an ADR (`Record = ADR-NNN`) are frozen — reverse them with a superseding
ADR and a new row, never an in-place edit (see [design.md](design.md) `## ADR
Linkage`). Reconcile the editable surface around them.

## Reading the Sibling Artifact

When one artifact is absent and seeded by the other (a PRD seeded by an existing
PRODUCT, or a PRODUCT seeded by an existing PRD), read the sibling for coverage and
context only. Its tokens never cross verbatim into the artifact being built, and the
PRD/PRODUCT boundary holds: requirements stay in the PRD, positioning stays in
PRODUCT, with audience-as-relationship, refused aesthetics, and differentiation on
the PRODUCT side. The sibling fills discovery gaps; it is not copied. The Design Doc
has no sibling to seed it, so this applies to the product-doc pair only.

## Frontmatter on Reconcile

Preserve the existing `created` date and `sources`. Bump `updated` to the current
date. Where the doc carries a `status` (PRD, PRODUCT), leave it as it stands — a
reconcile does not reset an accepted doc to `draft` unless the user is deliberately
reopening it. The Design Doc has no `status` field.
