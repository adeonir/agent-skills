# Lessons Layer

A project-local learning layer: audit failures become candidate lessons, recurrence confirms them, and confirmed lessons load into future specify and design phases. Managed by `scripts/lessons.py`.

## When to Use

During audit, when judging whether a FAIL is worth recording (write). During specify and design, when loading confirmed lessons as context (read). The skill itself never changes — the project's lesson set improves, guiding the agent on future features.

## Mechanics

- After an audit FAIL, judge whether the failure is worth a lesson. If so, add it as a `candidate`.
- When the same lesson recurs across two distinct features, it becomes `confirmed`.
- `confirmed` lessons are loaded in **specify** and **design**.
- A clean PASS records nothing.

## Files

| File | Role |
|------|------|
| `scripts/lessons.py` | add, list, promote, normalize, render lessons |
| `.artifacts/lessons.json` | canonical state (machine-owned) |
| `.artifacts/LESSONS.md` | rendered for reading (never hand-edit) |
| `.artifacts/CONTEXT.md` | lessons that became project-level decisions/gotchas |

## `lessons.json` format

```json
{
  "lessons": [
    {
      "id": "L-001",
      "text": "Card-validation ACs need a discrimination check that fails if the rule is removed",
      "origin": "validation.md: AC-2 survived mutation",
      "status": "confirmed",
      "features": ["checkout-2026-07-01", "payment-2026-07-10"],
      "created": "2026-07-01",
      "confirmed_at": "2026-07-10"
    }
  ]
}
```

## Commands

Run the bundled script; it owns `lessons.json` and re-renders `LESSONS.md`. Paths default to `.artifacts/` and are overridable with `--store` / `--render`.

```bash
# add a candidate lesson from an audit failure
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py add \
  --text "..." --origin "validation.md: AC-2 survived mutation" --feature "{slug}"

# list lessons (optionally filter by status)
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py list --status confirmed

# promote a candidate to confirmed when it recurs on a second feature
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py promote --id L-001 --feature "{slug}"

# normalize the store (dedupe, sort, backfill ids) and re-render
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py normalize

# re-render LESSONS.md from lessons.json
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py render
```

`add` auto-promotes to `confirmed` when the text already exists on a different feature, so recording the same lesson on a second feature confirms it in one step. `promote` forces the transition explicitly.
