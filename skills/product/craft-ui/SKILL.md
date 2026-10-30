---
name: craft-ui
allowed-tools: Bash(bun:*) Bash(python3:*) Bash(git:*) Read Write Edit Grep Glob WebFetch
description: "Creates lo-fi wireframes for UI structure, hi-fi mockups for visual directions, and in-app experiments that compare variants inside an existing codebase. Use for landing pages, dashboards, product UI, and app screens, or to try a new UI idea in the running app. Not for visual identity, copywriting, single-component design, built-UI audits, or code review."
---

# Craft UI

Three phases over the brief and the other supplied inputs. The wireframe phase is optional: when it runs, it settles the arrangement and passes it to mockups through `structure.yaml`; without it, each mockup direction chooses its own arrangement. Experiments test an idea inside the running app of a project that already has UI, comparing variants there.

## Triggers

- **Wireframes** ("plan the layout", "map the screen flow", "arrange the screens", "compare arrangements", "settle the structure first") → [wireframes.md](instructions/wireframes.md)
- **Mockups** ("generate directions", "compare looks", "preview a direction", "try an editorial direction", "adjust the chosen look") → [mockups.md](instructions/mockups.md)
- **Experiments** ("try this in the app", "compare variants in the running app", "test a new layout on the existing page", "try an idea in the codebase") → [experiments.md](instructions/experiments.md)

A request to try an idea against the UI a codebase already has routes to experiments; with no codebase, or no UI yet, it routes to wireframes and mockups.

## Workflow

```text
[wireframes] → structure.yaml → mockups → docs/design/mockup.html
      └──────── skipped ────────┘  (each direction picks its own arrangement)

experiments → variants in the app on a throwaway branch → VARIANTS.md
```

Final copy comes after the mockup and is an input to no phase.

## References

- [direction-memory.md](references/direction-memory.md) — loaded by the mockups and experiments instructions
