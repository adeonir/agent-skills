# ADR — Architecture Decision Record

Record a single architecture decision with its context, consequences,
and rejected alternatives.

## When to Use

When a meaningful architecture decision has been made (or is about to
be made) that future engineers will need to understand: technology
choice, integration pattern, data model shape, deprecation, migration
strategy. One ADR per decision. ADRs are short (1-2 pages) and become
immutable once accepted — superseded by new ADRs, never edited in
place.

**Key principle:** ADRs capture *the* decision and *why*, not the
exploration that led to it. If multiple decisions are still in play
or trade-offs are being weighed, write a Design Doc first and record
the outcomes as ADRs.

## When NOT to Write an ADR

- The decision is trivial or has no meaningful alternatives
- Multiple decisions are bundled — split into separate ADRs or step
  back to a Design Doc
- The decision is still being explored — use a Design Doc to discuss
  trade-offs first
- The decision is implementation detail, not architecture
  (variable naming, file layout, formatting)

## Workflow

```text
context → validation → drafting
```

### Phase 1: Context

Load [discovery.md](discovery.md) for shared interview patterns and
critical posture.

**Check Existing Context:**

Scan upstream artifacts for embedded decisions that should be lifted
into their own ADR:

| Source | Where decisions hide |
|--------|---------------------|
| `docs/tech/design-doc.md` | `## 4. Alternatives Considered & Trade-offs` rows (rows with `Record = —` are candidates for promotion) |
| `docs/product/PRD.md` | Constraints, NFR rationale, research notes |

If found, list candidate decisions and ask the user which one this
ADR records. Multiple decisions in a single source means multiple
ADRs — one per decision, not one ADR summarizing all of them.

Look for existing ADRs at `docs/adr/`. If found, list them
and ask whether this ADR supersedes any.

**Discovery (1 topic):**

#### Topic: The Decision

**Opening questions:**

- What is the decision being recorded?
- What forces (technical, business, regulatory, team) made this
  decision necessary now?
- What alternatives were considered?
- What positive and negative consequences are being accepted?

**Deepen when:**

- Multiple decisions surface → "These look like separate decisions.
  Should we split into multiple ADRs?"
- No alternatives mentioned → "What other options were on the table?
  If none, is this really an architecture decision?"
- Consequences are all positive → "What cost or limitation are we
  accepting? Every decision has trade-offs."
- Decision is vague → "Stated as a positive imperative, what will we
  do? 'We will X' or 'We will not X'."

**Sufficient when:**

- One decision is clearly named
- Context forces are documented
- At least one alternative is recorded with rejection reason
- Positive AND negative consequences are both identified

### Phase 2: Validation

Before drafting, confirm:

- [ ] Exactly one decision (not bundled)
- [ ] Decision can be stated as a positive imperative ("We will...")
- [ ] Context is value-neutral (facts, not advocacy)
- [ ] Consequences include trade-offs accepted, not just benefits
- [ ] Numbering checked: next sequential ID in `docs/adr/`

### Phase 3: Drafting

Use the template below. Run the gates in [quality.md](quality.md) before
writing, then write the ADR to `docs/adr/NNNN-slug.md` and report a brief prose
summary in chat (up to 2-3 paragraphs) — the ADR ID and the decision recorded.
Do not paste the full document.

**Numbering:** Scan `docs/adr/` for existing files. Next ADR
takes the next zero-padded ID (`001`, `002`, ...). Filename and
frontmatter `name` use bare ID (`001-slug`); document title heading
uses prefix (`ADR-001`).

## ADR Template

ALWAYS use this exact template structure:

