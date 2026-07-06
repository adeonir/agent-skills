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

## `AC-N` identity and tombstones

`AC-N` is a monotonic identifier per feature — never renumbered, never reused. Removing an AC leaves a tombstone instead of renumbering, so existing task and test references stay stable:

```text
- AC-3 removed: folded into AC-1
```

## Backward provenance — `Satisfies`

Only when the Author starts from a structured document with its own IDs (a PRD's `FR/BR/EC/NFR`), each AC that operationalizes a requirement carries a `**Satisfies**` sub-line naming that ID — backward provenance the specify completeness check consumes to confirm every PRD requirement reached an AC. The audit stays AC-keyed; it never anchors on the requirement ID. Prompt and story seeds do not write it (a story inherits the link 1:1 via the `sources:` pointer). Keep the link on the `**Satisfies**` line, never in prose.

## Case convention — two classes

- **EARS operators** (requirement prose) → the reserved words above, as written.
- **Tags / metadata / status / markers** (labels) → lowercase / kebab: `[blocking]`, `[deferrable]`, `[assumption]`, `[needs-clarification]`, `(confirm @ design)`, `(verify @ design)`.
- `AC-N` is an identifier — its own format, neither class.

## Non-functional criteria

Any performance, latency, throughput, capacity, or availability claim carries a number and the condition it holds under (`p95 ≤ 200ms under 50 RPS`), or it is not an acceptance criterion — demote it to an Open Question. Vague adjectives ("fast", "scalable", "responsive") are not testable and never ship as ACs.

## Ambiguity closure

An inline draft marker `[needs-clarification: question]` may appear while drafting; none may remain at the end. Anti-fabrication: an unresolved open question's default never appears as a statement of fact in Overview or Goals. Closure is a self-check, scope-tiered — Large/Complex resolve fully; Medium resolves the obvious and logs the rest; trivial skips.
