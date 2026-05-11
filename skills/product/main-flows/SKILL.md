---
name: main-flows
description: >-
  Reads PRD and domain artifacts to produce detailed sequence and
  decision flows for each journey plus background system flows
  triggered by non-user events. Cites entity lifecycle
  transitions from domain.md and verifies BR/EC coverage against
  the PRD. Writes flows.md so downstream architecture and
  implementation work can trace decisions back to flow steps.
  Use when PRD and domain artifacts exist and journeys must be
  traced through the system before architecture, or when
  implementation surfaces a flow gap. Triggers: "build main
  flows", "map flows", "journey flows", "flow coverage", "show
  how entities dance", "system flows", "main flows from PRD",
  "trace journeys", "flow gap found", "update flows". Not for UI
  design, system architecture, or implementation specs.
---

# Main Flows

Trace each PRD journey and background process through the system as a
sequence of actor steps, entity transitions, and side effects.

## Workflow

```
discovery --> inventory --> drafting --> coverage --> output
                  ^_______________________|  (orphan rule adds a flow)
```

Discovery loads the PRD and domain model. Inventory enumerates candidate
flows and confirms the list with the user. Drafting fills the per-flow
template. Coverage verifies BR/EC traceability. Output writes the
artifact and hands off downstream.

## Triggers

- **Build flows from PRD + domain** ("build main flows", "map flows",
  "trace journeys", "show how entities dance") →
  [discovery.md](references/discovery.md)
- **Confirm candidate flow list** (loaded after discovery completes) →
  [discovery.md](references/discovery.md) (inventory section)
- **Draft a flow** ("draft flow", "fill flow template") →
  [drafting.md](references/drafting.md)
- **Verify coverage** ("flow coverage", "check BR coverage", "orphan
  rule") → [coverage.md](references/coverage.md)
- **Produce artifact** ("output", "produce flows.md") →
  [coverage.md](references/coverage.md) (output section)
- **Update mode** ("update flows", "flow gap found", "spec found
  missing flow") → [discovery.md](references/discovery.md) (update
  mode)

The full workflow always starts with discovery regardless of trigger.
Load each subsequent reference only when its phase begins.

## Guidelines

- Read the PRD and `domain.md` before any other action — flows derive
  from both, and a missing entity or invariant breaks the trace
- Trace every flow back to a PRD journey (foreground) or a functional
  requirement that implies a system trigger (background)
- Cite `Entity.lifecycle.state` from `domain.md` for every state
  transition — invented states signal a domain gap, not a flow gap
- Mark every side effect with its source rule (`Source: BR-N` or
  `Source: FR-N`); side effects without a source are guesses
- Group flows by bounded context from `domain.md` — cross-context
  flows must name every context they touch
- Defer UI detail to the design layer — describe the actor action
  once, never expand into widget labels or screen layout

## Anti-Pattern: Implementation Leakage

Flows live at the domain level. API endpoints, SQL statements, ORM
calls, framework function names, and file paths belong to architecture
and implementation specs, not here. The test: would a non-engineer
stakeholder still recognize the flow? If the sequence reads like a
stack trace, it has leaked. Strip the implementation language and keep
the actor → action → effect shape.

## Anti-Pattern: Surface Step Inflation

A flow is the system's behavior, not the surface's behavior. The
surface may be a screen, a CLI prompt, a voice command, an inbound
webhook, or a sensor reading — the flow treats the actor's intent as
one step. Expanding it into per-control interactions (button taps,
prompt re-renders, validation toasts, gesture recognizers, parser
sub-states) turns the flow into a surface script and buries the
system steps that follow. Surface shape is a separate concern
handled by the design and presentation layers.

## Anti-Pattern: Re-Stating the PRD Journey

A flow that paraphrases the PRD journey adds nothing. The flow
extends the journey with the system's response: which entity changes
state, which event is emitted, which notification is logged, which
downstream branch fires from a business rule. If the flow body could
sit in the PRD unchanged, the system layer is missing — go back and
add it.
