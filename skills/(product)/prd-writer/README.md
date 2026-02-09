# PRD Writer

Generate structured Product Requirements Documents through guided discovery.

## What It Does

Guides you through a 3-phase process to create a comprehensive PRD:

```mermaid
flowchart LR
    A[Discovery] --> B[Analysis]
    B --> C[Drafting]
    C --> D[prd.md]
```

| Phase | Purpose |
| ----- | ------- |
| **Discovery** | Interview to understand problem, audience, solution, features |
| **Analysis** | Synthesize inputs, identify risks, define non-goals |
| **Drafting** | Generate PRD using structured schema with measurable criteria |

## PRD Sections

1. **Executive Summary** -- Problem, solution, success criteria (KPIs)
2. **Product Definition** -- Value proposition, target audience, pain points
3. **User Experience & Functionality** -- User stories, acceptance criteria, features, non-goals
4. **Technical Specifications** -- Architecture, integrations, security
5. **Risks & Roadmap** -- Phased rollout (v1.0/v1.1/v2.0), risks, unknowns

## Usage

```
create PRD for my project
define product requirements
write PRD for a task management app
```

The agent will guide you through discovery questions before drafting.

## Output

```
.specs/docs/prd-{project-name}.md
```

## Integration

| Skill | How PRD is used |
| ----- | --------------- |
| **design-builder** | Sections 1, 2, 3 inform copy and design extraction |
| **spec-driven** | Sections 1, 3, 4, 5 inform feature initialization |

## Quality Standards

All requirements must be concrete and measurable:

- "Search returns results within 200ms" (not "search should be fast")
- "New users complete onboarding in under 2 minutes" (not "easy to use")
- Unknowns marked as TBD, never invented

## Requirements

Works with any agent supporting standard skill format.
