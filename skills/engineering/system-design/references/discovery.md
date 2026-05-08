# Discovery

Problem framing phase. Understand what needs to be built before touching
requirements, trade-offs, or architecture.

## When to Use

Always the entry point. Load at the start of every system design session,
regardless of how much context the user provides.

## Core Principle

The problem statement a user provides at the start is rarely the complete
picture. Discovery exists to surface what they know but haven't said, what
they haven't thought about yet, and what constraints will shape the design.

## Interview Strategy

Discovery is adaptive, not scripted. The topics below define the territory.
The agent decides when to deepen and when to move on based on answer quality.

### Topics

**1. Problem and context**
- What problem are you solving?
- Who encounters this problem? (users, systems, teams)
- What happens today without this system?

**2. Users and usage patterns**
- Who are the users? (end users, internal teams, external services)
- How do they interact with the system? What are the main actions?
- What does a normal session or request look like?

**3. Scope and boundaries**
- What is in scope for this design?
- What is explicitly out of scope?
- Are there existing systems this integrates with or replaces?

**4. Constraints and context**
- Are there existing technology choices or preferences?
- Team size and operational capacity?
- Timeline or budget signals?

### Adaptive Deepening

Probe further when answers are:

- **Vague**: "users want something better" → ask for specifics
- **Solution-first**: describes what to build before why → redirect to the
  problem
- **Assumed**: stated as fact without evidence → ask for evidence or mark as
  hypothesis
- **Overly broad**: "everyone", "all cases" → narrow to the most important

Move on when:
- The topic is sufficiently understood
- The user explicitly says "I don't know" (mark as open question)
- Further questioning would not yield new information

### Question Principles

- One question at a time — never batch multiple questions in a single message
- Open-ended first, specific later
- Never suggest answers in the question
- Build follow-ups on what the user actually said
- Summarize understanding before moving to the next topic

## Quality Gate

Before loading `requirements.md`, verify:

- [ ] Problem is understood — what it is, who it affects, why it matters
- [ ] Users and usage patterns are defined
- [ ] Scope boundaries are established
- [ ] Key constraints or preferences are noted
- [ ] Open questions are explicitly listed as such

## Next Steps

When the quality gate passes, summarize the problem framing to the user and
confirm before loading [requirements.md](requirements.md).
