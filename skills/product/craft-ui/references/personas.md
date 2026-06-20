# Personas

Five user archetypes to test an interface through. Each exposes failure modes a
single "design director" perspective would miss. Report specific red flags —
what broke for them — not generic concerns.

## When to Use

Composed by `critique.md` (the persona red-flag step). Select 2–3 personas most
relevant to the surface, walk the primary action as each, and name the exact
elements that fail. Not a direct trigger.

## 1. Impatient Power User — "Alex"

**Profile:** Expert with similar products. Expects efficiency, hates
hand-holding. Will find shortcuts or leave.

**Behaviors:** skips onboarding; looks for keyboard shortcuts; bulk-selects and
batch-edits; frustrated by unnecessary required steps; abandons if it feels slow
or patronizing.

**Test:** core task in <60s? keyboard shortcuts for common actions? onboarding
skippable? modals dismiss on Esc? a power-user path (bulk actions)?

**Red flags:** forced/unskippable onboarding; no keyboard path for primary
actions; unskippable slow animations; one-at-a-time where batch is natural;
redundant confirmations for low-risk actions.

## 2. Confused First-Timer — "Jordan"

**Profile:** Never used this kind of product. Needs guidance at every step. Will
abandon rather than figure it out.

**Behaviors:** reads instructions; hesitates at anything unfamiliar; hunts for
help; misreads jargon; takes labels literally.

**Test:** first action obvious in 5s? icons labeled? contextual help at decision
points? terminology assumes prior knowledge? clear back/undo at every step?

**Red flags:** icon-only nav, no labels; jargon without explanation; no visible
help; ambiguous next step after an action; no confirmation an action succeeded.

## 3. Accessibility-Dependent User — "Sam"

**Profile:** Screen reader (VoiceOver/NVDA), keyboard-only. May have low vision,
motor, or cognitive differences.

**Behaviors:** tabs linearly; relies on ARIA and heading structure; can't see
hover or visual-only cues; needs ≥4.5:1 contrast; may zoom to 200%.

**Test:** whole primary flow keyboard-only? all interactive elements focusable
with visible focus? meaningful alt text? contrast WCAG AA? state changes
announced (loading/success/error)?

**Red flags:** click-only with no keyboard alternative; missing/invisible focus;
meaning by color alone; unlabeled fields/buttons; time-limited actions with no
extension; custom components that break screen-reader flow.

## 4. Deliberate Stress Tester — "Riley"

**Profile:** Methodical; pushes past the happy path. Tests edge cases and
unexpected input.

**Behaviors:** tries empty/long/special-character inputs; submits emoji, RTL,
very long values; navigates backward, refreshes mid-flow, opens multiple tabs;
hunts for UI-vs-reality mismatches.

**Test:** edges (0 / 1000 items, very long text)? error states recover
gracefully? refresh mid-flow preserves state? features that look like they work
but don't? unexpected input (emoji, paste from Excel)?

**Red flags:** features that silently fail or produce wrong results; error
handling that exposes internals or leaves the UI broken; empty states with no
guidance; workflows that lose data on refresh; inconsistent behavior between
similar interactions.

## 5. Distracted Mobile User — "Casey"

**Profile:** Phone, one-handed, on the go, frequently interrupted, maybe slow
connection.

**Behaviors:** thumb only, prefers bottom-of-screen actions; interrupted and
returns later; switches apps; low patience; types as little as possible.

**Test:** primary actions in the thumb zone? state preserved on leave/return?
works on 3G? forms use autocomplete and smart defaults? touch targets ≥44×44pt?

**Red flags:** important actions at the top (unreachable by thumb); no state
persistence (progress lost on switch); large text inputs where selection would
do; heavy assets with no lazy loading; tiny or too-close tap targets.

## Selecting personas

| Surface | Personas | Why |
|---------|----------|-----|
| Landing / marketing | Jordan, Riley, Casey | first impressions, trust, mobile |
| Dashboard / admin | Alex, Sam | power users, accessibility |
| E-commerce / checkout | Casey, Riley, Jordan | mobile, edge cases, clarity |
| Onboarding | Jordan, Casey | confusion, interruption |
| Data-heavy / analytics | Alex, Sam | efficiency, keyboard nav |
| Form / wizard | Jordan, Sam, Casey | clarity, accessibility, mobile |

## Project-specific personas

When the project carries audience/brand context (a PRD, brief, or product doc),
derive 1–2 personas the five predefined ones don't cover:

```text
##### [Role] — "[Name]"
**Profile:** [2–3 traits from the project context]
**Behaviors:** [3–4 specific behaviors]
**Red flags:** [3–4 things that would alienate this user]
```

Only generate these when real context exists — don't invent audience details;
fall back to the five predefined personas.
