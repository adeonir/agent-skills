# Refine

Restructure, shorten, or extend one app flow the user names, and write the result back to `docs/product/FLOWS.md`.

## Load first

Read [flow-model.md](../references/flow-model.md) — the rewrite changes structure, so the structure rules govern what counts as better.

Read [discovery.md](../references/discovery.md) and run its intake step — the flow arrives from the artifact or the user describes it in chat.

## Contents

- Workflow — locate, name the goal, draft, judge and keep, write back

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Locate the flow — artifact section or chat description
- [ ] Step 2: State the improvement goal, confirmed or declared
- [ ] Step 3: Draft the new happy path in wireflow notation
- [ ] Step 4: Judge against the goal; keep the dead-end register; update the connect map
- [ ] Step 5: Write back with before/after wireflows in chat

If the draft loses a hand-off, return to Step 3.
```

**Step 1. Locate.** In `docs/product/FLOWS.md`, find the named flow's section and the role it plays on the connect map. When the artifact exists, the flow's shape (errors, dead ends) comes from what it says, not recalled; when it is being described, carry the description as a claim to check — where the described path contradicts the artifact's version, surface the disagreement before rewriting.

**Step 2. Name the goal.** In one line: shorter, fewer screens, a branch added, a dead end closed, two tasks unmerged. Have the user confirm the goal — or proceed as a declared assumption they can redirect. Rebuilding a flow for the wrong goal is the cost this confirm prevents.

**Step 3. Draft the new happy path first.** Entry → screens → success exit, in wireflow notation, before touching branches — a rewrite that starts from the old branch list inherits the old shape.

**Step 4. Judge and keep.**

- **Against the goal, not eternally** — count screens, exits, and hand-offs against the stated goal; a shorter flow with a lost hand-off is a worse flow.
- **Keep the dead-end register** — every state of the old flow that survives the rewrite keeps its exit; a state dropped while a branch it served still exists is a hole.
- **Update the connect map** — the flow's inbound and outbound hand-offs are re-named where the rewrite moved them.

**Step 5. Write back.** Apply the result to the flow's section in `docs/product/FLOWS.md` (create the file from [../assets/flows-template.md](../assets/flows-template.md) when the product has none yet, carrying only this flow plus, empty, the connect map). Show the before-and-after wireflows of the changed structure in chat, with what the count of screens and dead ends did — the change should make the flow measurably better, and when a rewrite makes it longer for no structural gain, say so instead of writing it.
