# Drafting

Fill the per-flow template for each confirmed candidate. One template,
applied identically to foreground and background flows.

## When to Use

Load after [discovery.md](discovery.md) quality gate passes and before
[coverage.md](coverage.md). Apply to every confirmed candidate, in
bounded-context order.

## Workflow

```
trigger + actors --> main success scenario --> extensions --> side effects --> success guarantees
```

For each flow, walk the template top to bottom. Resolve every section
before moving to the next flow.

### Step 1: Trigger and Actors

State the trigger in one sentence: who or what initiates the flow.
List actors in the order they appear in the scenario. Use the actor
names defined in `domain.md` first; for system-side actors not in
the domain (the system itself, the scheduler, an external service,
a device, an operator), pick one term per role and reuse it across
flows so the artifact reads consistently.

### Step 2: Main Success Scenario

Number every step of the happy path. Each step has the shape:

```
N. {Actor} {action} → {effect on entity, citing Entity.lifecycle.state}
```

The arrow separates the actor's action from the system effect. If a
step has no system effect (pure user input with no state change yet),
state that explicitly with `→ no state change` so the reader knows it
was not omitted.

For **read-only flows** (every step has no effect — typical for view
or list flows), the per-step `→ no state change` reads heavy. Use the
short form instead: drop the arrow on each step and add a single line
under the scenario:

```
*All steps are read-only — no state changes, no side effects.*
```

Use the short form only when the entire flow is read-only. Mixed
flows (some steps mutate, some read) keep the per-step arrows.

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

Every EC referenced by a flow must appear as an extension (or be
explicitly noted in coverage as not exercised by this flow).

### Step 4: Side Effects

List domain-level side effects emitted by the flow. Each side effect
names its source rule. The exact verb depends on what the project's
domain calls the side effect — match `domain.md` vocabulary. Common
shapes (use the ones that fit, add others as needed):

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
`domain.md`. An invented kind is a domain gap, not a flow choice.

### Step 5: Success Guarantees

State the entity states present after the flow completes
successfully, plus any new entities created. Success guarantees are
the input pre-conditions for downstream flows that read these
entities.

### Step 6: References

List the PRD and domain references the flow exercises:

- PRD: `J-N`, `FR-N`, `BR-N`, `EC-N`
- Domain: `Entity.lifecycle.state`, `Entity.invariant`

Coverage uses these references to build the traceability matrix.

### Step 7: Mermaid Diagram (Optional)

A `sequenceDiagram` block is recommended for foreground journeys
where the visual aids the reader. Skip for background flows where
the diagram adds noise without insight (single-actor scheduled
loops, simple inbound-event handlers, deterministic batch passes).

When included, the diagram mirrors the numbered scenario — do not let
the diagram and the prose diverge.

## Per-Flow Template

ALWAYS use this exact template structure for every flow:

```markdown
### {ID} — {Title}

**Trigger:** {what starts the flow}
**Actors:** {ordered list, same vocabulary across flows}
**Bounded Context:** {primary} (touches: {secondary contexts, if any})

#### Pre-conditions

- {entity state required before this flow can start}
- {prior flow that produced these conditions, if relevant}

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

- {entity states after the flow completes}
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

Before loading [coverage.md](coverage.md), verify each drafted flow:

- [ ] Every section in the template is filled (or marked
      explicitly empty with reason)
- [ ] Every state transition cites a state defined in `domain.md`
- [ ] Every side effect names its source rule
- [ ] Every EC referenced by the flow appears as an extension
- [ ] No implementation language (no API endpoints, no SQL, no
      framework function names, no file paths)
- [ ] No UI step inflation (one actor action per step, not one
      widget interaction per step)

## Next Steps

Load [coverage.md](coverage.md) to verify BR/EC traceability and
produce the final artifact.
