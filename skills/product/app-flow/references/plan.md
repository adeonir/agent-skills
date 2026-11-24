# Plan

Plan the app flows for a product and write them into `docs/product/FLOWS.md`. Handle a from-scratch product, a prose description, or an upstream product doc.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Load flow-model and discovery, then settle platform, tasks, priority flows, entry points
- [ ] Step 2: List the flows, one per task, mark the priority ones
- [ ] Step 3: Draft happy path per flow, in wireflow notation
- [ ] Step 4: Fill the dead-end register and rules per flow — all template categories, exits included
- [ ] Step 5: Name every hand-off on the connect map
- [ ] Step 6: Write docs/product/FLOWS.md from the template

If a draft reveals an unmapped task, return to Step 1.
```

**Step 1. Discover.** Load [flow-model.md](flow-model.md) · the vocabulary, wireflow notation, and structure rules, and [discovery.md](discovery.md) · the intake and the interview. Settle: the platform in the product's own words (a website, a mobile app, a desktop client — whatever the intake names), the tasks users perform, which 1–2 flows carry the value, and where a first-time user enters versus a returning one. When the intake is an upstream product doc, read it for context only: its section numbers, doc codes, and framing never cross into `FLOWS.md`. Do not draft off settlement shortcuts — a flow guessed from the task name opens the wrong screens.

**Step 2. List the flows.** One per task, unmerged — split anything covering two tasks (flow-model's type table shows the shapes). Mark the 1–2 priority ones.

**Step 3. Happy path first per flow.** Entry → screens → success exit, in wireflow notation.

**Step 4. Fill the dead-end register and rules.** Enumerate the five categories the template carries — error, cancel, timeout, empty state, denied — per flow. For each category that applies, draw the branch in wireflow notation and give it its exit into a known screen; for each that does not, mark `n/a` in the register. A state missing from the register is an unexamined category, not an oversight to smooth over. Record the business rules the flow enforces in its rules field, or `none`.

**Step 5. Connect.** Name every hand-off: which flow ends where, which flow receives it. A flow that ends with no named receiver is a gap to flag, not to smooth over.

**Step 6. Write.** Create `docs/product/FLOWS.md` using [../assets/flows-template.md](../assets/flows-template.md) — flexible: marks one flow section, the connect map, the dead-end register, and the rules field; carry those across every flow, in priority order. Detail by priority: full branch coverage on the priority flows, happy-path only on the rest. State at the end which flows are priority-complete and which are happy-path-only, so a later audit knows what to press on.
