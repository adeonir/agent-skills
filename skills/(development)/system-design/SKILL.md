---
name: system-design
description: >-
  Guided system design from problem to architecture. Starts from the problem,
  not the document. Runs interactive discovery, elicits non-functional
  requirements, produces visual trade-off tables, and maps components. Agnostic
  to domain, stack, and experience level. Use when designing a new system,
  planning architecture for a feature, choosing between technical approaches,
  or when facing scale, consistency, or reliability decisions.
when_to_use: >-
  Triggers on "design a system", "architecture for", "how should I structure",
  "system for X", "what architecture", "scale this", "handle X users",
  "microservices vs monolith", "how to store", "real-time notifications",
  "event-driven", "distributed system", "system design interview",
  "architect this", "technical approach for scale",
  "technical approach for architecture", "infrastructure for". Not for
  feature design.md (use spec-driven), TDD document (use docs-writer),
  or visual UI design (use design-builder).
effort: xhigh
---

# System Design

**Recommended effort:** xhigh for discovery and trade-off phases; high for
architecture mapping with clear requirements.

Interactive system design from problem framing to architecture blueprint.
Start from the problem — requirements, trade-offs, and components follow.
Use ultrathink during trade-off analysis and architecture mapping.

## Workflow

```
discovery --> requirements --> trade-offs --> architecture --> output
  ^______________|  (loop until requirements are clear)
```

Discovery and requirements iterate: ask, deepen, confirm. Trade-offs and
architecture are sequential once requirements are stable.

## Context Loading Strategy

Load `discovery.md` at the start of every session — even when the user
provides requirements upfront. Load each subsequent reference only when
its phase begins. Never load multiple references simultaneously.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Design a system, architecture for, how to structure | [discovery.md](references/discovery.md) |
| Requirements, constraints, scale, SLA, non-functional | [requirements.md](references/requirements.md) |
| Trade-offs, compare options, SQL vs NoSQL, sync vs async | [trade-offs.md](references/trade-offs.md) |
| Components, data flow, diagram, blueprint | [architecture.md](references/architecture.md) |
| Output, brief, document, hand off to docs-writer | [output.md](references/output.md) |

Notes:

- `discovery.md` is always the entry point. It loads `requirements.md` at the
  end of problem framing.
- `trade-offs.md` is loaded when key decisions surface during requirements.
- `architecture.md` is loaded after trade-offs are resolved.
- `output.md` is loaded when the user is ready to produce artifacts.

## Cross-References

```
discovery.md -----> requirements.md  (framing complete → elicit NFRs)
requirements.md --> trade-offs.md    (decisions surface → compare options)
trade-offs.md ---> architecture.md  (decisions resolved → map components)
architecture.md --> output.md       (blueprint ready → produce brief)
system-design ---> docs-writer      (brief feeds TDD or ADR)
system-design ---> spec-driven      (architectural decisions feed feature planning)
spec-driven -----> system-design    (feature needing architectural decision)
```

## Guidelines

**DO:**
- Start every session with discovery, even when requirements are provided
- Ask one question at a time during discovery and requirements phases
- Present trade-offs as tables with an explicit recommendation
- State the reasoning behind every architectural recommendation
- Mark unknowns as open questions rather than filling gaps with assumptions
- Acknowledge the user's experience level and adjust vocabulary accordingly

**DON'T:**
- Jump to architecture before requirements are stable (contrasts: iterate
  discovery until requirements are clear)
- Present trade-off tables without a recommendation (contrasts: always
  recommend with rationale)
- Assume scale, team size, or stack (contrasts: ask during requirements)
- Produce component diagrams before key decisions are resolved (contrasts:
  resolve trade-offs before architecture)
- Treat user technology preferences as fixed constraints without exploring
  trade-offs (contrasts: note preference, still surface alternatives)

## Output

Brief saved to `.artifacts/docs/system-brief.md`. Create the directory
if it does not exist.

Handoff options:
- `docs-writer` for a formal TDD (component-level) or ADR (single decision)
- `spec-driven` when the architecture feeds a feature implementation plan

## Error Handling

- No problem description: ask "what are you trying to build or solve?"
- User jumps to architecture without requirements: redirect to discovery
- Conflicting requirements: surface the conflict, ask user to resolve
- User states a technology preference: note it, still explore trade-offs
- Domain unfamiliar: ask clarifying questions, do not assume domain knowledge

## Compact Instructions

Preserve:
- Current phase, open questions from discovery, confirmed requirements
- Decisions resolved in trade-offs (with chosen option)
- Component list from architecture phase

Drop:
- Full question-and-answer transcript from discovery
- Intermediate trade-off reasoning scratch work
- Raw tool outputs
