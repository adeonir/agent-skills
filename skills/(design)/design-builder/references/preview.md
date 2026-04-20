# Preview

Visual preview of the design before implementation. Two base modes — guided
(per-question decisions) and exploratory (complete variants) — plus three
refinement tools available after a variant is chosen: tune, comment, and
apply-across.

## Prerequisites

- **design.json** (required) — validated design tokens
- **structure.md** (required) — approved layout decisions
- **copy.yaml** (optional) — structured content
- **[aesthetics.md](aesthetics.md)** (required) — design principles
- **[web-standards.md](web-standards.md)** (required) — implementation rules

## When to Use

- After structure is approved
- User wants to see the design with visual style applied
- User wants to compare visual directions
- User wants to refine a chosen variant (tune tokens, comment on elements)
- User wants to preview a single component in isolation

## Project Type Routes the Presets

Read `project_type` from `copy.yaml` or `structure.md`:

- **page-based** (`landing-page`, `website`): use page-based presets and full-page HTML
- **screen-based** (`web-app`, `mobile-app`): use screen-based presets, render the entry screen with navigation affordances, offer device viewport switching

## Two Base Modes

Agent suggests based on context, user chooses.

| Mode | Best for | How it works |
|------|----------|-------------|
| **Guided** | New projects, no clear reference, user wants control | One visual decision at a time, accumulates into final design |
| **Exploratory** | Strong reference, user wants to see full options | Complete variants (one per preset), pick one, refine |

## Guided Mode

Per-question visual decisions using the preview server.

### Workflow

1. **Start server** (if not running):

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/guided
   ```

2. **Present decisions one at a time.** For each decision:
   - Agent generates 2-3 HTML fragments showing the options
   - Server serves the fragment
   - User clicks their choice
   - Agent reads `.artifacts/design/preview/guided/.events` on next turn
   - Decision is recorded

3. **Visual decisions (in order):**

   | Decision | Options example |
   |----------|----------------|
   | Color mood | Warm neutrals / Cool blues / Dark mode / Monochrome |
   | Typography pairing | Serif headings + sans body / All geometric / Display + system |
   | Primary surface treatment | Gradient overlay / Split / Text-only / Full bleed (page) — Flat / Elevated / Layered (screen) |
   | Card or cell style | Flat with borders / Elevated with shadows / Glass morphism |
   | Rhythm | Alternating backgrounds / Uniform / Dark-light contrast |
   | CTA or primary action style | Solid filled / Outlined / Gradient / Text link |
   | Motion | Subtle fades / Slide-in / Bounce / None |

   Not all decisions apply to every project. Skip what is defined by
   `structure.md` or obvious from `design.json` tokens.

4. **Accumulate into final design.** After all decisions, generate the
   complete HTML combining all choices. Serve for user approval.

5. **Save** to `.artifacts/design/preview/guided/final.html`

### Fragment Format

Each fragment is a self-contained HTML snippet (no `<!DOCTYPE>`) showing
2-3 options. Use vanilla CSS with `design.json` tokens. Include
`data-choice="a"` / `data-choice="b"` / `data-choice="c"` on clickable
elements for the server to record.

```html
<div class="options">
  <div class="option" data-choice="a">
    <h3>Warm Neutrals</h3>
    <!-- visual example using tokens -->
  </div>
  <div class="option" data-choice="b">
    <h3>Cool Blues</h3>
    <!-- visual example using tokens -->
  </div>
</div>
```

## Exploratory Mode

Generate complete HTML variants for side-by-side comparison. Number and
flavor of presets depend on project type.

### Workflow

1. **Gather context:**
   - Read `design.json` (tokens)
   - Read `structure.md` (layout or flow decisions)
   - Read `copy.yaml` (content, if available)
   - Read reference image (if available)

2. **Read layout from `structure.md`.** All variants share the same structural
   skeleton — sections (page-based) or screens (screen-based) and their order.
   Variants differ only in visual treatment.

3. **Generate presets.** Each preset applies a unique mix across these
   dimensions:

   | Dimension | Description |
   |-----------|-------------|
   | Typography | Font pairing, size scale, weight contrast |
   | Color | 60-30-10 distribution, saturation, contrast |
   | Spacing | Density — generous to compact |
   | Backgrounds | Surface treatments, gradients, textures |
   | Decorative | Elements shown, intensity |
   | Motion | Animation style, speed, stagger |
   | Primary surface | Hero (page) or entry screen (app) treatment |
   | Cards or cells | Shadow, border, background, radius, hover |
   | Rhythm | Vertical or stack spacing pattern |

4. **Presets by project type:**

   **Page-based (landing-page, website) — 4 presets:**

   - **minimal** — Refined restraint. Near-monochrome, generous whitespace,
     typography-only hierarchy, subtle motion
   - **editorial** — Magazine sophistication. High-contrast serif headings,
     warm neutrals, editorial grid, section numbers
   - **startup** — Premium SaaS polish. Dark hero with glow, glass-morphism,
     micro-interactions, conversion-focused
   - **bold** — High-impact statement. Display fonts at extreme scale, dark
     palette, aggressive accent, compact density

   **Screen-based (web-app, mobile-app) — 4 presets:**

   - **utilitarian** — Data-dense. High information density, monospace labels,
     minimal chrome, keyboard-first affordances (web-app) or native-compact
     (mobile-app)
   - **consumer-polished** — Friendly and inviting. Rounded surfaces, generous
     padding, warm accents, soft shadows
   - **native-platform** — Follows platform conventions tightly. Web: system
     fonts and standard controls. Mobile: iOS HIG or Material aligned
   - **creative-tool** — Dark canvas, vibrant accents, floating panels, custom
     controls (Figma- or Linear-dark flavored)

   Users can request a custom preset alongside the fixed ones.

5. **Generate comparison page** (`index.html`) with all variants in a dark
   UI for side-by-side viewing (iframes). For screen-based projects, include
   viewport switcher controls (375 / 768 / 1440) that resize the iframe.

6. **Serve:**

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/variants
   ```

