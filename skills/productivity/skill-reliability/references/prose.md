# Prose

The checks for a skill's instructions, and the bar a rewrite meets.

## Checks

- **No-op** — the instruction changes no behavior; the model does it unaided. Cut it.
- **Ambiguous** — two readings are possible. Name both, and keep one in the rewrite.
- **Duplicated** — the same rule in two places. Keep one.
- **Over-specified** — a procedure for a decision the model makes well. State the goal instead.
- **No done-when** — the step does not say when it is finished. Add the condition.

## The rewrite

Quote the line, name the check, and write the replacement in the skill's own voice. A rewrite that only adds emphasis does not count: it repeats the instruction louder. Report a no-op even when it changes no decision, because it costs tokens on every load.
