# Acceptance Criteria

Gherkin acceptance criteria: the form, the two authoring modes, `AC-N.M` identity, the `Serves` and `Satisfies` lines, the case convention, non-functional criteria, ownership of the obligation, calibration against the goal, and ambiguity closure.

## When to Use

During specify, when writing or reshaping the acceptance criteria under each user story, and when confirming every PRD requirement reached an AC. Also read during audit to confirm each AC maps to a discriminating test.

## Form

One criterion is one `#### AC-N.M:` heading, one fenced `gherkin` block, and the lines that link it upward.

````markdown
#### AC-1.1: Sign in with registered credentials
```gherkin
Scenario: User signs in with registered credentials
  Given the user is on the sign-in page
  And the user has a registered account
  When they submit a valid email and password
  Then they are authenticated
```
**Serves** G-1
**Satisfies** FR-1
````

- One criterion is one scenario. Two criteria never carry the same scenario.
- `Scenario` states a single case and carries no `Examples`. `Scenario Outline` carries exactly one `Examples` table: one non-empty, unique-column header and at least one data row; every row matches the header width, every placeholder is a column, and every column binds a placeholder.
- `Given`, `When` and `Then` each open a step group, and `And` or `But` continues the group open at that point.
- A `Then` asserting two independent outcomes is two criteria — split it, however they were joined, in one step with `and` or across an `And` continuation. Two observables of one outcome stay one criterion. The audit maps each criterion to one discriminating test and draws its mutation points from them, so a criterion carrying three observables has no single assertion.
- A conjunctive precondition that names one state the criterion needs whole stays one `Given` group: "the user is signed in and has three items in the cart".
- Measure the `Then` alone. `Given` and `When` narrow when the criterion applies, and narrowing what a criterion covers promises nothing extra.
- Write the outcome as something observable: "the modal appears", never "the flow feels natural".
- An invariant is written as the event that would violate it — `When a record is written / Then the audit log carries the actor` — since every scenario carries a trigger.
- A non-obvious criterion carries its `(because …)` rationale on the heading, after the title.
- A story past five criteria has usually stopped being one outcome: split it, or record the size as deliberate.

## `AC-N.M` identity

`N` is the number of the story the criterion sits under, `M` its position within that story. An id is unique across the whole spec.

While the spec is `draft`, renumber freely: a removed criterion leaves no marker and the ids close up behind it. Once the spec is `ready`, `design.md` references these ids in `Requirements Traceability` and `tasks.md` references them in `Covers` — a renumbering after that is carried into both artifacts in the same pass, and the linter reports every reference left pointing at an id the spec no longer declares.

## Two modes

The agent judges inline — no formal type detection:

- **Reshape** — the input already carries criteria or a definition of done. Convert one to one, changing the notation and never the substance. An input already in Gherkin keeps its scenarios as they stand; a definition of done or a bullet list becomes one scenario each, its condition entering as the `Given`/`When` and its obligation as the `Then`. Split an obligation joining two independent assertions into one criterion each, and carry its requirement id onto both. A reason stated beside an item crosses with it as that criterion's `(because …)`, and a requirement id it names crosses on the `Satisfies` line.
- **Author** — a prompt or PRD with no criteria. Write them from the intent.

An input carrying acceptance criteria is a set of claims, not a settled contract. Reshape's freeze binds the *silent* change: substance never moves on the agent's own authority. It does not oblige the agent to carry a criterion unexamined — one that fails Ownership or Calibration below surfaces as a discuss question and is resolved there, not rewritten in place. Author mode inherits nothing and calibrates the same way.

## `Serves`

Name the one `G-N` of `## Goals` the criterion serves. Carry exactly one id, never a list, and never put the link in prose.

Write no line for a criterion that serves no declared goal and only demonstrates its story's benefit. Where a criterion serves two goals, one of the two is what its `Then` asserts and the other is a consequence: name the one asserted.

## Backward provenance — `Satisfies`