7. **User picks one, then refines.** Route to the refinement tools below.

8. **Save** to `.artifacts/design/preview/variants/`

## Refinement Tools (post-variant)

Once a variant is chosen, three tools refine it without regenerating.

### Tune (sliders)

Expose key tokens as sliders that re-render the variant live. The server
serves a tune fragment alongside the variant iframe; sliders write `tune`
events to `.events`, and the page swaps matching CSS custom properties
(`--color-primary`, `--spacing-unit`, `--radius-md`, `--font-size-body`,
etc.) without regenerating HTML.

Default slider set:

- Spacing scale multiplier (0.75x — 1.5x)
- Color saturation (desaturated — vivid)
- Typography contrast (flat — high-contrast hero vs body ratio)
- Border radius scale (sharp — pill)

Agent can generate custom sliders when the user wants to tune something
specific ("make the accent more lavender", "more compact cards"). Each
slider is a `data-tune="<token-key>"` element wired to emit `tune` events.

**Commit:** when the user is done tuning, agent reads the final `tune`
events and writes the resolved values into `design.json`.

### Comment (inline feedback on elements)

User clicks any element in the served preview. An overlay appears with a
text input. On submit, the client posts a `comment` event with:

- `selector` — CSS path to the clicked element
- `text` — the user's comment
- `screenshot` — optional, inline via canvas (skip if heavy)

Agent reads `comment` events on the next turn, addresses each, and shows
the updated variant.

### Apply Across

When a refinement targets a repeated element (a card, a section, an input),
propagate the change to every instance of that element type — not just the
one the user commented on. Agent announces the propagation before applying.

Example: user comments "make the border radius softer" on one card. Agent
updates the radius token for all cards, not just the clicked one. Report
the scope of the change so the user can object before the update ships.

## Component Isolation Mode

For screen-based projects (and occasionally page-based) the user may want
to preview a single component (button, card, input, badge, sheet) outside
any layout.

### Workflow

1. User requests component preview: "preview the button component"
2. Agent reads the component definition from `design.json`
3. Agent generates a clean canvas HTML showing the component in all states
   (default, hover, focus, active, disabled, error) and all sizes (sm, md, lg)
4. Serve via the preview server under `.artifacts/design/preview/components/<name>.html`
5. Tune and comment tools work the same way

Useful for design system sanity-checking before composing full screens.

## Viewport Switching

For screen-based projects, the variants page includes viewport controls that
resize the iframe: 375 (mobile), 768 (tablet), 1440 (desktop). No device
chrome frames — just viewport width — to keep HTML vanilla and self-contained.

Page-based variants can also use the switcher, but typically default to
1440 unless the user requests mobile preview.

## After Approval

Design is approved. Suggest next steps:

- "Run `spec-driven` to implement the approved design"
- "Send to Paper, Pencil, or Figma for further refinement (MCP available)"
- "Run handoff to package artifacts for another agent or developer"
- "Keep as HTML" (done)

If the user iterates in a derivative (Pencil, implementation code) later,
suggest running sync to propagate changes back to `design.json` and
`structure.md`.

## Design Quality

Apply [aesthetics.md](aesthetics.md) principles and [web-standards.md](web-standards.md)
rules to all output. Each variant (exploratory) or accumulated design (guided)
must feel like a professional designer made it.

All HTML uses vanilla CSS — no frameworks, no build tools, self-contained.

## Guidelines

**DO:**
- Route presets by project type — page-based and screen-based have different preset sets
- Let user choose the base mode — suggest based on context, never force
- Ask one visual decision at a time in guided mode
- Generate all presets in exploratory mode
- Preserve the structural skeleton from `structure.md` across all variants
- Apply `aesthetics.md` and `web-standards.md` to every output
- Use distinct font pairings per variant (exploratory)
- Announce apply-across scope before propagating a comment-driven change
- Serve every generated preview through the preview server so the user sees it in a browser
- Swap CSS custom properties during tune — keep the DOM, change only the tokens

**DON'T:**
- Mix base modes in a single session (contrasts: pick one and commit)
- Change structural layout between variants (contrasts: only visual treatment differs)
- Use CSS frameworks (contrasts: vanilla CSS only, self-contained)
- Generate previews without `design.json` and `structure.md` (contrasts: treat them as prerequisites)
- Skip serving the result (contrasts: serve every generated preview through the preview server)
- Regenerate HTML during tune when a CSS custom property swap is enough (contrasts: swap CSS custom properties, keep the DOM)

## Error Handling

- No `design.json`: suggest running extract design first
- No `structure.md`: suggest running structure first
- Server port in use: try alternative port
- No `copy.yaml`: use placeholder content from `structure.md`
- User wants to switch base modes mid-session: allow it, start fresh
- Comment event has no selector: ask user to re-click the target element
- Tune event targets a token not in `design.json`: ask user how to add it
