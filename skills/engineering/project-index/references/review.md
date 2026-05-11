# Review

Generate `.agents/codebase/review.md` — main agent self-assessment after the fan-out completes.

## When to Use

- Loaded by the **main agent** (not a sub-agent) after all 6 fan-out outputs are written
- Synthesizes cross-document consistency, completeness gaps, and concerns
- Cannot be split across sub-agents — main agent owns this synthesis

## Scope

Read all 6 newly-generated files together:

- `.agents/codebase/architecture.md`
- `.agents/codebase/conventions.md`
- `.agents/codebase/testing.md`
- `.agents/codebase/integrations.md`
- `.agents/codebase/checklist.md`
- `.agents/codebase/workflows.md`

Check for:

- **Consistency**: do service names, file paths, layer names, and patterns match across files?
- **Completeness**: are there areas the scan could not cover deeply? Flag them
- **Gaps**: what would an agent still need to know that is not documented?
- **Concerns**: outdated or vulnerable dependencies, inconsistent patterns, missing test coverage in critical areas, hard-coded values that should be configurable, security issues (exposed secrets, missing auth checks)

## Output

Save to `.agents/codebase/review.md`. Update existing on re-run.

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources: []
---

# Review

## Consistency Check

- {{pass/fail}} {{what was checked and result}}

## Completeness

### Well-Documented Areas

- {{area}}

### Areas Lacking Detail

- {{area}} — {{why and what's needed}}

### Recommendations

1. {{actionable recommendation}}

## Concerns

(omit this section entirely if no issues found)

| Area | Severity | Description |
|------|----------|-------------|
| {{area}} | {{high/medium/low}} | {{what and why it matters}} |

## Severity Guide

- **high**: stability, security, or correctness
- **medium**: slows development, complicates maintenance
- **low**: inconsistency or desirable improvement
````

## Guidelines

- Run only after all 6 fan-out outputs exist
- Concerns section: include only when real issues are detected, omit otherwise
- Recommendations are actionable, not aspirational
- Severity reflects impact on agents working in this codebase, not abstract code quality
