# Blueprint

Plans `blueprint.md` — the design-blind layout payload a design consumes.

## What It Does

```mermaid
flowchart TD
    Conv[Conversation / Brief / Description] -->|create| B[blueprint.md]
    Wire[Wireframe sketch / mockup / screenshot] -->|validate| F[Coherence findings]
    F -.->|apply| B
    B --> D[Design work consumes blueprint.md]
```

| Step | Trigger | Output |
| ---- | ------- | ------ |
| **Create** | Author a fresh layout plan from conversation — surfaces, blocks, shapes, flow | `docs/design/blueprint.md` |
| **Validate** | Check a wireframe or existing plan for IA, flow, and intent coherence | Findings (patch via create, confirm-before-write) |

Arrangement is orthogonal to visual identity: the same `blueprint.md` holds
independent of visual styling, so this skill plans structure only — never
colors, fonts, tokens, copy strings, or requirement IDs. It emits the plan; a
downstream renderer draws the wireframe.

## Usage

```text
# Create a fresh layout plan
plan the layout for this landing page
map the information architecture for this app
arrange the screens and flow from this brief
draft a wireframe plan from this brief

# Validate a wireframe or existing plan
check this wireframe for coherence
does this screen flow hold up?
validate blueprint.md
review the page composition before we style it
```

## Output

`docs/design/blueprint.md` — a YAML frontmatter region tree (surfaces → blocks
with shape hints) plus a markdown body (screen map + per-surface rationale),
derived from the conversation or a brief.

## Requirements

- `WebFetch` for pulling a reference URL's structure (optional — sketches,
  screenshots, and described layouts work without it).
