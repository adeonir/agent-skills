# Discovery and Inventory

Read the PRD and domain artifacts, enumerate candidate use cases
(user-initiated + system-initiated), confirm the list with the user,
and group by bounded context.

## When to Use

Always the entry point. Load before any other reference, in both
new-use-case and update modes.

## Workflow

```
locate inputs --> extract candidates --> confirm list --> group by context
```

### Step 1: Locate Inputs

Read `.artifacts/docs/prd.md` and `.artifacts/docs/domain.md`. If
either is missing, stop and ask the user to provide a path or run the
upstream skill first. Use cases derive from both — the PRD provides
journeys and rules, the domain model provides entities, lifecycle
states, and bounded contexts.

In **update mode** (triggered by an implementation gap or downstream
discovery): also read `.artifacts/docs/use-cases.md` (current
artifact) and `.agents/knowledge.md` `## Flow Gaps` section before
narrowing scope.

### Step 2: Extract Candidate Use Cases

Scan in two passes.

**User-initiated pass — one use case per PRD journey:**

1. Open PRD section 5 (User Journeys)
2. For each journey J-N, record one user-initiated candidate:
   - ID matches the journey ID (`J-1`, `J-2`, ...)
   - Trigger is the actor action that opens the journey
   - Primary actor is the journey's owner
   - Source: the journey number

**System-initiated pass — use cases driven by FRs:**

Scan PRD section 4 (Scope / FRs) and section 6 (Business Rules) for
capabilities that imply a non-user trigger. System-initiated trigger
shapes (illustrative, not exhaustive — adapt to the project's
domain):

| Shape | Example FR signals |
|-------|--------------------|
| Time-based | "every N minutes/hours/days", "on schedule", "periodic", "tick", "frame" |
| External event | "third-party callback", "inbound webhook", "external system notifies", "push notification", "device event" |
| Internal event | "when {entity} changes state", "on configuration change", "after {prior use case} completes" |
| Privileged action | "admin override", "manual reprocess", "force resync", "operator intervention" |
| Sensor / batch input | "ingest batch", "sensor reading", "uploaded file", "stream message" |

For each system-initiated candidate, record:

- ID prefixed `F-` followed by a short name that matches the trigger
  in the project's vocabulary (examples from different domains:
  `F-Tick` for a game loop, `F-PushHandler` for a mobile push
  notification, `F-FirmwareCheck` for a device update, `F-IngestBatch`
  for a data pipeline, `F-AdminOverride` for an operator action,
  `F-DailyClose` for an accounting cutoff, `F-RetrainModel` for an ML
  scheduled job)
- Trigger (one sentence describing what fires the use case)
- Primary actor (use the actors named in `domain.md` plus the
  triggering source; common sources include `System`, `Scheduler`,
  `External system`, `Device`, `Operator`)
- Source: the FR or BR that implies the trigger

### Step 3: Confirm Candidate List

Present the combined list (user-initiated + system-initiated) to the
user:

- Confirm each candidate is a real use case (not a duplicate of
  another)
- Add missing use cases the user knows exist
- Drop irrelevant use cases (e.g., a journey that is pure read with
  no state change may not need a use case — confirm before dropping)
- Mark use cases that span multiple bounded contexts

Do not proceed to drafting until the user confirms the list.

### Step 4: Group by Bounded Context

Read `domain.md` section "Bounded Contexts". For each confirmed use
case:

- Assign a primary bounded context (the context that owns the
  triggering entity)
- List secondary bounded contexts the use case touches (cross-context
  use cases must name all of them)

Group the confirmed list by primary context. This grouping carries
through to the final artifact's section ordering.

### Step 5 (Update Mode Only)

Narrow to the reported gap before loading drafting:

- Identify which use case is missing, incorrect, or contradicted by
  the current artifact
- Confirm the scope of the update with the user (single use case,
  set of use cases, or full re-coverage pass)
- After drafting and coverage complete, append a row to `## Processed
  Gaps` in `knowledge.md` with the gap ID, resolution summary, and
  date

## Quality Gate

Before loading [drafting.md](drafting.md), verify:

- [ ] PRD and `domain.md` have been read
- [ ] Every PRD journey has a user-initiated candidate
- [ ] Every FR with a non-user trigger has a system-initiated
      candidate (or an explicit decision to skip with reason)
- [ ] Each candidate has a source (PRD reference or FR/BR ID)
- [ ] User has confirmed the candidate list
- [ ] Each confirmed use case has a primary bounded context assigned
- [ ] Update mode scope is confirmed (if applicable)

## Next Steps

Load [drafting.md](drafting.md) to fill the per-use-case template.
