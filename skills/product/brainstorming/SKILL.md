---
name: brainstorming
description: >-
  Structured idea exploration from vague to direction, or stress-test of an
  existing plan. Feeds docs-writer, spec-driven, and design-builder. Use when
  ideas are vague, multiple directions exist, or the user wants to explore
  options or pressure-test a plan before building.
when_to_use: >-
  Triggers on "brainstorm", "explore ideas", "what should we build",
  "explore options", "think through this", "idea exploration",
  "compare approaches", "stress-test this", "grill me on this plan".
argument-hint: "[deep]"
---

# Brainstorming

Structured idea exploration from vague to direction.

## Workflow

```
trigger --> detect path --> discover --> diverge --> converge --> capture
              ^________________________________|  (if no viable direction)
```

Detect path from entry state (standard for vague ideas, relentless for existing
plans). Discover maps the problem space. Diverge generates alternatives. Converge
evaluates trade-offs and picks a direction. Capture produces the artifact.

## Context Loading Strategy

Load only the reference matching the current phase. The workflow always starts
with discovery.

- Start with `discovery.md` on every trigger
- Load `diverge.md` after discovery quality gate passes
- Load `converge.md` after diverge produces at least 4 alternatives
- Load template only during capture (after user approves direction)

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Brainstorm, explore ideas, idea exploration | [discovery.md](references/discovery.md) |
| What should we build, think through this | [discovery.md](references/discovery.md) |
| Explore options, compare approaches | [discovery.md](references/discovery.md) |

Notes:

- `diverge.md` is not a direct trigger. It is loaded after discovery completes.
- `converge.md` is not a direct trigger. It is loaded after diverge completes.
- The full workflow always starts with discovery regardless of trigger.

## Cross-References

```
discovery.md  -------> diverge.md     (context feeds alternative generation)
diverge.md    -------> converge.md    (alternatives feed evaluation)
brainstorming -------> docs-writer    (direction feeds PRD, epic, design doc)
brainstorming -------> spec-driven    (direction feeds feature specification)
brainstorming -------> design-builder (direction feeds visual exploration)
```

## Guidelines

**DO:**
- Generate at least 4 alternatives during diverge, including non-obvious options
- Challenge every alternative with trade-offs during converge
- Require explicit user approval before capturing the direction
- Mark unknowns as TBD rather than inventing constraints
- Stay at the problem-and-direction level; defer implementation choices
- Suggest the appropriate next skill after capture

**DON'T:**
- Generate only 2-3 obvious alternatives (contrasts: push for non-obvious options)
- Let the user commit to a direction without evaluating trade-offs (contrasts: challenge every alternative)
- Include implementation details (contrasts: stay at the problem-and-direction level)
- Proceed past converge without user confirmation (contrasts: require explicit approval)

## Output

- Artifact: `.artifacts/brainstorm/{topic}.md`
- `{topic}` in kebab-case, derived from the brainstorm subject
- **USE TEMPLATE:** `templates/brainstorm.md`
- Create `.artifacts/brainstorm/` if it does not exist

## Error Handling

- No `.artifacts/brainstorm/` directory: create it
- User arrives with a clear plan or solution: detect as relentless path, proceed
  with stress-test discovery. Only redirect to docs-writer if they want to skip
  discovery entirely.
- No viable direction after converge: loop back to discovery with refined
  understanding
- Scope too broad: decompose into sub-problems, brainstorm one at a time
- User wants to skip diverge: warn that brainstorming value comes from exploring
  alternatives, suggest docs-writer if they already have a direction
