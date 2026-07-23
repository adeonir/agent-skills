# Scoring

The shared rubric for craft-ui evaluation: severity, score bands, and the report shape that `critique.md` and `audit.md` both produce.

## When to Use

Composed by `critique.md` (direction verdict on a variant) and `audit.md` (defect report on a running UI). It carries the numbers and the template; the modes supply the findings. Not a direct trigger.

## Severity (P0–P3)

Tag every finding, in both modes, with one level:

| Priority | Name | Meaning | Action |
|---|---|---|---|
| **P0** | Blocking | Prevents the task; a showstopper | Fix immediately |
| **P1** | Major | Significant difficulty, confusion, or a WCAG AA violation | Fix before release |
| **P2** | Minor | Annoyance with a workaround | Fix next pass |
| **P3** | Polish | No real user impact | Fix if time permits |

Unsure between two levels? Ask "would a user contact support about this?" If yes, it is at least P1.

`anti-patterns.md` rules carry an `error | warning` severity for generation.
Map them into findings: **error → P0/P1** (P0 if it blocks use, else P1); **warning → P2/P3** (P2 if a user would notice, else P3).

## Score bands

Each dimension scores **0–4**: 0 absent, 1 major gaps, 2 partial, 3 good with minor gaps, 4 genuinely excellent. Be honest — a 4 is rare; most real interfaces land mid-scale.

**Critique — 10 Nielsen heuristics, total /40:**

| Band | Total | Reading |
|---|---|---|
| Excellent | 36–40 | Ship; polish only |
| Good | 28–35 | Address the weak heuristics |
| Acceptable | 20–27 | Real work needed |
| Poor | 12–19 | Major rework |
| Critical | 0–11 | Fundamental redesign |

Most real interfaces score 20–32. Treat anything claimed above 35 with suspicion unless every heuristic is genuinely clean.

**Audit — 5 technical dimensions, total /20:**

| Band | Total | Reading |
|---|---|---|
| Excellent | 18–20 | Minor polish |
| Good | 14–17 | Address weak dimensions |
| Acceptable | 10–13 | Significant work |
| Poor | 6–9 | Major overhaul |
| Critical | 0–5 | Fundamental issues |

## Report template

Here is a sensible default format, but use your best judgment — the verdict leads, the score supports it, and the findings are ordered by severity:

```markdown
## Verdict

{Slop verdict (critique) or anti-pattern verdict (audit): does this read as
distinctive / trustworthy, or AI-generated? One honest paragraph.}

## Score

{Heuristic or dimension table with a per-row key issue, total /40 or /20, band.}

## Findings

### P0 — Blocking
- **{name}** — {where}. {why it matters to the user}. {fix}.

### P1 — Major
- ...

### P2 / P3
- {grouped; one line each}

## Strengths

{2–3 things working, and why — so they survive the next change.}
```

## Acting on findings

Map each finding to a concrete next step, in priority order (P0 first):

- A variant that reads too safe or too noisy → re-render it with a tune verb (`bolder` / `quieter` / `distill` / `animate` / `delight` / `harden`).
- A structural gap (dangling flow, buried primary action, arrangement wrong for the register) → re-plan the structure phase and re-render ([structure.md](structure.md)).
- A technical or accessibility defect on a shipped UI → a source fix in implementation. craft-ui reports it; it does not apply it (non-mutating).

Never prescribe a fix craft-ui would have to mutate source to make — the report names the defect and its impact; the change happens in implementation.
