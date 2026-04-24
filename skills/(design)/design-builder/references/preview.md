# Preview

Visual preview of the design before implementation. Two base modes — guided (per-question decisions) and exploratory (complete variants) — plus three refinement tools available after a variant is chosen: tune, comment, and apply-across. Default push target is HTML via the preview server; the user may also push to an external design tool when the matching MCP is available.

Use ultrathink when generating variants or resolving comments — visual choices compound and are hard to undo.

## Prerequisites

- `<project-root>/DESIGN.md` with frontmatter and prose populated by [inputs.md](inputs.md) and [structure.md](structure.md)
- `.artifacts/design/copy.yaml` (optional) — structured content
- [aesthetics.md](aesthetics.md) (required) — design principles
- [web-standards.md](web-standards.md) (required) — implementation rules

## When to Use

- After tokens and structure are in DESIGN.md
- User wants to see the design with visual style applied
- User wants to compare visual directions
- User wants to refine a chosen variant (tune tokens, comment on elements)
- User wants to preview a single component in isolation
- User wants to push the current design into an external design tool

## Project Type Routes the Presets

Read `project_type` from discovery context or `copy.yaml`:

- **page-based** (`landing-page`, `website`): page-based presets and full-page HTML
- **screen-based** (`web-app`, `mobile-app`): screen-based presets, render the entry screen with navigation affordances, offer device viewport switching

## Two Base Modes

Agent suggests based on context, user chooses.

| Mode | Best for | How it works |
|------|----------|-------------|
| **Guided** | New projects, no clear reference, user wants control | One visual decision at a time, accumulates into the final design |
| **Exploratory** | Strong reference, user wants to see full options | Complete variants (one per preset), pick one, refine |

## Preset Sets

**Page-based** (landing-page, website):

- Editorial — typography-driven, generous whitespace
- Marketing — hero-forward, conversion-oriented
- Product — feature-dense, modular sections
- Branded — bold color, distinctive shapes

**Screen-based** (web-app, mobile-app):

- Utilitarian — dense, efficient, power-user
- Consumer-polished — approachable, friendly, rounded
- Native-platform — respects platform conventions (iOS/Android/macOS/Windows)
- Creative-tool — canvas-first, tool palette, minimal chrome

Custom presets are valid when the user asks for something outside the set.

## Guided Mode

Per-question visual decisions using the preview server.

### Workflow

1. **Start server** (if not running):

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/guided
   ```

2. **Present decisions one at a time.** For each decision, serve an HTML fragment with options. User clicks to choose. Agent reads events and advances to the next decision.
3. **Accumulate** choices into a final variant. Save as `.artifacts/design/preview/guided/final.html`.

## Exploratory Mode

All presets at once. User picks one.

### Workflow

1. **Start server**:

   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/variants
   ```

2. **Generate one HTML per preset**. Preserve the structural skeleton from DESIGN.md `## Layout` / `## Screen Flow` across all variants. Vary only visual treatment (palette weight, typography pairing, component styling, motion intensity).
3. **Serve** all variants side by side via the server. User picks one.
4. **Mark** the chosen variant as `final.html` in its preset directory.

## Refinement Tools

Once a variant is chosen, three tools refine it without regenerating HTML.

### Tune (sliders)

Expose key tokens as sliders that re-render the variant live. The server serves a tune fragment alongside the variant iframe; sliders write `tune` events to `.events`, and the page swaps matching CSS custom properties (`--color-primary`, `--spacing-unit`, `--radius-md`, `--font-size-body`, etc.) without regenerating HTML.

Default slider set:

- Spacing scale multiplier (0.75x — 1.5x)
- Color saturation (desaturated — vivid)
- Typography contrast (flat — high-contrast hero vs body ratio)
- Border radius scale (sharp — pill)

Agent can generate custom sliders when the user wants to tune something specific ("make the accent more lavender", "more compact cards"). Each slider is a `data-tune="<token-key>"` element wired to emit `tune` events.

**Commit:** when the user is done tuning, agent reads the final `tune` events and patches the matching keys in DESIGN.md frontmatter. Section-scoped patch — replace only the affected frontmatter blocks (`colors`, `typography`, `rounded`, `spacing`, `motion`, or `components`). Leave everything else untouched.

### Comment (inline feedback on elements)

User clicks any element in the served preview. An overlay appears with a text input. On submit, the client posts a `comment` event with:

