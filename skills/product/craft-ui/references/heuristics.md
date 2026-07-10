# Heuristics

The usability heuristics and visual-design laws a rendered surface is judged against — *why* a decision works, and how to score each one 0–4.

## When to Use

Composed by `critique.md` (scores the ten heuristics 0–4) and read by `render.md` to apply the laws while generating. The practical recipes that *implement* these laws live in the craft dimensions (color/typography/layout/motion/interaction/responsive). Aggregate bands, severity, and the report template live in [scoring.md](scoring.md). Not a direct trigger.

## Scoring

Score each heuristic 0–4 — be honest, a 4 is genuinely excellent (not "good enough"), and most real interfaces land 20–32 / 40. Each heuristic below carries what to **check for** and the 0–4 criteria.

## Nielsen's 10 heuristics

### 1. Visibility of system status

Keep users informed through timely, appropriate feedback. **Check for:** loading indicators, action confirmation (save/submit/delete), progress for multi-step flows, current location (breadcrumbs/active states), inline validation.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| no feedback; guessing | rare; most actions silent | partial; major gaps | most actions clear, minor gaps | every action confirms, progress always visible |

### 2. Match between system and the real world

Speak the user's language, follow real-world conventions, natural order. **Check for:** familiar terms (no unexplained jargon), logical order, recognizable icons/metaphors, domain-appropriate language, natural reading flow.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| pure jargon, alien | mostly confusing | mixed; some jargon leaks | mostly natural, occasional term | speaks the user's language fluently |

### 3. User control and freedom

A clear emergency exit from unwanted states. **Check for:** undo/redo, cancel on forms/modals, clear path back to safety, easy clear of filters/search, escape from multi-step flows.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| users trapped; refresh to escape | difficult, obscure exits | main flows exit, edges don't | exit and undo most actions | undo, cancel, back, escape everywhere |

### 4. Consistency and standards

Same words/actions mean the same thing. **Check for:** consistent terminology, same action → same result, platform conventions, visual consistency (color/type/ spacing/components), consistent interaction patterns.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| inconsistent everywhere | many inconsistencies | main flows match, details diverge | mostly consistent | fully cohesive, predictable |

### 5. Error prevention

Prevent problems beats good error messages. **Check for:** confirmation before destructive actions, constraints preventing invalid input, smart defaults, clear labels, autosave/draft recovery.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| errors easy, no guardrails | few safeguards | common errors caught, edges slip | most error paths blocked | errors near-impossible by design |

### 6. Recognition rather than recall

Minimize memory load; make options visible or retrievable. **Check for:** visible options (not buried), contextual help, recent items/history, autocomplete, labels on icons (not icon-only nav).

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| heavy memorization | mostly recall, few cues | main actions visible, rest hidden | most discoverable | everything discoverable |

### 7. Flexibility and efficiency of use

Accelerators for experts, invisible to novices. **Check for:** keyboard shortcuts, customization, recents/favorites, bulk/batch actions, power features that don't complicate basics.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| one rigid path | limited alternatives | basic shortcuts, limited bulk | keyboard nav, some customization | multiple paths, power features |

### 8. Aesthetic and minimalist design

Every element earns its place. **Check for:** only necessary info per step, clear hierarchy, purposeful color/emphasis, no decorative clutter, focused layouts.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| overwhelming, all competes | cluttered, hard to scan | main clear, periphery noisy | mostly clean, minor noise | every element earns its pixel |

### 9. Help users recognize, diagnose, recover from errors

Plain language, precise problem, constructive fix. **Check for:** plain-language messages (no raw codes), specific problem ("Email is missing @"), actionable recovery, errors near the source, non-blocking (don't wipe the form).

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| cryptic codes or nothing | vague ("something went wrong") | names problem, not fix | problem + next step | pinpoints, suggests fix, preserves work |

### 10. Help and documentation

Easy to find, task-focused, concise. **Check for:** searchable help, contextual help (tooltips/hints/tours), task-focused organization, scannable content, access without leaving context.

| 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| none anywhere | exists but hard to find | basic FAQ, not contextual | searchable, task-focused | right info at the right moment |

## Visual Design Laws

Universal principles for how the eye reads a surface — *why* a decision works. The recipes that apply them live in the craft dimensions (color/typography/layout/motion/interaction/responsive).

### Gestalt

The mind groups visual elements by predictable rules — use them to compose hierarchy without explicit borders.

- **Proximity** — close elements read as a group; separate groups with larger gaps.
- **Similarity** — shared color/shape/size reads as related; vary to signal difference.
- **Continuity** — the eye follows lines/curves; align to guide reading order.
- **Closure** — incomplete shapes are mentally completed; partial borders suggest containment.
- **Figure-ground** — separate foreground from background by contrast.
- **Common region** — a shared container groups; use sparingly to avoid card-noise.

### Hierarchy

Five signals, used in concert, not size alone.

- **Size** — larger = more important; ratios beat absolutes (3x hero-vs-body).
- **Weight** — bold beats light; pair extremes (100-200 vs 800-900).
- **Color** — high-contrast dominates; muted recedes; accents capture disproportionate attention.
- **Position** — top-left dominates LTR; center draws focus; bottom-right anchors CTAs.
- **Spacing** — generous space isolates and elevates; cramped space groups and lowers.

### Balance, contrast, rhythm

- **Balance** — symmetric reads formal/stable; asymmetric dynamic; radial ceremonial. Default-centering reads generic.
- **Contrast** — typographic, color (min AA 4.5:1 body / 3:1 large), scale, and weight each carry hierarchy; stack two or three for focal points.
- **Rhythm** — repetition with variation creates pace; alternate backgrounds, density, or direction between sections.

### Reading patterns

- **F-pattern** — dense text scanned top horizontal → second horizontal → left vertical. Anchor key copy along the F.
- **Z-pattern** — sparse marketing scanned top-left → top-right → bottom-left → bottom-right. Brand mark top-left, CTA bottom-right.
- **Gutenberg** — symmetric long-form: strong primary (top-left) and terminal (bottom-right) areas.
- **Center-out** — heavily centered layouts draw outward; works for short hero pages, fails for scrollable long-form.

Squint at the design — the elements that survive blur are what the eye locks onto first. Reorder weight until the survivors match the intended reading order.
