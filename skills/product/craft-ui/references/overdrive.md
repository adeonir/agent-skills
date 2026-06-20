# Overdrive

The ambitious-tier motion tune — push a chosen variant past conventional limits
to show a ceiling worth deciding on: a dialog that morphs from its trigger, a
table that scrolls a million rows at 60fps, a scroll-driven sequence that feels
cinematic. Like every tune it is a *direction*, not a build: the effect lives
only in the re-rendered variant HTML for the session, and the production version
is implemented downstream — never here.

## When to Use

Composed by `render.md` when the user names `overdrive` on the chosen variant.
**Brand register only** — product surfaces stay calm and in-task; an orchestrated
WebGL hero that wows on a portfolio embarrasses a settings page. Name the register
first ([brand.md](brand.md) / [product.md](product.md)); on a product surface
reach for `animate` ([motion.md](motion.md)) instead.

This is the highest-misfire tune. It previews what a surface *could* feel like at
its most ambitious so the user can judge whether the ceiling is worth the cost —
it does not ship a shader pipeline or a view-transition system. The variant
demonstrates the direction; implementation builds the real thing.

## Propose before rendering

Because the downside of a wrong call is large, do not jump straight to a single
ambitious variant:

1. **Sketch 2–3 directions** — different techniques, levels of ambition, and
   aesthetic takes. For each, name in a line what it would look and feel like and
   its cost (browser support, performance, complexity).
2. **Get the user's pick** before rendering — surface the trade-offs so the
   choice is informed.
3. **Render only the chosen direction**, then verify it in the served preview
   (render serves variants for exactly this — switch viewports, leave comments).

Ambitious effects rarely read right on the first render; expect a few rounds of
visual iteration in the preview before the direction holds.

## What "extraordinary" means here

The right ambition depends on the surface — ask what would make a user of *this*
interface say "that's nice":

- **Visual / marketing** (hero, landing, portfolio) — the wow is sensory: a
  scroll-driven reveal, a shader background, a cinematic page transition.
- **Functional UI** (tables, forms, dialogs) — the wow is in how it *feels*: a
  dialog that morphs from its trigger, a form with streaming validation, drag
  with spring physics.
- **Performance-critical** — the wow is invisible but felt: a filter over 50k
  items with no flicker; the interface never hesitates.
- **Data-heavy** (charts, dashboards) — the wow is fluidity: GPU-rendered visuals
  for large sets, animated transitions between data states.

The technique serves the experience, not the reverse.

## The toolkit

Organized by intent — what the variant demonstrates, with the fallback it implies.

- **Cinematic transitions** — View Transitions API (shared-element morph),
  `@starting-style` (animate from `display: none`, CSS only), spring physics
  (mass/tension/damping; motion, GSAP).
- **Tie motion to scroll** — `animation-timeline: scroll()` (CSS-only parallax,
  progress, reveals; always a static fallback via `@supports`).
- **Render beyond CSS** — WebGL / Canvas / OffscreenCanvas for shaders, particles,
  GPU charts the cascade can't express; lazy-init near viewport, pause off-screen,
  fall back to WebGL2 / CSS.
- **Make data feel alive** — virtual scrolling (tens of thousands of rows at
  60fps), GPU-accelerated charts, morphed data-state transitions.
- **Animate complex properties** — `@property` (interpolate gradients and colors
  the cascade normally can't), Web Animations API (composable, cancellable).

This is about how an interface *feels*, not what the product *does* — real-time
collaboration, offline support, or new backend capability are product decisions,
not an overdrive direction.

## Render with discipline

- **Progressive enhancement is non-negotiable** — the variant without the
  enhancement must still read well; gate effects behind `@supports` or feature
  detection so the fallback is always good.
- **Performance** — target 60fps; if it drops below 50, simplify. Lazy-init heavy
  resources (WebGL contexts, WASM) near the viewport; pause off-screen rendering.
- **Reduced motion** — honor `prefers-reduced-motion` always, with a beautiful
  static alternative ([motion.md](motion.md)).
- **Focus over excess** — one extraordinary moment lands; several competing ones
  read as noise.

Never mask weak fundamentals with technical ambition: if the variant reads safe or
unclear, that is a `bolder` / `distill` problem first ([tune.md](tune.md)). Never
reach for a bleeding-edge API without a functional fallback.

## Verify the direction

Judge the rendered variant, not the idea:

- **Wow** — show it to someone who hasn't seen it; do they react?
- **Removal** — take the effect away. Is the experience diminished, or does nobody
  notice? If nobody notices, it was decoration.
- **Device** — does it stay smooth on a mid-range phone, not just the dev machine?
- **Accessibility** — enable reduced motion. Is it still good?
- **Context** — does this fit *this* brand and audience, or is it spectacle for
  its own sake?

## Guidelines

- Brand register only — on a product surface, use `animate`, not overdrive
- Propose 2–3 directions and get the pick before rendering the ambitious variant
- The variant demonstrates the ceiling; it never ships a production effect
- Progressive enhancement and `prefers-reduced-motion` are non-negotiable
- One focused extraordinary moment beats several competing ones
- Ambition never substitutes for fundamentals — fix safe / unclear with
  `bolder` / `distill` first
