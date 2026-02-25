# RFC -- Request for Comments

## Workflow

```
discovery --> analysis --> drafting
```

3-phase workflow. RFCs propose changes that need team discussion before implementation.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

### Topic 1: Problem & Motivation

**Opening questions:**
- What problem or opportunity is this addressing?
- Why is the current state insufficient?
- Who is affected?

**Deepen when:**
- Change without clear motivation → "What breaks or degrades if we don't do this?"
- Scope of impact unclear → "Who else is affected by the current state?"
- Assumed consensus → "Does everyone agree this is a problem? What's the evidence?"

**Sufficient when:**
- Current state and desired state are clearly different
- Impact of inaction is understood

### Topic 2: Proposed Solution

**Opening questions:**
- What is the proposed change?
- What are the key design decisions?
- What are the constraints?

**Deepen when:**
- Solution is hand-wavy → "Walk me through how this would work in practice."
- No constraints acknowledged → "What limits what we can do here?"
- Single option presented as obvious → "What alternatives did you consider?"

**Sufficient when:**
- Solution is concrete enough to evaluate trade-offs
- Key constraints are identified

### Topic 3: Impact (if needed)

**Opening questions:**
- What systems or teams are affected?
- Are there breaking changes?
- Are there migration concerns?

**Deepen when:**
- "Just our system" → "Does anything consume our API/data? Any downstream effects?"
- Breaking changes mentioned casually → "Who needs to change and what's the migration path?"

**Sufficient when:**
- Affected systems and teams identified
- Breaking changes documented or confirmed as none

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