````markdown
---
name: {{NNNN-slug}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: proposed
supersedes: []
superseded-by: []
sources: []
---

# ADR-{{NNNN}}: {{Decision Title}}

## Context

{{Forces at play that make this decision necessary: technical
constraints, business pressures, regulatory requirements, team
realities, prior decisions. Value-neutral — describe the situation
without advocating for an outcome. Reader should understand why a
decision is being forced now.}}

## Decision

{{The decision being made, stated as a positive imperative: "We will
adopt X", "We will deprecate Y in favor of Z", "We will not introduce
W". One decision per ADR. Be specific and unambiguous.}}

## Consequences

### Positive

- {{Capability unlocked, problem resolved, or benefit gained}}
- {{Another positive outcome}}

### Negative

- {{Cost, limitation, or risk accepted by this decision}}
- {{Another trade-off being absorbed}}

### Neutral

- {{Downstream change that is neither good nor bad — migration work,
  new dependency, vocabulary shift, knock-on decisions surfaced}}

## Alternatives Considered

| Option | Reason Rejected | Record |
|--------|-----------------|--------|
| {{Alternative A}} | {{Why this was not chosen}} | {{— or ADR-NNNN}} |
| {{Alternative B}} | {{Why this was not chosen}} | {{— or ADR-NNNN}} |

## References

- {{Link to the Design Doc's Alternatives Considered section, e.g. `docs/tech/design-doc.md`}}
- {{Link to PRD that contains broader context}}
- {{External RFCs, vendor docs, prior art}}
````

## ADR Schema

5 sections matching the template:

| Section | Content | Discovery Source |
|---------|---------|-----------------|
| Context | Forces making the decision necessary | Topic: opening + deepen |
| Decision | The change, stated as positive imperative | Topic: deepen |
| Consequences | Positive, negative, neutral outcomes | Topic: deepen |
| Alternatives Considered | Rejected options with reasoning and Record column linking to other ADRs when relevant | Topic: deepen |
| References | Anchor link back to Design Doc Alternatives row when extracted from one, plus PRD, prior ADRs, external links | All phases |

## Guidelines

- One decision per ADR — split or step back to a Design Doc if bundled
- State the decision as a positive imperative ("We will...")
- Keep context value-neutral — facts that force the decision, not
  arguments for the outcome
- Always record both positive and negative consequences — every
  decision has trade-offs
- ADRs are immutable once accepted — supersede with a new ADR, never
  edit history
- Number ADRs sequentially with zero-padding — filename `001-slug.md`, heading `ADR-001`
- When extracted from a Design Doc Alternatives row, the ADR's
  References section links back to the design doc section anchor;
  the Design Doc row's `Record` column is updated to this ADR's ID
- Alternatives Considered Record column defaults to `—`; populate
  with `ADR-NNNN` only when the alternative itself has been
  recorded as a separate ADR
- An ADR references only prior ADRs — a genuine backward dependency,
  never a thematic "see also"; it never anticipates or links a later
  one. Inter-ADR lifecycle links live in frontmatter
  (`supersedes`/`superseded-by`), not the body
- Title and slug name the decision the same way — filename
  `NNNN-slug.md` and heading `# ADR-NNNN: Title` use the same term
- Monitoring criteria, confirmation steps, and follow-up actions belong
  in the issue tracker, not in the ADR
- External facts (vendor pricing, provider capabilities) are dated and
  kept verifiable — e.g. "rates valid as of {{Month YYYY}}"

## Status Lifecycle

```text
proposed → accepted → deprecated
                      → superseded (by ADR-NNNN)
```

- **proposed**: Drafted, awaiting review. Editable.
- **accepted**: Approved and in effect. Immutable.
- **deprecated**: No longer recommended but not replaced. Immutable.
- **superseded**: Replaced by a newer ADR. Frontmatter `superseded-by`
  links to the replacement. Immutable.

When superseding an ADR, the new ADR's frontmatter `supersedes` lists
the prior ADR ID, and the prior ADR's status moves to `superseded`
with `superseded-by` populated.

## Anti-Pattern: Bundled Decisions

An ADR titled "API and Database Decisions" or "Q2 Architecture
Choices" bundles unrelated decisions, making each one harder to
reference, supersede, or reason about. One decision per ADR. If the
draft has multiple "We will..." statements covering distinct concerns,
split into separate ADRs.

## Anti-Pattern: Advocacy as Context

Context that argues for the chosen outcome ("Postgres is the obvious
choice because...") is not context — it's a sales pitch. Context
states the forces; the Decision states the choice; the Alternatives
Considered table justifies the rejection of other options. Keeping
these separate makes the ADR honest and reviewable.

## Anti-Pattern: Consequences Without Trade-offs

Listing only positive consequences hides the cost of the decision.
Every architecture decision absorbs a trade-off — vendor lock-in,
operational complexity, learning curve, deprecation debt. If the
Negative section is empty, the decision either has no trade-offs (rare
— reconsider whether this needs an ADR) or the trade-offs are being
ignored (more likely — push back).

## Anti-Pattern: Anticipating Future ADRs

An ADR records a decision at a point in time and does not know the
future — even when authored retroactively. It must not reference, link
to, or promise an ADR or decision made after it: "will be handled in a
separate ADR", a "see ADR-012" pointing forward, or a scope note ("this
decision does not prescribe X") that presupposes X is already a known
future question. The author may know what came next; the ADR must not.

Legitimate references point backward — to a prior ADR the decision
genuinely depends on — or state conditional reversibility ("may be
revisited if volume grows") without naming a future decision.

## Anti-Pattern: Speculative Neutral

The Neutral section records factual downstream consequences — migration
work, a new dependency, a vocabulary shift, a knock-on decision
surfaced. It is not a place to speculate about the future of the
decision itself: "will be revisited if X", "metrics evaluated later",
"validated live after launch". Those presume the ADR knows whether and
when the decision will be revised, which it cannot. State the neutral
fact and stop. If the Neutral section has nothing factual to say, omit
it rather than fill it with speculation.

## Anti-Pattern: Strawman Alternatives

Rejecting a real alternative with a reason that does not hold makes the
ADR dishonest and the decision unreviewable. The recurring example:
dismissing a workspace monorepo because it "forces shared tooling/CI" —
it does not; workspaces give per-package tooling. Every rejection reason
must be accurate and must actually apply to that option. If the
strongest alternative can only be rejected with a weak or false reason,
the decision itself needs reexamining — not a tidier excuse.

## Anti-Pattern: Planning or Scope in the Decision

The Decision states the choice and the rationale behind it — nothing
else. It does not carry implementation planning ("automated via CI,
pipeline TBD") or product scope (feature lists, tier/plan allocation).
Planning belongs in the tracker or design doc; product scope belongs in
the PRD. If the Decision reads like a build plan or a requirements
table, lift that content out and leave only the decision and why.

## Anti-Pattern: Narrative Context

Context states the force that makes the decision necessary — directly,
in the first sentence. It does not re-introduce the product ("Acme is a
platform that...", "The product needs a..."), narrate the situation
conversationally, or smuggle in the argument for the chosen option as
background (an inventory of everything two options share is an argument
for merging them, not context). Re-establishing what the product is
belongs in the PRD or design doc; the argument for the choice belongs in
the Decision and Alternatives. Open on the force.

## Output

Save to: `docs/adr/{{NNNN}}-{{slug}}.md`

ADRs accumulate as an append-only log. Never overwrite a prior ADR;
write a new one that supersedes it.
