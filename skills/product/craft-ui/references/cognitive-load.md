# Cognitive Load

The total mental effort an interface demands. Overloaded users make mistakes, get frustrated, and leave. The checklist, the working-memory limit, and the common overload patterns a critique weighs.

## When to Use

Composed by `critique.md` (the cognitive-load step) to score how much the interface makes the user think. Not a direct trigger.

## Three types of load

- **Intrinsic** — complexity inherent to the task. Can't be eliminated, only structured: break into steps, give scaffolding (templates, defaults), disclose progressively, group related decisions.
- **Extraneous** — effort caused by bad design. **Eliminate ruthlessly** — pure waste. Confusing navigation, unclear labels, visual clutter, inconsistent patterns, unnecessary steps.
- **Germane** — effort spent building understanding. *Good* load; it leads to mastery. Support it with progressive disclosure, consistent patterns, confirming feedback, learn-by-doing onboarding.

## The checklist

Evaluate against these 8 — count the failures:

- [ ] **Single focus** — primary task free of competing elements
- [ ] **Chunking** — information in digestible groups (≤4 per group)
- [ ] **Grouping** — related items visually grouped (proximity, border, shared bg)
- [ ] **Visual hierarchy** — the most important thing is obvious at a glance
- [ ] **One thing at a time** — one decision before the next
- [ ] **Minimal choices** — ≤4 visible options per decision point
- [ ] **Working memory** — no need to carry info from a previous screen
- [ ] **Progressive disclosure** — complexity revealed only when needed

**Scoring:** 0–1 failures = low load (good); 2–3 = moderate (address soon); 4+ = high (critical fix).

## The working-memory rule

Humans hold **≤4 items** in working memory at once (Miller's Law, revised by Cowan 2001). At any decision point, count the distinct options/actions/pieces a user must consider simultaneously:

- **≤4** — within limits, manageable
- **5–7** — pushing it; group or disclose progressively
- **8+** — overloaded; users skip, misclick, or abandon

Applied: ≤5 top-level nav items; ≤4 fields per form group before a break; 1 primary + 1–2 secondary actions (rest in a menu); ≤4 key metrics without scrolling; ≤3 pricing tiers.

## Common overload patterns

1. **Wall of options** — 10+ choices, no hierarchy → group, highlight a recommended one, disclose progressively.
2. **Memory bridge** — must remember step 1 to finish step 3 → keep context visible, or repeat it where needed.
3. **Hidden navigation** — must build a mental map → always show location (breadcrumbs, active states, progress).
4. **Jargon barrier** — domain language forces translation → plain language; define unavoidable terms inline.
5. **Visual noise floor** — everything the same weight, nothing stands out → one primary, 2–3 secondary, the rest muted.
6. **Inconsistent pattern** — similar actions behave differently → standardize; same action type = same UI.
7. **Multi-task demand** — read + decide + navigate at once → sequence the steps.
8. **Context switch** — jump across screens/tabs to gather info for one decision → co-locate what each decision needs.
