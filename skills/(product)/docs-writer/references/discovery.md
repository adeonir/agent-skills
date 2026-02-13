# Shared Discovery Patterns

Common interview and discovery patterns used across document types.

## Core Principle

Never assume context. Always ask before drafting. The depth of discovery varies by document type, but the principle is the same: understand the problem before writing the solution.

## Interview Strategy

Ask questions in stages, not all at once. Each stage should build on the previous answers.

### Stage Flow

1. Ask 2-4 questions per stage
2. Wait for user response
3. Ask follow-up questions based on answers
4. Move to next stage when sufficient context is gathered
5. Minimum stages before drafting depends on document type

### Question Principles

- Open-ended first, specific later
- Never suggest answers in the question (avoid leading questions)
- If the user gives a vague answer, ask for specifics
- If the user says "I don't know", mark it as TBD and move on
- Summarize understanding before moving to the next stage

## Discovery Depth by Type

| Type | Minimum Stages | Focus |
|------|---------------|-------|
| PRD | 3 stages | Problem, users, business & scope |
| Issue (feature) | 1-2 stages | Problem, proposed solution |
| Issue (discussion) | 1 stage | Topic, context |
| User Story | 1-2 stages | Persona, action, benefit |
| RFC | 2-3 stages | Problem, proposal, alternatives |
| ADR | 1-2 stages | Context, decision drivers |
| TDD | 2-3 stages | Requirements, constraints, architecture |

Types that skip discovery: Task, Issue (bug -- uses structured reproduction instead).

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

- [ ] Core questions for the document type have been answered
- [ ] Unknowns are explicitly marked as TBD
- [ ] User has confirmed the synthesis
- [ ] No critical ambiguity remains (ask if unclear)
- [ ] Problem is understood with evidence or explicitly marked as hypothesis
