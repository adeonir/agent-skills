# RFC -- Request for Comments

## When to Use

When proposing a significant change that needs team review and discussion.

## Workflow

```
[clarification] --> analysis --> drafting
```

2-phase workflow with optional clarification. RFCs propose changes that need team discussion before implementation. The author typically comes with the problem and proposal -- only clarify when input is incomplete.

## Clarification (when input is incomplete)

Evaluate the user's input against the sufficiency criteria below. If all criteria are met, skip directly to analysis. If gaps exist, ask only about the gaps.

### Problem & Motivation

**Sufficient when:**
- The problem and why it matters are clear
- Impact of inaction is understood

**Clarify when:**
- Change without clear motivation
- Scope of impact unclear

### Proposed Solution

**Sufficient when:**
- Solution is concrete enough to evaluate trade-offs
- Key constraints are identified

**Clarify when:**
- Solution is hand-wavy
- No constraints acknowledged
- Single option presented as obvious without alternatives

## Analysis

Synthesize input into structured analysis:

1. Identify alternatives to the proposed solution
2. Evaluate trade-offs for each alternative
3. Surface risks and unknowns
4. Present analysis to user for feedback before drafting

## Drafting

**USE TEMPLATE:** `templates/rfc.md`

Generate the RFC using the schema below. Present draft to user for review.

## RFC Schema

7 sections matching `templates/rfc.md`:

| Section | Content |
|---------|---------|
| 1. Motivation | Why this change is needed, what problem it solves |
| 2. Proposal | Concise description of the proposed solution |
| 3. Design | Structure, model, or technical detail. Use tables when possible |
| 4. Alternatives | Options evaluated with rejection rationale |
| 5. Risks | Trade-offs and risks with mitigation |
| 6. Unresolved Questions | Open items needing discussion |
| 7. References | Links to related documents |

### Section guidelines

- **Motivation** should stand alone -- a reader understands the problem without external context
- **Design** uses tables and lists over prose. No implementation details unless the RFC is about a technical change
- **Alternatives** includes genuine options with real trade-offs, not straw-man arguments. Include "Do Nothing" when inaction is a viable option
- **Risks** pairs each risk with a mitigation. Keep the list short (3-5 items max)
- **Unresolved Questions** are expected -- do not force premature decisions

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

**DO:**
- Keep RFCs concise -- optimized for quick analysis and decision-making
- Make RFCs self-contained -- a reader should understand the proposal without external context
- Include genuine alternatives with real trade-offs
- Keep unresolved questions open -- they are expected
- Create an ADR when an RFC is accepted (use docs-writer)

**DON'T:**
- Repeat information that exists in referenced documents (PRD, design docs, etc.)
- Include implementation details unless the RFC is specifically about a technical change
- Use straw-man arguments as alternatives
- Force premature decisions on unresolved questions
- Add sections that don't contribute to the decision

## Output

Save to: `.artifacts/docs/rfc/{number}-{name}.md`

Use kebab-case for `{name}` and auto-detect the next sequential number from existing files in `.artifacts/docs/rfc/`.
