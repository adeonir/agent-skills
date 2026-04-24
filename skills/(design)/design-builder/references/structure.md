# Structure

Define how content is organized before visual style is applied. Owns the `## Layout` and `## Screen Flow` prose sections of `DESIGN.md`. Behavior bifurcates by project type: page-based products ask layout questions; screen-based products ask flow questions.

## Prerequisites

- `<project-root>/DESIGN.md` exists with frontmatter populated by [inputs.md](inputs.md) — at minimum `spacing` tokens
- `.artifacts/design/copy.yaml` (optional) — content payload for context
- PRD, brief, or discovery context

## When to Use

- After tokens are extracted and validated
- When defining page layout, content hierarchy, or screen flow
- When validating an existing wireframe against tokens and intent

## Output

Patch `<project-root>/DESIGN.md`:

- `## Layout` — always present
- `## Screen Flow` — screen-based projects only (`web-app`, `mobile-app`). Omit the section entirely for page-based projects (`landing-page`, `website`)

Never overwrite frontmatter, `## Overview`, `## Colors`, `## Typography`, `## Elevation & Depth`, `## Shapes`, `## Motion`, `## Components`, `## Variants`, or `## Do's and Don'ts` — those are owned by [inputs.md](inputs.md). Never overwrite content payload — owned by [copy.md](copy.md).

**USE TEMPLATE:** [`../templates/design.md`](../templates/design.md) (Layout and Screen Flow sections only).

The template file is lowercase (`design.md`) by skill convention. The artifact written into the user's project root must use the uppercase filename `DESIGN.md`.

## Project Type Routes the Flow

Read `project_type` from discovery context or `copy.yaml`. Ask the user if not set. It routes into one of two decision sets:

- **page-based** → `landing-page`, `website`: ask page composition questions
- **screen-based** → `web-app`, `mobile-app`: ask screen flow and navigation questions

The modes below (Create / Validate) apply to both routes.

## Two Modes

### Create Mode (no wireframe)

Agent proposes structure from content + intent. Per-question approach: present one decision at a time, user approves, agent advances. Skip any decision that is obvious from context.

#### Decisions — Page-based (landing-page, website)

1. **Page set** (when `website`): which pages exist? (home, about, pricing, contact)
2. **Hero**: fullscreen image, split layout, text-only, video background?
3. **Section order**: what comes after the hero? (features, social proof, pricing, CTA)
4. **Content hierarchy**: what is primary, secondary, tertiary?
5. **CTA placement**: above the fold, repeated, footer-only?
6. **Navigation**: sticky header, sidebar, minimal, none?
7. **Footer**: full footer, minimal, CTA-focused?

#### Decisions — Screen-based (web-app, mobile-app)

1. **Screen inventory**: which screens exist? (auth, home, detail, settings, empty states)
2. **Entry screen**: which screen does the user land on first?
3. **Navigation pattern**:
   - web-app: sidebar, top nav, command palette, nested routes
   - mobile-app: bottom tab bar, stack with back, drawer, modal-first
4. **Primary action per screen**: what is the most important action on each screen?
5. **Screen flow**: which transitions matter? (auth → home, list → detail, edit → save)
6. **State variants**: which screens need explicit empty, loading, error variants?
7. **Modals and sheets** (mobile-app especially): when used instead of a new screen?

Ask one question at a time. When the preview server is running, present options as visual fragments (HTML served via the server). User clicks to choose. Agent reads events and advances. When the server is not running, present options as text descriptions.

### Validate Mode (wireframe exists)

Agent reads the wireframe and questions coherence and consistency against tokens and intent. Wireframe can be: image, design-tool file (read via the matching MCP), ASCII, or text description. Skill never creates these wireframes — they are user-supplied.

**Validation questions — Page-based:**

- Is the primary CTA visible without scroll?
- Does information flow match user intent (from discovery or PRD)?
- Are content sections grouped by hierarchy or scattered?
- Does navigation surface the highest-value paths?
- Does spacing rhythm match the `spacing` tokens?

