# Preview

Visual preview of the design before implementation. Two modes: guided
(per-question decisions) and exploratory (4 complete variants).

## Prerequisites

- **design.json** (required) -- validated design tokens
- **structure.md** (required) -- approved layout decisions
- **copy.yaml** (optional) -- structured content
- **[aesthetics.md](aesthetics.md)** (required) -- design principles
- **[web-standards.md](web-standards.md)** (required) -- implementation rules

## When to Use

- After structure is approved
- User wants to see the design with visual style applied
- User wants to compare visual directions

## Two Modes

Agent suggests based on context, user chooses.

| Mode | Best for | How it works |
|------|----------|-------------|
| **Guided** | New projects, no clear reference, user wants control | One visual decision at a time, accumulates into final design |
| **Exploratory** | Strong reference, user wants to see full options | 4 complete variants, pick one, refine |

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
   | Hero treatment | Gradient overlay / Split layout / Text-only / Full bleed image |
   | Card style | Flat with borders / Elevated with shadows / Glass morphism |
   | Section rhythm | Alternating backgrounds / Uniform / Dark-light contrast |
   | CTA style | Solid filled / Outlined / Gradient / Text link |
   | Motion | Subtle fades / Slide-in / Bounce / None |

   Not all decisions apply to every project. Skip what is defined by
   structure.md or obvious from design.json tokens.

4. **Accumulate into final design.** After all decisions, generate the
   complete HTML page combining all choices. Serve for user approval.

5. **Save** to `.artifacts/design/preview/guided/final.html`

### Fragment Format

Each fragment is a self-contained HTML snippet (no `<!DOCTYPE>`) showing
2-3 options. Use vanilla CSS with design.json tokens. Include
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

Generate 4 complete HTML variants for side-by-side comparison.

### Workflow

1. **Gather context:**
   - Read design.json (tokens)
   - Read structure.md (layout decisions)
   - Read copy.yaml (content, if available)
   - Read reference image (if available)

2. **Read layout from structure.md.** The structure document defines the
   section order, hierarchy, and CTA placement. All variants share this
   structural skeleton.

3. **Generate 4 presets.** Each uses the same structure but applies a
   unique mix of visual properties across all dimensions:

   | Dimension | Description |
   |-----------|-------------|
   | Typography | Font pairing, size scale, weight contrast |
   | Color | 60-30-10 distribution, saturation, contrast |
   | Spacing | Density -- generous to compact |
   | Backgrounds | Section treatments, gradients, textures |
   | Decorative | Elements shown, intensity |
   | Motion | Animation style, speed, stagger |
   | Hero | Visual treatment (overlay, gradient, text size) |
   | Cards | Shadow, border, background, radius, hover |
   | Sections | Alternating background pattern |
   | 60-30-10 | Dominant/secondary/accent ratio |
   | Hierarchy | How visual importance is communicated |
   | Rhythm | Vertical spacing pattern |

4. **4 Fixed presets:**

   - **minimal** -- Refined restraint. Near-monochrome, generous whitespace,
     typography-only hierarchy, subtle motion
   - **editorial** -- Magazine sophistication. High-contrast serif headings,
     warm neutrals, editorial grid, section numbers
   - **startup** -- Premium SaaS polish. Dark hero with glow, glass-morphism,
     micro-interactions, conversion-focused
   - **bold** -- High-impact statement. Display fonts at extreme scale, dark
     palette, aggressive accent, compact density

   Users can request a custom preset alongside the 4 fixed ones.

5. **Generate comparison page** (`index.html`) with all variants in a dark
   UI for side-by-side viewing (iframes).

6. **Serve:**
   ```bash
   bun run scripts/preview-server.ts --session .artifacts/design/preview/variants
   ```

7. **User picks one, then refines** via feedback. Agent adjusts the chosen
   variant until approved.

8. **Save** to `.artifacts/design/preview/variants/`

## After Approval

Design is approved. Suggest next steps:

- "Run spec-driven to implement the approved design"
- "Send to Paper/Pencil/Figma for further refinement" (if MCP available)
- "Keep as HTML" (done)

## Design Quality

Apply [aesthetics.md](aesthetics.md) principles and [web-standards.md](web-standards.md)
rules to all output. Each variant (exploratory) or accumulated design (guided)
must feel like a professional designer made it.

All HTML uses vanilla CSS -- no frameworks, no build tools, self-contained.

## Guidelines

**DO:**
- Let user choose the mode -- suggest based on context, never force
- Ask one visual decision at a time in guided mode
- Generate all 4 presets in exploratory mode
- Preserve the structural skeleton from structure.md across all variants
- Apply aesthetics.md and web-standards.md to every output
- Use distinct font pairings per variant (exploratory)

**DON'T:**
- Mix modes in a single session (pick one and commit)
- Change structural layout between variants (only visual treatment differs)
- Use CSS frameworks -- vanilla CSS only
- Generate previews without design.json and structure.md
- Skip serving -- the user needs to see the result in a browser

## Error Handling

- No design.json: suggest running extract design first
- No structure.md: suggest running structure first
- Server port in use: try alternative port
- No copy.yaml: use placeholder content from structure.md
- User wants to switch modes mid-session: allow it, start fresh
