# Discovery

Establishes planning context and routes to the right mode.

## When to Use

Load at the start of every blueprint operation — before any mode runs,
never invoked directly.

## Workflow

### Step 1: Check Existing Context

Look for:

- an existing `docs/design/blueprint.md` — a prior layout plan (signals brownfield)
- a wireframe on hand: sketch, mockup, screenshot, or a described layout
- a brief, PRD, or description the user provides — intent and surfaces
- existing content the user points to — arrange real blocks against it when given

Read what is found for surfaces, primary actions, and flow. Skip to the
relevant mode.

### Step 2: Classify Field

Infer from context — do not ask explicitly:

- **greenfield** — no existing plan → create a fresh layout from conversation.
- **brownfield** — a plan or a wireframe exists → validate it for coherence,
  then optionally roll into create for missing decisions.

### Step 3: Route to Operation

| Intent | Reference |
|--------|-----------|
| Author a fresh layout plan | [create.md](create.md) |
| Check a wireframe or existing plan | [validate.md](validate.md) |

### Step 4: Fill Gaps

When context is missing, ask one question at a time: which surfaces or screens
the product has, the primary action per surface, and any flow between them.
Derive topics from the conversation — do not force a project type or a fixed
surface set.
