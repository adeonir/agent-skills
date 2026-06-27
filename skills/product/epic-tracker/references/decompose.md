# Decompose Milestone

Turn a milestone into the set of epics it needs, seeding each from the
milestone's expected-epics sketch.

## When to Use

- User says "decompose milestone", "break down milestone",
  "create epics from a milestone"
- A milestone is defined in the registry and its epics have not been created
- A milestone needs its delivery broken into epics before story work begins

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Locate the Milestone

1. Read `.artifacts/epics/milestones.md`. If it does not exist, route the user
   to define a milestone first via [milestone.md](milestone.md) (epics can
   still be created directly via [epic.md](epic.md)).
2. List the registry's milestones. If more than one, ask which to decompose.
3. Read the chosen milestone's Outcome, Scope boundary, and Expected epics.

**Read for context only.** The milestone stays in the registry; its tokens never
cross verbatim into any epic. The Expected epics sketch is a set of seeds —
capability area plus a one-line expectation each — not epic definitions.

### 2. Confirm the Epic Set

1. Check which epics already exist for this milestone — scan
   `.artifacts/epics/` (or the tracker) for epics whose `milestone:` matches.
   Re-running over a living registry is expected: propose only the **missing**
   epics, and never recreate or overwrite one that exists.
2. Cleanse each seed before presenting it:
   - If a seed describes a UI widget, field list, endpoint, technology, or
     implementation mechanism (e.g., "tooltips no primeiro RPD" or "lista
     com nome, último registro e atividade"), translate it into an objective
     or capability (e.g., "conduz o paciente ao primeiro registro sem ajuda
     externa" or "visão consolidada dos pacientes do terapeuta").
   - If a seed is just one field, indicator, or small sub-feature of another
     sketched epic (e.g., "status-engajamento" that is only a weekly activity
     badge inside a patient dashboard), propose merging it into the broader
     epic rather than creating a separate one.
3. Present the cleansed missing epics as a proposed set, noting any
   translations or merges applied.
4. Let the user add, drop, merge, split, or rename. The sketch is a starting
   point, not a fixed list — the delivery breakdown is decided here, not in
   the registry.
5. Settle the epic set before creating anything.

This workflow only *adds* epics. When a milestone's definition changed and an
existing epic needs adjusting, that is a manual call — decompose does not
reconcile drift against epics already created.

### 3. Create Each Epic

For each confirmed epic, run the [epic.md](epic.md) creation flow, with two
additions specific to decomposition:

- Set frontmatter `milestone: {milestone-name}` — the epic's direct parent
  (see the translate-don't-replicate note in [epic.md](epic.md)). Record the
  pointer only; never copy the milestone's outcome, scope boundary, or
  deliverables into the epic body.
- Add a **Milestone** entry under the epic's References so the link travels
  into the tracker on push.

Each epic carries its own scope, rabbit holes, and stories — derived
here, never inherited from the sketch line.

### 4. Offer Story Breakdown

After the epics exist, offer to break each into stories via
[story.md](story.md), or leave story creation for later. Do not auto-create
stories — the user chooses when to go deeper.

## Guidelines

**DO:**
- Treat the Expected epics sketch as seeds, not specifications
- Confirm the epic set with the user before creating any epic
- Record the `milestone:` pointer on every epic created from a milestone
- Let each epic define its own scope and AC, independent of the sketch
- Re-run safely over a living registry: add only epics missing for the milestone, leaving existing ones untouched

**DON'T:**
- Copy the milestone's outcome, scope boundary, or deliverables into an
  epic body (contrasts: record the `milestone:` pointer, strip the content)
- Create epics the user has not confirmed (contrasts: settle the set first)
- Create stories automatically (contrasts: offer, let the user choose)

## Error Handling

- No registry found: route to defining a milestone first via `milestone.md`,
  or to `epic.md` for direct epic creation without a milestone
- Registry has no milestones defined: route the user to define one via
  `milestone.md` first, or proceed with direct epic creation
- Milestone has no Expected epics sketch: ask the user to outline the epics,
  or derive candidates from the milestone's Outcome and Scope boundary and
  confirm before creating
- Epic name conflicts with an existing epic: suggest an alternative or
  confirm overwrite (defer to `epic.md` handling)
