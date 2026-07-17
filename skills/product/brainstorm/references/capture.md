# Capture -- Save the Direction

Persist the chosen direction as a structured artifact. Single project-level file. Pivot or validate existing entries rather than spawning new files.

## When to Use

After the user approves a direction and it survives the grill in converge. Loaded as the final phase.

## Workflow

### Step 1: Review

Verify the artifact before saving:

- [ ] No unresolved TBDs that block the chosen direction
- [ ] No contradictions between constraints and chosen alternative
- [ ] Scope is focused enough to act on (one direction, not three)
- [ ] Trade-offs are explicit (nothing hidden to make the choice look better)
- [ ] Open questions are genuine unknowns, not laziness
- [ ] No implementation detail or codebase symbols (file paths, function or class names) — the artifact stays at the problem-and-direction level

If issues found: fix inline before saving. Don't deliver a flawed artifact.

### Step 2: Detect Existing File

Save the artifact to `docs/product/brainstorm.md` (single project-level file).

If the file already exists, compare the chosen direction against the existing `## Decision`:

- **Validated** — the chosen direction matches the existing Decision. Do not ask pivot-or-replace. Refresh Alternatives Considered with any new challengers, then append a `— Validated` entry to Revision History recording what the grill attacked and why the direction survived.
- **Direction changed** — ask the user: pivot the existing direction, or replace from scratch?
  - **Pivot** — keep Context/Constraints/Success Criteria as-is unless discovery surfaced changes, update Alternatives Considered and Decision, append a `— Pivot` entry to Revision History.
  - **Replace** — confirm with the user that the prior direction is being abandoned (not pivoted), then rewrite the file fresh; Revision History resets to a single `— Replaced` entry recording the abandoned direction and the reason, so the abandonment leaves a trace.

Always bump `updated:` to today's date and increment `revisions:` on any change.

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
revisions: 0
---

# Brainstorm: {{Project or Direction Title}}

## Context

{{Summary of motivation, current state, and timing from discovery}}

## Constraints

### Hard Constraints

- {{Non-negotiable boundary}}

### Soft Constraints

- {{Preference that can flex}}

## Success Criteria

- {{How the direction will be evaluated}}

## Alternatives Considered

- **{{Chosen Name}}** — selected (rationale in Decision below)
- **{{Alternative Name}}** — rejected: {{one-line reason}}
- **{{Alternative Name}}** — rejected: {{one-line reason}}
- **{{Alternative Name}}** — rejected: {{one-line reason}}

{Add one line per alternative explored. Keep rejected reasons concrete
and concise — tie them back to constraints or success criteria.}

## Decision

**Chosen Direction:** {{name of chosen alternative}}

**Why this over the others:** {{2-3 sentences linking to criteria and
naming the deciding factor against the strongest rejected option}}

**Trade-offs Accepted:**

- {{what was given up and why it is acceptable}}

**Key Assumption:** {{what must hold for this direction to work}}

## Open Questions

- [ ] TBD: {{question that needs answering before proceeding}}

## Revision History

{Append a dated entry on every pivot, validation, or replace, using
the matching format below. Omit this section on the initial capture.
On replace, the `— Replaced` entry is the one entry the reset keeps.}

### {{YYYY-MM-DD}} — Pivot

**From:** {{prior chosen direction}}
**To:** {{new chosen direction}}
**Trigger:** {{what changed — new evidence, failed assumption, user
request, etc.}}
**Trade-offs reassessed:** {{short note on what shifted in the
trade-off picture}}

### {{YYYY-MM-DD}} — Validated

**Direction:** {{unchanged chosen direction}}
**Grilled against:** {{what the grill attacked — the key assumption,
or every assumption on deep}}
**Survived because:** {{why the direction held; name the strongest
challenger and why it lost}}

### {{YYYY-MM-DD}} — Replaced

**Abandoned:** {{prior chosen direction}}
**Reason:** {{why the direction was dropped rather than pivoted}}
````
