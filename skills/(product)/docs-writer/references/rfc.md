# RFC -- Request for Comments

## Workflow

```
discovery --> analysis --> drafting
```

3-phase workflow. RFCs propose changes that need team discussion before implementation.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

**Stage 1 -- Problem & Motivation:**
- What problem or opportunity is this addressing?
- Why is the current state insufficient?
- Who is affected?

**Stage 2 -- Proposed Solution:**
- What is the proposed change?
- What are the key design decisions?
- What are the constraints?

**Stage 3 -- Scope & Impact (if needed):**
- What systems or teams are affected?
- What is the expected timeline?
- Are there migration concerns?

Minimum 2 stages before moving to analysis.

## Phase 2: Analysis

Synthesize discovery into structured analysis:

1. Identify alternatives to the proposed solution
2. Evaluate trade-offs for each alternative
3. Surface risks and unknowns
4. Identify dependencies on other systems or decisions
5. Present analysis to user for feedback before drafting

### Alternatives Evaluation

For each alternative (including the proposed solution):

| Criteria | Alternative A | Alternative B | Proposed |
|----------|--------------|--------------|----------|
| Complexity | | | |
| Risk | | | |
| Timeline | | | |
| Trade-offs | | | |

## Phase 3: Drafting

**USE TEMPLATE:** `templates/rfc.md`

Generate the RFC using the schema below. Present draft to user for review.

## RFC Schema

### 1. Summary

One-paragraph description of the proposal.

### 2. Motivation

- Why is this change needed?
- What problem does it solve?
- What is the current state?

### 3. Detailed Design

- Technical description of the proposed change
- How it works
- Key implementation details

### 4. Alternatives Considered

- What other approaches were evaluated?
- Why were they rejected?
- Trade-offs of each

### 5. Adoption Strategy

- How will this be rolled out?
- Migration path (if applicable)
- Breaking changes (if any)

### 6. Unresolved Questions

- Open items that need further discussion
- Decisions deferred to implementation

## Status Lifecycle

```
draft --> under-review --> accepted / rejected / withdrawn
```

- **draft**: Initial creation, not yet shared
- **under-review**: Shared with team for feedback
- **accepted**: Approved for implementation
- **rejected**: Not approved (reason documented)
- **withdrawn**: Author pulled the proposal

## Guidelines

- RFCs should be self-contained -- a reader should understand the proposal without external context
- Alternatives must include genuine options, not straw-man arguments
- Unresolved questions are expected -- don't force premature decisions
- An accepted RFC can lead to an ADR (use docs-writer to create one)

## Output

Save to: `.artifacts/docs/rfc.md`
