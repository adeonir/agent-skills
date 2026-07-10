# Brand register

When design IS the product: brand sites, landing pages, marketing surfaces, campaign pages, portfolios, long-form content, about pages. The deliverable is the design itself; a visitor's impression is the thing being made.

## When to Use

Read by `critique.md` and `audit.md` when the surface is brand — to set the judging posture — and by `render.md` to lean a variant toward this register. Name the register first, then read only the matching file: brand here, or [product.md](product.md) when design serves a task. Not a direct trigger.

The register spans every genre. A tech brand (Stripe, Linear, Vercel). A luxury brand (a hotel, a fashion house). A consumer product (a restaurant, a travel site, a CPG page). A studio portfolio, a band's album page. They share the stance — *communicate, not transact* — and diverge wildly in aesthetic. Don't collapse them into a single look.

## Posture of judgment

| | Brand |
|---|---|
| Question | "Would someone say AI made this?" |
| Bar | Distinctiveness — a clear point of view |
| Failure | Safe, average, undifferentiated |
| Permission | Ambitious motion, committed color, art direction per section |

Restraint without purpose reads as generic, not refined. A move that is voice on a brand surface (a drenched hero, an orchestrated page-load) would be noise on a product surface — judge it by this register, not the other.

## The brand slop test

If someone could look at this and say "AI made that" without hesitation, it failed. The bar is distinctiveness; a visitor should ask "how was this made?", not "which AI made this?"

AI-generated landing pages have flooded the internet; average is no longer findable. Brand surfaces need a POV, a specific audience, a willingness to risk strangeness.

**Second altitude: aesthetic lane.** Before committing, name the reference. A Klim-style specimen page is one lane; Stripe-minimal another; acid-maximalism another. Don't drift into editorial-magazine aesthetics on a brief that isn't editorial. Then the inverse test: describe what you're about to build the way a competitor would describe theirs. If that sentence fits the modal landing page in the category, restart.

## Typography

### Font selection procedure

Every project. Never skip.

1. Read the brief. Write three concrete brand-voice words — physical-object words ("warm and mechanical and opinionated"), not "modern" or "elegant".
2. List the three fonts you'd reach for by reflex. If any appear in the reflex-reject list, reject them — they are training-data defaults.
3. Browse a real catalog (Google Fonts, Pangram Pangram, Future Fonts, Klim, Velvetyne) with the three words in mind. Find the font for the brand as a *physical object*. Reject the first thing that "looks designy."
4. Cross-check. "Elegant" is not necessarily serif; "technical" not necessarily sans; "warm" is not Fraunces. If the pick lines up with the reflex, restart.

### Reflex-reject list

Training-data defaults. Look further:

Fraunces · Newsreader · Lora · Crimson · Playfair Display · Cormorant · Syne · IBM Plex (Mono/Sans/Serif) · Space Mono · Space Grotesk · Inter · DM Sans · DM Serif · Outfit · Plus Jakarta Sans · Instrument Sans · Instrument Serif

### Reflex-reject aesthetic lanes

Saturated aesthetic families that have flooded brand surfaces. If a brief lands in one without a register reason that *requires* it, it's the second-order reflex — the trap one tier past picking a Fraunces font.

- **Editorial-typographic.** Display serif (often italic) + small mono labels + ruled separators + monochromatic restraint. The fingerprint: three rule-separated columns, an italic Fraunces/Recoleta/Newsreader headline, lowercase track-spaced metadata, no imagery.

The reflex-reject lists apply to **new design choices** and deliberate departures from an existing identity. When the brand has already committed to a font or lane as part of its identity, identity-preservation wins.

### Pairing, voice, scale

Distinctive + refined is the goal; the shape depends on the brand, not its category. Two families is the rule *only* when the voice needs it — a single well-chosen family with committed weight/size contrast beats a timid pair. Modular scale, fluid `clamp()` for headings, ≥1.25 ratio between steps; flat scales read as uncommitted. Light text on dark: add 0.05–0.1 to line-height.

## Color

Brand has permission for Committed, Full palette, and Drenched. Use it. A single saturated color across a hero is voice, not excess; a beige-and-muted-slate landing page ignores the register.

- Name a real reference before picking a strategy ("Klim #ff4500 orange drench", "Vercel pure-black monochrome"). Unnamed ambition becomes beige.
- Palette IS voice. A calm brand and a restless brand should not share palette mechanics. When the strategy is Committed or Drenched, commit — don't hedge with neutrals around the edges.
- Don't converge across projects. When a cultural-symbol palette is the obvious pull, reach past it — let culture come from type, imagery, and copy.

## Layout

- Asymmetric compositions are one option; break the grid intentionally for emphasis. Fluid `clamp()` spacing that breathes on larger viewports.
- For image-led briefs (hotels, restaurants, magazines), full-bleed hero imagery with overlaid menu and centered headline is canonical — let the photograph be the design.

## Imagery

Brand surfaces lean on imagery. A restaurant, hotel, or product page without imagery reads as incomplete, not restrained. **When the brief implies imagery, imagery must ship** — zero images is a bug, not a choice. A solid-color rectangle where a hero image belongs is worse than a representative photo.

- Greenfield without local assets: use stock (Unsplash default). **Verify URLs before referencing** — guessed IDs 404 and ship as broken-image placeholders.
- Search for the brand's *physical object* ("handmade pasta on a scratched wooden table"), not the generic category ("Italian food").
- One decisive photo beats five mediocre ones. Alt text is part of the voice.

"Imagery" is broader than stock photos: product screenshots, data viz, generated SVG, and canvas/WebGL scenes count. Text-only pages where type carries the entire visual weight are the failure mode.

## Motion

One well-orchestrated page-load beats scattered micro-interactions, when the brand invites it. Some brands skip entrance motion entirely; the restraint is the voice.

## Brand bans (on top of the shared [anti-patterns.md](anti-patterns.md))

- Monospace as lazy shorthand for "technical / developer" when the brand isn't.
- Large rounded-corner icons above every heading — screams template.
- Single-family pages that picked the family by reflex, not voice.
- All-caps body copy. Reserve caps for short labels and headings.
- Timid palettes and average layouts. Safe = invisible.
- Zero imagery on a brief that implies it; colored blocks where a hero photo belongs.
- Defaulting to editorial-magazine aesthetics on briefs that aren't magazine-shaped. Editorial is ONE lane, not the default brand aesthetic.
- Repeated tiny uppercase tracked labels above every section heading. One strong kicker can be voice; repeating it as section grammar is AI scaffolding.

## Brand permissions

Brand can afford things product can't. Take them.

- Ambitious first-load motion — reveals and typographic choreography that earn their place; not fade-on-scroll for every section.
- Single-purpose viewports — one dominant idea per fold, long scroll, deliberate pacing.
- Unexpected color strategies — palette IS voice.
- Art direction per section — different sections can have different visual worlds if the narrative demands it. Consistency of *voice* beats consistency of *treatment*.

## Register is not surface

**Register** (brand vs product) is the posture — two values. **Surface** is the granular type the work actually is (landing, campaign, portfolio, about, storefront-marketing…). A surface sits under a register, but the register is not a finer surface list. Surfaces under this register:

**Brand surfaces** — landing, campaign, portfolio, long-form / editorial, about, the marketing shell of a storefront. Storefronts straddle: the marketing / catalog shell is Brand, the checkout / account flow is Product (see [product.md](product.md)).
