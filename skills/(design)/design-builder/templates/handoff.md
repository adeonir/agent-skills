---
name: {{project-name}}
project_type: {{landing-page/website/web-app/mobile-app}}
created: {{YYYY-MM-DD}}
---

# Handoff: {{Project Name}}

## Summary

{{One sentence describing what this design is for}}

## Intent

**Primary user outcome:** {{the outcome the design should produce}}

**Primary audience:** {{who uses it}}

**Non-negotiables:**

- {{decision 1 with rationale}}
- {{decision 2 with rationale}}

**Out of scope:**

- {{non-goal 1}}
- {{non-goal 2}}

## Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| Tokens | `.artifacts/design/design.json` | Colors, typography, spacing, components |
| Structure | `.artifacts/design/structure.md` | Page or screen layout decisions |
| Content | `.artifacts/design/copy.yaml` | Text content (if extracted) |
| Visual reference | `.artifacts/design/preview/.../final.html` | Approved variant |
| Pencil file | `.artifacts/design/design.pen` | Iteration surface (optional) |

Remove rows that do not apply.

## Key Design Decisions

{{For each critical decision, one short paragraph. Choice first, rationale second.}}

- **{{decision name}}**: {{choice}} — {{rationale}}
- **{{decision name}}**: {{choice}} — {{rationale}}

## Implementation Framing

- {{recommended approach, framework-agnostic}}
- {{constraints the implementer must respect}}
- {{areas where the implementer has flexibility}}

## Reference Images or Inspirations

{{Paste paths or URLs to reference materials used during discovery}}

## After Implementation

If tokens or structural decisions change during implementation, propagate them
back to `design.json` and `structure.md` via the design-builder sync operation.
