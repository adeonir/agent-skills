# Create Milestone

Define a delivery phase and record it in the milestones registry, so its
epics can be decomposed from it.

## When to Use

- User says "create milestone", "new milestone", "add milestone", "define
  milestones", "plan milestones"
- The delivery splits into phases and those phases are not yet recorded
- Before decomposing a milestone into epics, when the milestone does not
  exist yet

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Read Context

Look for `docs/product/PRD.md`. If it exists, read its requirements,
journeys, and scope to decide what each phase delivers.

**Read for context only.** The PRD stays the source of product requirements;
its tokens never cross verbatim into the milestone. Strip PRD IDs (FR-N, BR-N,
EC-N), section numbers (§x.x), and any cross-reference that doesn't stand
alone — the milestone authors its own outcome and scope in plain language.

If there is no PRD, derive the phases from the user directly. The registry
never depends on the PRD existing.

### 2. Draft the Entry

Fill the registry-entry template (below):

- **Name**: kebab-case slug — the stable key the epic's `milestone:` pointer
  matches (`checkout-sem-friccao`). No numeric prefix, declarative.
- **Title**: short human-readable phrase (`Checkout sem fricção`) — the name
  the tracker grouping (GitHub Milestone / Linear Initiative) uses on push.
- **Outcome**: the capability this phase delivers and the value it unlocks —
  one or two sentences, plain language.
- **Scope boundary**: what this phase includes and what it defers. Resolves
  ambiguity a later epic sketch might introduce.
- **Expected epics**: a light sketch — capability area + one line each.
  **Seeds, not specifications.** Each names a capability or objective, never a
  UI widget, field list, endpoint, or technology. The delivery breakdown is
  decided later in [decompose.md](decompose.md), not here.
  - Good: `checkout-rapido — comprador conclui a compra sem recriar dados a cada vez`
  - Bad: `checkout-rapido — botão de 1-clique no carrinho` (a UI mechanism, not a capability)
  - Bad: `historico-pedidos — tabela com data, valor e status` (UI fields, not the objective)

A milestone carries no success criteria and no acceptance criteria — it is
"done" when its epics are delivered (a rollup).

### 3. Save to the Registry

The registry is a single file: `.artifacts/epics/milestones.md`.

1. If the file does not exist, create it with the `# Milestones` heading.
2. If an entry with this name already exists, update it in place — never
   duplicate. Otherwise append the new entry.
3. Entry order is delivery sequence; place the entry where the phase falls.

This workflow only records milestone definitions; it does not create epics.

## Guidelines

**DO:**
- Author the outcome and scope in plain language, independent of the PRD
- Keep expected epics as capability seeds, not specifications
- Update an existing entry in place; never create a duplicate
- Order entries by delivery sequence

**DON'T:**
- Copy PRD requirements, IDs, or section numbers into the entry (contrasts:
  read for context, author in plain language)
- Add success criteria or acceptance criteria (contrasts: a milestone is done
  by rollup of its epics)
- Let expected epics name UI widgets, fields, endpoints, or technologies
  (contrasts: name a capability or objective)

## Template

The registry is a list: a `# Milestones` heading once, then one `##` block
per milestone in delivery order. ALWAYS use this exact structure:

````markdown
# Milestones

## {{milestone-name}}

- **Title:** {{Milestone Title}}
- **Outcome:** {{capability this phase delivers and the value it unlocks}}
- **Scope boundary:** {{what this phase includes and what it defers}}
- **Expected epics:**
  - {{epic-name}} — {{one-line capability expectation}}

## {{next-milestone-name}}

- **Title:** {{Milestone Title}}
- **Outcome:** {{capability this phase delivers and the value it unlocks}}
- **Scope boundary:** {{what this phase includes and what it defers}}
- **Expected epics:**
  - {{epic-name}} — {{one-line capability expectation}}
````

MUST NOT contain: success criteria, acceptance criteria, per-story detail,
PRD IDs (FR-N, BR-N, EC-N), section numbers, or implementation specifics.

## Error Handling

- No PRD found: proceed from the user's input; the registry never requires a PRD
- Milestone name conflicts with an existing entry: update it in place or
  confirm a rename
- Registry file malformed: report the issue, suggest manual fix
