# Output

Produce the system brief and ask the user what to do next.

## When to Use

Load after the architecture is confirmed by the user.

## System Brief

The brief consolidates everything from the session into a single structured
document. Save to `.artifacts/docs/system-brief.md`. Create the directory
if it does not exist.

**USE TEMPLATE:** `../templates/system-brief.md`

The brief is the source of truth for the design session. It is input for
the next step — not the final deliverable.

## Handoff

After saving the brief, ask directly:

> "Brief saved to `.artifacts/docs/system-brief.md`. What's next?
> - **docs-writer TDD** — technical planning for a specific component
> - **docs-writer ADR** — one decision record per major trade-off
> - **spec-driven** — start implementing a feature from this architecture
> - **Nothing for now** — brief is enough"

Wait for the user's answer. If they choose docs-writer or spec-driven,
pass the relevant section of the brief as context:

- TDD: pass the Architecture section (components, data flow, patterns)
- ADR: pass one trade-off table at a time; generate one ADR per decision
- spec-driven: pass the Architecture section and the Functional Requirements

## Quality Gate

Before delivering the brief:

- [ ] All sections are complete (no empty sections)
- [ ] Trade-off decisions reference the requirements that drove them
- [ ] Architecture diagram matches the component list
- [ ] Open questions are listed with owner or context

## Error Handling

- `.artifacts/docs/` does not exist: create it before saving
- User wants to change a decision after output: return to `trade-offs.md`
  and propagate the change through `architecture.md` before regenerating
- User chooses ADR and there are multiple decisions: generate one ADR per
  decision, ask which to start with
