# Review

Generate `.agents/codebase/review.md` — main agent self-assessment after the fan-out completes.

## When to Use

- Loaded by the **main agent** (not a sub-agent) after all fan-out outputs are written
- Synthesizes cross-document consistency, completeness gaps, and concerns
- Cannot be split across sub-agents — main agent owns this synthesis

## Scope

Read all newly-generated fan-out files together:

- `.agents/codebase/architecture.md`
- `.agents/codebase/conventions.md`
- `.agents/codebase/testing.md`
- `.agents/codebase/integrations.md`
- `.agents/codebase/checklist.md`
- `.agents/codebase/workflows.md`
- `.agents/codebase/features.md` (when vertical slicing detected)

Check for:

- **Consistency**: do service names, file paths, layer names, and patterns match across files?
- **Completeness**: are there areas the scan could not cover deeply? Flag them
- **Gaps**: what would an agent still need to know that is not documented?
- **Concerns**: outdated or vulnerable dependencies, inconsistent patterns, missing test coverage in critical areas, hard-coded values that should be configurable, security issues (exposed secrets, missing auth checks)

## Output

Save to `.agents/codebase/review.md`. On re-run, follow [merge-policy.md](merge-policy.md).

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources:
  - .agents/codebase/architecture.md
  - .agents/codebase/conventions.md
  - .agents/codebase/testing.md
  - .agents/codebase/integrations.md
  - .agents/codebase/checklist.md
  - .agents/codebase/workflows.md
---

# Review

## Coverage Map

Confidence reflects how well the doc reflects current source. High = scan reached every priority listed in the ref. Medium = priorities mostly covered, sampling shallow in places. Low = scan blocked, gated by missing access, or skipped.

| Doc | Confidence | Scope Covered | Known Gaps |
|-----|-----------|---------------|------------|
| architecture.md | {{high/medium/low}} | {{layers, entries, flows hit}} | {{areas not scanned, with reason}} |
| conventions.md | {{high/medium/low}} | {{naming, errors, types, etc. covered}} | {{patterns left unscanned}} |
| testing.md | {{high/medium/low}} | {{test types sampled}} | {{gaps in coverage observed}} |
| integrations.md | {{high/medium/low}} | {{services and env vars seen}} | {{configs not opened}} |
| checklist.md | {{high/medium/low}} | {{scripts and tooling traced}} | {{commands without evidence}} |
| workflows.md | {{high/medium/low}} | {{user and dev flows traced}} | {{flows partially traced}} |
| features.md (if present) | {{high/medium/low}} | {{features cataloged}} | {{slices ambiguous}} |

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

- Run only after all fan-out outputs exist
- Concerns section: include only when real issues are detected, omit otherwise
- Recommendations are actionable, not aspirational
- Severity reflects impact on agents working in this codebase, not abstract code quality
- Coverage Map is mandatory — every fan-out output gets a row, even if confidence is high and gaps empty
- Confidence reflects scan thoroughness against the ref's Reading Priorities, not subjective doc quality
- `sources:` lists the fan-out docs read this run (review consumes them, not source code directly)
