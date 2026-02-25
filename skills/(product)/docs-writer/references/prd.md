# PRD -- Product Requirements Document

## Workflow

```
discovery --> validation --> synthesis --> drafting
```

4 sequential phases. Never skip discovery -- always interview the user first.

## Phase 1: Discovery (Interview)

**LOAD:** [discovery.md](discovery.md) for shared interview patterns and critical posture.

Never assume context. Discovery is adaptive -- deepen topics based on the quality of answers, not a fixed script. Each topic has opening questions, signals for when to probe further, and criteria for when to move on.

### Topic 1: Problem

**Opening questions:**
- What problem are you solving?
- How do you know this problem exists? (evidence, data, user feedback)
- What is the cost of not solving it?

**Deepen when:**
- User describes symptoms, not root cause → "Why does this happen? What causes it?"
- No evidence → "What would convince you this is real? Have you talked to users?"
- Multiple problems mixed → "These sound like separate problems. Which one is primary?"
- User starts with solution → "What problem does this solution address? Let's start there."

**Sufficient when:**
- Problem can be stated in one clear sentence
- Evidence exists or is explicitly marked as hypothesis
- Single primary problem identified (secondary problems noted separately)

### Topic 2: Users

**Opening questions:**
- Who specifically has this problem?
- What are they trying to accomplish? (job to be done)
- Why would they use this over the status quo?

**Deepen when:**
- "Everyone" or too broad → "Who is the *most* affected? Describe one specific person."
- Multiple user types → "Which persona is primary? What happens when their needs conflict?"
- Vague motivation → "Walk me through a concrete scenario. What does their day look like?"
- Can't articulate why they'd switch → "What would they have to give up? What's the switching cost?"

**Sufficient when:**
- At least one concrete persona with clear motivation
- Job to be done is specific enough to derive features from
- If multiple personas, priority between them is understood

### Topic 3: Market & Differentiation

**Opening questions:**
- How do people solve this today? (existing tools, workarounds, competitors)
- What makes your approach different or better?
- Why hasn't this been solved yet? (timing, technology, market gap)

**Deepen when:**
- "Nothing like this exists" → "How do people cope today? Even manual workarounds count."
- Crowded market → "With X, Y, Z already out there, why would someone switch to this?"
- Weak differentiator → "If a competitor copied this feature tomorrow, what would you still have?"
- Unaware of alternatives → surface known alternatives and ask how this compares

**Sufficient when:**
- Clear picture of how the problem is currently solved
- Differentiator is articulated beyond feature comparison
- User understands the competitive context

### Topic 4: Value & Scope

**Opening questions:**
- What type of thing is this? (product, feature, internal tool, platform)
- How does it generate value? (monetization, cost reduction, efficiency)
- What must exist at launch vs. what can wait?

**Deepen when:**
- Everything is "must have" → "If you could only ship 3 features, which 3?"
- Scope keeps expanding → "We started with X, now it's X+Y+Z. Should we narrow down?"
- Features without clear user connection → "Which persona needs this? What problem does it solve for them?"
- No clear value model → "Who pays? How? What justifies the cost?"

**Sufficient when:**
- Clear must/should/could prioritization
- Each must-have connects to the primary problem and persona
- Value generation model is understood or marked as TBD
- Boundaries are defined (what is explicitly out of scope)

## Phase 2: Validation

Challenge what was learned. This phase exists to prevent building the wrong thing.

1. **Challenge viability**: Point out risks and weak spots identified during discovery
2. **Question scope**: Is the scope realistic for a first version? If not, push back
3. **Suggest simplifications**: Propose cuts when scope is ambitious. "Do you need X for launch, or can it wait?"
4. **Propose pivots**: If the idea seems fragile after discovery, suggest alternative approaches
5. **Define scope**: Categorize features into must/should/could priorities
6. **Identify hypotheses**: What assumptions need evidence before or during implementation?
7. **Confirm with user**: Present validation findings and get explicit agreement before proceeding

Do not proceed to synthesis until the user confirms scope and priorities.

## Phase 3: Synthesis

Synthesize everything from discovery and validation into a structured summary.

1. Summarize what was learned across all discovery topics
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
- Generate Brief alongside PRD during drafting

**DON'T:**
- Skip discovery topics or advance without meeting sufficiency criteria
- Assume project type -- discover it
- Include visual/design direction (that belongs in design-builder)
- Use vague adjectives as requirements ("fast", "easy", "intuitive")
- Proceed past validation without user confirmation on scope

## Output

- PRD: `.artifacts/docs/prd.md`
- Brief: `.artifacts/docs/brief.md`

## Integration

- **design-builder**: PRD informs copy extraction and design extraction (sections 1-5: problem, goals, value prop, competitive landscape, personas)
- **spec-driven**: PRD informs feature initialization (sections 1, 6, 7, 9: problem, scope, user stories, technical specs)
