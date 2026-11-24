# Audit

Examine a product's app flows for structural and notation defects — dead ends, unmerged steps, broken hand-offs, labels against the notation — and report findings in chat, writing no artifact.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Take the flows in — artifact, description, or code
- [ ] Step 2: Check each flow against the rubric, priority flows first
- [ ] Step 3: Rank findings — four named fields each, evidence required
- [ ] Step 4: Report with the one-line verdict — no file edited

If a finding exposes an unstated flow boundary, return to Step 1.
```

**Step 1. Take the flows in.** Load [flow-model.md](references/flow-model.md) · the structure rules and wireflow notation, and [discovery.md](references/discovery.md) · the intake. When the artifact exists, read every flow section in it, including the connect map and the dead-end register — the audit reads what was written, not what the conversation adds. When the user describes flows in chat, build the same mental model first and confirm the description back in one sentence before judging it. When the product is code, explore instead of asking: read the routing, screen list, and navigation state to extract the flows that actually run — extract the flow, not the code; implementation detail states evidence for a finding but never becomes new content in the report.

**Step 2. Check the rubric.** In priority order — priority flows first, non-priority flows checked only for consistency with the same rules. The findings:

- **Dead end** — a screen or state whose only outcome is neither success nor a return (error, empty, denied).
- **Merged flows** — one flow covering two tasks; each task deserves its own diagram and its own metric.
- **Broken hand-off** — a flow ends with no named receiver, or connects to a flow from a state that flow does not cover.
- **Action as step** — a step drawn for an action ("pay") instead of the screen it happens on.
- **Branch before happy path** — the happy path cannot be read as its own line.
- **Notation** — a label, condition, or state change drawn against the wireflow notation rules: a label that carries a rule or "X or not X", a condition repeated across paths with no diamond, a domain state in the exit circle.
- **Priority without detail** — a flow marked most valuable with nothing but its happy path drafted.

**Step 3. Rank.** By impact — a broken hand-off on a priority flow outranks a merged flow on a settings one. Every finding carries the four named fields — **flow** / **rule** / **evidence** / **severity** (high, medium, low) — and a finding without an evidence line is dropped before ranking, not ranked with a hole. The evidence names where the path breaks down: the screen, state, hand-off, or arrow label.

**Step 4. Report.** Print the ranked findings in chat and end with a one-line verdict on which 1–2 fixes would change the product most. Do not edit `docs/product/FLOWS.md` or the flows themselves — the user decides what happens to the findings.
