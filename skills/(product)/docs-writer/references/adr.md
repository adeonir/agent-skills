# ADR -- Architecture Decision Record

## When to Use

When recording an architectural decision and its rationale.

## Workflow

```
[clarification] --> drafting
```

Direct drafting with optional clarification. ADRs record decisions that were already made -- the author comes with context, options, and the chosen path. Only clarify when input is incomplete.

## Clarification (when input is incomplete)

Evaluate the user's input against the sufficiency criteria below. If all criteria are met, skip directly to drafting. If gaps exist, ask only about the gaps.

### Context & Drivers

**Sufficient when:**
- Decision is stated as a clear choice between options
- Context includes technical and non-technical factors
- Decision drivers are identified

**Clarify when:**
- Decision not clearly framed → "Frame it as a choice: 'We need to decide between X and Y.'"
- Context missing non-technical dimension → "What business or team forces influence this?"
- Drivers not prioritized → "Which of these forces matters most?"

### Options

**Sufficient when:**
- At least 2 genuine options documented with pros/cons
- Chosen option has clear rationale
- Rejected options have clear rejection reasons

**Clarify when:**
- Only one option → "What else was considered? Every decision has alternatives."
- Trade-offs one-sided → "What are the downsides of the chosen option?"
- No rejection rationale → "Why not option X? What specifically ruled it out?"

## Numbering

ADRs are numbered sequentially. Before creating a new ADR:

1. Scan `.artifacts/docs/adr/` for existing files matching `{number}-*.md`
2. Extract the highest number
3. Use the next number (e.g., if `003-*` exists, use `004`)
4. If no ADRs exist, start at `001`

Format: 3-digit zero-padded (`001`, `002`, `003`).

## Drafting

**USE TEMPLATE:** `templates/adr.md`

Generate the ADR using the schema below. Present draft to user for review.

**Title:** Derived from the decision -- short and descriptive (e.g., "Use PostgreSQL for primary data store"). Goes in the filename: `{number}-{name}.md`.

**Frontmatter:** Template includes YAML frontmatter with `status`, `date`, and `deciders`. Status values: `proposed` | `accepted` | `deprecated` | `superseded`.

## ADR Schema

8 sections matching `templates/adr.md`:

| Section | Content |
|---------|---------|
| 1. Context | Situation requiring a decision -- technical, business, team forces (value-neutral language) |
| 2. Decision Drivers | Numbered forces that influenced the decision |
| 3. Options Considered | Each option with pros/cons (at least 2 genuine options) |
| 4. Decision | Chosen option in active voice ("We will..."), with rationale tied to drivers |
| 5. Consequences | Positive, negative, neutral outcomes and residual risks |
| 6. Confirmation | How to validate the decision is working (tests, fitness functions, metrics, reviews) |
| 7. Follow-Up Actions | Tasks required to implement or communicate the decision |
| 8. References | Links to related RFCs, ADRs, documentation |

## Status Lifecycle

```
proposed --> accepted --> deprecated / superseded
```

- **proposed**: Decision documented but not yet agreed upon
- **accepted**: Decision agreed upon and in effect
- **deprecated**: Decision no longer relevant
- **superseded**: Replaced by a newer decision (link to it)

## Guidelines

**DO:**
- Keep ADRs short and focused -- one decision per record
- Write context understandable by someone who was not in the room
- Document consequences honestly, including negative ones
- Link to related RFCs or Design Docs when applicable
- Create new ADRs that supersede old ones when decisions change

**DON'T:**
- Edit accepted ADRs -- they are immutable once accepted
- Combine multiple decisions into a single ADR
- Omit negative consequences to make the decision look better

## Output

Save to: `.artifacts/docs/adr/{number}-{name}.md`
