# Assets

Generate image assets — hero banners, product shots, OG cards, promotional
banners — driven by `DESIGN.md` tokens. Two modes: direct generation via an
image-generation MCP (when available), or prompt-only (user pastes into their
preferred image tool).

## When to Use

- After preview is approved and tokens are stable
- User asks to generate hero, banner, product image, or OG card
- User wants a ready-to-paste prompt for an external image tool
- Auto-invoked as a sub-phase of `preview.md` after the user approves a variant

## Prerequisites

- `<project-root>/DESIGN.md` with `colors`, `typography`, and prose sections
  populated — tokens drive the generated prompts
- `.artifacts/design/copy.yaml` (optional) — copy informs asset naming and
  content context

## Two Modes

| Mode | When | Output |
|------|------|--------|
| **MCP-direct** | Image-generation MCP available | Binary asset saved to `.artifacts/design/assets/` |
| **Prompt-only** | No MCP, or user explicitly requests | `prompts.md` for user to run in their image tool |

Default to prompt-only when no MCP is detected. Never block on MCP absence.

User may also request prompt-only explicitly even when an MCP is present — honor it without switching modes.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### Step 1: Read DESIGN.md

Read `<project-root>/DESIGN.md`. Extract:

- `colors.primary`, `colors.secondary`, `colors.background`, `colors.accent`
  (or equivalents)
- `typography.heading.fontFamily` and the typographic vibe from prose
- Voice tone and mood from `## Overview` and `## Do's and Don'ts`

### Step 2: Detect Mode

Check for an available image-generation MCP. If present, propose MCP-direct.
If absent, default to prompt-only. If user requests prompt-only explicitly,
skip detection.

### Step 3: Ask for Asset List

Ask the user which assets to generate. Offer these defaults:

- Hero banner — full-width, primary visual
- Product shot — feature highlight
- OG card — 1200×630 social share
- Promotional banner — campaign-specific

User may specify custom dimensions or add items not on the list.

### Step 4: Build Prompt per Asset

For each asset, compose a generation prompt using extracted tokens:

```
{asset_type} for {project_name}.
Color palette: {colors.primary}, {colors.secondary}, {colors.background}.
Typography vibe: {typography.heading.fontFamily} — clean, {vibe_adjective}.
Mood: {mood_from_overview}.
Visual rules: {relevant_dos_and_donts}.
Composition: {composition_hint}.
Output: {width}x{height}px, {format}.
```

Derive `vibe_adjective` and `mood` from the prose in DESIGN.md, not from
invented descriptions. If the prose is thin, ask the user for one direction
word before generating.

### Step 5: Route by Mode

**MCP-direct:**
1. Invoke the image-generation MCP with the composed prompt.
2. Save the result to `.artifacts/design/assets/{slug}.{ext}`.
3. Report path and thumbnail (if MCP returns one) to the user.

**Prompt-only:**
1. Write all prompts to `.artifacts/design/assets/prompts.md`.
2. Instruct the user to run each prompt in their image tool of choice.
3. Ask them to save the resulting files under `.artifacts/design/assets/`.

### Step 6: Inject into Preview (when sub-phase)

When invoked as a sub-phase of `preview.md` after variant approval:

1. Replace placeholder elements in the active preview HTML with `<img>` tags
   pointing at the generated asset paths (MCP-direct) or `prompts.md` paths
   (prompt-only, marked as pending).
2. Re-render the preview so the user sees the full result.
3. Return control to `preview.md` for final approval.

### Step 7: Report

List generated assets and their paths. For prompt-only, remind the user to
add the files once generated externally so the preview can be updated.

## Guidelines

**DO:**
- Derive every prompt attribute from DESIGN.md tokens and prose — grounded prompts produce consistent results
- Default to prompt-only when MCP is absent; never block the workflow
- Save assets under `.artifacts/design/assets/` so preview can reference them
- Ask for one direction word when the prose is too thin to extract mood

**DON'T:**
- Invent palette or typography values not present in DESIGN.md (contrasts: read tokens first)
- Generate assets before tokens are stable — running before preview approval produces mismatched output (contrasts: auto-invoke only after variant approval)
- Name tool brands in prompts or instructions (contrasts: use "your image tool")
- Block when the user requests prompt-only even if MCP is available (contrasts: honor the explicit mode request)

## Output

```
.artifacts/design/assets/
├── prompts.md         # prompt-only mode: one prompt block per asset
├── hero.{ext}         # MCP-direct: binary asset
├── product.{ext}
├── og-card.{ext}
└── banner.{ext}
```

Asset filenames use the slug from the asset list (e.g., `hero`, `og-card`).
Extension matches the MCP output format; default to `png` if unspecified.

## Error Handling

- DESIGN.md missing or unpopulated: route user to `inputs.md`; do not generate
- Prose too thin to derive mood: ask for one direction word before proceeding
- MCP invocation fails: fall back to prompt-only for that asset; continue
- User wants a format not supported by the MCP: note the gap, write the prompt to `prompts.md` for manual generation
- Asset list empty: ask the user which assets to generate before proceeding

## Next Steps

After generating assets:

- Assets approved: return to `preview.md` for final approval (when sub-phase), or hand off to `spec-driven` for implementation
- Prompts written: remind user to generate externally and place files in `.artifacts/design/assets/` for preview injection
- Tokens need adjustment based on asset output: route back to `inputs.md` for a targeted patch
