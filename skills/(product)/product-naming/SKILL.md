---
name: product-naming
description: >-
  Research and validate product names with competitor analysis, quality
  scoring, domain and social media availability, and trademark checks. Use
  when naming products, startups, apps, or brands, evaluating name candidates,
  or checking domain availability.
when_to_use: >-
  Triggers on "suggest names for", "find a name for", "what should I call",
  "name ideas for", "evaluate these names", "check if a name is available",
  "domain available", "check this name", "check availability of".
effort: high
---

# Product Naming

**Recommended effort:** high for research and generation phases; medium for
availability-only checks.

Research, evaluate, and validate product/startup/app names with domain, social
media, and trademark checks. Use ultrathink for competitor analysis and quality
scoring.

## Workflow

```
detect entry --> research --> present --> validate* --> report
```

Two phases with implicit transition: the agent presents research results and the user decides whether to proceed to validation.

## Context Loading Strategy

Load references based on the detected entry point:

- **User needs suggestions**: load [research.md](references/research.md) first, then [validation.md](references/validation.md) after user approval
- **User has candidates for quality review**: load [research.md](references/research.md) only (scoring section)
- **User wants availability checks**: load [validation.md](references/validation.md) only

The [tld-guide.md](references/tld-guide.md) is always loaded as part of the validation phase.

## Triggers

| Trigger Pattern | Entry Point | References |
|-----------------|-------------|------------|
| Suggest names, find a name, name ideas, what should I call | Phase 1 (research + generation) --> Phase 2 (validation) | [research.md](references/research.md) + [validation.md](references/validation.md) |
| Evaluate these names (quality focus) | Phase 1 only (scoring, no generation) | [research.md](references/research.md) |
| Check availability, domain available, check this name | Phase 2 only (domains, socials, trademark) | [validation.md](references/validation.md) |

Notes:

- "Evaluate" is flexible -- it can enter Phase 1 or Phase 2 depending on context. Quality evaluation enters Phase 1; availability check enters Phase 2.
- [tld-guide.md](references/tld-guide.md) is not a direct trigger. It is loaded by [validation.md](references/validation.md) during domain checks.

## Cross-References

```
brainstorming  --> product-naming (direction feeds name generation context)
product-naming --> docs-writer    (validated name feeds into PRD/Brief)
product-naming --> design-builder (chosen name informs brand/logo direction)
```

## Guidelines

**DO:**
- Check domain availability for every name candidate
- Check .com and .com.br for every name (universal requirement); add .io and .app for tech/mobile products
- Add extra TLDs based on product type (see tld-guide.md)
- Bias invented names toward PT+EN bilingual phonetics
- Flag the strongest option as TOP PICK when one clearly stands out
- Present eliminated names with clear reasons
- Run competitor analysis before generating names
- Suggest name variations for top candidates

**DON'T:**
- Skip domain checks -- availability is critical for final decisions
- Eliminate names solely on domain unavailability (note as caveat instead)
- Use emojis outside of status indicators (availability uses traffic light emojis only)
- Generate more than 20 candidates (keep focused)

## Output

Reports are saved as `.md` files in `.artifacts/docs/` (create the directory if needed):

- **Research flow**: `.artifacts/docs/{product}-research.md` -- uses `templates/research-report.md`
- **Validation flow**: `.artifacts/docs/{product}-validation.md` -- uses `templates/validation-report.md`

Status indicators: 🟢 available  🔴 unavailable  🟡 uncertain

## Compact Instructions

Preserve:
- Current phase (research or validation), product context (what it does, audience, tone)
- Generated candidates with quality scores
- User approval on which candidates to validate

Drop:
- Competitor analysis raw output
- Intermediate generation scratch work

## Error Handling

- No product context provided: ask what the product does and who it's for
- Too many candidates (10+): batch availability checks for efficiency
- Domain check uncertain: mark as 🟡 and note it
- Rate-limiting: add delays between requests
- No tools available: mark all availability as 🟡 Uncertain
- All candidates eliminated: suggest the user adjust constraints or generate a new batch
- Trademark search returns no results: mark as 🟡 and recommend manual verification
