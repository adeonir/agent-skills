# Tune

The named directions render re-renders a chosen variant along — bolder, quieter, distill, delight, harden. Each is a *direction*, not an edit: the move lives only in the re-rendered variant HTML for the session. None touches DESIGN.md, `structure.yaml`, copy.yaml, or production code.

## When to Use

Composed by `render.md` when the user names a tune on the chosen variant, and by `critique.md` (Step 7) when a priority issue maps to a tune. Not a direct trigger. The motion tunes live elsewhere — `animate` in [motion.md](motion.md), `overdrive` in [overdrive.md](overdrive.md); this file owns the five that reshape the look itself.

Each verb reads differently for brand vs product — name the register first ([brand.md](brand.md) / [product.md](product.md)). The moves below are variant-level re-renders, never source mutations.

## bolder

Make the variant *distinctive*, not merely louder. The failure it fixes is a look with no point of view — safe type, hedged color, even spacing everywhere. More effects is not bolder; a committed decision is.

- **Brand** — push scale and risk: a dominant display size, a committed or drenched color strategy ([color.md](color.md)), real spatial drama, one signature move the page is remembered for.
- **Product** — strengthen hierarchy and clarity, not decoration: sharpen the primary action, widen the type-scale contrast, let one screen carry a category color. Restraint stays the baseline.

Moves: push display contrast hard — 3–5× scale jumps, not a timid 1.5×, and weight pairings at the extremes (900 against 200, not 600/400); commit the color step up one level toward a ~60% dominant; exaggerate the spatial rhythm around the focal element; give the signature detail room. Re-render, don't redecorate.

## quieter

Pull an overworked variant back toward restraint — without flattening it into the generic default. Reducing noise is not the same as removing the point of view; the signature survives, the clutter goes.

- **Brand** — calm the decoration but keep the voice: fewer simultaneous effects, one focal moment instead of five competing ones.
- **Product** — desaturate toward tinted neutrals, drop weight, shorten and soften motion, let whitespace carry the structure.

Moves: cut accent surface area; pull saturation back toward 70–85% and drop weight a full step (900→600); reduce elevation and radius emphasis; shorten or remove decorative motion — keep state feedback. Quieter is a deliberate strategy, not an absence of one.

## distill

Strip the variant to its essence — remove what does not earn its place so the core reads instantly. *Perfection is reached not when there is nothing left to add, but when there is nothing left to take away.*

- Remove redundant or purely decorative elements; merge anything that says the same thing twice.
- Tighten the hierarchy so the primary action and key information are unmistakable.
- Push secondary detail behind progressive disclosure rather than onto the first screen.

Moves: drop ornament with no function; collapse duplicate affordances; increase the spacing ratio between primary and secondary; defer the non-essential. The test: can anything be removed without losing meaning? If yes, remove it.

## delight

Add personality at the moments that earn it — never on every section. Delight everywhere reads as noise; one well-placed moment is what users remember and share. It must amplify the task, never block or hide it.

- **Brand** — personality can run across the surface: voice in the copy stays the copy skill's job, but section transitions, discovery rewards, and a distinctive empty or success state are fair game here.
- **Product** — delight at specific moments only: a completion, a first-time action, an error softened. Reliability carries the rest.

Moves (variant-level, earned and subtle): a satisfying press/hover on the primary control; a considered empty or success state instead of a blank panel; one micro-interaction at the moment of accomplishment. Keep it quick, skippable, and honored by `prefers-reduced-motion` ([motion.md](motion.md)). Match it to the domain — read the room before adding charm.

## harden

Re-render the variant's edge states so the direction is judged on more than the happy path. A look that only holds with perfect data is not a real decision yet. This is a preview of resilience, not production validation — no error handling or i18n libraries get built here; the variant simply *shows* the hard cases.

Re-render the chosen variant against:

- **Long and short text** — a name at 100+ characters, an empty field, a headline that wraps to three lines; confirm truncation/clamp/wrap holds ([typography.md](typography.md), [layout.md](layout.md)).
- **Empty, loading, error, and blocked states** — the panel with no data, mid-load, after a failure, plus permission-denied and rate-limited, each with a clear next action ([interaction.md](interaction.md)).
- **Density extremes** — a list at 1000+ rows and at zero; a table column with an outlier value.
- **Internationalization shape** — a 30–40% longer translation and an RTL mirror, to expose fixed widths and directional assumptions ([responsive.md](responsive.md)).

Moves: render these states as additional frames of the same variant so the critique sees them side by side with the happy path. The deliverable is a direction that survives reality, not a hardened codebase.

## Motion tunes (cross-link)

`animate` (motion that conveys state — transitions, feedback, reveals) is defined in [motion.md](motion.md); `overdrive` (the ambitious tier — view transitions, scroll-driven choreography, GPU effects; brand register only, product stays calm) in [overdrive.md](overdrive.md). Apply them as re-renders the same way: the motion lives in the variant HTML for the session, never in a source artifact.

## Guidelines

- Tune the variant by re-rendering — never edit tokens, layout, copy, or code
- Name the register first; every verb reads differently for brand vs product
- bolder means a committed decision, not more effects; quieter keeps the point of view, not just removes noise
- distill by subtraction — remove until removing more would lose meaning
- delight at earned moments only; delight everywhere is noise
- harden previews edge states; it does not build production resilience
