# Presets

Curated tone library for variant generation. Each preset is a pre-blended
direction across the Style Axes — token overrides, prompt addendum, and
layout hints packed into a single named recipe.

## When to Use

Auto-loaded by `preview.md` whenever the user invokes a named vibe
("Editorial", "Cyberpunk", "Bento", "Luxury", ...) instead of composing
freely across Style Axes. Presets are *starting points*, not constraints —
the agent may compose further or blend two adjacent presets.

## How Presets Work

A preset overlays its token map on top of the project's `DESIGN.md`
frontmatter for variant generation only — the underlying DESIGN.md is not
mutated. If the user approves a variant and runs the preview commit-back
workflow, the preset overlay propagates through the usual surgical patch
list (`preview.md` Commit Back to DESIGN.md).

Presets are orthogonal to project type: any preset is usable on
landing-page, website, web-app, mobile-app, or e-commerce. Layout hints
adapt the recipe to the project's structure.

## Recipe Template

ALWAYS use this exact template structure:

```markdown
### {preset-name}
**Vibe:** {one-line aesthetic description}
**Token overrides:**
- `colors.background`: {value or characterization}
- `colors.primary`: {value or characterization}
- `colors.accent`: {value or characterization}
- `typography.display.fontFamily`: {value or characterization}
- `typography.body.fontFamily`: {value or characterization}
- `spacing` scale multiplier: {factor}
- `rounded` scale: {sharp | subtle | medium | pill}
- `elevation` profile: {flat | subtle | layered | dramatic}
- `duration` profile: {snappy | gentle | bouncy | none}
**Prompt addendum:** "{one-sentence aesthetic guidance appended to variant generation prompt}"
**Layout hints:**
- {composition hint 1}
- {composition hint 2}
- {density / asymmetry / focal point guidance}
**Signature move:** {the one unforgettable detail per the Four Questions}
**Best for:** {project types where preset excels}
**Avoid for:** {project types where preset misfires}
```

## Presets

(recipes pending — 13 tones from prior Tone Catalog to be authored: Brutally minimal,
Maximalist chaos, Retro-futuristic, Organic / natural, Luxury / refined,
Playful / toy-like, Editorial / magazine, Brutalist / raw, Art deco /
geometric, Soft / pastel, Industrial / utilitarian, Neo-grotesque,
Kinetic / motion-first)

### brutally-minimal

(pending)

### maximalist-chaos

(pending)

### retro-futuristic

(pending)

### organic-natural

(pending)

### luxury-refined

(pending)

### playful-toy

(pending)

### editorial-magazine

(pending)

### brutalist-raw

(pending)

### art-deco

(pending)

### soft-pastel

(pending)

### industrial-utilitarian

(pending)

### neo-grotesque

(pending)

### kinetic-motion-first

(pending)
