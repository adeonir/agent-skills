# Epic -- Deliverable Feature Slice

## When to Use

When defining a deliverable slice of functionality within a milestone. Epics group related requirements (FRs) from the PRD into a cohesive unit that can be built, tested, and shipped independently.

## Workflow

```
[clarification] --> drafting
```

Direct drafting with optional clarification. The user comes with the problem and proposed solution -- only clarify when input is incomplete.

## Step 1: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and use as context for drafting. PRD provides personas (section 3), scope (section 4), journeys (section 5), and business rules (section 6) that inform epic writing. Less clarification needed.

If no PRD exists: rely on user input and clarify more proactively.

## Step 2: Clarification (when input is incomplete)

Evaluate the user's input (and PRD context if available) against the sufficiency criteria below. If all criteria are met, skip directly to drafting. If gaps exist, ask only about the gaps.

### Problem

**Sufficient when:**
- Problem is described with a concrete scenario or real user situation
- Who experiences the problem is clear
- Impact or frequency is understood

**Clarify when:**
- Problem is abstract -> "Can you describe a real situation where this happens?"
- No clear who -> "Who runs into this problem? Describe a specific person or role."
- Solution disguised as problem -> "That sounds like a solution. What's the underlying pain?"

### Solution

**Sufficient when:**
- Proposed approach is described (even at high level)
- Key interactions or changes are understood
- It's clear what changes for the user

**Clarify when:**
- No solution yet -> "Do you have an idea of how to solve this, or should we explore options?"
- Too vague -> "Walk me through what the user would see or do differently."
- Over-specified -> "This feels like implementation detail. What's the user-facing change?"

### Scope

**Sufficient when:**
- What's included is clear
- At least one explicit no-go exists
- Scope feels achievable (not an entire product rewrite)

**Clarify when:**
- Scope keeps growing -> "We started with X, now it's X + Y + Z. Should we narrow down?"
- No boundaries -> "What's explicitly out of scope for this epic?"

## Drafting

**USE TEMPLATE:** `templates/epic.md`

### Problem Format

Describe the problem as a narrative -- a real situation, not an abstract statement. Show the person, the context, and the friction.

| Bad | Good |
|-----|------|
| "Users need better search" | "Maria manages 200+ invoices monthly. When a client calls about a specific invoice, she scrolls through pages because there's no date filter. She loses 5 minutes per lookup." |
| "The onboarding is confusing" | "New users land on the dashboard with 12 empty widgets and no guidance. 60% drop off before creating their first project." |

### Solution Format

Describe the solution as what changes for the user -- interactions, screens, behaviors. Not implementation details.

| Bad | Good |
|-----|------|
| "Add a REST endpoint with date params" | "Add a date range picker above the invoice list. Maria selects a range and results filter instantly." |
| "Implement a wizard component" | "Replace the empty dashboard with a 3-step setup flow: create project, invite team, import data." |

## Schema

7 sections matching `templates/epic.md`:

| Section | Content |
|---------|---------|
| 1. Problem | Narrative describing who has the problem, when, and the impact |
| 2. Solution | What changes for the user -- interactions and behaviors |
| 3. Scope In | What's included in this epic |
| 4. Scope Out (No-gos) | What's explicitly excluded |
| 5. Rabbit Holes | Known complexities or traps to avoid |
| 6. Acceptance Criteria | 2-5 verifiable conditions for the epic |
| 7. References | Links to PRD, Design Doc, Figma, related epics |

## Guidelines

**DO:**
- Describe problems as narratives with real people and situations
- Describe solutions as user-facing changes
- Be explicit about no-gos -- they are as important as scope
- Flag known complexities upfront in rabbit holes to prevent wasted time
- Suggest breaking large epics into multiple epics
- Place acceptance criteria here -- they validate the epic as a whole
- Link to the parent milestone when one exists

**DON'T:**
- Write problems as abstract statements
- Describe solutions with implementation details
- Leave no-gos undefined or vague
- Put acceptance criteria in issues -- they belong at the epic level

## Output

Save to: `.artifacts/docs/epic.md`
