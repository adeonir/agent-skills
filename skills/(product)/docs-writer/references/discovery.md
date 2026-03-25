# Shared Discovery Patterns

Common interview and discovery patterns used across document types.

## When to Use

Auto-loaded by PRD, Design Doc, and TDD workflows during the discovery phase. Not a direct trigger.

## Core Principle

Never assume context. Always ask before drafting. The depth of discovery varies by document type, but the principle is the same: understand the problem before writing the solution.

## Interview Strategy

Discovery is adaptive, not scripted. Each document type defines topics with opening questions. The agent decides when to deepen and when to move on based on the quality of answers received.

### How It Works

1. Start each topic with its opening questions (2-4 per topic)
2. Evaluate answers against the topic's sufficiency criteria
3. If criteria are not met, deepen -- ask follow-ups targeting the gap
4. If criteria are met, move to the next topic
5. Summarize understanding before advancing

### Adaptive Deepening

Probe further when answers are:

- **Vague**: "users want something better" → ask for specifics
- **Assumed**: stated as fact without evidence → ask for evidence or mark as hypothesis
- **Conflated**: multiple concepts mixed in one answer → separate and explore each
- **Solution-first**: describes what to build before why → redirect to the problem
- **Overly broad**: "everyone", "all cases" → narrow down to the most important

Move on when:

- The topic's sufficiency criteria are met
- The user explicitly says "I don't know" (mark as TBD)
- Further questioning would not yield new information

### Question Principles

- Open-ended first, specific later
- Never suggest answers in the question (avoid leading questions)
- Build follow-ups on what the user actually said, not on a script
- One question at a time -- never batch multiple questions in a single message
- Summarize understanding before moving to the next topic

## Discovery Depth by Type

**Full discovery** (adaptive deepening, sufficiency criteria, critical posture):

| Type | Topics | Focus |
|------|--------|-------|
| PRD | 5 topics | Problem, users, market, scope, journeys & constraints |
| Design Doc | 3 topics | System overview, architecture & design, cross-cutting concerns |
| TDD | 3 topics | Requirements & stack, architecture & integrations, operations & risk |

**Clarification only** (ask only when input is incomplete):

| Type | Focus |
|------|-------|
| RFC | Problem, proposal, impact |
| ADR | Context, options |

## Synthesis Pattern

After discovery is complete, synthesize before drafting:

1. Summarize what was learned
2. Identify gaps (mark as TBD)
3. Surface assumptions made
4. Present synthesis to user for confirmation
5. Only proceed to drafting after user confirms

## Critical Posture

Discovery is not a formality. Challenge ideas with respect, but never be a yes-man.

### Principles

- **Ask for evidence.** When the user claims a problem exists, ask: "How do you know this problem exists? What evidence do you have?" Accept anecdotal evidence but distinguish it from data.
- **Challenge weak ideas.** If an idea sounds like a solution looking for a problem, say so. "This sounds like you already decided the solution -- can we go back to the problem?"
- **Suggest pivots.** If the problem is real but the proposed approach seems fragile, propose alternatives. "Have you considered X instead?" Frame pivots as questions, not demands.
- **Flag scope creep.** If the user keeps adding features or expanding scope during discovery, pause and realign. "We started with X -- this is now X + Y + Z. Should we narrow down?"
- **Gate advancement.** Only move from discovery to the next phase when you have confidence that the problem is understood. If something feels off, ask one more question rather than proceeding with uncertainty.

### What This Looks Like

| Situation | Passive Response | Critical Response |
|-----------|-----------------|-------------------|
| User describes vague problem | "Okay, let's proceed" | "Who specifically has this problem? How often?" |
| User jumps to solution | "Got it, I'll include that" | "Before we define the solution -- what problem does this solve?" |
| User adds scope mid-discovery | "I'll add that too" | "This changes the scope significantly. Should we focus on the core first?" |
| User has no evidence | "Noted" | "Without evidence, this is an assumption. Should we mark it as a hypothesis to validate?" |

## Quality Gate

Before moving from discovery to drafting, verify:

- [ ] All topics have met their sufficiency criteria or gaps are marked as TBD
- [ ] Unknowns are explicitly marked as TBD
- [ ] User has confirmed the synthesis
- [ ] No critical ambiguity remains (ask if unclear)
- [ ] Problem is understood with evidence or explicitly marked as hypothesis
