# Main Flows

Trace each PRD journey and system-initiated process as a use case —
actor, goal, preconditions, main success scenario, extensions, entity
transitions, and side effects.

## What It Does

Bridge the gap between the domain model (entities, invariants,
lifecycle) and system design (architecture, components, NFRs):

```mermaid
flowchart LR
    D[Discovery] --> I[Inventory]
    I --> DR[Drafting]
    DR --> C[Coverage]
    C --> O[Output]
```

| Phase | What Happens | Output |
|-------|--------------|--------|
| Discovery | Read PRD + domain.md, extract user-initiated (per journey) and system-initiated (per FR trigger) candidates | Candidate list |
| Inventory | Confirm list with user, group by bounded context | Confirmed use case list |
| Drafting | Fill the per-use-case template (goal, trigger, actors, main success scenario, extensions, side effects, success guarantees) | Drafted use cases |
| Coverage | Build BR/EC matrix, resolve orphans, document non-exercises | Verified set |
| Output | Write the artifact and hand off downstream | `use-cases.md` |

## Usage

```
build main flows from the PRD
map flows for the journeys
trace journeys through the system
create use cases from the PRD
verify coverage
update flows — implementation found a gap
```

## Output

```
.artifacts/docs/use-cases.md
```

## Requirements

- `.artifacts/docs/prd.md` — produced upstream
- `.artifacts/docs/domain.md` — produced upstream

If either input is missing, the discovery phase stops and asks for it.

## FAQ

**Q: Are Mermaid diagrams required?**
A: No — recommended for user-initiated journeys where the visual
aids the reader, skipped for single-actor system-initiated use cases
where the diagram adds noise.

**Q: What goes in "Not Exercised by Use Cases"?**
A: Pure-data invariants (format constraints, enum bounds,
referential integrity) that live in entity definitions in
`domain.md`. Listing them keeps the coverage matrix honest without
forcing a use case that does not exist.

**Q: How does update mode work?**
A: When a downstream skill reports a gap, it writes a row to
`## Flow Gaps` in `.agents/knowledge.md`. The discovery phase reads
that queue, narrows scope to the gap, and after coverage completes,
appends a row to `## Processed Gaps`.

**Q: Can a use case span multiple bounded contexts?**
A: Yes — assign one primary context (the one that owns the
triggering entity) and list secondary contexts the use case touches.
Cross-context use cases must name every context they touch.
