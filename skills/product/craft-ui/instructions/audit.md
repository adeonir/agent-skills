# Audit

Judge a running production UI for quality defects after implementation — a
prioritized P0–P3 report, not a fix. Audit is independent of render: it works on
any build. Quality-only and non-mutating — it documents defects, never applies
them.

## When to Use

- A shipped or running UI needs a pre-ship quality pass
- User asks for an accessibility, performance, responsive, or theming audit
- User asks "is this production-ready?" or wants a defect report on a live screen
- The polish pass before release — surface what is wrong, ranked by impact

Inputs degrade gracefully — only the running UI is required:

- **Running UI** (required) — the live screen, or a screenshot of it
- **Source** (optional) — enables deeper technical and markup checks

Composes:

- [brand.md](../references/brand.md) / [product.md](../references/product.md) — set the bar (read the matching one)
- [web-standards.md](../references/web-standards.md) — technical rubric (a11y, theming, forms)
- [performance.md](../references/performance.md) — perf diagnosis + Core Web Vitals measurement
- [color.md](../references/color.md) — palette coherence, harmony, orphan accents
- [layout.md](../references/layout.md) — hierarchy, hero composition, spacing, depth
- [motion.md](../references/motion.md) — the animate gate, timing, reduced-motion
- [anti-patterns.md](../references/anti-patterns.md) — perceptual failure modes
- [scoring.md](../references/scoring.md) — severity, bands, report template

## Scope

Audit is **quality-only**. It checks whether the UI is accessible, performant,
responsive, themed consistently, and free of AI-slop tells. It does **not** check
conformance to a design system or token source — whether a build matches its
intended tokens is a separate concern craft-ui does not own. Audit judges the
UI on its own merits, as a user meets it.

## Workflow

### Step 1: Infer the surface and register

A standalone audit has no layout or content plan to read the surface from. Infer
it from the running UI (a dashboard, a checkout, a landing page), or ask the
user. Set the register from `PRODUCT.md`'s default plus the surface convention
(landing/marketing = brand, dashboard/app = product), falling back to the running
UI or the user; then read the matching [brand.md](../references/brand.md)
or [product.md](../references/product.md) — the bar differs for brand vs product.

When `PRODUCT.md` is present, also read its declared anti-references as context
for the anti-pattern verdict below — read only; audit never edits `PRODUCT.md`.

### Step 2: Score five dimensions

Score each 0–4 (bands in [scoring.md](../references/scoring.md)); total /20.

1. **Accessibility** — contrast, ARIA, keyboard path, semantic HTML, alt text, labelled forms
2. **Performance** — loading, rendering, network, framework, Core Web Vitals (see [performance.md](../references/performance.md)); measure CWV when a perf tool is available, otherwise judge from static checks
3. **Responsive** — fixed widths, touch targets ≥44px, overflow, text scaling, breakpoints
4. **Theming** — consistent token use, working dark mode, no orphan hard-coded values
5. **Anti-patterns** — AI-slop tells from [anti-patterns.md](../references/anti-patterns.md), including color-harmony failures (orphan or clashing accents, palette incoherence) judged against the brand hue family in [color.md](../references/color.md)

Source, when present, sharpens dimensions 1–4 (real markup, real CSS). Without
it, judge from the rendered UI and screenshots.

### Step 3: Anti-pattern verdict

Start the report here, honestly: does the UI read as AI-generated? List the
specific tells. Some are deterministic checks you verify against the markup,
others are perceptual reads you weigh by eye — cover both (see the two kinds of
check in [anti-patterns.md](../references/anti-patterns.md)).

Apply the token test — read the token names and values; do they belong to this
product's world, or would they fit any project? — and name where the product's
signature actually appears. When `PRODUCT.md` declares anti-references, judge
whether the build has drifted into one of those named lanes.

### Step 4: Findings by severity

Tag every defect P0–P3 (definitions in [scoring.md](../references/scoring.md)).
For each: name, location, the user impact, the standard it violates if any, and
the fix. Group P2/P3 to keep the signal clean — too many P3s is noise.

### Step 5: Report

Assemble using the template in [scoring.md](../references/scoring.md): verdict,
the 5-dimension table and total /20, findings by severity, systemic patterns (a
defect repeated across many components), and what is working. craft-ui
reports; the fix happens in implementation.

## Guidelines

- Only the running UI is required — never hard-gate on missing source
- Lead with the anti-pattern verdict; be brutally honest about slop
- Every finding states user impact — why it matters, not just what it is
- Quality-only — do not flag token or design-system drift; that is out of scope
- Report, never apply — the non-mutating invariant holds for audit too

## Error Handling

- No running UI and no screenshot: nothing to audit — ask for a URL or an image
- Surface unclear: infer from the UI or ask before setting the register
- Source absent: proceed from the rendered UI; note which checks are limited without markup
- User asks to fix the defects: redirect — audit documents; the change is an implementation task
