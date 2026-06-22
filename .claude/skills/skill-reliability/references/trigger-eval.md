# Trigger Reliability

Probe a skill's name and description as a retrieval surface, then draft fixes —
no execution, no eval runs.

## When to Use

Step 3 of the analysis: judging whether a skill fires on the right requests and
stays quiet on the wrong ones.

## Deterministic Pass

Run the linter first to catch the mechanical problems before any reasoning:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/trigger_lint.py <skill-dir>
```

It checks the frontmatter conventions: kebab-case `name`, third-person
description with inline "Use when" triggers, the length envelope, and the
anti-patterns (filler openings, a numbered `(1)…(2)` trigger list, first/second
person, reserved name tokens). Treat its findings as the structural floor; reason
about the rest below.

## Probe Set

Generate a small, decision-relevant set of requests — not an exhaustive suite:

- 1–2 **explicit** — the user names the capability directly
- 2–3 **implicit** — the user describes the intent without naming the skill
- 2 **negative** — adjacent requests that must NOT fire
- 1 **ambiguous** — a boundary case

For each probe, reason about two things and compare them:

- **Would** the current description fire? (retrieval match)
- **Should** it fire? (intended scope)

## Diagnosis

| Symptom | Verdict | Fix direction |
|---------|---------|---------------|
| Misses explicit/implicit probes | Narrow | add missing task-family, file-type, or synonym terms |
| Fires on negative probes | Leaky | remove overloaded nouns and generic verbs ("helps with") |
| Right on every probe | Clean | leave the description alone |

## Description Rewrite

When a probe misses, propose the smallest description change that fixes it
without overfitting — generalize to the intent category, never append a growing
list of literal queries. Hold the rewrite to the repo conventions:

- imperative and intent-first ("Use when …", not "this skill does …")
- third person, distinctive enough to compete with sibling skills
- triggers woven into prose, never a separate numbered list
- under the 1024-character description cap

Report the verdict (Clean / Leaky / Narrow), the probes that drove it, and the
rewrite if any. The rewrite is applied to the target's SKILL.md only on the
user's confirmation (Step 8 of the analysis), never silently.
