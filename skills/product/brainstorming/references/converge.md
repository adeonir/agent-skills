# Converge -- Evaluate and Decide

Narrow the field. Evaluate trade-offs systematically. Pick a direction with
eyes open.

## When to Use

After diverge produces at least 4 alternatives. Loaded automatically as
third phase.

## Core Principle

Every alternative gets a fair hearing before elimination. Trade-offs are
explicit, not hidden. The user decides, the agent informs.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### Pre-screen: Surface TBDs

Before screening, check for open TBDs carried from discovery:

- **Constraint TBDs:** Resolve or explicitly accept the ambiguity before
  screening. Alternatives cannot be properly eliminated against unknown
  constraints. Ask the user to clarify or acknowledge the risk.
- **Criteria TBDs:** Note as evaluation gaps in the comparison table — they
  will produce incomplete scores, which is acceptable.
- **Motivation TBDs:** If present, consider looping back to discovery.

### Step 1: Screen

Quick pass: eliminate alternatives that violate hard constraints identified
in discovery. State why each eliminated option fails (one sentence).

Also eliminate alternatives that violate YAGNI -- solutions that add
complexity for hypothetical future needs, solve problems that don't exist
yet, or over-engineer beyond the stated success criteria.

Remaining alternatives proceed to evaluation.

### Step 2: Evaluate Against Criteria

Use the success criteria from discovery as evaluation dimensions. For each
surviving alternative, assess against each criterion.

| Alternative | {Criterion 1} | {Criterion 2} | {Criterion 3} |
|-------------|---------------|---------------|---------------|
| {Name A} | strong | adequate | weak |
| {Name B} | adequate | strong | strong |
| {Name C} | weak | adequate | strong |

### Step 3: Trade-off Analysis

For each surviving alternative:

```markdown
**{Name}**
- Gain: {what you get}
- Give up: {what you lose}
- Risk: {what could go wrong}
- Assumption: {what must hold}
```

Surface tensions explicitly: "Alternative A is best for speed but worst for
flexibility."

### Step 4: Identify Hybrids

Check if strengths from multiple alternatives can be combined. Only propose
hybrids if they resolve a genuine trade-off -- not frankensteining parts
together without purpose.

### Step 5: Recommend

Present a recommendation with rationale. Make it clear this is a recommendation,
not a decision.

If no clear winner: present the top 2 with the key deciding factor between them.

### Step 6: User Decision

User picks the direction or asks to loop back.

- If approved: proceed to capture
- If loop back: return to discovery with refined understanding, articulate what
  new information is needed before restarting

If approved, proceed to review before capture.

### Step 7: Review Artifact

Before saving, verify the brainstorm artifact:

- [ ] No unresolved TBDs that block the chosen direction
- [ ] No contradictions between constraints and chosen alternative
- [ ] Scope is focused enough to act on (one direction, not three)
- [ ] Trade-offs are explicit (nothing hidden to make the choice look better)
- [ ] Open questions are genuine unknowns, not laziness

If issues found: fix inline before saving. Don't deliver a flawed artifact.

## Guidelines

**DO:**
- Give every alternative a fair screening before elimination
- Make trade-offs explicit and visible
- Present a recommendation but let the user decide
- Allow looping back if no direction feels right
- Present the comparison table for structured evaluation

**DON'T:**
- Dismiss alternatives without stating why
- Hide trade-offs to make a recommendation look stronger
- Force a decision when the user needs more exploration
- Skip the comparison table
- Combine all alternatives into one "best of everything" hybrid

## Error Handling

- All alternatives eliminated by constraints: loop back to discovery --
  constraints may be too tight, or the problem needs reframing
- User cannot decide between top 2: identify the one question that would break
  the tie, suggest answering it before deciding
- User wants to combine everything: warn about complexity, ask which trade-off
  they are trying to avoid

## Next Steps

After the user approves a direction, capture it and save to
`.artifacts/brainstorm/{topic}.md` (`{topic}` in kebab-case, derived from
the brainstorm subject). Then suggest the appropriate next step:
formalize the direction as a document, specify and implement directly,
or explore the visual direction.

## Capture Template

ALWAYS use this exact template structure:

````markdown
---
name: {{topic}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources: []
---

# Brainstorm: {{Topic Title}}

## Context

{{Summary of motivation, current state, and timing from discovery}}

## Constraints

### Hard Constraints

- {{Non-negotiable boundary}}

### Soft Constraints

- {{Preference that can flex}}

## Success Criteria

- {{How the direction will be evaluated}}

## Alternatives Explored

### {{Alternative 1 Name}} (chosen)

{{One-paragraph description}}

**Strengths:** {{key advantages}}
**Weaknesses:** {{key disadvantages}}
**Key Assumption:** {{what must hold for this to work}}

### {{Alternative 2 Name}} (rejected)

{{One-paragraph description}}

**Strengths:** {{key advantages}}
**Weaknesses:** {{key disadvantages}}
**Rejected Because:** {{one-sentence rationale}}

{Repeat for each alternative explored}

## Decision

**Chosen Direction:** {{name of chosen alternative}}

**Rationale:** {{why this direction over the others}}

**Key Trade-offs Accepted:**

- {{what was given up and why it is acceptable}}

## Open Questions

- [ ] TBD: {{question that needs answering before proceeding}}

## Next Step

{{Recommended next action and which workflow to use:}}
{- Formalize direction into a PRD, epic, or design doc}
{- Specify and implement directly}
{- Explore visual direction}
````
