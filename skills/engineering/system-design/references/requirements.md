# Requirements

Elicit functional and non-functional requirements after problem framing.
Non-functional requirements drive most architectural decisions — do not
skip or estimate them.

## When to Use

Load after `discovery.md` quality gate passes. Runs before trade-off analysis.

## Functional Requirements

Identify the core actions the system must support:

- What operations does the system perform? (create, read, update, delete,
  stream, notify, process, etc.)
- What data does it produce or consume?
- What are the primary flows? (happy path first, then failure paths)

Capture as a numbered list. Requirements must be concrete and verifiable.

| Weak | Strong |
|------|--------|
| "Fast search" | "Search returns results within 200ms at p99" |
| "Handle many users" | "Support 10,000 concurrent users" |
| "Store files" | "Store files up to 100MB per user, retain 30 days" |

## Non-Functional Requirements

These define quality attributes that shape architecture. Ask about each
category explicitly — users rarely volunteer NFRs unprompted.

### Scale

- How many users or requests at peak?
- What is the expected growth over 12 months?
- Are there burst patterns? (time of day, seasonal spikes)

### Latency

- What response time is acceptable for the main operations?
- Are there real-time requirements? (< 100ms, streaming, websockets)
- Are background or async operations acceptable for some flows?

### Availability and Reliability

- What is the acceptable downtime? (99.9%, 99.99%?)
- What happens when the system is unavailable?
- Is there a recovery time objective (RTO)?

### Consistency

- Does the system require strong consistency? (bank transactions, inventory)
- Is eventual consistency acceptable? (social feeds, analytics, notifications)
- Are there partial failure scenarios that need explicit handling?

### Data

- What is the read/write ratio?
- How long must data be retained?
- Are there compliance or privacy requirements? (GDPR, HIPAA, etc.)

### Operations

- Who operates the system? (internal team, third-party, self-hosted)
- Are there on-call expectations?
- What observability is required?

## Constraint Summary

After NFR elicitation, summarize constraints that eliminate architectural options:

- Hard constraints: must-haves that cannot be traded (compliance, existing
  infrastructure, team skill set)
- Soft constraints: preferences that can be revisited under trade-off analysis

## Quality Gate

Before loading `trade-offs.md`, verify:

- [ ] Functional requirements listed as concrete, verifiable statements
- [ ] Scale numbers are defined (even rough estimates are acceptable)
- [ ] Latency expectations are explicit
- [ ] Consistency model is stated (strong vs eventual)
- [ ] Hard constraints are separated from soft preferences

## Next Steps

When the quality gate passes, present the requirements summary to the user
for confirmation. Surface the key decisions that need trade-off analysis,
then load [trade-offs.md](trade-offs.md).
