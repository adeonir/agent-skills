# Structure

Define how content is organized before visual style is applied. Behavior
bifurcates by project type: page-based products ask layout questions;
screen-based products ask flow questions.

## Prerequisites

- **design.json** (required) — validated design tokens
- **copy.yaml** (optional) — structured content from extract copy
- PRD, brief, or discovery context

## When to Use

- After tokens are extracted and validated
- When defining page layout, content hierarchy, or screen flow
- When validating an existing wireframe

## Project Type Routes the Flow

Read `project_type` from `copy.yaml` (or ask user if not set). It routes
into one of two decision sets:

- **page-based** → `landing-page`, `website`: ask page composition questions
- **screen-based** → `web-app`, `mobile-app`: ask screen flow and navigation questions

The modes below (Create / Validate) apply to both routes.

## Two Modes

### Create Mode (no wireframe)

Agent proposes structure from content + intent. Per-question approach:
present one decision at a time, user approves, agent advances.

Skip any decision that is obvious from context.

#### Decisions — Page-based (landing-page, website)

1. **Page type** (when `website`): which pages exist? (home, about, pricing, contact)
2. **Hero**: fullscreen image, split layout, text-only, video background?
3. **Section order**: what comes after the hero? (features, social proof, pricing, CTA)
4. **Content hierarchy**: what is primary, secondary, tertiary?
5. **CTA placement**: where are the calls to action? Above fold? Repeated?
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
6. **Empty, loading, error states**: which screens need explicit variants?
7. **Modals and sheets** (mobile-app especially): when are they used instead of a new screen?

Ask one question at a time. When the preview server is running, present options
as visual fragments (HTML served via the server). User clicks to choose. Agent
reads events and advances. When the server is not running, present options as
text descriptions.

### Validate Mode (wireframe exists)

Agent analyzes the wireframe and questions coherence and consistency.
Wireframe can be: image, `.pen` file, Figma link, ASCII, or text description.

**Validation questions — Page-based:**

- Is the primary CTA visible without scroll?
- Does the information flow match the user's intent (from discovery or PRD)?
- Does the content hierarchy reflect business priority?
- Are there missing sections that content or PRD indicates should exist?
- Are there competing elements that dilute focus?
- Is the content tone coherent with the visual direction (from `design.json`)?
- Does the layout support the key user journey?

**Validation questions — Screen-based:**

- Is the primary action reachable without more than one intermediate tap or click?
- Is navigation consistent across screens? (same placement, same pattern)
- Are empty, loading, and error states considered?
- Do transitions between screens match the user's mental model?
- Are modal and sheet usage justified, or would a dedicated screen be clearer?
- Is the screen inventory complete for the flows the PRD describes?

Report findings. Suggest adjustments if issues found. User approves or
requests changes.

## Output

Save to `.artifacts/design/structure.md`. Use the template fragment matching
the project type:

**Page-based fragment:**

```markdown
# Structure: {{Project Name}}

## Project Type
{{landing-page or website}}

## Pages (when website)

### {{Page Name}}
- **Purpose**: {{what this page does}}

## Sections (in order)

### 1. {{Section Name}}
- **Purpose**: {{what this section does}}
- **Content**: {{what goes here from copy.yaml}}
- **Hierarchy**: {{primary / secondary / tertiary}}
- **CTA**: {{call to action if any}}

## Layout Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Hero | {{choice}} | {{why}} |
| Navigation | {{choice}} | {{why}} |
| CTA placement | {{choice}} | {{why}} |
| Footer | {{choice}} | {{why}} |
```

**Screen-based fragment:**

```markdown
# Structure: {{Project Name}}

## Project Type
{{web-app or mobile-app}}

## Screens

### {{Screen Name}}
- **Purpose**: {{what this screen does}}
- **Entry points**: {{how the user arrives here}}
- **Primary action**: {{the most important action}}
- **Secondary actions**: {{other actions}}
- **States**: {{empty / loading / error / populated}}
- **Content**: {{what goes here from copy.yaml}}

## Navigation Pattern
{{sidebar / top nav / bottom tabs / stack / drawer / modal-first}}

## Flow

{{describe key transitions: screen → screen, trigger, what changes}}

## Layout Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Navigation | {{choice}} | {{why}} |
| Primary action placement | {{choice}} | {{why}} |
| Modal vs screen | {{rule}} | {{why}} |
| Empty states | {{approach}} | {{why}} |
```

Validation notes section appears in both when validate mode was used.

## Optional Wireframe

After structure decisions are made, agent suggests generating a wireframe.
User decides method:

- **ASCII** — always available, drawn in terminal (pages or single screens)
- **Paper MCP** — `.pen` file saved in repo
- **Pencil MCP** — design in cloud
- **Figma MCP** — design in Figma (bidirectional)
- **Skip** — structure document is enough

The wireframe illustrates structure decisions, not visual style. Low fidelity
is intentional.

## Guidelines

**DO:**
- Route by project type first — page-based and screen-based ask different questions
- Walk through decisions one at a time (no batching)
- Validate structure even when a wireframe exists
- Ground decisions in content (`copy.yaml`) and intent (PRD or discovery)
- Question hierarchy: does the most important content or action get the most attention?

**DON'T:**
- Apply visual style in this phase (contrasts: leave visual decisions to preview)
- Use page-based questions for a web-app or mobile-app (contrasts: route by project type)
- Skip validation when a wireframe is provided (contrasts: always validate)
- Assume structure without checking against content and intent (contrasts: ground in artifacts)
- Generate a wireframe without asking the user first (contrasts: offer the choice)

## Error Handling

- No `design.json`: suggest running extract design first
- No content context: ask user for project purpose and key sections or screens
- Project type missing: ask user before proceeding (page-based vs screen-based changes the whole flow)
- Wireframe format not readable: ask user to describe the layout
- Structure too complex: suggest splitting into multiple pages (page-based) or separate screens (screen-based)

## Next Steps

After structure is approved, suggest:

- "Run preview to see the design with visual style applied"
