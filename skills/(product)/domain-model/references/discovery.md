# Discovery

Read the PRD artifact and identify candidate domain entities from
journeys, functional requirements, and business rules.

## When to Use

Always the entry point. Load before any other reference, in both
new-model and update modes.

## Workflow

```
read PRD --> extract candidates --> confirm with user --> gate
```

### Step 1: Locate PRD

Read `.artifacts/docs/prd.md`. If absent, ask the user to provide
a path or run docs-writer first.

In **update mode** (triggered by spec-driven domain gap): also read
`.artifacts/docs/domain.md` and `.agents/knowledge.md` `## Domain Gaps`
section to understand the current model and queued gaps before narrowing
scope.

### Step 2: Extract Candidates

Scan the PRD in this order:

1. Section 5 (User Journeys) — nouns that act, receive actions, or
   carry state are entity candidates
2. Section 6 (Business Rules BR-xxx) — subjects and objects of rules
3. Section 4 (Scope / FRs) — capabilities that imply persistent state
4. Section 7 (Edge Cases EC-xxx) — exceptional states reveal lifecycle

For each candidate, record:

- Name (singular noun)
- Source (journey step, FR-xxx, BR-xxx, or EC-xxx)
- Candidate type: Entity (has lifecycle) or Value Object (no lifecycle)

### Step 3: Confirm Candidates

Present candidate list to user. For each:

- Confirm entity vs. value object classification
- Identify missing entities the user knows exist
- Mark entities that belong together (candidate bounded contexts)

Do not proceed to `entities.md` until user confirms the list.

### Step 4 (Update Mode Only)

Narrow to the reported gap:

- Identify which entity or rule is missing or incorrect
- Confirm scope of the update with the user before loading `entities.md`

## Quality Gate

Before loading `entities.md`, verify:

- [ ] PRD has been read
- [ ] All journeys and BRs have been scanned for candidates
- [ ] Each candidate has a source (PRD reference)
- [ ] User has confirmed or amended the candidate list
- [ ] Update mode scope is confirmed (if applicable)

## Next Steps

Load [entities.md](entities.md).
