# Interaction

The design of interactive behavior — states, focus, forms, overlays, keyboard
paths, and destructive actions. (The *technical-correctness* rules an audit
checks — ARIA, semantic HTML — live in [web-standards.md](web-standards.md);
this file is the interaction *design*.)

## When to Use

Composed by `render.md` (apply while generating), and by `critique.md` /
`audit.md` (judge a rendered surface against it). Not a direct trigger.

## The eight interactive states

Every interactive element needs all eight designed — the common miss is hover
without focus (keyboard users never see hover):

| State | When | Treatment |
|-------|------|-----------|
| Default | at rest | base |
| Hover | pointer over (not touch) | subtle lift, color shift |
| Focus | keyboard/programmatic | visible ring (below) |
| Active | pressed | pressed-in, darker |
| Disabled | not interactive | reduced opacity, no pointer |
| Loading | processing | spinner / skeleton |
| Error | invalid | red border + icon + message |
| Success | completed | green check, confirmation |

## Focus rings

Never `outline: none` without a replacement. Use `:focus-visible` (keyboard
only):

```css
button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}
```

High contrast (≥3:1 against adjacent), 2–3px, offset from the element, consistent
everywhere.

## Forms

Placeholders aren't labels — they disappear on input; always a visible
`<label>`. Validate on **blur**, not every keystroke (exception: password
strength). Errors **below** the field, linked with `aria-describedby`.

## Loading

Skeleton screens > spinners — they preview content shape and feel faster.
Optimistic updates (show success, roll back on failure) for low-stakes actions
only, never payments or destructive ones.

## Overlays: modals, popovers, dropdowns

- **Modal** — native `<dialog>` (`showModal()` traps focus, closes on Esc) or
  `inert` on the background. Modal-as-first-thought is usually laziness; exhaust
  inline / progressive alternatives.
- **Popover API** — native `popover` for tooltips, dropdowns, non-modal
  overlays: light-dismiss, top-layer stacking (no z-index wars), accessible by
  default.
- **The dropdown-clip bug** — a dropdown with `position: absolute` inside an
  `overflow: hidden`/`auto` container gets clipped (the most common generated-UI
  bug). Escape the stacking context: native `<dialog>`/popover, `position:
  fixed`, CSS anchor positioning, or a portal (`createPortal` / `<Teleport>`).
  With anchor positioning, `@position-try` flips at viewport edges automatically.

## Destructive actions: undo > confirm

Users click through confirmations mindlessly. Remove from the UI immediately,
show an undo toast, delete after it expires. Reserve confirmation for truly
irreversible (account deletion), high-cost, or batch operations.

## Keyboard navigation

- **Roving tabindex** for component groups (tabs, menus, radios): one item
  `tabindex="0"`, the rest `-1`; arrow keys move within, Tab moves out.
- **Skip links** (`<a href="#main">Skip to content</a>`), hidden off-screen,
  visible on focus.

## Gestures

Swipe-to-delete and similar are invisible — hint at them (partial reveal of the
action, coach marks on first use) and always provide a visible fallback. Never
make a gesture the only way to do something.

## Interaction anti-defaults

- Removing focus indicators without a replacement.
- Placeholder text as the only label.
- Touch targets <44×44px.
- Hover-only functionality (touch users can't hover).
- Custom controls without ARIA/keyboard support.
