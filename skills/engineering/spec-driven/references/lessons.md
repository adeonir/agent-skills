# Lessons Layer

A project-local learning loop: audit failures become candidate lessons, recurrence confirms them, confirmed lessons load into future specify and design, and a lesson that fails as guidance is retired. Managed by `scripts/lessons.py`.

## When to Use

During audit, when a `validation.md` signal grounds a lesson (write) or when a loaded lesson failed to prevent the failure it warned about (penalize). During specify and design, when loading confirmed lessons as context (read). The skill itself never changes — the project's lesson set improves, guiding the agent on future features.

## The loop

The agent is stateless across features and the skill is static text, so the only way a project's hard-won knowledge reaches the next feature is by being written down and loaded back in. The audit is where that knowledge is produced: it is the one place a failure is established by an independent check rather than self-reported.

```text
detect (audit FAIL / spec defect)
  → quarantine (candidate)
  → confirm (same lesson, second feature)
  → inject (specify + design load confirmed)
  → measure (did the failure recur with the lesson loaded?)
  → retire (penalize → quarantined)
```

Every confirmed lesson is paid in tokens at the load step of every future feature, so entry needs a gate, permanence has to be earned, and there has to be an exit. The three ways the loop dies: ungrounded lessons enter (the gate stops it), no two lessons ever read the same so nothing promotes (the phrasing rules stop it), a lesson that no longer holds is loaded forever (the penalty stops it).

The split: the agent supplies judgment — read the failure, phrase the lesson, cite its grounding. The script owns everything mechanical — ids, recurrence counting, promotion, quarantine, dedupe. Hand-kept bookkeeping is what rots, so it is not the agent's job.

## Scope

A lesson is about **this codebase**: a rule a future feature in this project could apply. It is never about how to run the skill itself ("discuss earlier", "write more ACs") — that is a change to the skill, made by its maintainer, not a fact about the project. A candidate that reads as methodology is not recorded.

## Grounding

Only a row in `validation.md` grounds a lesson. No signal, no lesson — one without grounding is an opinion, and `add` refuses it (`--signal` and `--origin` are both required).

| `--signal` | The row that grounds it |
|------------|-------------------------|
| `goal_unmet` | `## Goals` — a goal at Unmet or Unmeasurable |
| `ac_fail` | `## Acceptance Criteria` — an AC at FAIL |
| `surviving_mutant` | `## Discrimination Sensor` — a mutant that survived and the main agent promoted to a gap |
| `spec_defect` | `## Spec Defects` — an AC over-specifying its goal |
| `suite_red` | `## Re-run` — the suite exits non-zero |

`## Gaps → Fix Tasks` is not a signal: every gap is derived from one of the rows above, and recording both counts the same failure twice.

A clean PASS — no unmet goal, no failed AC, no promoted survivor, no spec defect — records nothing. A survivor the judge declined is not a grounding row; it left no gap. That is the layer working, not a miss.

## Phrasing

Dedupe is exact-match on the text, so two lessons that mean the same thing but read differently never merge: each sits as a candidate on one feature and neither ever promotes. The layer then looks alive and injects nothing. Phrasing is what makes recurrence detectable.

- State the general rule, not the incident: `Assert the persisted status value, not the field's presence` — never `the subscription test at line 88 was weak`.
- Terse and canonical, so the same lesson written on a later feature comes out identical.
- One lesson per signal. Never bundle two rules into one text.

## Status

| Status | Meaning | Loaded as guidance |
|--------|---------|--------------------|
| `candidate` | Grounded but seen on one feature — could be an accident of that feature | no |
| `confirmed` | The same lesson recurred on a second distinct feature — a pattern of this codebase | yes |
| `quarantined` | Was loaded as guidance and the failure recurred anyway — the lesson does not work | no |

A quarantine is final: recurrence never revives it, since that would reinstate the exact lesson the penalty retired.

## Files

| File | Role |
|------|------|
| `scripts/lessons.py` | the only way to mutate lessons: add, list, promote, penalize, normalize |
| `.artifacts/LESSONS.json` | canonical state (machine-owned) |

The store is machine-owned — never hand-write it. The format is documented for reading only:

```json
{
  "lessons": [
    {
      "id": "L-001",
      "text": "Assert the persisted status value, not the field's presence",
      "signal": "surviving_mutant",
      "origin": "validation.md ## Discrimination Sensor: flip condition src/payment.ts:42 survived",
      "status": "confirmed",
      "features": ["checkout", "billing"],
      "penalties": 0,
      "created": "{YYYY-MM-DD}",
      "confirmed_at": "{YYYY-MM-DD}"
    }
  ]
}
```

## Commands

The store path defaults to `.artifacts/LESSONS.json` and is overridable with `--store`, on either side of the subcommand.

```bash
# record a lesson from a validation.md row (candidate; confirms on a second feature)
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py add \
  --text "..." \
  --signal surviving_mutant \
  --origin "validation.md ## Discrimination Sensor: flip condition src/payment.ts:42 survived" \
  --feature "{slug}"

# load the guidance (this is the read surface for specify and design)
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py list --status confirmed

# retire a lesson that was loaded and failed to prevent its own failure
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py penalize --id L-001

# force a candidate to confirmed without waiting for a second feature
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py promote --id L-001 --feature "{slug}"

# dedupe, sort, and backfill the store
python3 ${CLAUDE_SKILL_DIR}/scripts/lessons.py normalize
```

`add` auto-promotes to `confirmed` when the text already exists on a different feature, so recording the same lesson on a second feature confirms it in one step. `promote` forces the transition explicitly, on a single feature if need be — and `normalize` preserves that forced status when it merges duplicate texts, keeping the lower id and the earliest `created`. Two penalties quarantine a lesson, and `normalize` preserves a quarantine over any other status.

## Anti-Pattern: Loading the whole store

Reading `LESSONS.json` directly puts every `candidate` and `quarantined` lesson into the context window alongside the confirmed ones. A candidate is explicitly *not trusted yet* — it is a single-feature observation held in quarantine precisely because it may be an accident — and a quarantined lesson is one that already failed. Loading either as guidance defeats the promotion rule that is the whole point of the store. The read surface is `list --status confirmed`, never the file.