**Validation questions — Screen-based:**

- Is the primary action obvious on every screen?
- Does navigation reach every screen in the inventory?
- Are state variants (empty, loading, error) covered?
- Do transitions follow a consistent direction (forward = right/up, back = left/down)?
- Do modals interrupt only when blocking input or confirming destruction?

Report findings. User decides what to change before agent patches DESIGN.md.

## Workflow

### Step 1: Establish Context

If discovery did not capture it, ask one question at a time:

1. Project type: landing-page, website, web-app, mobile-app?
2. Existing wireframe to validate, or starting from scratch?
3. Existing `## Layout` or `## Screen Flow` in DESIGN.md — patch or replace?

### Step 2: Choose Mode

- No wireframe → Create Mode
- Wireframe present → Validate Mode (then optionally roll into Create Mode for missing decisions)

### Step 3: Walk Decisions

Run through the decision set matching the project type. One question at a time. Skip what is obvious from copy or discovery.

### Step 4: Patch DESIGN.md

Read DESIGN.md first to preserve sections owned by other refs. Replace only `## Layout` (and `## Screen Flow` for screen-based) from each `##` heading to the next.

Section content shape:

**`## Layout`** — short paragraphs covering:

- Spacing rhythm with explicit token references (e.g. "8px base from `spacing.unit`; section margins use `spacing.section-margin`")
- Container conventions (max width, gutters)
- Grid behavior (column count, breakpoints if relevant)
- Density choices (compact vs comfortable)
- For page-based: hero treatment, section order, CTA placement, navigation pattern, footer treatment
- For screen-based: navigation pattern summary and primary action placement (full screen-by-screen detail goes into `## Screen Flow`)

**`## Screen Flow`** — screen-based only. Cover:

- Screen inventory (one short bullet per screen with its purpose)
- Primary user paths (entry → key actions → exit)
- Transitions that matter (with direction convention)
- Modal vs full-screen patterns
- State variants per screen (empty, loading, error)

If the project is page-based, omit `## Screen Flow` entirely.

### Step 5: Present

Show the user:

- Path to patched DESIGN.md
- Summary of decisions captured
- Validation findings (if Validate Mode ran)
- Suggested next step (preview if both inputs and structure are populated)

## Guidelines

**DO:**

- Read DESIGN.md before patching to preserve sections owned by other refs
- Ask one question at a time when walking decisions
- Reference `spacing` and other tokens by their YAML key in the prose
- Skip decisions that are already obvious from copy.yaml or discovery context
- Validate against tokens and intent, not personal taste
- Treat wireframes as inputs only — never create or modify them

**DON'T:**

- Overwrite frontmatter or any section other than `## Layout` / `## Screen Flow` (contrasts: patch only sections this ref owns)
- Bundle layout decisions and screen flow into one section for screen-based projects (contrasts: keep them in their own sections)
- Include `## Screen Flow` for page-based projects (contrasts: omit the section entirely when not applicable)
- Generate a wireframe automatically (contrasts: wireframes come from the user, never the skill)
- Restate token values in prose (contrasts: reference token keys so the prose stays anchored)

## Error Handling

- No DESIGN.md at project root: ask the user to run inputs first
- DESIGN.md frontmatter missing `spacing` tokens: ask user to run inputs to fill them, or fall back to text descriptions in prose
- Project type unknown: ask user before proceeding (page-based vs screen-based changes the whole flow)
- Wireframe format unreadable (corrupted image, MCP unavailable): ask user to describe the layout in text
- Existing `## Layout` content has unknown structure: preserve the heading, replace body content
- Structure too complex: suggest splitting into multiple pages (page-based) or grouping screens (screen-based)

## Next Steps

After patching DESIGN.md, suggest:

- "Run preview to see the design with the layout applied"
- "Run inputs again if Components or Variants need updating to match the layout"
