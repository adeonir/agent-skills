# Render

Render the real product in N visual directions for decision-making. Resolve the layout structure first — a region tree plus screen flow ([structure.md](../references/structure.md)) — then combine it with DESIGN.md tokens and copy.yaml content into full-page HTML variants, serve them side by side, refine the visual direction, comment, and switch viewports. A decision aid — output is HTML in `.artifacts/`, never a source artifact.

One structure feeds every variant: the arrangement stays constant while the look varies, so the variants compare treatments of the same page rather than different pages. Variant generation deserves careful reasoning — structural and visual choices compound across a full page.

## When to Use

- A visual direction needs to be seen on the real product before committing
- User wants to compare visual directions side by side
- User wants to explore a layout or style direction on a rendered page
- User wants only the layout structure — a region tree, screen inventory, or screen flow — before any visual direction; the structure phase resolves and stops
- After or alongside DESIGN.md and copy.yaml — each optional, see Inputs; the structure phase resolves the layout itself

## Inputs and Fallbacks

Reads two upstream artifacts and resolves the layout structure itself. Each input is optional — a missing one falls back so a variant always renders:

- `docs/design/DESIGN.md` — visual identity (tokens in YAML frontmatter). **Absent** → compose seed tokens from [design-thinking.md](../references/design-thinking.md) + the craft dimensions.
- **Layout structure** — the region tree plus flow the structure phase resolves ([structure.md](../references/structure.md)), cached at `.artifacts/design/variants/structure.yaml`. **Absent** → the structure phase composes it from the conversation, a brief, or a conventional layout ([layout.md](../references/layout.md)); an existing `structure.yaml` is read, not re-planned.
- `docs/design/copy.yaml` — structured content. **Absent** → placeholder strings from DESIGN.md H1 and `description`, or generic lorem when DESIGN.md is absent too.

The fallback rule is uniform: **any missing input → compose a seed from [design-thinking.md](../references/design-thinking.md) + the craft dimensions, follow [anti-patterns.md](../references/anti-patterns.md)**. Render the best coherent page from whatever exists. render is the integrator — the one place that resolves structure, tokens, and content together. It writes only the session artifacts (`structure.yaml` and variant HTML) under `.artifacts/`, never a `docs/` source.

> Before writing variants, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

Required references, auto-loaded:

- [structure.md](../references/structure.md) — region tree, shape vocabulary, reflow, structural self-check
- [design-thinking.md](../references/design-thinking.md) — choose a visual direction, slop test
- [heuristics.md](../references/heuristics.md) — heuristics + visual laws
- [color.md](../references/color.md) — OKLCH, palette, contrast, dark mode
- [typography.md](../references/typography.md) — scale, pairing, loading
- [layout.md](../references/layout.md) — spacing, grid, hierarchy, hero composition, depth
- [motion.md](../references/motion.md) — the animate gate, timing, easing, materials
- [interaction.md](../references/interaction.md) — states, focus, overlays
- [responsive.md](../references/responsive.md) — breakpoints, input, safe areas
- [web-standards.md](../references/web-standards.md) — implementation rules
- [anti-patterns.md](../references/anti-patterns.md) — failure modes + fallback discipline

## Structure

First fix the **register** and **surface**, since both the arrangement and the look read from them. Register comes from `PRODUCT.md`'s default plus the surface convention (landing/marketing = brand, dashboard/app = product — [brand.md](../references/brand.md) / [product.md](../references/product.md)); read which surfaces the project has from an existing `structure.yaml`, `copy.yaml`, or the user, and ask only when neither register nor surface is available.

Then resolve the layout structure ([structure.md](../references/structure.md)) — the region tree plus screen flow every variant shares. Read an existing `.artifacts/design/variants/structure.yaml` when present; otherwise compose the arrangement from the conversation, a brief, `copy.yaml`, or a conventional layout, walking one decision at a time and biasing each surface by its register. Run the structural self-check, then cache the plan to `structure.yaml`.

When the request is only for structure — "map the screen flow", "arrange the screens", "plan the layout" — resolve the tree, draw the mermaid screen-flow from `flow:`, and stop before generating variants. Otherwise carry the resolved structure into generation.

## Direction

With the register and surface fixed, compose the **visual direction** from [design-thinking.md](../references/design-thinking.md): when the user names one ("Cyberpunk", "Editorial dark mode", "Bento Grid"), compose from it; with no direction, compose one biased by the register (brand and product permit different things — see their files) and fitting the surface. Vary the direction per variant; never converge on a house style.

