---
name: craft-ui
allowed-tools: Bash(bun:*) Bash(python3:*) Read Write Edit Grep Glob WebFetch
description: "Creates lo-fi wireframes for UI structure and hi-fi mockups for visual directions. Use for landing pages, dashboards, product UI, and app screens. Not for visual identity, copywriting, single-component design, built-UI audits, or code review."
---

# Craft UI

Two phases over the brief and the other supplied inputs. The wireframe phase is optional: when it runs, it settles the arrangement and passes it to mockups through `structure.yaml`; without it, each mockup direction chooses its own arrangement.

## Triggers

- **Wireframes** ("plan the layout", "map the screen flow", "arrange the screens", "compare arrangements", "settle the structure first") → [wireframes.md](instructions/wireframes.md)
- **Mockups** ("generate directions", "compare looks", "preview a direction", "try an editorial direction", "adjust the chosen look") → [mockups.md](instructions/mockups.md)

## Workflow

```text
[wireframes] → structure.yaml → mockups → docs/design/mockup.html
      └──────── skipped ────────┘  (each direction picks its own arrangement)
```

Final copy comes after the mockup and is an input to neither phase.
