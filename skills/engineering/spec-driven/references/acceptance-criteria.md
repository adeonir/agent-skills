# Acceptance Criteria

EARS-lite acceptance criteria: the five clause shapes, the two authoring modes, `AC-N` identity and tombstones, backward provenance, and the case convention.

## When to Use

During specify, when writing or reshaping the acceptance criteria under each user story, and when confirming every PRD requirement reached an AC. Also read during audit to confirm each AC maps to a discriminating test.

## EARS-lite — five shapes

One trigger, one outcome per AC, 1:1 — no compound "and" clauses. The shape names how the requirement is triggered; the sentence states one observable obligation. The shape label is not required in the text.

```text
Ubiquitous:  The system shall {action}.
Event:       When {trigger}, the system shall {action}.
State:       While {state}, the system shall {action}.
Optional:    Where {feature/condition}, the system shall {action}.
Unwanted:    If {unwanted condition}, then the system shall {mitigation}.
```

EARS operators (`shall`, `when`, `while`, `where`, `if…then`) are the requirement prose. Happy paths go in ACs; boundary conditions go in Edge Cases.

## Two modes

The agent judges inline — no formal type detection:

- **Reshape** — the input already has ACs or a DoD. Convert 1:1 to EARS, changing only the notation, never the substance (Given + When → trigger; Then → "the system shall…").
- **Author** — a prompt or PRD with no ACs. Write ACs from the intent.

An input carrying acceptance criteria is a set of claims, not a settled contract. Reshape's freeze binds the *silent* change: substance never moves on the agent's own authority. It does not oblige the agent to carry an AC unexamined — a criterion that fails Calibration below surfaces as a discuss question and is resolved there, not rewritten in place. Author mode inherits nothing and calibrates the same way.

## `AC-N` identity and tombstones

`AC-N` is a monotonic identifier per feature — never renumbered, never reused. Removing an AC leaves a tombstone instead of renumbering, so existing task and test references stay stable:

```text
- AC-3 removed: folded into AC-1
```

## Backward provenance — `Satisfies`

Only when the Author starts from a structured document with its own IDs (a PRD's `FR/BR/EC/NFR`), each AC that operationalizes a requirement carries a `**Satisfies**` sub-line naming that ID — backward provenance the specify completeness check consumes to confirm every PRD requirement reached an AC. The audit stays AC-keyed; it never anchors on the requirement ID. Prompt and story seeds do not write it (a story inherits the link 1:1 via the `sources:` pointer). Keep the link on the `**Satisfies**` line, never in prose.

## Case convention — three classes

- **EARS operators** (requirement prose) → the reserved words above, as written.
- **Tags / metadata / status / markers** (labels) → lowercase / kebab: `[deferrable]`, `[assumption]`, `[needs-clarification]`, `(confirm @ design)`, `(verify @ design)`.
- **Identifiers** (owned, monotonic, never renumbered) → uppercase letter(s) + hyphen + number: `S-N` (story), `T-N` (task), `AC-N` (criterion), `L-NNN` (lesson). `P-N` shares the grammar but is a priority label, not a sequence — `P-1` is the highest rank, carried on the story heading as an attribute.

## Non-functional criteria

Any performance, latency, throughput, capacity, or availability claim carries a number and the condition it holds under (`p95 ≤ 200ms under 50 RPS`), or it is not an acceptance criterion — demote it to an Open Question. Vague adjectives ("fast", "scalable", "responsive") are not testable and never ship as ACs.

## Calibration

An AC may assert less than its story needs — that gap is a coverage hole, and every gate looks for it. It may also assert *more*, and nothing looks for that. Ask of each AC: **is there an implementation the story's `so that {benefit}` would accept and this AC forbids?** Where an AC serves a top-level Goal directly, the Goal is the anchor.

The failure shape: an AC naming a **timing**, a **count**, a **threshold**, or a **mechanism** where the benefit names only an **outcome**. "On the next read", "in a single query", "without a cache" — each forbids an implementation the benefit permits. The usual leak detector misses it because no forbidden noun appears: the leak is in the clause's **strength**, not its vocabulary.

Two clauses are exempt, or the rule flags its own grammar:

- **The EARS trigger.** `When {trigger}` states the precondition, not the promise. Over-specification lives in the outcome after `shall`.
- **A non-functional AC.** The number is required (see above) — provided it came from the goal, not from the author.

A miscalibrated AC changes an AC, so it is load-bearing — resolved with the user, never rewritten unilaterally. An inherited AC that arrives before drafting surfaces during discuss; an AC authored in the body is caught at the self-check over the drafted spec; either way the approval gate presents the outcome before the phase closes. The resolution is one of two:

- **Loosen** to the observable the benefit requires. The spec then states the correct AC while the source input still asserts the tighter clause — a real pendency, carried as a `[deferrable]` line so it survives the session.
- **Keep** the strictness as a deliberate constraint, carrying its `(because …)` rationale.

## Ambiguity closure

An inline draft marker `[needs-clarification: question]` may appear while drafting; none may remain at the end. Anti-fabrication: an unresolved open question's default never appears as a statement of fact in Overview or Goals. Closure is a self-check, scope-tiered — Large/Complex resolve fully; Medium resolves the obvious and logs the rest.
