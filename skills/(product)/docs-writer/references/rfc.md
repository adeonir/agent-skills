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
- Current state and desired state are clearly different
- Impact of inaction is understood

**Clarify when:**
- Change without clear motivation → "What breaks or degrades if we don't do this?"
- Scope of impact unclear → "Who else is affected by the current state?"

### Proposed Solution

**Sufficient when:**
- Solution is concrete enough to evaluate trade-offs
- Key constraints are identified

**Clarify when:**
- Solution is hand-wavy → "Walk me through how this would work in practice."
- No constraints acknowledged → "What limits what we can do here?"
- Single option presented as obvious → "What alternatives did you consider?"

### Impact

**Sufficient when:**
- Affected systems and teams identified
- Breaking changes documented or confirmed as none

**Clarify when:**
- "Just our system" → "Does anything consume our API/data? Any downstream effects?"
- Breaking changes mentioned casually → "Who needs to change and what's the migration path?"

## Analysis

Synthesize input into structured analysis:

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

## Drafting

**USE TEMPLATE:** `templates/rfc.md`

Generate the RFC using the schema below. Present draft to user for review.

## RFC Schema

12 sections matching `templates/rfc.md`:

| Section | Content |
|---------|---------|
| 1. Summary | One-paragraph description of the proposal |
| 2. Motivation | Why this change is needed, current vs desired state |
| 3. Detailed Design | Technical description with overview and implementation details |
| 4. Impact Analysis | Performance impact, dependencies, team impact |
| 5. Drawbacks | Accepted trade-offs and open risks (separated explicitly) |
| 6. Alternatives | Options evaluated with rejection rationale, starting with "Do Nothing" |
| 7. Prior Art | How others solved this problem -- other teams, companies, open source projects |
| 8. Adoption Strategy | Rollout plan, migration path, breaking changes |
| 9. Unresolved Questions | Open items needing discussion or deferred to implementation |
| 10. Future Possibilities | What this enables or opens up for future work |
| 11. Feedback | Reviewer table for tracking review status |
| 12. References | Links to related RFCs, documentation |

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

Save to: `.artifacts/docs/rfc/{number}-{name}.md`

Use kebab-case for `{name}` and auto-detect the next sequential number from existing files in `.artifacts/docs/rfc/`.
