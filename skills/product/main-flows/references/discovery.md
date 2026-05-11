# Discovery and Inventory

Read the PRD and domain artifacts, enumerate candidate flows
(foreground + background), confirm the list with the user, and group
by bounded context.

## When to Use

Always the entry point. Load before any other reference, in both
new-flows and update modes.

## Workflow

```
locate inputs --> extract candidates --> confirm list --> group by context
```

### Step 1: Locate Inputs

Read `.artifacts/docs/prd.md` and `.artifacts/docs/domain.md`. If
either is missing, stop and ask the user to provide a path or run the
upstream skill first. Flows derive from both — the PRD provides
journeys and rules, the domain model provides entities, lifecycle
states, and bounded contexts.

In **update mode** (triggered by an implementation gap or downstream
discovery): also read `.artifacts/docs/flows.md` (current artifact)
and `.agents/knowledge.md` `## Flow Gaps` section before narrowing
scope.

### Step 2: Extract Candidate Flows

Scan in two passes.

**Foreground pass — one flow per PRD journey:**

1. Open PRD section 5 (User Journeys)
2. For each journey J-N, record one foreground candidate:
   - ID matches the journey ID (`J-1`, `J-2`, ...)
   - Trigger is the actor action that opens the journey
   - Primary actor is the journey's owner
   - Source: the journey number

**Background pass — system-driven flows from FRs:**

Scan PRD section 4 (Scope / FRs) and section 6 (Business Rules) for
capabilities that imply a non-user trigger. Background trigger
shapes (illustrative, not exhaustive — adapt to the project's
domain):

| Shape | Example FR signals |
|-------|--------------------|
| Time-based | "every N minutes/hours/days", "on schedule", "periodic", "tick", "frame" |
| External event | "third-party callback", "inbound webhook", "external system notifies", "push notification", "device event" |
| Internal event | "when {entity} changes state", "on configuration change", "after {prior flow} completes" |
| Privileged action | "admin override", "manual reprocess", "force resync", "operator intervention" |
| Sensor / batch input | "ingest batch", "sensor reading", "uploaded file", "stream message" |

For each background candidate, record:

- ID prefixed `F-` followed by a short name that matches the trigger
  in the project's vocabulary (examples from different domains:
  `F-Tick` for a game loop, `F-PushHandler` for a mobile push
  notification, `F-FirmwareCheck` for a device update, `F-IngestBatch`
  for a data pipeline, `F-AdminOverride` for an operator action,
  `F-DailyClose` for an accounting cutoff, `F-RetrainModel` for an ML
  scheduled job)
- Trigger (one sentence describing what fires the flow)
- Primary actor (use the actors named in `domain.md` plus the
  triggering source; common sources include `System`, `Scheduler`,
  `External system`, `Device`, `Operator`)
- Source: the FR or BR that implies the trigger

### Step 3: Confirm Candidate List

Present the combined list (foreground + background) to the user:

- Confirm each candidate is a real flow (not a duplicate of another)
- Add missing flows the user knows exist
- Drop irrelevant flows (e.g., a journey that is pure read with no
  state change may not need a flow — confirm before dropping)
- Mark flows that span multiple bounded contexts

Do not proceed to drafting until the user confirms the list.

### Step 4: Group by Bounded Context

Read `domain.md` section "Bounded Contexts". For each confirmed flow:

- Assign a primary bounded context (the context that owns the
  triggering entity)
- List secondary bounded contexts the flow touches (cross-context
  flows must name all of them)

Group the confirmed list by primary context. This grouping carries
through to the final artifact's section ordering.

### Step 5 (Update Mode Only)

Narrow to the reported gap before loading drafting:

- Identify which flow is missing, incorrect, or contradicted by the
  current artifact
- Confirm the scope of the update with the user (single flow, set of
  flows, or full re-coverage pass)
- After drafting and coverage complete, append a row to `## Processed
  Gaps` in `knowledge.md` with the gap ID, resolution summary, and
  date

## Quality Gate

Before loading [drafting.md](drafting.md), verify:

- [ ] PRD and `domain.md` have been read
- [ ] Every PRD journey has a foreground candidate
- [ ] Every FR with a non-user trigger has a background candidate (or
      an explicit decision to skip with reason)
- [ ] Each candidate has a source (PRD reference or FR/BR ID)
- [ ] User has confirmed the candidate list
- [ ] Each confirmed flow has a primary bounded context assigned
- [ ] Update mode scope is confirmed (if applicable)

## Next Steps

Load [drafting.md](drafting.md) to fill the per-flow template.
