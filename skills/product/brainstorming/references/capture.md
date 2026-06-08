# Capture -- Save the Direction

Persist the chosen direction as a structured artifact. Single
project-level file. Pivot existing entries rather than spawning new
files.

## When to Use

After the user approves a direction in converge. Loaded as the final
phase.

## Workflow

### Step 1: Review

Verify the artifact before saving:

- [ ] No unresolved TBDs that block the chosen direction
- [ ] No contradictions between constraints and chosen alternative
- [ ] Scope is focused enough to act on (one direction, not three)
- [ ] Trade-offs are explicit (nothing hidden to make the choice look better)
- [ ] Open questions are genuine unknowns, not laziness
- [ ] No implementation detail or codebase symbols (file paths, function or class names) — the artifact stays at the problem-and-direction level

If issues found: fix inline before saving. Don't deliver a flawed
artifact.

### Step 2: Detect Existing File

Save the artifact to `docs/product/brainstorm.md` (single
project-level file).

If the file already exists, treat the current run as a pivot or
revision instead of a fresh write:

- Ask the user: pivot the existing direction, or replace from scratch?
- **Pivot** — keep Context/Constraints/Success Criteria as-is unless
  discovery surfaced changes, update Alternatives Considered and
  Decision, append an entry to Revision History with the date and what
  changed.
- **Replace** — confirm with the user that the prior direction is
  being abandoned (not pivoted), then rewrite the file fresh,
  resetting Revision History.

Always bump `updated:` to today's date and increment `revisions:` on
any change.

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
revisions: 0
sources: []
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

{Append a dated entry on every pivot. Omit this section on the
initial capture.}

### {{YYYY-MM-DD}} — Pivot

**From:** {{prior chosen direction}}
**To:** {{new chosen direction}}
**Trigger:** {{what changed — new evidence, failed assumption, user
request, etc.}}
**Trade-offs reassessed:** {{short note on what shifted in the
trade-off picture}}
````
