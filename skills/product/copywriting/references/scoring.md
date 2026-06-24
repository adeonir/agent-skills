# Scoring

The shared rubric for copywriting evaluation: severity, score bands, and the
report shape that `critique.md` and `audit.md` both produce.

## When to Use

Composed by `critique.md` (quality verdict on a draft or direction) and
`audit.md` (ship-readiness report on `copy.yaml`). It carries the numbers and
the template; the modes supply the findings. Not a direct trigger.

## Severity (P0–P3)

Tag every finding, in both modes, with one level:

| Priority | Name | Meaning | Action |
|---|---|---|---|
| **P0** | Blocking | Misleads the reader, or blocks comprehension or the action | Fix immediately |
| **P1** | Major | A claim with no proof, real friction, or off-register voice | Fix before ship |
| **P2** | Minor | Reads as slop a reader would notice; weak but not broken | Fix next pass |
| **P3** | Polish | No real reader impact | Fix if time permits |

Unsure between two levels? Ask "would this cost a conversion or mislead the
reader?" If yes, it is at least P1.

`anti-patterns.md` rules carry an `error | warning` severity. Map them into
findings: **error → P0/P1** (P0 if it misleads or blocks, else P1);
**warning → P2/P3** (P2 if a reader would notice, else P3).

## Score bands

Each dimension scores **0–4**: 0 absent, 1 major gaps, 2 partial, 3 good with
minor gaps, 4 genuinely excellent. Be honest — a 4 is rare; most real copy lands
mid-scale.

**Critique — the seven sweeps as judgment axes, total /28:**

Score Clarity, Voice consistency, So what, Prove it, Specificity, Heightened
emotion, and Zero risk (defined in [editing-sweeps.md](editing-sweeps.md)) 0–4 each.

| Band | Total | Reading |
|---|---|---|
| Excellent | 25–28 | Ship; polish only |
| Good | 20–24 | Address the weak sweeps |
| Acceptable | 14–19 | Real work needed |
| Poor | 8–13 | Major rewrite |
| Critical | 0–7 | Start over from intent |

Each weak axis maps straight to the matching refresh sweep — that is the loop.

**Audit — five ship-readiness dimensions, total /20:**

Score Readability, Claim integrity, Conversion readiness, Microcopy
correctness, and Anti-pattern density 0–4 each.

| Band | Total | Reading |
|---|---|---|
| Excellent | 18–20 | Minor polish |
| Good | 14–17 | Address weak dimensions |
| Acceptable | 10–13 | Significant work |
| Poor | 6–9 | Major overhaul |
| Critical | 0–5 | Not ready to ship |

## Report template

Here is a sensible default format, but use your best judgment — the verdict
leads, the score supports it, and the findings are ordered by severity:

```markdown
## Verdict

{Slop verdict (critique) or anti-pattern verdict (audit): does this read as
distinctive / trustworthy, or generic / AI-written? One honest paragraph.}

## Score

{Sweep or dimension table with a per-row key issue, total /28 or /20, band.}

## Findings

### P0 — Blocking
- **{name}** — {where: the copy.yaml path or the line}. {why it costs the
  reader}. {fix}.

### P1 — Major
- ...

### P2 / P3
- {grouped; one line each}

## Strengths

{2–3 things working, and why — so they survive the next edit.}
```

## Required shape

The layout is flexible; these invariants are not. Whatever the format:

- the score table lists **every** axis (all seven sweeps for critique) or
  dimension (all five for audit) — none dropped;
- the printed total equals the sum of the rows;
- every finding carries its `copy.yaml` path or the quoted line, a severity
  (P0–P3), the reader impact, and a fix.

critique and audit self-check these before presenting the verdict.

## Acting on findings

copywriting owns the fix, so the loop closes inside the skill — but critique and
audit themselves never write. Map each finding to a concrete next step, in
priority order (P0 first):

- A weak critique axis → the matching `refresh` sweep (Clarity → clarity pass,
  Prove it → prove it pass, and so on); re-critique after.
- An off-register voice that needs more than tightening → `revoice`.
- An audit defect on shipping copy → `refresh` for wording, `write` for a missing
  part. Apply it as that operation; the judgment modes report, they do not patch.

Never present a fix as applied — critique and audit produce the verdict; a
permanent change is the relevant authoring operation, confirmed before write.
