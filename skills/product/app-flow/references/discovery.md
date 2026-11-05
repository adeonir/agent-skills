# Discovery — Intake and Interview

Classify what the user brought and settle what flows need before drafting, auditing, or rewriting. Shared intake for all three jobs.

## When to Use

At the start of any `app-flow` job, before flow work begins, to know what the user brought and what is still unknown.

## Entry Detection

Classify the intake from what the user brought:

- **Prose** — an app described in a sentence or a paragraph, no document.
- **Product doc** — a PRD, feature brief, or similar upstream artifact on disk.
- **Artifact** — `docs/product/FLOWS.md` from a previous run.
- **Code** — a product described as a codebase; when the question about current state can be answered by reading the code, explore it instead of asking, and state what was found before moving on — as in "the routing shows 9 screens with no route back from the payment result; match that?".

Macro state of an existing app and the presence of the artifact decide the entry; never ask for what an exploration or a read settles.

## Interview

Hybrid: infer what the intake already settles, ask only what would change a branch in the flow work. State the read as a proposed interpretation the user confirms or redirects — never a cold open-ended question.

**Proposed interpretation:** open with the read — "Flows look like signup, payment, and booking, with checkout carrying the value — right?" — and end the turn on the invite.

**Carry a recommendation:** every question pairs with a recommended answer — "Should the flow start on first-open or on the notification deep link? I'd map both, first-open first."

**Batch only independent, low-stakes questions** — 2–3 at a time. A dependent question waits for its own turn. Where confidence is high, declare the assumption instead: "Assuming mobile, since the doc names it — correct anything wrong" — stated for correction, never silent.

**Summarize before advancing:** each settled topic is confirmed in a line before the next begins.

## What must be settled

The flow work cannot start without:

1. **Platform** — the kind of surface the app ships on, named in the product's own words (a website, a mobile app, a desktop client, a PWA — whatever the intake says); it shapes screens and entry patterns.
2. **Tasks** — the list of things users do, one flow per task.
3. **Priority** — which 1–2 flows carry the value; detail follows priority.
4. **Entry** — where a first-time user enters vs. a returning one.

The user's corrections through the interview overrule the intake in every case, and unsettled points are carried to the artifact as TBD, not invented constraints.
