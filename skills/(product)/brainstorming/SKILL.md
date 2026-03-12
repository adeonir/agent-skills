---
name: brainstorming
description: >-
  Structured idea exploration from vague to direction. Discover
  context, diverge with techniques (constraint removal, analogy, inversion,
  converge on a direction with trade-off analysis, capture as artifact. Produces
  output that feeds docs-writer, spec-driven, and design-builder. Use when ideas
  are vague, multiple directions exist, or the team needs to explore before
  committing. Also use when the user wants to think through options, compare
  approaches, or explore before building. Triggers on "brainstorm", "explore
  ideas", "what should we build", "explore options", "think through this",
  "idea exploration", "compare approaches".
metadata:
  author: Adeonir Kohl
  version: "1.0.0"
---

# Brainstorming

Structured idea exploration from vague to direction.

## Workflow

```
discover --> diverge --> converge --> capture
  ^________________________|  (if no viable direction)
```

Discover maps the problem space (context, constraints, success criteria). Diverge
generates alternatives using structured techniques. Converge evaluates trade-offs
and picks a direction. Capture produces the artifact.

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
brainstorming -------> product-naming (direction feeds name generation)
brainstorming -------> docs-writer    (direction feeds PRD, pitch, design doc)
brainstorming -------> spec-driven    (direction feeds feature specification)
brainstorming -------> design-builder (direction feeds visual exploration)
```

## Guidelines

**DO:**
- Always complete discovery before diverging
- Generate at least 4 alternatives during diverge, including non-obvious options
- Challenge every alternative with trade-offs during converge
- Require explicit user approval before capturing the direction
- Mark unknowns as TBD rather than inventing constraints
- Suggest the appropriate next skill after capture

**DON'T:**
- Skip directly to a solution (the point is exploration)
- Generate only 2-3 obvious alternatives (push for non-obvious options)
- Let the user commit to a direction without evaluating trade-offs
- Include implementation details (that belongs in spec-driven)
- Proceed past converge without user confirmation

## Output

- Artifact: `.artifacts/brainstorm/{topic}.md`
- `{topic}` in kebab-case, derived from the brainstorm subject
- **USE TEMPLATE:** `templates/brainstorm.md`
- Create `.artifacts/brainstorm/` if it does not exist

## Error Handling

- No `.artifacts/brainstorm/` directory: create it
- User arrives with a clear solution: ask if they want to explore alternatives
  first, or redirect to docs-writer
- No viable direction after converge: loop back to discovery with refined
  understanding
- Scope too broad: decompose into sub-problems, brainstorm one at a time
- User wants to skip diverge: warn that brainstorming value comes from exploring
  alternatives, suggest docs-writer if they already have a direction
