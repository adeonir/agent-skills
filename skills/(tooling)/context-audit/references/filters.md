# The Five Filters

Qualitative judgment for catching dead-weight rules in CLAUDE.md, slash
commands, agents, and skill bodies. The script pre-flags candidates;
this file tells you how to confirm or reclassify them.

## When to Use

- Loaded in the reconcile-filters phase of the audit workflow
- Apply to every rule the script flagged in `flagged_rules` arrays
- Apply to instructions the script could not detect (cross-file
  contradictions, redundancy between user-scope and project-scope files)

## Workflow

For each candidate rule the script flagged, run the rule through the
filter that caught it. Confirm, reclassify, or drop the flag based on
context. Then scan for cross-file cases the script cannot detect.

### Filter 1: Default behavior

**Question:** Does Claude already do this without being told?

If yes, the rule is dead weight. Examples:

| Rule | Why flag |
|------|----------|
| "Write clean, readable code." | Default behavior. |
| "Handle errors appropriately." | Default behavior. |
| "Use descriptive variable names." | Default behavior. |
| "Don't expose secrets in logs." | Default behavior. |
| "Be helpful and accurate." | Default behavior. |

A rule passes this filter only when it specifies *how* to deviate from
the default. "Use single quotes for strings, never double" is fine
because it is a project-specific override.

### Filter 2: Contradiction

**Question:** Does this conflict with another rule, in this file or elsewhere?

The script cannot detect contradictions. Scan for them manually after
running the script. Common patterns:

- One CLAUDE.md says "use tabs", another says "use spaces"
- A skill says "always run tests" while CLAUDE.md says "skip tests on docs-only PRs"
- "Be concise" alongside "explain your reasoning step by step"

Resolution: pick the rule that wins more often, cut the other.

### Filter 3: Redundancy

**Question:** Is this already covered elsewhere?

Look for:

- The same rule restated in different words ("be concise" plus "keep it short" plus "don't be verbose")
- A rule in `~/.claude/CLAUDE.md` repeated in the project CLAUDE.md
- A skill repeating the project's general code-style rules

Cut the duplicate. Keep the version closest to where it actually applies.

### Filter 4: Bandaid

**Question:** Was this added to fix one specific bad output?

Bandaid rules are the silent killer. Pattern: model produces bad
output once, user adds a hyper-specific rule, file grows, future outputs
get worse because the model is now navigating dozens of edge-case rules.

Tells:

- Mentions a specific function name, file path, or error message
- Reads like a postmortem ("Don't do X like you did before")
- Solves a problem that has not recurred in months

Cut these. If the underlying issue still matters, replace with a
general principle in plain language.

### Filter 5: Vague

**Question:** Would the model interpret this differently each time?

Vague rules waste tokens and produce inconsistent output:

| Rule | Problem |
|------|---------|
| "Be natural." | Means anything. |
| "Use good tone." | Undefined. |
| "Write professionally." | Subjective. |
| "Don't overdo it." | Threshold unclear. |

Either rewrite with a concrete criterion ("Match the tone of the
existing README -- first person, no headers above h2") or cut.

## Guidelines

**DO:**
- Confirm each script-flagged rule against the filter that caught it
- Reclassify when context contradicts the heuristic (a rule that looks default may be a project override)
- Add cross-file contradictions and redundancies the script could not detect
- Record exact text, file path, line, filter, and one-line reason for the report

**DON'T:**
- Trust the script's pre-filter without reading the rule (contrasts: confirm against the filter)
- Skip cross-file contradictions because the script did not flag them (contrasts: add cross-file cases manually)
- Cut a project-specific override just because it pattern-matches (contrasts: reclassify when context contradicts heuristic)
- Record only the filter name without the reason (contrasts: record file, line, filter, and one-line reason)

## Error Handling

- Pre-filter flagged a rule that is actually a project override: drop the flag, do not report
- Multiple filters match the same rule: pick the most specific, note the others in the reason
- A rule is borderline: include it with a `?` qualifier in the report so the user decides
