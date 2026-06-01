# Direction

Explore visual mood from scratch when no reference exists — diverge across
aesthetic directions, converge on one, capture it as a moodboard that downstream
token authoring consumes.

## When to Use

- Greenfield with **no visual reference** — audience, PRD, or a vague feeling on
  hand, but no images, brand URL, codebase, or design-tool file to extract a
  direction from.
- User wants to *explore* or *decide* a look before committing to tokens —
  "not sure what it should feel like", "help me find a direction", "explore
  some moods", "I don't have a reference".
- Skip when a direction is already given (images, brand URL, codebase, or a text
  description like "warm retro-futuristic neo-grotesque"). Token authoring
  extracts that directly — the mood is not absent, so this exploration is the
  wrong tool.

## Workflow

Text-only throughout. No tokens, no color hexes, no rendered HTML — this is the
early diverge, before any visual identity exists. The moment you reach for
tokens you have crossed into token authoring; stop and hand off the moodboard.

### Step 1: Frame

Pull the brief from `docs/product/prd.md`, `docs/product/brief.md`, or
`docs/product/brainstorm.md` when present. Otherwise ask one question at a time:

1. What is the product, and who uses it?
2. Any feeling or adjectives already in mind? (optional — absence is fine)
3. Hard constraints — locked brand colors, accessibility target, platform?

Lock **Purpose** and **Constraints** — Four Questions 1 and 3 in
[aesthetics.md](../references/aesthetics.md). These anchor the converge.

### Step 2: Diverge

Generate **3 candidate moods** (honor any N the user names). Each candidate is
composed, not rendered:

- Compose across the **Style Axes** in
  [aesthetics.md](../references/aesthetics.md) — pick one pattern per axis
  (Layout & Structure, Texture & Depth, Atmosphere & Era, Color & Contrast), or
  blend two within an axis.
- Seed from a **named tone** in [presets.md](../references/presets.md) when one
  fits — read its Vibe, Signature move, and layout-hint prose. Ignore its token
  overrides; tokens do not exist yet.
- Make the three genuinely distinct — different atmospheres, not three shades of
  one idea.

Present each candidate as:

- **Name** — short evocative label
- **Statement** — one or two sentences, "feels like X × Y"
- **Axes** — the chosen pattern per Style Axis
- **Signature** — the single unforgettable detail (Four Questions 4)
- **Touchstones** — 2-3 reference points (products, eras, materials)

### Step 3: Converge

The user reacts. Support:

- **Pick** — choose one candidate as-is.
- **Blend** — combine across candidates ("the warmth of A with the structure of
  B").
- **Refine** — regenerate variations around the leaning candidate (new round,
  same loop).

Pressure-test the leaning direction against the Four Questions — does it serve
the Purpose, respect the Constraints, carry a real Signature? Reject mood that
looks good but misses the audience; evocative is not the same as right. Loop
until one direction is locked.

### Step 4: Capture

Write the locked direction to `docs/design/moodboard.md` — the only artifact
this workflow produces. It is the highest-fidelity form of the "text
description" that token authoring later consumes. The workflow ends here; do not
author tokens.

> Ensure the directory exists: `mkdir -p docs/design`

ALWAYS use this exact template structure:

```markdown
---
direction: <Name>
status: locked
---

# Moodboard — <Name>

## Mood

<One or two paragraphs of evocative prose: atmosphere, density, contrast
strategy, what it feels like. "Feels like X × Y." Describe the visual feel,
not what the product does or for whom — no product pitch.>

## Style Axes

- **Layout & Structure**: <pattern> — <one-line rationale>
- **Texture & Depth**: <pattern> — <one-line rationale>
- **Atmosphere & Era**: <pattern> — <one-line rationale>
- **Color & Contrast**: <pattern> — <one-line rationale>

## Signature

<The single unforgettable detail — a motion moment, a typographic trick, an
unusual color move. Every direction needs one.>

## Touchstones

- <reference 1>
- <reference 2>
- <reference 3>

## Constraints

<Hard requirements carried from framing: locked brand colors, accessibility
target, platform. "None" if unconstrained.>
```

While exploring, write `status: draft` and firm it up as the direction settles;
set `status: locked` only once the user commits to a single direction.

## Guidelines

- Keep it text-only — hexes, tokens, or HTML mean you have crossed into token
  authoring; stop and hand off the moodboard
- Make the three candidates genuinely distinct; near-duplicates waste the diverge
- Anchor every candidate in the Style Axes vocabulary so the direction is
  reproducible, not a vibe with no handles
- Give every direction a Signature — a mood with no unforgettable detail is
  generic
- Pull the brief from existing product docs before asking the user to repeat
  themselves

## Error Handling

- No product docs and a user who cannot describe the audience: explore anyway
  with broad candidates, but flag that the direction is unanchored and may need
  a second pass once the audience is clear.
- User already has a clear reference (images, URL, codebase): this is
  direction-given, not absent — token authoring should extract directly rather
  than explore mood here.
- User picks no candidate after a refine round: widen the axes (a new Atmosphere
  or Color pattern) rather than producing finer variations of a rejected
  leaning.
