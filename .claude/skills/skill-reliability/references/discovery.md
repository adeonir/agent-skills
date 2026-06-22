# Discovery

Determine scope and focus before running the analysis.

## When to Use

When `$ARGUMENTS` is empty, ambiguous, or the user asks to analyze multiple
skills or "all skills".

## Discovery Questions

Ask only what you need — most invocations provide a skill name and skip this
entirely.

**Scope** (ask when no argument):
> Which skill should I analyze? (e.g., `git-helpers`, `spec-driven`, or "all"
> to get a ranked list across the repo)

**Focus** (ask when the user's intent suggests a specific concern):
> Are you looking to:
> (a) understand where reliability is lowest and prioritize improvements
> (b) evaluate a specific step or workflow you already suspect

Do not ask both questions if one answer makes the other obvious.

## Scope Variants

**Single skill** (default): run the full workflow from SKILL.md and produce
the standard analysis report.

**All skills**: list every skill in `skills/` and `.claude/skills/`. Run the
step-map for each, then produce a ranked summary table:

| Skill | Workflows | Total steps | Weakest link | Est. end-to-end |
|-------|-----------|-------------|--------------|-----------------|
| ...   | ...       | ...         | ...          | ~X% (tier)      |

Sort by estimated end-to-end ascending (lowest first) — those are the
candidates to improve first.
