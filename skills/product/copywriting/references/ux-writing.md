# UX Writing

The clarity discipline for copy — diagnose what makes a line unclear, then
rewrite it so the reader understands at once and knows what to do. The method and
principles hold for every line; microcopy (errors, labels, states) is one area,
where clarity is hardest. Craft, applied during write and refresh — alongside
[voice.md](voice.md) and [editing-sweeps.md](editing-sweeps.md), not on top of
them.

## When to Use

Loaded by the write and refresh workflows to keep copy clear and effective, and
by audit for the microcopy, i18n, and terminology checks.
Composes with [voice.md](voice.md) (voice, proof) and
[editing-sweeps.md](editing-sweeps.md) (tightening passes for persuasive prose) —
this file does not repeat them. It owns the clarity method and the microcopy
craft those two do not cover.

## The Method

Unclear copy creates friction — confusion, errors, abandonment; clear copy gets
the reader through. Four moves on any line:

1. **Assess** — name what makes it fail: jargon, ambiguity, passive voice, wrong
   length, assumed knowledge, missing context, tone mismatch.
2. **Plan** — the primary message (the ONE thing to land), the action (what to do
   next), the tone (by moment, below), the constraints (length, space, locale).
3. **Improve** — rewrite by the principles below.
4. **Verify** — comprehension (clear without context?), actionability (knows the
   next step?), brevity (as short as stays clear?), consistency (matches terms
   elsewhere?), tone (right for the moment?).

## Clarity Principles

Every line, persuasive or functional:

- **Specific** — "Your work email", not "Enter value".
- **Concise** — cut words that carry nothing; never cut clarity.
- **Active** — "Save changes", not "Changes will be saved".
- **Human** — "Something went wrong on our end", not "System error encountered".
- **Tell the reader what to do**, not only what happened.
- **Consistent** — one term per concept; don't vary for variety.

## Microcopy

One area of clarity — the interface text that carries a task, where vague copy
hurts most. Write each by what the reader needs at that moment:

- **error** — what happened, why, how to fix; name the situation (network,
  server, permission, validation) so the fix fits. *"Invalid input" → "Email needs
  an @ symbol. Try name@example.com."* Never blame the user; never a bare code.
- **form label** — specific, format by example, the why when not obvious. *"Enter
  value" → "Your work email."* Labels, not placeholder-only (they vanish on type).
- **button** — verb + object, the outcome. *"OK / Submit" → "Save changes /
  Create account."* Destructive names the act: *"Delete 5 items."*
- **help / tooltip** — add value, answer the implicit question; don't restate the
  label.
- **empty state** — acknowledge, explain the value of filling it, give the
  action. *"No items" → "No projects yet. Create your first to get started."*
- **success** — confirm what happened and what is next.
- **loading** — set the expectation. *"Loading…" → "Analyzing your data — about
  30 seconds."*
- **confirmation** — name the action and its consequence; specific button labels.
  Prefer undo over confirming low-stakes actions.
- **navigation** — specific, user-language labels with clear hierarchy.

## Tone by Moment

Voice is the constant personality (set in [voice.md](voice.md)); **tone** shifts
with the reader's state:

| Moment | Tone |
|--------|------|
| Success | brief, celebratory — "Done. Your changes are live." |
| Error | empathetic, helpful — "That didn't work. Here's what to try…" |
| Loading | reassuring — "Saving your work…" |
| Destructive confirm | serious, plain — "Delete this? This can't be undone." |

Never use humor in an error — the reader is already stuck.

## Writing for Accessibility

Author the **text** assistive tech reads; whether a control requires it is a
build concern, out of scope here.

- **Link text** stands alone out of context: *"Click here" → "View pricing
  plans."*
- **Alt text** states the information, not the picture: *"Chart" → "Revenue up
  40% in Q4."* Decorative images take empty alt.
- **Icon-button label** names the action the icon performs.

## Writing for Translation

Author strings that survive other languages:

- **Budget for expansion and contraction** — German runs ~30% longer, Finnish
  30–40%, and some languages contract (Chinese ~30% shorter at similar width);
  write so the layout survives either way. The layout that holds it is a build
  concern.
- **Keep variables separate** — *"You have 3 new messages" → "New messages: 3."*
- **One sentence, one string** — never concatenate fragments.
- **No abbreviations** — *"5 mins ago" → "5 minutes ago."*
- **Give context** — note where a string appears so a translator can place it.

## Terminology Consistency

Pick one term per concept and hold it — varying it reads as different features.

| Drifting | Consistent |
|----------|------------|
| Delete / Remove / Trash | Delete |
| Settings / Preferences / Options | Settings |
| Sign in / Log in / Enter | Sign in |

Pick the truthful term, not just the consistent one — *Delete* (permanent) is not
*Remove* (recoverable); collapsing them hides a real difference from the reader.

Keep a small per-project glossary and enforce it across every line.

## Anti-Redundancy

Say it once. If the heading explains it, the intro is redundant; if the button is
clear, do not re-explain it. Cut the second instance, keep the strongest.

## Guidelines

- Run the method on any line that reads unclear — persuasive or functional.
- Be specific, active, human; tell the reader what to do, not only what happened.
- Match the tone to the moment; hold voice and register across all of them.
- Author label, alt, and aria text as content; leave the requirement to the build.
- Don't repeat [voice.md](voice.md) or [editing-sweeps.md](editing-sweeps.md) —
  cross-link them for voice, proof, and prose tightening.
