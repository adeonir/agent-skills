# Discovery

Establishes planning context and routes to the right mode.

## When to Use

Load at the start of every blueprint operation — before any mode runs,
never invoked directly.

## Workflow

### Step 1: Check Existing Context

Look for:

- an existing `docs/design/blueprint.md` — a prior layout plan
- a wireframe on hand: sketch, mockup, screenshot, or a described layout
- a brief, PRD, or description the user provides — intent and surfaces
- existing content the user points to — arrange real blocks against it when given

Read what is found for surfaces, primary actions, and flow. Skip to the
relevant mode.

### Step 2: Route by Intent

Infer from what the user wants — do not ask explicitly:

| Intent | Reference |
|--------|-----------|
| Author or edit a layout plan (fresh, or patch an existing one) | [create.md](create.md) |
| Check a wireframe or existing plan for coherence | [validate.md](validate.md) |

### Step 3: Fill Gaps

When context is missing, ask one question at a time: which surfaces or screens
the product has, the primary action per surface, and any flow between them.
Derive topics from the conversation — do not force a project type or a fixed
surface set.
