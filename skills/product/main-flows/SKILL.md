---
name: main-flows
description: >-
  Reads PRD and domain artifacts to produce use cases for each
  user journey and each system-initiated process. Cites entity
  lifecycle transitions from domain.md and verifies
  BR/EC coverage against the PRD. Writes use-cases.md so
  downstream architecture and implementation work can trace
  decisions back to use case steps. Use when PRD and domain
  artifacts exist and journeys must be traced through the system
  before architecture, or when implementation surfaces a gap.
  Triggers: "main flows", "build flows", "map flows", "trace
  journeys", "journey flows", "system flows", "create use cases",
  "map use cases", "use case modeling", "update flows". Not for
  UI design, system architecture, or implementation specs.
---

# Main Flows

Trace each PRD journey and system-initiated process as a use case —
actor, goal, preconditions, main success scenario, extensions,
entity transitions, and side effects.

## Workflow

```
discovery --> inventory --> drafting --> coverage --> output
                  ^_______________________|  (orphan rule adds a UC)
```

Discovery loads the PRD and domain model. Inventory enumerates
candidate use cases and confirms the list with the user. Drafting
fills the per-use-case template. Coverage verifies BR/EC
traceability. Output writes the artifact and hands off downstream.

## Triggers

- **Build use cases from PRD + domain** ("main flows", "build flows",
  "map flows", "trace journeys", "journey flows", "system flows",
  "create use cases", "map use cases", "use case modeling") →
  [discovery.md](references/discovery.md)
- **Confirm candidate list** (loaded after discovery completes) →
  [discovery.md](references/discovery.md) (inventory section)
- **Draft a use case** → [drafting.md](references/drafting.md)
- **Verify coverage** → [coverage.md](references/coverage.md)
- **Produce artifact** → [coverage.md](references/coverage.md)
  (output section)
- **Update mode** ("update flows") →
  [discovery.md](references/discovery.md) (update mode)

The full workflow always starts with discovery regardless of trigger.
Load each subsequent reference only when its phase begins.

## Guidelines

- Read the PRD and `domain.md` before any other action — use cases
  derive from both, and a missing entity or invariant breaks the trace
- Trace every use case back to a PRD journey (user-initiated) or a
  functional requirement that implies a system trigger
  (system-initiated)
- Cite `Entity.lifecycle.state` from `domain.md` for every state
  transition — invented states signal a domain gap, not a use case
  gap
- Mark every side effect with its source rule (`Source: BR-N` or
  `Source: FR-N`); side effects without a source are guesses
- Group use cases by bounded context from `domain.md` — cross-context
  use cases must name every context they touch
- Defer UI detail to the design layer — describe the actor action
  once, never expand into widget labels or screen layout

## Anti-Pattern: Implementation Leakage

Use cases live at the domain level. API endpoints, SQL statements,
ORM calls, framework function names, and file paths belong to
architecture and implementation specs, not here. The test: would a
non-engineer stakeholder still recognize the use case? If the
sequence reads like a stack trace, it has leaked. Strip the
implementation language and keep the actor → action → effect shape.

## Anti-Pattern: Surface Step Inflation

A use case captures the system's behavior, not the surface's
behavior. The surface may be a screen, a CLI prompt, a voice command,
an inbound webhook, or a sensor reading — the use case treats the
actor's intent as one step. Expanding it into per-control
interactions (button taps, prompt re-renders, validation toasts,
gesture recognizers, parser sub-states) turns the use case into a
surface script and buries the system steps that follow. Surface
shape is a separate concern handled by the design and presentation
layers.

## Anti-Pattern: Re-Stating the PRD Journey

A use case that paraphrases the PRD journey adds nothing. The use
case extends the journey with the system's response: which entity
changes state, which event is emitted, which notification is logged,
which downstream branch fires from a business rule. If the use case
body could sit in the PRD unchanged, the system layer is missing —
go back and add it.