Set the density and variance dials (design-thinking.md) to the level the brief implies — a scanning dashboard runs dense, a premium landing runs sparse — and build the variant to that level.

## Token Extraction

The YAML frontmatter at the top of DESIGN.md is the source of truth for tokens. At variant generation time, parse the frontmatter, resolve every `{path.to.token}` reference, and embed CSS custom properties directly in the generated HTML:

- **Colors** — from `colors.*`. Each token becomes a CSS custom property. String hex used directly; `{ hex, oklch }` objects emit oklch (Tailwind-native) with hex as fallback comment.
- **Typography** — from `typography.*`. Each role becomes related custom properties (`--font-display-family`, `--font-display-size`, ...).
- **Spacing / Radius / Elevation / Motion / Breakpoints** — from `spacing.*`, `rounded.*`, `elevation.*`, `duration.*`/`easing.*`, `breakpoints.*`. Scale keys become custom properties.
- **Components** — from `components.*`. Each entry becomes a class with properties resolved through the reference chain.

When DESIGN.md is absent, compose seed tokens from [design-thinking.md](../references/design-thinking.md) + the craft dimensions in place of the frontmatter. No external parser, no token endpoint — read the YAML (or compose the seed), resolve references, map to CSS variables, ship the file.

## Generated HTML Stack

Dependencies load via CDN — no build step. Resolve the canonical CDN entry from each library's official docs at generation time; do not hardcode version pins.

- **Tailwind CSS** — include the official browser-build script in `<head>` so utility classes resolve client-side.
- **Icons (iconify-icon)** — include the official `iconify-icon` web-component script before `</body>`. One include covers every icon set (`lucide`, `tabler`, `simple-icons` for brand/social marks, etc.). Markup `<iconify-icon icon="<set>:<name>"></iconify-icon>`. Decorative icons add `aria-hidden="true"`; meaningful icons keep `aria-label` on the containing button.
- **Tailwind theme customization** goes inline via `<style type="text/tailwindcss">@theme { ... }</style>` after the Tailwind script, mapping tokens (`colors`, `typography`, `rounded`, `spacing`, `elevation`, `duration`, `easing`, `breakpoints`) to Tailwind theme keys. The frontmatter parser lives in `scripts/render-server.ts`.
- Every variant must work offline-of-build: opening the `.html` directly renders correctly without a bundler.
- React/JSX variants follow the same CDN pattern; production builds replace CDN with bundled imports.

## Tailwind Token Conventions

Prefer standard Tailwind tokens over arbitrary `[value]` syntax. Arbitrary values bypass the theme, break dark mode and theme switching, and erode consistency.

- Map tokens into the Tailwind theme via `<style type="text/tailwindcss">@theme { --color-primary: ...; --radius-md: ...; }</style>` so `bg-primary`, `rounded-md`, `text-lg` resolve to project values.
- Use the nearest standard token when an exact value lacks a named key (`p-4` vs `p-[15px]`, `rounded-lg` vs `rounded-[10px]`).
- Arbitrary values (`w-[317px]`, `bg-[#abc123]`) only when genuinely one-off, not reusable, and documented in a comment. When the same arbitrary value appears 2+ times, promote it to `@theme`.
- Colors always go through the theme — never inline hex in class names when the value belongs to the palette.

| Avoid | Prefer |
|-------|--------|
| `bg-[#3b82f6]` | `bg-primary` (mapped) or `bg-blue-500` |
| `p-[16px]` | `p-4` |
| `rounded-[8px]` | `rounded-lg` |

## Workflow

Generate one HTML per variant from the resolved structure (`structure.yaml`), the tokens (DESIGN.md or a composed seed), and the content (copy.yaml or placeholders). Every variant draws the same structure in a different look.

1. **Resolve the structure.** Fix the register and surface, then resolve the region tree and flow per the Structure section above, caching it to `structure.yaml`. Stop here when the request was only for structure.

2. **Confirm count and direction.** Scale N to the stage of the inputs — 1–2 when DESIGN.md already fixes the visual (a look to confirm), 4–5 greenfield where the space is open — and honor any N the user names. Compose the direction from [design-thinking.md](../references/design-thinking.md): the user's named direction ("Editorial", "Cyberpunk + Bento Grid") when given, otherwise one biased by the register and fitting the surface.

