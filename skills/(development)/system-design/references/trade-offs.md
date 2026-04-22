# Trade-offs

Identify key architectural decisions and present them as structured
comparisons with explicit recommendations.

## When to Use

Load after `requirements.md` quality gate passes. Run before architecture
mapping.

## Decision Identification

Surface decisions that requirements leave open. Common categories:

- **Storage**: relational vs document vs key-value vs graph vs time-series
- **Communication**: synchronous (REST, gRPC) vs asynchronous (queues, events)
- **Consistency model**: strong vs eventual, SAGA vs 2PC for distributed tx
- **Deployment topology**: monolith vs microservices vs modular monolith
- **Caching strategy**: no cache vs CDN vs application cache vs write-through
- **Real-time mechanism**: polling vs long-polling vs SSE vs WebSocket
- **Search**: database full-text vs dedicated search engine
- **Authentication**: session vs JWT vs OAuth / OIDC

Every significant decision must produce a table — even when one option is
clearly dominant, showing the reasoning in table form makes the decision
auditable. The only exception: if a decision is truly trivial (only one
viable option exists given the constraints), state the choice and the
single-line rationale without a table.

## Table Format

Each trade-off produces one table. Use this structure:

```markdown
### Decision: [decision name]

| Criterion        | Option A     | Option B     |
|------------------|--------------|--------------|
| [criterion 1]    | [value]      | [value]      |
| [criterion 2]    | [value]      | [value]      |
| ...              | ...          | ...          |
| Recommendation   | -            | X            |

**Rationale:** [one or two sentences explaining why the recommendation fits
the requirements established earlier]
```

### Criterion Selection

Pick 4-7 criteria that matter for the specific decision. Generic criteria
(cost, complexity, maturity) apply to most decisions. Domain-specific
criteria (consistency guarantees, schema flexibility, query patterns) apply
when the NFRs make them relevant.

Common criteria by category:

**Storage decisions**
Consistency, schema flexibility, query complexity, write throughput,
read throughput, horizontal scaling, operational overhead

**Communication decisions**
Latency, decoupling, ordering guarantees, back-pressure handling,
operational complexity, debugging ease

**Deployment decisions**
Team cognitive load, independent scalability, deployment independence,
fault isolation, shared code overhead, operational surface

## Recommendation Rules

- Every table must have exactly one recommendation
- Recommendation must tie back to a specific NFR or constraint
- If requirements do not determine the choice, state that explicitly and ask
  the user to decide before proceeding
- If the user stated a technology preference: note it, run the table anyway,
  confirm or challenge the preference based on the output

## Quality Gate

Before loading `architecture.md`, verify:

- [ ] Every significant decision has a markdown comparison table with a
  `Recommendation` row — no prose-only decisions
- [ ] Every table has exactly one `X` in the Recommendation row
- [ ] Every recommendation references a specific NFR or constraint by name
- [ ] Unresolved decisions are flagged and the user has confirmed how to proceed
- [ ] No architecture-blocking decisions remain open

If any significant decision is documented only in prose, convert it to a
table before proceeding. The table format is not optional — it is the mechanism
that makes decisions traceable to requirements and reviewable by the user.

## Next Steps

Present resolved decisions to the user. When all decisions are confirmed,
load [architecture.md](architecture.md).
