---
paths:
  - "skills/**/*.md"
---

## No Cross-Skill References

**Impact: MEDIUM**

A SKILL.md or reference never names another skill or links to a file in
another skill's directory. Skills ship standalone, so a cross-skill reference
breaks the moment the sibling is not installed. Composition between skills
happens through artifacts on disk, never through direct file links.

**Incorrect:**

```markdown
For the visual identity, see the design-brief skill's DESIGN.md.
```

**Correct:**

```markdown
Read the design tokens from the agreed artifact path; this skill never names
which skill produced them.
```

## Own-Artifact Isolation

**Impact: MEDIUM**

A skill names only the artifact it produces, never a sibling's output by name
or path, and states a boundary in terms of its own concern rather than where
the excluded thing lives. The one exception is an integrator — a renderer or
cross-artifact validator whose job is to compose several artifacts — which may
name what it integrates.

**Incorrect:**

```markdown
This plan carries no styling — styling belongs to DESIGN.md.
```

**Correct:**

```markdown
This plan carries no styling; it describes structure only.
```

## Inline Subagent Execution

**Impact: MEDIUM**

A skill executes inline by default. It may spawn a subagent only when
**context isolation** is the goal — the subagent receives a narrow,
task-specific input (a diff, a file) with no conversation history and returns
structured output. Spawning subagents for arbitrary parallelism or convenience
is not allowed.

**Incorrect:**

```markdown
Spawn one subagent per file to review them in parallel.
```

**Correct:**

```markdown
Spawn an isolated subagent with only the staged diff and the message schema —
no conversation context. The subagent returns `{type, subject, body}`.
```
