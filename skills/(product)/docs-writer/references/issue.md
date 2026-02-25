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

### Feature (1-2 topics)

#### Topic 1: Problem

**Opening questions:**
- What problem does this feature solve?
- Who is affected?
- How are they currently working around it?

**Deepen when:**
- Solution disguised as problem → "That sounds like a solution. What's the underlying pain?"
- Unclear who is affected → "Is this one person's request or a pattern you're seeing?"
- No workaround described → "How do people handle this today without the feature?"

**Sufficient when:**
- Clear problem with identified affected users
- Current workaround (or lack thereof) understood

#### Topic 2: Solution Direction (optional, if user has ideas)

**Opening questions:**
- What is the proposed solution?
- What changes for the user if this is built?
- Are there alternatives you've considered?

**Deepen when:**
- Only one approach considered → "What else could solve this?"
- Impact unclear beyond the feature → "Who else benefits? What second-order effects?"

**Sufficient when:**
- At least one approach described with expected impact
- Or user has no preference (mark as open for design)

### Discussion (1 topic)

#### Topic 1: Context

**Opening questions:**
- What is the topic?
- What context is needed to understand it?
- What specific questions or decisions need to be addressed?

**Deepen when:**
- Topic too broad → "Can we narrow this down? What's the most important aspect?"
- No clear questions → "What decisions need to come out of this discussion?"

**Sufficient when:**
- Topic is scoped and context is clear
- Specific questions or decisions are identified

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
