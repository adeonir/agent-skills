---
name: prd-writer
description: >-
  Generate Product Requirements Documents through structured discovery.
  3 phases: Discovery interview, Analysis & Scoping, Technical Drafting.
  Use when: defining new products, planning features, documenting requirements.
  Triggers on "create PRD", "define product", "product requirements",
  "write PRD".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# PRD Writer

Generate structured Product Requirements Documents through guided discovery.

## Workflow

```
discovery --> analysis --> drafting
```

3 sequential phases. Never skip discovery -- always interview the user first.

## Process

### Phase 1: Discovery (Interview)

Never assume context. Ask questions in stages, not all at once.

**Stage 1 -- Problem & Audience:**
- What problem are you solving?
- Who is the target audience?
- What pain points do they have?

**Stage 2 -- Solution & Features:**
- What is your proposed solution?
- What are the key features?
- What makes it different from alternatives?

**Stage 3 -- Structure & Scope:**
- What is the product structure? (pages, screens, sections)
- What are the success criteria?
- Any known technical constraints?

Minimum 2 question stages before moving to analysis. Ask follow-ups as needed.

### Phase 2: Analysis & Scoping

Synthesize user inputs into structured findings:

1. Identify dependencies and risks
2. Define non-goals (what is out of scope)
3. Surface unknowns (mark as TBD)
4. Present synthesis to user for feedback before drafting

### Phase 3: Drafting

**USE TEMPLATE:** `templates/prd.md`

Generate the PRD using the schema below. Present draft to user for review.

## PRD Schema

### 1. Executive Summary

- **Problem Statement**: What problem exists and for whom
- **Proposed Solution**: High-level description of what will be built
- **Success Criteria**: Measurable KPIs (concrete numbers, not vague goals)

### 2. Product Definition

- **Value Proposition**:
  - Headline: main benefit
  - Subheadline: supporting text
  - Key Benefits: 3-5 benefits
- **Target Audience**:
  - Personas: who uses this
  - Pain Points: what problems they face
  - Goals: what they want to achieve

### 3. User Experience & Functionality

- **User Stories**: "As a [user], I want [action], so that [benefit]"
- **Acceptance Criteria**: When/Then/Shall format
- **Features List**: with descriptions
- **Non-Goals**: what is explicitly out of scope

### 4. Technical Specifications

- **Architecture Overview**: high-level system design
- **Integration Points**: APIs, databases, auth
- **Security & Privacy**: requirements and constraints

### 5. Risks & Roadmap

- **Phased Rollout**: v1.0, v1.1, v2.0 (never frame as MVP)
- **Technical Risks**: known challenges
- **Unknowns**: marked as TBD

## Quality Standards

Requirements must be concrete and measurable.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Guidelines

**DO:**
- Always complete discovery before drafting
- Present draft for user feedback
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep phased rollout realistic (v1.0/v1.1/v2.0, not MVP framing)

**DON'T:**
- Skip discovery with fewer than 2 question stages
- Assume project type -- discover it
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")

## Output

Save to: `.specs/docs/prd-{project-name}.md`

Create `.specs/docs/` if it doesn't exist.

## Integration with Other Skills

- **design-builder**: PRD informs copy extraction and design extraction (sections 1, 2, 3)
- **spec-driven**: PRD informs feature initialization (sections 1, 3, 4, 5)