3. **Start the render server** (if not running):

   ```bash
   bun run ${CLAUDE_SKILL_DIR}/scripts/render-server.ts --session .artifacts/design/variants
   ```

4. **Generate one HTML per variant.** Resolve structure, tokens, and content per the fallback rule. Wire Tailwind + iconify-icon via CDN — see Generated HTML Stack and Tailwind Token Conventions. Write each variant to `.artifacts/design/variants/<slug>.html`.

5. **Serve** all variants side by side via the server. User picks one.

6. **Mark** the chosen variant as `final.html` in the variants directory.

## Variant-Tune

Once a variant is chosen, tune its **visual direction** — not its tokens. Variant tune re-renders the variant along four direction axes; it never edits DESIGN.md and never commits. To make a tuned direction permanent, the change happens in the owning place — a layout change re-plans `structure.yaml` through the structure phase, a style change goes to DESIGN.md authoring (design-brief).

Four axes:

- **Layout pattern** — a page arrangement from the fixed shape vocabulary in [structure.md](../references/structure.md) (`full-width | split | grid-N | stack | sidebar | modal | overlay`)
- **Style direction** — a composition from [design-thinking.md](../references/design-thinking.md) (Editorial, Brutalist, Cyberpunk, ...)
- **Density** — airy ↔ dense spacing and component padding
- **Decoration** — austere ↔ playful elevation, radius, accent emphasis

The user names an axis change ("make it denser", "try a bento layout", "more editorial"). Re-render the chosen variant with the adjusted direction and re-serve. Each tune is a local exploration of the rendered page — the result lives only in the variant HTML for the session.

### Tune verbs

Named shortcuts over the four axes — each names a move and re-renders the variant. All are non-mutating: they change the variant HTML for the session, never DESIGN.md. Critique drives these in its refinement loop.

- **bolder / quieter / distill / delight / harden** — the look-reshaping directions, defined in [tune.md](../references/tune.md).
- **animate** — the everyday motion direction (state, feedback, reveals), defined in [motion.md](../references/motion.md).
- **overdrive** — the ambitious-tier direction (view transitions, scroll-driven, GPU), brand register only, defined in [overdrive.md](../references/overdrive.md).

Each reads differently for brand vs product — read the register file first. Wording and labels stay out of scope — copy is a content concern, not a tune.

## Comment

User alt+clicks any element in the served preview. An overlay appears with a text input. On submit, the client posts a `comment` event with:

- `selector` — CSS path to the clicked element
- `text` — the user's comment
- `screenshot` — optional, inline via canvas (skip if heavy)

Agent reads `comment` events on the next turn, addresses each, and shows the updated variant.

## Viewport Switching

Variants page includes viewport controls that resize the iframe: 375 (mobile), 768 (tablet), 1440 (desktop). No device chrome frames — just viewport width — to keep HTML vanilla and self-contained.

Default viewport: 1440 (desktop) for brand surfaces and storefronts; 375 (mobile) for mobile app screens; 1440 for product / dashboard screens.

## Guidelines

- Resolve structure, tokens, and content via the fallback rule — render the best coherent page from whatever exists
- Resolve the layout structure first ([structure.md](../references/structure.md)); one region tree feeds every variant
- Resolve every `{path.to.token}` reference when emitting CSS custom properties
- Compose the direction from [design-thinking.md](../references/design-thinking.md) biased by register + surface when the user gives none; use the user's direction when given
- Scale variant count to the stage of the inputs (1–2 when DESIGN.md is fixed, 4–5 greenfield); honor any N the user names
- Apply [design-thinking.md](../references/design-thinking.md), the craft dimensions (color/typography/layout/motion/interaction/responsive), and [web-standards.md](../references/web-standards.md) to every output
- Serve every generated variant through the render server
- Tune the visual direction by re-rendering — never edit tokens or write a source artifact

## Error Handling

- All inputs absent: the structure phase composes a conventional layout and render seeds tokens from [design-thinking.md](../references/design-thinking.md) + the craft dimensions with placeholder content; flag that the page is illustrative until real inputs exist
- DESIGN.md frontmatter unparseable: compose a seed for this render and suggest the user audit DESIGN.md
- Server port in use: try an alternative port
- Comment event has no selector: ask the user to re-click the target element
- User asks to commit a tuned direction: redirect — a layout change re-plans `structure.yaml` through the structure phase, a style change goes to DESIGN.md authoring; render writes no `docs/` source
