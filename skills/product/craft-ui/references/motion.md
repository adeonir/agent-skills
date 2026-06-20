# Motion

Motion that conveys state, gives feedback, and clarifies hierarchy — and the cut
of motion that exists only for decoration. Animation fatigue is a real cost;
spend the budget on the moments that need it. The ambitious tier (scroll-driven,
view transitions, GPU rendering) is its own brand-only tune — see
[overdrive.md](overdrive.md).

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

## animate (tune verb)

The everyday motion tune render re-renders a variant along — motion that conveys
state: feedback, reveals, transitions, loading. Like every tune it is a
direction, not an edit; the motion lives only in the variant HTML for the
session, never in a source artifact. Reach for it when a variant reads flat or
gives no feedback, and apply the timing, easing, and materials above within the
register's budget.

The ambitious tier — view transitions, scroll-driven choreography, GPU effects —
is a separate, brand-only tune: see [overdrive.md](overdrive.md).

## Motion anti-defaults

- Bounce/elastic easing; animating layout properties casually; durations >500ms
  for feedback; animation without purpose; animating everything; ignoring
  `prefers-reduced-motion`; bleeding-edge APIs without a functional fallback.
