# Signals and Lessons

The local memory layer that records verified failures and promotes recurring project rules into guidance.

## When to Use

During implement and audit when a verified failure is found; during tasks when report signals are triaged; during audit when signals are promoted; and during specify and design when confirmed lessons are loaded.

## The distinction

- A **finding** is the detailed, actionable observation in `validate.md` or `audit.md`.
- A **signal** is a structured, persistent record of an eligible finding in the feature's `SIGNALS.md`.
- A **lesson** is a short, general rule promoted from signals that recur across distinct features.
- A task in `tasks.md` is the correction derived from a verified finding, not a copy of the finding.

The flow is:

```text
finding in a phase report
  → signal in .artifacts/specs/{slug}/SIGNALS.md
  → recurrence across features
  → candidate lesson in .artifacts/LESSONS.md
  → confirmed lesson loaded by specify/design
```

## Signals

`SIGNALS.md` is Markdown, machine-owned, local to one feature, and excluded from commits. Only `scripts/signals.py` writes it.

### Producers

`implement` and `audit` may add signals. Add a row only when the phase verifies a failure of an upstream artifact, contract, test, task, or repository rule. Do not signal a temporary check failure that the same run corrects.

`validate` adds none. A lesson is a general rule about how the project builds, and stating one takes having seen the mechanism; validate never opens code, so it sees that an outcome diverged and never why. Its findings stay in `validate.md` and reach correction through `STATE.md`.

### Format

```markdown
# Signals: {slug}

| Code | Phase | Reference | Report | Status |
|------|-------|-----------|--------|--------|
| agreed-behavior | audit | AC-1.1 | audit.md#1 | open |
```

`Reference` identifies the affected contract or artifact, such as `AC-N.M`, `G-N`, `T-N`, `OQ-N`, or `file:line`. `Report` points to the detailed row in `audit.md`.

The signal identity is `Code + Reference` while the signal is open. A repeated run does not duplicate an open signal. A PASS resolves the corresponding signal; a later recurrence creates a new occurrence with the same code and reference.

### Codes

Use only these codes:

| Code | Meaning |
|------|---------|
| `agreed-behavior` | The delivery contradicts an agreed observable behavior. |
| `test-case` | A required test is missing, weak, or does not prove the behavior. |
| `test-suite` | The declared suite or gate is red or absent where required. |
| `planned-task` | A completed task has no corresponding implementation or proof. |
| `source-code` | The delivery contradicts a design or repository rule. |
| `spec-defect` | The spec asks for more than its goal or benefit supports. |
| `open-question` | A required open question remains unresolved at the gate. |

### Commands

Use the script from the skill directory:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/signals.py add \
  --spec-dir .artifacts/specs/{slug} \
  --code agreed-behavior \
  --phase audit \
  --reference AC-1.1 \
  --report audit.md#1

python3 ${CLAUDE_SKILL_DIR}/scripts/signals.py resolve \
  --spec-dir .artifacts/specs/{slug} \
  --code agreed-behavior \
  --reference AC-1.1
```

## Lessons

`LESSONS.md` is Markdown, machine-owned, local to the project workspace, and excluded from commits. It lives at `.artifacts/LESSONS.md`. Only `scripts/lessons.py` writes it.

### Sections and status

```markdown
## Confirmed

## Candidates

## Quarantined
```

| Status | Meaning | Loaded as guidance |
|--------|---------|--------------------|
| `candidate` | Grounded in one feature and not yet corroborated. | no |
| `confirmed` | The same rule recurred in two or more distinct features. | yes |
| `quarantined` | The rule was loaded and the warned failure recurred. | no |

Every entry carries a permanent `L-NNN` id, one canonical rule sentence, its signal code, the features that grounded it, and its signal references.

### Promotion and retirement

- `add` refuses a lesson unless `--source` points to the 1-based signal row in the named feature's `SIGNALS.md` (`.artifacts/specs/{slug}/SIGNALS.md#{row}`).
- Recurrence counts distinct feature slugs, not repeated runs of one feature.
- The agent supplies the judgment, the evidence, and the general rule sentence.
- The script owns IDs, exact-after-normalization deduplication, recurrence, rendering, and status changes.
- `penalize` records that a confirmed lesson failed when loaded; two penalties move it to `quarantined`.
- A quarantine is final and is never promoted again.
- A clean PASS produces no lesson.
- Load only `confirmed` lessons in `specify` and `design`; never load candidates or quarantined lessons as guidance.

### Commands

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py add \
  --feature {slug} \
  --signal agreed-behavior \
  --source .artifacts/specs/{slug}/SIGNALS.md#1 \
  --text "Assert the persisted status value, not the field's presence"

python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py list --status confirmed
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py penalize --id L-001 --feature {slug}
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py normalize
```

Phrase one short, actionable rule per signal. Use the same canonical wording when the rule recurs; deduplication is exact after normalization, not semantic.
