# Structure

Define how content is organized before visual style is applied.

## Prerequisites

- **design.json** (required) -- validated design tokens
- **copy.yaml** (optional) -- structured content from extract copy
- PRD, brief, or discovery context

## When to Use

- After tokens are extracted and validated
- When defining page layout and content hierarchy
- When validating an existing wireframe

## Two Modes

### Create Mode (no wireframe)

Agent proposes structure from content + intent. Uses per-question approach:
present one layout decision at a time, user approves, agent advances.

**Decisions to make (in order):**

1. **Page type**: what kind of page is this? (landing, dashboard, form, content)
2. **Hero**: fullscreen image, split layout, text-only, video background?
3. **Section order**: what comes after the hero? (features, social proof, pricing, CTA?)
4. **Content hierarchy**: what is primary, secondary, tertiary?
5. **CTA placement**: where are the calls to action? Above fold? Repeated?
6. **Navigation**: sticky header, sidebar, minimal, none?
7. **Footer**: full footer, minimal, CTA-focused?

Not all decisions apply to every project. Skip what is obvious from context.
Ask one question at a time.

When the preview server is running, present options as visual fragments
(HTML served via the server). User clicks to choose. Agent reads events
and advances.

When the server is not running, present options as text descriptions.

### Validate Mode (wireframe exists)

Agent analyzes the wireframe and questions coherence and consistency.
Wireframe can be: image, .pen file, Figma link, ASCII, or text description.

**Validation questions:**

- Is the primary CTA visible without scroll?
- Does the information flow match the user's intent (from discovery/PRD)?
- Does the content hierarchy reflect business priority?
- Are there missing sections that content/PRD indicates should exist?
- Are there competing elements that dilute focus?
- Is the content tone coherent with the visual direction (from design.json)?
- Does the layout support the key user journey?

Report findings. Suggest adjustments if issues found. User approves or
requests changes.

## Output

Save to `.artifacts/design/structure.md`:

```markdown
# Structure: {{Project Name}}

## Page Type
{{type}}

## Sections (in order)

### 1. {{Section Name}}
- **Purpose**: {{what this section does}}
- **Content**: {{what goes here from copy.yaml}}
- **Hierarchy**: {{primary / secondary / tertiary}}
- **CTA**: {{call to action if any}}

### 2. {{Section Name}}
...

## Layout Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Hero | {{choice}} | {{why}} |
| Navigation | {{choice}} | {{why}} |
| CTA placement | {{choice}} | {{why}} |
| Footer | {{choice}} | {{why}} |

## Validation Notes (if validate mode)

- {{finding and recommendation}}
```

## Optional Wireframe

After structure decisions are made, agent suggests generating a wireframe.
User decides method:

- **ASCII** -- always available, drawn in terminal
- **Paper MCP** -- .pen file saved in repo
- **Pencil MCP** -- design in cloud
- **Figma MCP** -- design in Figma (bidirectional)
- **Skip** -- structure document is enough

The wireframe illustrates the structure decisions, not the visual style.
Low fidelity is intentional.

## Guidelines

**DO:**
- Ask one question at a time -- never batch layout decisions
- Always validate structure even when wireframe exists
- Ground decisions in content (copy.yaml) and intent (PRD/discovery)
- Question hierarchy: does the most important content get the most attention?

**DON'T:**
- Apply visual style in this phase -- that happens in preview
- Skip validation when wireframe is provided
- Assume structure without checking against content and intent
- Generate wireframe without asking user first

## Error Handling

- No design.json: suggest running extract design first
- No content context: ask user for page purpose and key sections
- Wireframe format not readable: ask user to describe the layout
- Structure too complex: suggest splitting into multiple pages

## Next Steps

After structure is approved, suggest:
- "Run preview to see the design with visual style applied"
