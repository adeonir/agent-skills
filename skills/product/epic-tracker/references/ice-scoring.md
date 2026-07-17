# ICE Scoring

Evaluate and prioritize derived candidates with ICE — Impact, Confidence, Ease — to break ties within a dependency-bounded order.

## When to Use

Composed by `decompose` after derivation, over candidates that already exist. Level 1 (epics): always. Level 2 (stories/tasks): **optional** — apply it only when there is a value spread worth discriminating; skip it when dependency already dictates the order.

## The Three Axes

Score each candidate on each axis; keep the scale consistent across the set (a simple 1–5 or low/medium/high is enough — the ranking matters, not the absolute number).

- **Impact** — how much this candidate moves the outcome the PRD cares about. A candidate that unlocks a core journey scores higher than a peripheral one.
- **Confidence** — how sure the boundary and the value are. A well-understood capability scores higher than a speculative one; low confidence is a signal to keep the candidate small or to sequence it early to learn.
- **Ease** — how self-contained and deliverable the candidate is on its own. High ease = few dependencies, a clear done-state.

Combine the three into one comparable score per candidate (the product or the sum — hold one method across the set).

## Ordering: dependency bounds, ICE decides the slack

ICE is a **soft** signal; dependency is a **hard** constraint. Never let ICE override a dependency:

- **Dependency is primary and bounds the sequence** — a candidate never precedes one it depends on, however high its ICE.
- **ICE decides within that bound** — when two candidates are both unblocked, the higher ICE score comes first.

A foundation epic with low Impact and low Ease still comes first when others depend on it. The hard constraint defines the field; the soft signal plays inside it.

## Guidelines

- Score to rank, not to grade — the output is an order, not a report.
- Be honest about Confidence; it is the axis that most often exposes an epic that should be split or sequenced early to de-risk.
- At level 2, reach for ICE only when stories in the epic genuinely spread in value; otherwise dependency ordering is enough.
