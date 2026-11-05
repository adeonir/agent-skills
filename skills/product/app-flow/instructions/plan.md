# Plan

Plan the app flows for a product and write them into `docs/product/FLOWS.md`. Handle a from-scratch product, a prose description, or an upstream product doc.

## Load first

Read [flow-model.md](../references/flow-model.md) — vocabulary, wireflow notation, and structure rules before drafting anything.

Read [discovery.md](../references/discovery.md) and run its steps — intake shape, hybrid interview, what must be settled before flows exist.

## Contents

- Workflow — discover, list the flows, draft per flow, connect, write

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Settle platform, tasks, priority flows, entry points — Load first refs
- [ ] Step 2: List the flows, one per task, mark the priority ones
- [ ] Step 3: Draft happy path per flow, in wireflow notation
- [ ] Step 4: Branch error, cancel, timeout per flow — each with its exit
- [ ] Step 5: Name every hand-off on the connect map
- [ ] Step 6: Write docs/product/FLOWS.md from the template

If a draft reveals an unmapped task, return to Step 1.
```

**Step 1. Discover.** Settle: the platform in the product's own words (a website, a mobile app, a desktop client — whatever the intake names), the tasks users perform, which 1–2 flows carry the value, and where a first-time user enters versus a returning one. Do not draft off settlement shortcuts — a flow guessed from the task name opens the wrong screens. When the intake is a product doc, treat it as a claim, not authority: where its feature list names no user task, or two sections imply contradictory paths, surface the disagreement instead of forcing a flow around it.

**Step 2. List the flows.** One per task, unmerged — split anything covering two tasks (flow-model's type table shows the shapes). Mark the 1–2 priority ones.

**Step 3. Happy path first per flow.** Entry → screens → success exit, in wireflow notation.

**Step 4. Branch second.** Error, cancel, timeout — each branch carries its own exit into a known screen. Enumerate the flow's dead ends explicitly.

**Step 5. Connect.** Name every hand-off: which flow ends where, which flow receives it. A flow that ends with no named receiver is a gap to flag, not to smooth over.

**Step 6. Write.** Create `docs/product/FLOWS.md` using [../assets/flows-template.md](../assets/flows-template.md) — flexible: marks one flow section, the connect map, and the dead-end register; carry those across every flow, in priority order. Detail by priority: full branch coverage on the priority flows, happy-path only on the rest. State at the end which flows are priority-complete and which are happy-path-only, so a later audit knows what to press on.
