# Issue -- Bug Report, Feature Request, Discussion

## When to Use

When reporting bugs, requesting features, or creating discussion topics.

## Workflow

```
classification --> [clarification] --> drafting
```

First, classify the issue subtype. Then check for existing context. Clarification depth depends on the subtype and available context.

## Step 1: Classification

Ask the user or detect from trigger:

| Trigger | Subtype |
|---------|---------|
| "report bug" | Bug |
| "feature request" | Feature |
| "create discussion" | Discussion |
| "create issue" | Ask user which subtype |

## Step 2: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and use as context. PRD provides problem (section 1), personas (section 3), scope (section 4), journeys (section 5), business rules (section 6), and edge cases (section 7) that inform issue writing. Less clarification needed.

If no PRD exists: rely on user input and clarify more proactively.

## Step 3: Clarification (subtype-dependent)

### Bug (no clarification -- structured collection)

Collect structured fields directly:

1. **What happened?** (actual behavior)
2. **What should have happened?** (expected behavior)
3. **How to reproduce?** (step-by-step + reproduction link if applicable)
4. **Did this work before?** (last working version for regression detection)
5. **Environment** (OS, browser, version, etc.)
6. **Workaround?** (any known mitigation -- critical for triage prioritization)
7. **Screenshots or logs?** (optional)

### Feature (when input is incomplete)

**Sufficient when:**
- Clear problem with identified affected users
- Current workaround (or lack thereof) understood

**Clarify when:**
- Solution disguised as problem → "That sounds like a solution. What's the underlying pain?"
- Unclear who is affected → "Is this one person's request or a pattern you're seeing?"
- No workaround described → "How do people handle this today without the feature?"

If the user has a proposed solution, capture it. If not, mark as open for design.

### Discussion (when input is incomplete)

**Sufficient when:**
- Topic is scoped and context is clear
- Specific questions or decisions are identified

**Clarify when:**
- Topic too broad → "Can we narrow this down? What's the most important aspect?"
- No clear questions → "What decisions need to come out of this discussion?"

## Drafting

**USE TEMPLATE:** `templates/issue.md`

The template adapts based on subtype. Fill in the fields collected during classification and clarification.

## Schema by Subtype

### Bug

- **Title**: Short description of the symptom
- **Priority**: Critical / High / Medium / Low
- **Actual Behavior**: What happened
- **Expected Behavior**: What should have happened
- **Reproduction Steps**: Numbered step-by-step
- **Reproduction Link**: Public repo, sandbox, or minimal reproduction
- **Last Working Version**: Version or commit where this worked, or "Unknown"
- **Environment**: OS, browser, version, runtime
- **Workaround**: Known mitigation, or "None known"
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

## Guidelines

- Bug titles should describe the symptom, not the cause: "Login fails with 500 error" not "Fix auth middleware"
- Feature requests should describe the problem, not prescribe the solution
- Severity levels are about business impact, not technical complexity
- Always check for existing PRD context before asking clarification questions
- Keep discussions scoped -- one topic per issue

## Output

Save to: `.artifacts/docs/issue.md`
