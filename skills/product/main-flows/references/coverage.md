# Coverage and Output

Verify that every PRD journey, BR, and EC is exercised by at least
one drafted flow (or explicitly listed as not exercised), then write
the final artifact.

## When to Use

Load after [drafting.md](drafting.md) quality gate passes. Run before
saving `flows.md`. In update mode, re-run coverage even when a single
flow changed — a new branch may close an orphan or a removed branch
may open one.

## Workflow

```
build matrix --> resolve orphans --> write artifact --> hand off
```

### Step 1: Build the Coverage Matrix

For each PRD reference (J-N, FR-N, BR-N, EC-N), record which flow's
References section cites it. The matrix has one row per reference and
one column per flow. A cell is filled when the flow cites that
reference.

```
| Ref   | J-1 | J-2 | F-{name} | F-{name} | ... |
|-------|-----|-----|----------|----------|-----|
| J-1   |  X  |     |          |          |     |
| J-2   |     |  X  |          |          |     |
| BR-1  |  X  |     |    X     |          |     |
| BR-10 |     |     |          |          |     |
| EC-3  |  X  |     |          |          |     |
```

A row with no `X` is an orphan — a rule that no flow exercises.

### Step 2: Resolve Orphans

Each orphan falls into one of three buckets. Assign every orphan to
exactly one bucket before proceeding:

| Bucket | Meaning | Action |
|--------|---------|--------|
| Missing flow | The orphan needs a flow that was not drafted | Loop back to discovery, add the flow, redraft |
| Wrong reference | A drafted flow exercises the orphan but failed to cite it | Update the flow's References section, re-build the matrix |
| Not exercised by flows | The orphan is a pure-data invariant or static config that flows do not exercise | List in the artifact's "Not Exercised by Flows" section with reason |

Pure-data invariants are common — examples include format
constraints (`BR-N: {attribute} must be {format}`), enum bounds
(`BR-N: {attribute} must be one of [...]`), or referential integrity
rules. These belong in the entity definition in `domain.md`, not in
a flow.

When listing in the artifact's "Not Exercised by Flows" section, use
this exact shape so each line carries both the reason and the
domain-side anchor:

```
- **BR-N** — {one-line reason} (lives in `domain.md` as
  `Entity.invariant`)
```

Concrete examples:

```
- **BR-N** — {attribute} must be one of [{enum values}]; enum-bound
  invariant enforced at the entity boundary (lives in `domain.md` as
  `Entity.invariant`).
- **BR-N** — {referenced entity} must exist before {referencing
  entity} can be created; referential integrity rule (lives in
  `domain.md` as a relationship constraint between {Entity A} and
  {Entity B}).
```

Do not silently drop an orphan. Every orphan must end up either as a
new flow, a corrected reference, or a documented non-exercise.

### Step 3: Write the Artifact

Save to `.artifacts/docs/flows.md` using the output template. The
file structure is fixed; flow ordering inside each context section
follows the inventory order from discovery.

### Step 4: Hand Off

After saving, suggest the next planning phase (typically the
architecture step that consumes flows). In update mode, append a row
to `## Processed Gaps` in `.agents/knowledge.md`:

```markdown
| Date | Gap ID | Resolution |
|------|--------|------------|
| YYYY-MM-DD | FG-N | {one-line summary of what changed} |
```

## Output Template

ALWAYS use this exact artifact structure:

```markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources:
  - .artifacts/docs/prd.md
  - .artifacts/docs/domain.md
---

# Main Flows — {{Project Name}}

## Coverage Matrix

| Ref | Flow IDs |
|-----|----------|
| J-1 | J-1 |
| FR-1 | J-1, F-{name} |
| BR-1 | J-1 |
| ... | ... |

## Not Exercised by Flows

- BR-N — {one-line reason} (lives in `domain.md` as
  `Entity.invariant`)
- BR-N — {one-line reason}

## Foreground Flows

### {Bounded Context A}

{flows here, one per template instance from drafting.md}

### {Bounded Context B}

{flows here}

## Background Flows

### {Bounded Context A}

{background flows here}

### {Bounded Context B}

{background flows here}
```

## Quality Gate

Before saving `flows.md`, verify:

- [ ] Every PRD journey (J-N) has a foreground flow with the same ID
- [ ] Every FR with a non-user trigger has a background flow (or an
      explicit decision to skip recorded during inventory)
- [ ] Every BR-N and EC-N appears in at least one flow's References,
      or is listed in "Not Exercised by Flows" with a reason
- [ ] Every state transition cites a state defined in `domain.md`
- [ ] Every emitted event uses a kind defined in `domain.md` (no
      invented kinds)
- [ ] No implementation details (no API endpoints, no SQL, no
      framework function names, no file paths)
- [ ] Coverage matrix is rebuilt and re-checked after any orphan fix
- [ ] Update mode appends a `## Processed Gaps` row (if applicable)

## Next Steps

Hand off downstream. The artifact at `.artifacts/docs/flows.md` is
the contract: architecture decisions and implementation specs trace
back to flow steps, side effects, and cross-context boundaries.