- `selector` — CSS path to the clicked element
- `text` — the user's comment
- `screenshot` — optional, inline via canvas (skip if heavy)

Agent reads `comment` events on the next turn, addresses each, and shows the updated variant.

### Apply Across

When a comment affects a repeated element (button, card, list item), ask whether the change should apply across all instances. Announce the scope before propagating ("applying to 12 button-primary instances"). If the change maps to a token, fold it into the next tune commit; if it is local (one instance only), regenerate just that fragment.

## Component Isolation

For design system sanity-checking before composing full pages or screens.

1. User requests component preview: "preview the button component"
2. Agent reads the component definition from DESIGN.md frontmatter (`components.button-primary` and its sibling variants)
3. Agent generates a clean canvas HTML showing the component in all states (default, hover, focus, active, disabled) and all sizes if defined
4. Serve via the preview server under `.artifacts/design/preview/components/<name>.html`
5. Tune and comment tools work the same way

## Viewport Switching

For screen-based projects, the variants page includes viewport controls that resize the iframe: 375 (mobile), 768 (tablet), 1440 (desktop). No device chrome frames — just viewport width — to keep HTML vanilla and self-contained.

Page-based variants can also use the switcher, but typically default to 1440 unless the user requests mobile preview.

## Push Targets

Default target is HTML via the preview server. The user may also push the current design into an external design tool, gated by the matching MCP.

| Target | MCP required | File ownership |
|--------|--------------|----------------|
| HTML (preview server) | none | skill writes `.artifacts/design/preview/*.html` |
| External design tool | matching MCP | user owns the file in the external tool |

Skill never creates files in an external design tool. The user creates the file first, then asks the skill to push into it. If the matching MCP is not available or the file does not exist, report the gap and offer the HTML fallback.

Push direction from skill is **write-only** from DESIGN.md to the target. Reverse flow (pulling changes from an external design tool back into DESIGN.md) is an input source — see [inputs.md](inputs.md).

## Guidelines

**DO:**

- Read DESIGN.md before generating to ground every visual choice in current tokens
- Route presets by project type — page-based and screen-based have different preset sets
- Let user choose the base mode — suggest based on context, never force
- Ask one visual decision at a time in guided mode
- Generate all presets in exploratory mode
- Preserve the structural skeleton from `## Layout` / `## Screen Flow` across all variants
- Apply [aesthetics.md](aesthetics.md) and [web-standards.md](web-standards.md) to every output
- Announce apply-across scope before propagating a comment-driven change
- Serve every generated preview through the preview server
- Swap CSS custom properties during tune — keep the DOM, change only tokens
- Patch DESIGN.md frontmatter section by section when committing tune events

**DON'T:**

- Mix base modes in a single session (contrasts: pick one and commit)
- Change structural layout between variants (contrasts: only visual treatment differs)
- Use CSS frameworks (contrasts: vanilla CSS only, self-contained)
- Generate previews without DESIGN.md tokens and structure (contrasts: treat them as prerequisites)
- Skip serving the result (contrasts: serve every generated preview through the preview server)
- Regenerate HTML during tune when a CSS custom property swap is enough (contrasts: swap CSS custom properties, keep the DOM)
- Rewrite the whole DESIGN.md frontmatter when committing tune (contrasts: patch only affected blocks)
- Create files in an external design tool (contrasts: treat those files as user-owned; push only when the file already exists)

## Error Handling

- No DESIGN.md at project root: suggest running inputs first; do not proceed
- DESIGN.md missing `## Layout`: suggest running structure first; do not proceed
- No `copy.yaml` (and DESIGN.md is populated): use generic placeholder strings derived from frontmatter `name` and `description`, plus the headings in `## Layout` / `## Screen Flow` prose
- Server port in use: try alternative port
- User wants to switch base modes mid-session: allow it, start fresh
- Comment event has no selector: ask user to re-click the target element
- Tune event targets a token not in DESIGN.md frontmatter: ask user whether to add the token or map the slider to an existing key
- Push target MCP not available: report the gap, offer the HTML fallback
- Push target file missing (no design-tool file at the user's path): report to user, do not create it

## Next Steps

After preview is approved, suggest:

- "Hand the approved design to spec-driven for implementation"
- "Run inputs again to pull any refinements from an external design tool back into DESIGN.md"
