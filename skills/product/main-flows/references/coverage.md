# Coverage and Output

Verify that every PRD journey, BR, and EC is exercised by at least
one drafted use case (or explicitly listed as not exercised), then
write the final artifact.

## When to Use

Load after [drafting.md](drafting.md) quality gate passes. Run before
saving `use-cases.md`. In update mode, re-run coverage even when a
single use case changed — a new branch may close an orphan or a
removed branch may open one.

## Workflow

```
build matrix --> resolve orphans --> write artifact --> hand off
```

### Step 1: Build the Coverage Matrix

For each PRD reference (J-N, FR-N, BR-N, EC-N), record which use
case's References section cites it. The matrix has one row per
reference and one column per use case. A cell is filled when the use
case cites that reference.

```
| Ref   | J-1 | J-2 | F-{name} | F-{name} | ... |
|-------|-----|-----|----------|----------|-----|
| J-1   |  X  |     |          |          |     |
| J-2   |     |  X  |          |          |     |
| BR-1  |  X  |     |    X     |          |     |
| BR-10 |     |     |          |          |     |
| EC-3  |  X  |     |          |          |     |
```

A row with no `X` is an orphan — a rule that no use case exercises.

### Step 2: Resolve Orphans

Each orphan falls into one of three buckets. Assign every orphan to
exactly one bucket before proceeding:

| Bucket | Meaning | Action |
|--------|---------|--------|
| Missing use case | The orphan needs a use case that was not drafted | Loop back to discovery, add the use case, redraft |
| Wrong reference | A drafted use case exercises the orphan but failed to cite it | Update the use case's References section, re-build the matrix |
| Not exercised by use cases | The orphan is a pure-data invariant or static config that use cases do not exercise | List in the artifact's "Not Exercised by Use Cases" section with reason |

Pure-data invariants are common — examples include format
constraints (`BR-N: {attribute} must be {format}`), enum bounds
(`BR-N: {attribute} must be one of [...]`), or referential integrity
rules. These belong in the entity definition in `domain.md`, not in
a use case.

When listing in the artifact's "Not Exercised by Use Cases" section,
use this exact shape so each line carries both the reason and the
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

Save to `.artifacts/docs/use-cases.md` using the output template. The
file structure is fixed; use case ordering inside each context
section follows the inventory order from discovery.

### Step 4: Hand Off

After saving, suggest the next planning phase (typically the
architecture step that consumes use cases). In update mode, append a
row to `## Processed Gaps` in `.agents/knowledge.md`:

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

# Use Cases — {{Project Name}}

## Coverage Matrix

| Ref | Use Case IDs |
|-----|--------------|
| J-1 | J-1 |
| FR-1 | J-1, F-{name} |
| BR-1 | J-1 |
| ... | ... |

## Not Exercised by Use Cases

- BR-N — {one-line reason} (lives in `domain.md` as
  `Entity.invariant`)
- BR-N — {one-line reason}

## User-Initiated Use Cases

### {Bounded Context A}

{use cases here, one per template instance from drafting.md}

### {Bounded Context B}

{use cases here}

## System-Initiated Use Cases

### {Bounded Context A}

{system-initiated use cases here}

### {Bounded Context B}

{system-initiated use cases here}
```

## Quality Gate

Before saving `use-cases.md`, verify:

- [ ] Every PRD journey (J-N) has a user-initiated use case with the
      same ID
- [ ] Every FR with a non-user trigger has a system-initiated use
      case (or an explicit decision to skip recorded during
      inventory)
- [ ] Every BR-N and EC-N appears in at least one use case's
      References, or is listed in "Not Exercised by Use Cases" with
      a reason
- [ ] Every state transition cites a state defined in `domain.md`
- [ ] Every emitted event uses a kind defined in `domain.md` (no
      invented kinds)
- [ ] No implementation details (no API endpoints, no SQL, no
      framework function names, no file paths)
- [ ] Coverage matrix is rebuilt and re-checked after any orphan fix
- [ ] Update mode appends a `## Processed Gaps` row (if applicable)

## Next Steps

Hand off downstream. The artifact at `.artifacts/docs/use-cases.md`
is the contract: architecture decisions and implementation specs
trace back to use case steps, side effects, and cross-context
boundaries.
