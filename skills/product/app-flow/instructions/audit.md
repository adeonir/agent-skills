# Audit

Examine a product's app flows for structural defects — dead ends, unmerged steps, broken hand-offs — and report findings in chat. The audit writes no artifact; it reports.

## Load first

Read [flow-model.md](../references/flow-model.md) — the structure rules are the audit's rubric.

Read [discovery.md](../references/discovery.md) and run its intake step — the flows may arrive as `docs/product/FLOWS.md`, as prose, or as a codebase that can be read for screens.

## Contents

- Workflow — take the flows in, check the rubric, rank, report

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Take the flows in — artifact, description, or code
- [ ] Step 2: Check each flow against the rubric, priority flows first
- [ ] Step 3: Rank findings by impact, with evidence per finding
- [ ] Step 4: Report with the one-line verdict — no file edited

If a finding exposes an unstated flow boundary, return to Step 1.
```

**Step 1. Take the flows in.** When the artifact exists, read every flow section in it, including the connect map and the dead-end register — the audit reads what was written, not what the conversation adds. When the user describes flows in chat, build the same mental model first and confirm the description back in one sentence before judging it. When the product is code, explore instead of asking: read the routing, screen list, and navigation state to extract the flows that actually run — extract the flow, not the code; implementation detail states evidence for a finding but never becomes new content in the report. An upstream doc or a described flow enters as a claim, not authority: a path the intake asserts exists is checked against the structure rules, and a contradiction is surfaced, not inherited.

**Step 2. Check the rubric.** In priority order — priority flows first, non-priority flows checked only for consistency with the same rules. The findings:

- **Dead end** — a screen or state whose only outcome is neither success nor a return (error, empty, denied).
- **Merged flows** — one flow covering two tasks; each task deserves its own diagram and its own metric.
- **Broken hand-off** — a flow ends with no named receiver, or connects to a flow from a state that flow does not cover.
- **Action as step** — a step drawn for an action ("pay") instead of the screen it happens on.
- **Branch before happy path** — the happy path cannot be read as its own line.
- **Priority without detail** — a flow marked most valuable with nothing but its happy path drafted.

**Step 3. Rank.** By impact — a broken hand-off on a priority flow outranks a merged flow on a settings one. Each finding states the flow, the rule it breaks, and evidence of where the path breaks down.

**Step 4. Report.** Print the ranked findings in chat and end with a one-line verdict on which 1–2 fixes would change the product most. Do not edit `docs/product/FLOWS.md` or the flows themselves — the user decides what happens to the findings.