Only when the seed carries per-item requirement IDs — a PRD's own `FR/BR/EC/NFR`, or a ticket whose criteria or done-conditions already name them — each criterion that operationalizes a requirement carries a `**Satisfies**` line naming that ID — backward provenance the specify completeness check consumes to confirm every PRD requirement reached a criterion. The audit stays criterion-keyed; it never anchors on the requirement ID. A seed without per-item IDs writes no `Satisfies` line: the link has no stable target, and one written by position breaks silently when the seed is edited. Its provenance is checked at specify's self-check instead. Keep the link on the `**Satisfies**` line, never in prose.

## Case convention — three classes

- **Gherkin keywords** (scenario prose) → `Scenario`, `Scenario Outline`, `Examples`, `Given`, `When`, `Then`, `And`, `But`, as written.
- **Tags / metadata / status / markers** (labels) → lowercase / kebab: `[needs-clarification]` only for discovery input; owned pendencies use `ASM-N` and `OQ-N` identifiers.
- **Identifiers** (owned, never reused across a story) → uppercase letter(s) + hyphen + number: `S-N` (story), `T-N` (task), `G-N` (goal), `AC-N.M` (criterion), `DV-N` (divergence), `L-NNN` (lesson). `P-N` shares the grammar but is a priority label, not a sequence — `P-1` is the highest rank, carried on the story heading as an attribute.

## Non-functional criteria

Any performance, latency, throughput, capacity, or availability claim carries a number and the condition it holds under (`p95 ≤ 200ms under 50 RPS`), or it is not an acceptance criterion — demote it to an `OQ-N`. Vague adjectives ("fast", "scalable", "responsive") are not testable and never ship as criteria.

## Ownership

The actor of every `Then` is the system under specification. A clause whose obligation something else satisfies — a platform, a runtime, a service, or a library behaving as documented — is not a criterion this feature can meet or fail: no code here implements it, and no test here discriminates it. Drop it, or replace it with the observable this system owns that rests on it.

An inherited clause that fails this surfaces as a discuss question, the same route a miscalibrated one takes; an authored one is caught at the self-check over the drafted spec. Neither is rewritten unilaterally, and the pendency it leaves on the seed is recorded exactly as Calibration's **Loosen** records one.

## Calibration

A criterion may assert less than its story needs — that gap is a coverage hole, and every gate looks for it. It may also assert *more*, and nothing looks for that. Ask of each one: **is there an implementation the story's `so that {benefit}` would accept and this criterion forbids?** Where a criterion serves a Goal directly, the Goal is the anchor.

The failure shape: a `Then` naming a **timing**, a **count**, a **threshold**, or a **mechanism** where the benefit names only an **outcome**. "On the next read", "in a single query", "without a cache" — each forbids an implementation the benefit permits. The usual leak detector misses it because no forbidden noun appears: the leak is in the clause's **strength**, not its vocabulary.

Two clauses are exempt, or the rule flags its own grammar:

- **`Given` and `When`.** They state when the criterion applies, not what it promises. Over-specification lives in the `Then`.
- **A non-functional criterion.** The number is required (see above) — provided it came from the goal, not from the author.

A miscalibrated criterion changes a criterion, so it is load-bearing — resolved with the user, never rewritten unilaterally. An inherited one that arrives before drafting surfaces during discuss; one authored in the body is caught at the self-check over the drafted spec; either way the approval gate presents the outcome before the phase closes. The resolution is one of two:

- **Loosen** to the observable the benefit requires. The spec then states the correct criterion while the seed still asserts the tighter clause — a real pendency, and one only the user can settle. It is recorded as a `Loosened` row in the spec's `## Divergences`, naming the criterion and the clause the seed still holds, and the next specify run removes it once the seed is corrected.
- **Keep** the strictness as a deliberate constraint, carrying its `(because …)` rationale.

## Ambiguity closure

An inline draft marker `[needs-clarification: question]` may appear while drafting; none may remain at the end. Anti-fabrication: an unresolved open question's default never appears as a statement of fact in Overview or Goals. Closure is a self-check, scope-tiered — Large/Complex resolve fully; Medium resolves the obvious and logs the rest.
