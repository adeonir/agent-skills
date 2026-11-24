# The Slop Catalog

A field guide to the specific defaults that make a design read as machine-generated, why each one happens, and what to do instead.

## Scope

Apply the color, typography, shape, surface, and elevation guidance to identity and tokens. Imagery entries guide the treatment recorded in `## Imagery`. Layout, iconography, and language entries provide context only: do not author page composition, product copy, or another concern's artifact from this skill. A tell never becomes a lint finding solely because it appears in this catalog.

**Contents**
- [The mechanism](#the-mechanism)
- [Color](#color)
- [Typography](#typography)
- [Shape, surface, and elevation](#shape-surface-and-elevation)
- [Layout](#layout)
- [Iconography and imagery](#iconography-and-imagery)
- [Language](#language)
- [The three legitimate exceptions](#the-three-legitimate-exceptions)
- [Final checklist](#final-checklist)

---

## The mechanism

None of the items below are *bad* in isolation. Indigo is a fine color. Inter is an excellent typeface. Rounded corners are pleasant. The problem is that each one is the **highest-probability answer** to its question, and a design assembled entirely from highest-probability answers has a recognizable texture: frictionless, competent, and completely anonymous.

**One authored decision beats ten avoided clichés.** A design that avoids every item below but argues for nothing reads as *differently* anonymous. Commit to a direction, derive from a source, accept a tradeoff.

The reliable test for any token: **can you finish the sentence "this value is what it is because ___" with something other than "it looked good"?**

---

## Color

### The tells

**The indigo-violet complex.** `#6366F1` (Tailwind indigo-500), `#8B5CF6` (violet-500), `#9333EA` (purple-600), `#4F46E5` (indigo-600). These four are the single most reliable signal of unconsidered AI output.

**The purple-to-cyan gradient**, and its siblings: violet→pink→orange, blue→purple, `from-purple-500 via-pink-500 to-orange-400`. Especially as a background mesh or blob behind a hero.

**Gradient text on the headline** — `bg-clip-text` with any two-stop gradient. The move is familiar enough to read as a default.

**Navy-slate dark mode.** `#0F172A` (slate-900) or `#020617` (slate-950) as the page background, with one saturated accent floating on it. Note that the tell is specifically the *blue-tinted* dark; dark UI is fine, this particular dark is not.

**Untouched framework ramps.** Every color pulled straight from Tailwind's default palette with no modification — `emerald-500` for success, `red-500` for error, `amber-500` for warning, `slate-*` for every neutral. The stock semantic triad is as recognizable as the stock accent.

**Pure neutral greys.** `#808080`, `#CCCCCC`, `#F5F5F5`, or any ramp where R=G=B. Real palettes almost never contain true greys, because real light is never neutral.

**Pure `#FFFFFF` and `#000000`** used as the page background and body text. Both are physically harsh, and both signal that nobody chose them.

**Neon glow shadows** — `shadow-[0_0_40px_rgba(99,102,241,0.5)]` and relatives.

**Accent inflation.** The brand color on the heading, the button, the icon, the border, the link, the badge, and the chart. Once it's on everything it emphasizes nothing.

### What to do instead

**Anchor the hue to a real referent, then name the referent in the DESIGN.md prose.** A sourced color is by construction not the median color, and the sourcing is legible to the reader. Load `color-craft.md` for the mechanics when the run does palette work: OKLCH ramps, hue shift, chroma taper, the neutral tint, and the endpoints.

**Enforce accent scarcity.** Pick one accent, give it exactly one job (usually: "this is the primary action" or "this is live/changed"), and hold it under ~5% of pixels. Everything else does its work through weight, size, spacing, and neutral value. Write this into Do's and Don'ts, because it's the rule most likely to erode later.

---

## Typography

### The tells

**Inter for everything.** Inter is genuinely well-made — that's why it's everywhere, and why using it reflexively signals that no typographic decision was made. Related defaults: **Poppins** (geometric, friendly, exhausted), **Montserrat**, **Roboto**, **Open Sans**, **Nunito**, **Lato**. **Playfair Display** is the same phenomenon on the serif side — it became the default "elegant" answer and now reads as a stock choice.

**One typeface doing every job**, with hierarchy carried entirely by size and weight.

**The full weight ladder** — 400/500/600/700 all in play, producing four steps that are hard to tell apart and none of which read as a decision.

**Framework-default metrics.** Tracking untouched at every size; line-height left at the framework default across the whole scale; a size ramp that's just `text-sm` through `text-6xl` with nothing considered in between.

**The hero configuration**: `text-6xl font-bold tracking-tight` centered, subhead in `text-xl text-slate-400` centered beneath, max-width around 2xl. This exact block appears in an enormous fraction of generated pages.

**Centered body copy** at any length past a sentence.

**Uppercase everything** without added tracking — uppercase needs breathing room; set solid, it looks broken rather than emphatic.

### What to do instead

Load `typography.md` when the run does type work: it sets the inverse of every tell above — the pairing, the optical tracking, the inverse line-height, two far-apart weights, and the measure.

**Use two typefaces only when each has a distinct job.** A grotesque + a serif, a serif + a mono, a humanist sans + a condensed display. Two grotesques together (Inter + Helvetica) is not a pairing, it's an accident.

---

## Shape, surface, and elevation

### The tells

- **`rounded-2xl` on everything.** One radius, applied uniformly to cards, buttons, inputs, images, avatars, and modals.
- **`shadow-lg` on everything**, particularly neutral black at low opacity with no light direction, applied to elements that aren't actually floating.
- **Glassmorphism** — `backdrop-blur-xl bg-white/5 border border-white/10`. Ubiquitous and still the default "make it look premium" move.
- **Border + shadow + radius together** on every container, so nothing has a distinct rank.
- **Decorative background gradients** — radial blobs, mesh gradients, faint dot-grids and line-grids behind the hero.
- **A visible card around every piece of content**, including content that has no reason to be a discrete object.

### What to do instead

**Make radius hierarchical.** Different element classes get different radii, chosen for a reason: inputs sharper than buttons, cards sharper than avatars. Or commit to `0` everywhere as a real structural position — sharp is a strong, legible choice when it's the whole direction rather than an accident.

**Prefer borders, tonal shifts, and space over shadows.** Most depth problems are actually grouping problems, and grouping is better solved with spacing. A 1px hairline in a tinted neutral does the work of a shadow with none of the mush.

**If you use shadows, give them physics.** A consistent light direction (usually top-down: y-offset positive, x near zero), a color sampled from the palette's dark end rather than neutral black, and at most two or three levels that mean genuinely different things. Ambient + direct layering (one tight dark shadow, one wide soft one) reads far more real than a single blur.

**Reserve elevation for things that are actually above other things.** Modals, dropdowns, drag states. A static card is not floating.

---

## Layout

### The tells

**The landing page template**, in this exact order: centered hero → three-column feature grid with icons in tinted rounded squares → "trusted by" logo strip → three-tier pricing with a ringed "Most Popular" middle → FAQ accordion → full-width CTA band → four-column footer. Any two or three of these in sequence is recognizable.

**Everything centered.** `max-w-7xl mx-auto` with symmetric padding and center-aligned text at every level.

**Uniform grids** — three equal columns, equal gutters, equal card heights, nothing spanning or breaking.

**Uniform density** across the whole page, so nothing is emphasized by contrast.

**Equal vertical rhythm** — every section separated by the same `py-24`, producing a page with no phrasing.

### What to do instead

**Commit to asymmetry, if the direction supports it.** Flush-left with a wide right margin. A 2/3–1/3 split. Content that breaks the grid deliberately. Asymmetry has to be a system-level commitment, though — sprinkled randomly it reads as a bug.

**Vary density on purpose.** A dense block next to a sparse one creates emphasis for free and costs nothing. Uniform generosity is as monotonous as uniform crowding.

**Vary section rhythm.** Sections that belong together sit closer. Spacing is the cheapest and most-ignored hierarchy tool available.

**Question the card.** Cards are for genuinely discrete, comparable objects. For a list of features, a plain list with strong typographic hierarchy is usually better and always less generic.

**Let structure follow content type.** Editorial content wants columns and rules. Data wants tables and alignment. Marketing wants a few large gestures. Copying a template designed for a different content type is how pages end up feeling arbitrary.

---

## Iconography and imagery

- **A single icon set applied uniformly** (Lucide/Heroicons at default stroke on everything) reads as default. Fine to use, but set a deliberate stroke weight, size, and optical alignment relative to your type — and note it in the file.
- **Emoji as feature icons** is an immediate tell.
- **Icons in tinted rounded squares above feature headings** is the single most recognizable AI layout unit in existence.
- **Generic 3D/isometric illustration** and abstract gradient blobs signal stock content.
- Better: no icons at all — typographic hierarchy usually does the job — or one strong image instead of many weak ones. Use a set with actual character only when the direction names one.

---

## Language

Copy is part of the design because it determines the shape of every block.

Tells: "Supercharge," "Effortlessly," "10x," "Seamlessly," "Unlock," "Take your X to the next level"; ✨🚀🎯 in headings; three-word feature titles with a one-sentence subtitle in exactly parallel structure; em-dash-heavy rhythm.

Better: say the specific thing the product does.

---

## The three legitimate exceptions

Do not follow this file off a cliff. There are real cases where the "slop" answer is correct:

1. **An existing brand mandates it.** If the company's color has been indigo for six years, it's indigo. Codify it and put the effort into the neutrals, type, and shape language instead.
2. **The platform convention is the accessible choice.** iOS/Android/system conventions exist so users don't have to relearn. Deviating from a platform pattern for novelty is worse than generic.
3. **Familiarity is the requirement.** Some products — payments, healthcare, government — should look like what users expect, because surprise costs trust. "Boring and credible" is a real direction; execute it deliberately rather than defaulting into it.

The distinction throughout: **choosing** a conventional answer is design; **arriving** at it is slop.

---

## Final checklist

Run this against the finished DESIGN.md before handing off. Every hit needs a fix or a stated reason.

**Color**
- [ ] No indigo/violet/purple in the `#6366F1`–`#9333EA` range as the primary, unless brand-mandated
- [ ] No multi-hue decorative gradients; no gradient text
- [ ] Not slate-900/950 navy as the dark background
- [ ] No color pulled unmodified from a framework's default palette
- [ ] No `R=G=B` neutrals — every grey is tinted
- [ ] No pure `#FFFFFF` background or `#000000` text
- [ ] Semantic colors derive from the brand family
- [ ] Exactly one accent, with one defined job
- [ ] The primary hue traces to a named real-world referent in the prose

**Typography**
- [ ] Not Inter/Poppins/Montserrat/Roboto/Playfair by default (using one deliberately, with a reason, is fine)
- [ ] Two typefaces that differ by classification
- [ ] At most three weights, spaced far apart
- [ ] Tracking varies with size (negative on display, positive on small caps)
- [ ] Line-height varies inversely with size
- [ ] Body measure constrained to 60–75ch

**Shape and surface**
- [ ] Radius is hierarchical, or deliberately zero everywhere
- [ ] Shadows have a light direction and a palette-derived color — or aren't used
- [ ] No glassmorphism unless it's the stated direction
- [ ] Elevation reserved for things actually above other things

**Layout**
- [ ] Layout structure follows the content type, not a landing-page template
- [ ] Density and section rhythm vary purposefully

**Overall**
- [ ] Every token can complete "this is what it is because ___"
- [ ] The system makes at least one identifiable sacrifice
- [ ] A specific person could have made this and would defend it
