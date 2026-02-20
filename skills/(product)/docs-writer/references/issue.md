# Issue -- Bug Report, Feature Request, Discussion

## Workflow

```
classification --> [discovery] --> drafting
```

First, classify the issue subtype. Discovery depth depends on the subtype.

## Phase 1: Classification

Ask the user or detect from trigger:

| Trigger | Subtype |
|---------|---------|
| "report bug" | Bug |
| "feature request" | Feature |
| "create discussion" | Discussion |
| "create issue" | Ask user which subtype |

## Phase 2: Discovery (subtype-dependent)

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

### Bug (no discovery -- structured reproduction)

Skip interview. Collect structured fields directly:

1. **What happened?** (actual behavior)
2. **What should have happened?** (expected behavior)
3. **How to reproduce?** (step-by-step)
4. **Environment** (OS, browser, version, etc.)
5. **Severity** (critical / high / medium / low)
6. **Screenshots or logs?** (optional)

### Feature (1-2 discovery stages)

**Stage 1 -- Problem:**
- What problem does this feature solve?
- Who is affected?
- How are they currently working around it?

**Stage 2 -- Solution (optional, if user has ideas):**
- What is the proposed solution?
- Are there alternatives?
- What is the expected impact?

### Discussion (1 discovery stage)

**Stage 1 -- Context:**
- What is the topic?
- What context is needed to understand it?
- What specific questions or decisions need to be addressed?

## Phase 3: Drafting

**USE TEMPLATE:** `templates/issue.md`

The template adapts based on subtype. Fill in the fields collected during classification and discovery.

## Schema by Subtype

### Bug

- **Title**: Short description of the bug
- **Severity**: Critical / High / Medium / Low
- **Actual Behavior**: What happened
- **Expected Behavior**: What should have happened
- **Reproduction Steps**: Numbered step-by-step
- **Environment**: OS, browser, version, runtime
- **Logs / Screenshots**: Optional attachments or references
- **Notes**: Additional context

### Feature

- **Title**: Short description of the feature
- **Problem Statement**: What problem this solves
- **Proposed Solution**: How to solve it
- **Alternatives Considered**: Other approaches (if discussed)
- **Impact**: Who benefits and how
- **Priority**: P1 / P2 / P3
- **Notes**: Additional context

### Discussion

- **Title**: Topic for discussion
- **Context**: Background information
- **Open Questions**: Specific questions to address
- **Notes**: Additional context

## Output

Save to: `.artifacts/docs/issue.md`
