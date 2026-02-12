# ADR -- Architecture Decision Record

## Workflow

```
discovery --> drafting
```

2-phase workflow. ADRs record architectural decisions with their context, options, and consequences.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

**Stage 1 -- Context & Drivers:**
- What decision needs to be made?
- What is the context? (technical, business, organizational)
- What are the decision drivers? (forces that influence the decision)

**Stage 2 -- Options (if not already clear):**
- What options were considered?
- What are the trade-offs of each?
- Which option was chosen and why?

Minimum 1 stage. If the user already has the decision and rationale, move directly to drafting.

## Numbering

ADRs are numbered sequentially. Before creating a new ADR:

1. Scan `.specs/docs/` for existing files matching `adr-*-*.md`
2. Extract the highest number
3. Use the next number (e.g., if `adr-003-*` exists, use `004`)
4. If no ADRs exist, start at `001`

Format: 3-digit zero-padded (`001`, `002`, `003`).

## Phase 2: Drafting

**USE TEMPLATE:** `templates/adr.md`

Generate the ADR using the schema below. Present draft to user for review.

## ADR Schema

### Title

Short, descriptive title of the decision (e.g., "Use PostgreSQL for primary data store").

### Status

One of: `proposed` | `accepted` | `deprecated` | `superseded`

If superseded, link to the new ADR: `superseded by [ADR-XXX](adr-xxx-name.md)`

### Context

What is the situation that requires a decision? Include:
- Technical context
- Business constraints
- Team constraints
- Related decisions (link to other ADRs if applicable)

### Decision Drivers

Numbered list of forces that influenced the decision:
1. Force or requirement that shaped the decision
2. Another force or constraint

### Options Considered

For each option:
- **Option name**: Brief description
  - Pros: advantages
  - Cons: disadvantages

### Decision

Which option was chosen and why. State the decision clearly in one sentence, then elaborate on the rationale.

### Consequences

- **Positive**: Benefits of this decision
- **Negative**: Downsides or trade-offs accepted
- **Neutral**: Side effects that are neither positive nor negative

## Status Lifecycle

```
proposed --> accepted --> deprecated / superseded
```

- **proposed**: Decision documented but not yet agreed upon
- **accepted**: Decision agreed upon and in effect
- **deprecated**: Decision no longer relevant
- **superseded**: Replaced by a newer decision (link to it)

## Guidelines

- ADRs are immutable once accepted -- don't edit old ADRs, create new ones that supersede
- Keep ADRs short and focused -- one decision per record
- Context should be understandable by someone who wasn't in the room
- Always document consequences honestly, including negative ones
- Link to related RFCs or TDDs when applicable

## Output

Save to: `.specs/docs/adr-{number}-{name}.md`
