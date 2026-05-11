# Drafting

Fill the per-use-case template for each confirmed candidate. One
template, applied identically to user-initiated and system-initiated
use cases.

## When to Use

Load after [discovery.md](discovery.md) quality gate passes and before
[coverage.md](coverage.md). Apply to every confirmed candidate, in
bounded-context order.

## Workflow

```
goal + trigger + actors --> main success scenario --> extensions --> side effects --> success guarantees
```

For each use case, walk the template top to bottom. Resolve every
section before moving to the next use case.

### Step 1: Goal, Trigger, and Actors

State the goal in one sentence from the primary actor's perspective:
what outcome the actor wants from the system. State the trigger in
one sentence: who or what initiates the use case. List actors in the
order they appear in the scenario. Use the actor names defined in
`domain.md` first; for system-side actors not in the domain (the
system itself, the scheduler, an external service, a device, an
operator), pick one term per role and reuse it across use cases so
the artifact reads consistently.

### Step 2: Main Success Scenario

Number every step of the happy path. Each step has the shape:

```
N. {Actor} {action} → {effect on entity, citing Entity.lifecycle.state}
```

The arrow separates the actor's action from the system effect. If a
step has no system effect (pure user input with no state change yet),
state that explicitly with `→ no state change` so the reader knows it
was not omitted.

For **read-only use cases** (every step has no effect — typical for
view or list use cases), the per-step `→ no state change` reads
heavy. Use the short form instead: drop the arrow on each step and
add a single line under the scenario:

```
*All steps are read-only — no state changes, no side effects.*
```

Use the short form only when the entire use case is read-only. Mixed
use cases (some steps mutate, some read) keep the per-step arrows.

Cite a `domain.md` lifecycle state for every state transition. If
the needed state does not exist in `domain.md`, stop and treat it as
a domain gap — open a `## Domain Gaps` entry in `knowledge.md` and
ask the user before inventing a state.

### Step 3: Extensions

An extension is an alternative path triggered by an EC, a BR guard,
or a failure mode. Anchor each extension to the parent step using
the letter convention:

```
{step}a — {condition / EC-N} → {alternate path, same arrow shape}
{step}b — {condition / EC-N} → {alternate path}
```

`{step}a` reads as "the first extension off step {step}", `{step}b`
as the second, and so on. For nested extensions (an extension that
itself branches), append a digit: `{step}a1`, `{step}a2`. Concrete
example:

```
3. System checks {guard condition} (BR-N guard) → no state change
4. System updates `Entity.attribute` →
   `Entity.attribute` updated

Extensions:
- 3a — {guard fails} (EC-N) → System returns `{ErrorKind}` error,
  no state change, no entity write, no event emitted
```

Every EC referenced by a use case must appear as an extension (or be
explicitly noted in coverage as not exercised by this use case).

### Step 4: Side Effects

List domain-level side effects emitted by the use case. Each side
effect names its source rule. The exact verb depends on what the
project's domain calls the side effect — match `domain.md`
vocabulary. Common shapes (use the ones that fit, add others as
needed):

- `Emits {EventKind} (Source: BR-N / FR-N)` — for event-driven
  domains
- `Writes {RecordKind} (Source: FR-N)` — for log/notification/audit
  records
- `Schedules {JobKind} (Source: FR-N)` — for deferred work
- `Sends {MessageKind} (Source: FR-N)` — for outbound messaging
- `Calls {EffectKind} (Source: FR-N)` — for cross-context effects

If the domain has none of these and side effects are direct entity
mutations, the entity transitions in the Main Success Scenario
section already capture them — the Side Effects section may be
empty.

Whatever shape is used, the kind name must match a value defined in
`domain.md`. An invented kind is a domain gap, not a use case
choice.

### Step 5: Success Guarantees

State the entity states present after the use case completes
successfully, plus any new entities created. Success guarantees are
the input preconditions for downstream use cases that read these
entities.

### Step 6: References

List the PRD and domain references the use case exercises:

- PRD: `J-N`, `FR-N`, `BR-N`, `EC-N`
- Domain: `Entity.lifecycle.state`, `Entity.invariant`

Coverage uses these references to build the traceability matrix.

### Step 7: Mermaid Diagram (Optional)

A `sequenceDiagram` block is recommended for user-initiated journeys
where the visual aids the reader. Skip for system-initiated use
cases where the diagram adds noise without insight (single-actor
scheduled loops, simple inbound-event handlers, deterministic batch
passes).

When included, the diagram mirrors the numbered scenario — do not let
the diagram and the prose diverge.

## Per-Use-Case Template

ALWAYS use this exact template structure for every use case:

```markdown
### {ID} — {Title}

**Primary Actor:** {actor name from domain.md or system-side role}
**Goal:** {what the actor wants from the system, one sentence}
**Trigger:** {what starts the use case}
**Actors:** {ordered list, same vocabulary across use cases}
**Scope:** {primary bounded context} (touches: {secondary contexts, if any})

#### Preconditions

- {entity state required before this use case can start}
- {prior use case that produced these conditions, if relevant}

#### Main Success Scenario

1. {Actor} {action} → {effect on entity, citing Entity.lifecycle.state}
2. {Actor} {action} → {effect}
3. ...

#### Extensions

- {step}a — {condition / EC-N} → {alternate path}
- {step}b — {condition / EC-N} → {alternate path}

#### Side Effects

- Emits `{EventKind}` (Source: BR-N / FR-N)
- Writes `{NotificationKind}` (Source: FR-N)

#### Success Guarantees

- {entity states after the use case completes}
- {new entities created}

#### References

- PRD: J-N, FR-N, BR-N, EC-N
- Domain: {Entity.lifecycle.state}, {Entity.invariant}

#### Diagram (optional)

\`\`\`mermaid
sequenceDiagram
    actor {Actor}
    participant System
    {Actor}->>System: action
    System-->>{Actor}: response
\`\`\`
```

## Quality Gate

Before loading [coverage.md](coverage.md), verify each drafted use
case:

- [ ] Every section in the template is filled (or marked
      explicitly empty with reason)
- [ ] Goal sentence states the actor's desired outcome
- [ ] Every state transition cites a state defined in `domain.md`
- [ ] Every side effect names its source rule
- [ ] Every EC referenced by the use case appears as an extension
- [ ] No implementation language (no API endpoints, no SQL, no
      framework function names, no file paths)
- [ ] No UI step inflation (one actor action per step, not one
      widget interaction per step)

## Next Steps

Load [coverage.md](coverage.md) to verify BR/EC traceability and
produce the final artifact.
