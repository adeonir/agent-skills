# Editing Sweeps

Focused passes that tighten existing copy without changing its voice. They support the refresh operation.

## When to Use

Loaded by the refresh workflow to improve copy already in `copy.yaml`. Each sweep targets one dimension; run them in order and loop back after edits so a later pass does not undo an earlier one. Edits enhance, they do not rewrite: preserve the core message and the voice. critique scores these same seven sweeps as judgment axes and audit pulls the readability checks; in those modes the sweeps grade rather than edit.

## The Seven Sweeps

Run per `copy.yaml` part, one dimension at a time. Hold the confirmed intent throughout: its constraints are gates, not suggestions. Do not improve a sweep by violating a required tone or using a forbidden technique.

1. **Clarity:** can the reader understand it at once? Kill confusing structures, unclear pronouns, jargon, sentences doing too much.
2. **Voice consistency:** does it sound the same throughout? Smooth shifts between formal and casual; keep the established voice. *Refresh never changes the voice; that is a different job.*
3. **Reader value:** does each part serve the reader's goal? For persuasive copy, bridge features to benefits ("…which means…"); for product/UX copy, make the next step clear; for informational copy, connect facts to the reader's question; for brand/editorial copy, make the point of view earn attention.
4. **Prove it:** are claims about capability, quality, or outcomes backed? Attach numbers, named proof, or soften the claim. Factual descriptions need accurate context. See proof hierarchy in [voice.md](voice.md).
5. **Specificity:** concrete over vague. "Save time" → "Save 4 hours a week"; "many customers" → "2,847 teams". Cut what cannot be made specific.
6. **Reader pull:** does the copy create the right reason to continue? Use emotional texture for conversion or brand/editorial copy, relevance for informational copy, and reduced friction for product/UX copy. Never manipulate.
7. **Reader confidence:** can the reader continue with the right level of trust? For conversion copy, check objections and risk signals near the decision; for product/UX copy, check the next step and recovery path; for informational copy, check context and caveats.

After the final sweep, run back through all seven once more.

## Quick-Pass Checks

For lighter edits when a full seven-sweep is overkill.

**Cut weak words:** very, really, extremely, just, actually, basically, in order to (→ to), that (often), things / stuff.

**Replace weak with strong:**

| Weak | Strong |
|------|--------|
| utilize | use |
| facilitate | help |
| implement | set up |

**Sentence-level:** one idea per sentence; vary length; front-load the important part; usually ≤25 words.

**Paragraph-level:** one topic; short (2-4 sentences for web); strong opener; white space for scannability.

## Plain English

Swap pompous words for plain ones.

| Complex | Plain |
|---------|-------|
| commence | start |
| ascertain | find out |
| due to the fact that | because |
| in the event of | if |
| prior to | before |
| sufficient | enough |
| terminate | end, stop |
| approximately | about |

Delete filler phrases outright: "a total of", "at this moment in time", "of course", "the fact of the matter is", "needless to say".

For dead marketing adjectives (passionate, world-class, synergy, …) see the dead-words catalogue in [anti-patterns.md](anti-patterns.md).

## Common Problems

- **Wall of features** → add "which means…" to bridge to benefits when the surface explains value; otherwise group the features by the reader's task or question.
- **Corporate speak** → "How would a human say this?" and use those words.
- **Weak conversion opening** → lead with the reader's problem or outcome, not history. For informational copy, lead with the subject, context, or fact the intent requires.
- **Buried next step** → make the next step obvious and early when the surface requires one.
- **Generic claim** ("we help businesses grow") → specify who, how, how much.
- **Hollow structure** ("it wasn't a detour, it was an evolution") → strip the false antithesis and say the real thing; thin out em-dashes used for drama. See dead structures in [anti-patterns.md](anti-patterns.md).
