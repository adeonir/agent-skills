# Critique

Judge a chosen variant before implementation — a direction verdict, not a defect
list. Critique is coupled to render: it evaluates one rendered variant and feeds
refinements back into the render tune loop. Perceptual judgment; non-mutating.

## When to Use

- A variant has been picked in render and needs a direction verdict before build
- User asks whether a design reads as distinctive / trustworthy or as AI slop
- User wants heuristic scoring, cognitive-load, or persona red flags on a variant
- Looping with render: critique → tune verb → re-render → critique again

Reads the chosen variant HTML in `.artifacts/` (render's output) and judges it.
It writes nothing — the verdict is the deliverable.

Composes:

- [brand.md](../references/brand.md) / [product.md](../references/product.md) — posture (read the matching one) first
- [design-thinking.md](../references/design-thinking.md) — visual direction, color strategy, slop test
- [heuristics.md](../references/heuristics.md) — Nielsen heuristics + 0–4 scoring + visual laws
- [cognitive-load.md](../references/cognitive-load.md) — load checklist, working-memory rule, overload patterns
- [personas.md](../references/personas.md) — the five archetypes to test through
- [anti-patterns.md](../references/anti-patterns.md) — perceptual failure modes
- [scoring.md](../references/scoring.md) — severity, score bands, report template

## Workflow

### Step 1: Fix the register

Name the register and surface, then read the matching [brand.md](../references/brand.md)
or [product.md](../references/product.md).
Brand judges for distinctiveness; product judges for earned familiarity. The
register sets every bar below — do not score before it is named.

### Step 2: Slop verdict (two altitudes)

Start here, honestly. Two passes:

1. **Category reflex** — could someone name the category and guess the whole
   look (theme + palette + layout) from the category alone? That is the
   first-order AI default.
2. **Anti-reference reflex** — name the aesthetic lane the variant is actually
   in. Could someone guess that lane from "category plus the obvious
   anti-references"? That is the trap one tier deeper. (See the slop test in
   [design-thinking.md](../references/design-thinking.md).)

A variant that fails either altitude has no point of view yet — say so plainly
before any number softens it.

### Step 3: Score the heuristics

Score all 10 Nielsen heuristics 0–4 — definitions and the 0–4 criteria per
heuristic are in [heuristics.md](../references/heuristics.md), aggregate bands in
[scoring.md](../references/scoring.md). Present as a table with a per-row key issue
and the total /40. Be honest — most real interfaces land 20–32.

### Step 4: Cognitive load

Walk the 8-item checklist in [cognitive-load.md](../references/cognitive-load.md);
count failures (0–1 low, 2–3 moderate, 4+ critical). Flag any decision point with
more than 4 simultaneous options — working memory holds ≤4.

### Step 5: Persona red flags

Select 2–3 personas by surface from [personas.md](../references/personas.md) and
walk the primary action as each. Report the exact elements that fail them — not
generic descriptions. personas.md carries the five archetypes, the
selection-by-surface table, and a template for project-specific personas.

As you walk each path, trace the **emotional journey** — where it dips
(confusion, friction, anxiety) and whether the high-stakes moments (payment,
deletion, irreversible submits) offer reassurance. Peak-end weighs the worst
moment and the last one most, so one unhandled valley colours the whole read.

### Step 6: Direction verdict and refinements

Write the verdict using the template in [scoring.md](../references/scoring.md):
slop verdict, the heuristic table and total, the priority issues (P0–P3), and
2–3 strengths. Then map each priority issue to a render tune verb so the loop
can continue — verb definitions live in [tune.md](../references/tune.md)
(motion verbs in [motion.md](../references/motion.md) /
[overdrive.md](../references/overdrive.md)); render invokes them:

- reads safe / undifferentiated → `bolder` or a committed color strategy
- noisy / over-decorated → `quieter` or `distill`
- flat, no feedback → `animate` (state) or `delight` (earned moments)
- thin on edge states → `harden` (preview empty / loading / error)

Close with 2–3 questions that open the next iteration instead of only grading
this one — "What would a more confident version of this look like?", "Does this
need to feel this complex?", "What if the primary action were twice as prominent?"
They aim render's next pass.

Hand the refinements back to render; re-render and re-critique until the
direction holds. Critique never edits the variant itself.

## Guidelines

- Name the register before scoring — the bar is meaningless without it
- Lead with the slop verdict; let the score support it, not replace it
- Be specific: "the submit button", not "some elements"; name what fails and why
- Prioritise ruthlessly — if everything is P0, nothing is
- Loop through render's tune verbs; critique judges, render re-renders

## Error Handling

- No chosen variant yet: ask the user to pick one in render first
- Variant renders blank or broken: report it as a render defect, not a design verdict
- Register ambiguous (a surface that straddles brand and product): judge the surface by the role it plays, per brand.md / product.md
- User asks to apply a fix: redirect — critique judges and refines via re-render; a permanent change is the owning skill's job
