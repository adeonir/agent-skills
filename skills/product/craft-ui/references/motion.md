# Motion

Motion that conveys state, gives feedback, and clarifies hierarchy — and the cut
of motion that exists only for decoration. Animation fatigue is a real cost;
spend the budget on the moments that need it. Includes the ambitious tier
(scroll-driven, view transitions, GPU rendering) for surfaces that earn it.

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md` /
`audit.md` (judge a rendered surface against it). Not a direct trigger.

## Register sets the budget

- **Brand** — motion is part of the voice; one well-rehearsed entrance beats
  scattered micro-interactions. The saturated AI default is fade-and-rise on
  every scrolled section — a tell, not choreography. See [brand.md](brand.md).
- **Product** — 150–250ms on most transitions; motion conveys state (feedback,
  reveal, loading, view transitions). No page-load choreography; users are in a
  task. See [product.md](product.md).

## Timing: the 100/300/500 rule

Timing matters more than easing for "feels right."

| Duration | Use |
|----------|-----|
| 100–150ms | instant feedback (press, toggle, color) |
| 200–300ms | state changes (menu, tooltip, hover) |
| 300–500ms | layout changes (accordion, modal, drawer) |
| 500–800ms | entrances (page load, hero reveal) |

Exit animations run ~75% of enter duration. Durations over 500ms for *feedback*
feel laggy.

## Easing

```css
--ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);   /* smooth */
--ease-out-quint: cubic-bezier(0.22, 1, 0.36, 1);  /* snappier */
--ease-out-expo:  cubic-bezier(0.16, 1, 0.3, 1);   /* decisive */
```

Never bounce (`0.34, 1.56, …`) or elastic — they read as dated and draw
attention to the animation itself. Ease-out for entrances; ease-in makes a task
feel shorter (peak-end weights the final moments).

## Motion materials

Transform and opacity are reliable defaults, not the whole palette — premium
surfaces need atmospheric properties. Match material to effect:

- **Transform / opacity** — movement, press, simple reveals, list stagger.
- **Blur / backdrop-filter** — focus pulls, depth, glass, softened entrances.
- **Clip-path / mask** — wipes, reveals, editorial cropping.
- **Shadow / glow / color filter** — energy, affordance, focus, active state.
- **grid-template-rows / FLIP** — expand and reflow without animating `height`.

The rule isn't "transform and opacity only" — it's: avoid animating
layout-driving properties casually (`width`, `height`, `top`, `left`, margins),
keep expensive effects bounded to small/isolated areas, and verify smoothness
in-browser.

## List stagger

Sibling stagger is legitimate for cards-in-a-grid or list items; whole-section
fade-on-scroll is not a list and not legitimate. Cap total stagger
(10 items × 50ms = 500ms); for more, reduce per-item delay or cap the count.
`animation-delay: calc(var(--i, 0) * 50ms)` with `style="--i: N"` per item.

## Performance & perceived performance

- `will-change` sparingly, on `:hover`/`.animating` only — never preemptively.
- Scroll triggers via Intersection Observer, not scroll listeners; unobserve
  after firing once. Bound blur/filter/shadow areas; `contain` where useful.
- The 80ms threshold feels instant — target it for micro-interactions.
  Optimistic UI for low-stakes actions (likes), never payments/destructive.
  Progressive reveal (skeletons, streaming) beats waiting for everything.

## Reduced motion (not optional)

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Reveal animations must enhance an already-visible default — never gate content
visibility on a class-triggered transition (it pauses on hidden tabs and
headless renderers, shipping the section blank).

## Pushing further (ambitious tier)

When the surface earns it, go beyond CSS — but the experience without the
enhancement must still be good (progressive enhancement is non-negotiable).

- **View Transitions API** — shared-element morphing (list item → detail, button
  → dialog). `@starting-style` animates from `display: none` with CSS only.
- **Scroll-driven** (`animation-timeline: scroll()`) — parallax, progress,
  reveals; CSS-only; always a static fallback (`@supports`).
- **Spring physics** — natural motion with mass/tension/damping (motion, GSAP).
- **WebGL / Canvas / OffscreenCanvas** — shaders, particles, GPU charts for
  effects/datasets CSS can't express; lazy-init near viewport, pause off-screen,
  fall back to WebGL2 / CSS.
- **Virtual scrolling** — tens of thousands of rows at 60fps.

Focus creates impact; layering multiple competing "extraordinary" moments
creates noise. Context decides: a particle system wows on a portfolio,
embarrasses on a settings page.

## Motion anti-defaults

- Bounce/elastic easing; animating layout properties casually; durations >500ms
  for feedback; animation without purpose; animating everything; ignoring
  `prefers-reduced-motion`; bleeding-edge APIs without a functional fallback.
