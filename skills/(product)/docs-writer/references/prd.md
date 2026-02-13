# PRD -- Product Requirements Document

## Workflow

```
discovery --> validation --> synthesis --> drafting
```

4 sequential phases. Never skip discovery -- always interview the user first.

## Phase 1: Discovery (Interview)

**LOAD:** [discovery.md](discovery.md) for shared interview patterns and critical posture.

Never assume context. Ask questions in stages, not all at once. Challenge weak ideas and ask for evidence.

**Stage 1 -- Problem:**
- What problem are you solving?
- How do you know this problem exists? (evidence, data, user feedback)
- How do people solve this today? (existing tools, workarounds, competitors)
- What is the cost of not solving it? (time, money, frustration)

**Stage 2 -- Users:**
- Who specifically will use this?
- What is their job to be done?
- What does their ideal outcome look like?
- Why would they pay for / switch to this? (or: why would they use this over the status quo?)

**Stage 3 -- Business & Scope:**
- What type of thing is this? (product, feature, internal tool, platform)
- How does it generate value? (monetization, cost reduction, efficiency)
- What makes it different from alternatives?
- How urgent is this? What happens if it ships 6 months late?

Minimum 2 question stages before moving to validation. Ask follow-ups as needed.

## Phase 2: Validation

Challenge what was learned. This phase exists to prevent building the wrong thing.

1. **Challenge viability**: Point out risks and weak spots identified during discovery
2. **Question scope**: Is the scope realistic for a first version? If not, push back
3. **Suggest simplifications**: Propose cuts when scope is ambitious. "Do you need X for launch, or can it wait?"
4. **Propose pivots**: If the idea seems fragile after discovery, suggest alternative approaches
5. **Define MVP scope**: Categorize features into must/should/could priorities
6. **Identify hypotheses**: What assumptions need evidence before or during implementation?
7. **Confirm with user**: Present validation findings and get explicit agreement before proceeding

Do not proceed to synthesis until the user confirms scope and priorities.

## Phase 3: Synthesis

Synthesize everything from discovery and validation into a structured summary.

1. Summarize what was learned across all discovery stages
2. Present the agreed scope (must/should/could)
3. List risks and hypotheses identified during validation
4. Identify gaps and mark as TBD
5. Surface assumptions made (distinguish from validated facts)
6. Present synthesis to user for confirmation
7. Only proceed to drafting after user confirms

## Phase 4: Drafting

**USE TEMPLATES:**
- PRD: `templates/prd.md`
- Brief: `templates/brief.md`

**LOAD:** [brief.md](brief.md) for brief generation rules.

Generate both documents using the confirmed synthesis. Present drafts to user for review before saving.

## PRD Schema

### 1. Executive Summary

- **Problem Statement**: What problem exists and for whom, with evidence
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
- **Competitive Landscape**:
  - How the problem is solved today
  - Existing tools/workarounds/competitors
  - Gaps that remain

### 3. Scope Definition

- **Must Have**: Core features required for launch
- **Should Have**: Important but not launch-blocking
- **Could Have**: Nice-to-have for future iterations
- **Non-Goals**: What is explicitly out of scope and why

### 4. User Experience & Functionality

- **User Stories**: "As a [user], I want [action], so that [benefit]"
- **Acceptance Criteria**: When/Then/Shall format
- **Features List**: with descriptions

### 5. Technical Specifications

- **Architecture Overview**: high-level system design
- **Integration Points**: APIs, databases, auth
- **Security & Privacy**: requirements and constraints

### 6. Risks, Assumptions & Validation

- **Phased Rollout**: v1.0, v1.1, v2.0 (never frame as MVP)
- **Technical Risks**: known challenges
- **Hypotheses to Validate**: assumptions that need evidence before or during implementation
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
- Challenge ideas during discovery and validation -- do not be a yes-man
- Present draft for user feedback
- Mark unknowns as TBD rather than inventing constraints
- Use concrete, measurable requirements
- Keep phased rollout realistic (v1.0/v1.1/v2.0, not MVP framing)
- Generate Brief alongside PRD during drafting

**DON'T:**
- Skip discovery with fewer than 2 question stages
- Assume project type -- discover it
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")
- Proceed past validation without user confirmation on scope

## Output

- PRD: `.specs/docs/prd-{name}.md`
- Brief: `.specs/docs/brief-{name}.md`

## Integration

- **design-builder**: PRD informs copy extraction and design extraction (sections 1-5: problem, goals, value prop, competitive landscape, personas)
- **spec-driven**: PRD informs feature initialization (sections 1, 6, 7, 9: problem, scope, user stories, technical specs)
