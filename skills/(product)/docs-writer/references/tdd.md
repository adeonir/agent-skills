# TDD -- Technical Design Document

## Workflow

```
discovery --> analysis --> drafting
```

3-phase workflow. TDDs are deep technical documents that plan system design before implementation.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

### Topic 1: Requirements

**Opening questions:**
- What is being built? (high-level overview)
- What must it do? (functional requirements)
- What are the quality constraints? (performance, scalability, security)

**Deepen when:**
- Only functional requirements → "What about performance, security, reliability?"
- Requirements are vague → "What does 'fast' mean? What numbers are acceptable?"
- Missing boundaries → "What does this NOT need to do?"

**Sufficient when:**
- Functional requirements are concrete and enumerable
- Non-functional requirements have measurable targets
- Scope boundaries are defined

### Topic 2: Constraints & Dependencies

**Opening questions:**
- What technical constraints exist? (stack, infrastructure, existing systems)
- What does this integrate with?
- Are there related ADRs or RFCs?

**Deepen when:**
- "Standard stack" → "Which specific versions, frameworks, infrastructure?"
- No dependencies mentioned → "Does this read from or write to any existing system?"
- Ignoring prior decisions → "Are there architectural decisions that constrain this?"

**Sufficient when:**
- Stack and infrastructure constraints are concrete
- Integration points identified
- Prior architectural decisions accounted for

### Topic 3: Architecture Preferences (if needed)

**Opening questions:**
- Are there architectural patterns to follow?
- How should this scale?
- What are the critical failure scenarios?

**Deepen when:**
- No pattern preference → "How does the rest of the system handle similar problems?"
- Scalability hand-waved → "What's the expected load? What happens at 10x?"
- Failure modes ignored → "What happens when [dependency] goes down?"

**Sufficient when:**
- Architectural direction is clear (or explicitly open for exploration in analysis)
- Scale expectations have concrete numbers
- Critical failure scenarios identified

## Phase 2: Analysis

Synthesize discovery into technical analysis:

1. Identify system boundaries and interfaces
2. Evaluate architectural options
3. Map data flows and state management
4. Identify technical risks and unknowns
5. Present analysis to user for feedback before drafting

### Architecture Evaluation

For key architectural decisions, consider:

- Complexity vs. maintainability
- Performance vs. development speed
- Flexibility vs. simplicity
- Build vs. buy

Reference existing ADRs when decisions have already been recorded.

## Phase 3: Drafting

**USE TEMPLATE:** `templates/tdd.md`

Generate the TDD using the schema below. Present draft to user for review.

## TDD Schema

### 1. Overview

- **Problem**: What is being solved
- **Scope**: What is included and excluded
- **Audience**: Who should read this document

### 2. Requirements

- **Functional**: What the system must do
- **Non-Functional**: Performance, scalability, security, reliability
- **Constraints**: Technical limitations, business rules

### 3. Architecture

- **System Design**: High-level architecture description
- **Components**: Key components and their responsibilities
- **Data Flow**: How data moves through the system

### 4. API Design

- **Endpoints / Interfaces**: Public API surface
- **Contracts**: Request/response formats
- **Error Handling**: How errors are surfaced

### 5. Data Model

- **Entities**: Core data structures
- **Relationships**: How entities relate to each other
- **Storage**: Where and how data is persisted

### 6. Trade-Offs

- **Decisions Made**: Key technical decisions with rationale
- **Alternatives Rejected**: What was considered and why it was dropped
- **Known Limitations**: What this design does not handle
- **Related ADRs**: Link to architecture decision records

### 7. Open Questions

- Items requiring further investigation
- Decisions deferred to implementation

## Guidelines

- TDDs should be written before implementation, not after
- Focus on the "why" behind design choices, not just the "what"
- Include concrete examples (API payloads, data schemas) when possible
- Reference ADRs for architectural decisions rather than duplicating rationale
- Keep diagrams text-based (ASCII or Mermaid) for version control friendliness
- Mark unknowns as TBD -- don't invent solutions for problems not yet understood

## Output

Save to: `.artifacts/docs/tdd.md`
