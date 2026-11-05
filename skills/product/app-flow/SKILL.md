---
name: app-flow
allowed-tools: Read Write Edit
description: "Plan, audit, and refine app flows — the user paths through a website, a mobile app, or another product surface, one flow per task. Use when mapping flows for a new product, drawing checkout, onboarding, or task flows, auditing an existing app's flows for dead ends and drop-off, or restructuring and shortening an existing flow. Not for UI design, wireframes, domain modeling, or implementation."
---

# App Flow

Plans the user paths of a website, a mobile app, or any other product surface as named flows — one flow per task — and keeps them in a committed artifact.

## Triggers

- **Plan new app flows** ("plan the app flow", "map the flows", "design the flow for this checkout", "what flows does this app need") → [plan.md](instructions/plan.md)
- **Audit** ("audit the flows", "check my app's flows", "find the dead ends") → [audit.md](instructions/audit.md)
- **Refine** ("improve this flow", "shorten the signup flow", "restructure the onboarding") → [refine.md](instructions/refine.md)

## References

- [discovery.md](references/discovery.md) — loaded by the plan, audit, and refine instructions
- [flow-model.md](references/flow-model.md) — flow vocabulary and wireflow notation, loaded by the plan, audit, and refine instructions
- [flows-template.md](assets/flows-template.md) — written by the plan instruction, read by the audit and refine instructions

## Workflow

```text
intake (prose | doc | artifact | code) → discovery → the flow
                                             ├ plan:   draft + connect + write docs/product/FLOWS.md
                                             ├ audit:  findings report, no edit
                                             └ refine: restructure the flow, written back
```

Each entry is independent. Every entry states its read of the situation before flow work and lets the user redirect.
