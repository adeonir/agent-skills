---
name: product-naming
description: >-
  Research and validate product names with domain and social media availability checks.
  Generates name candidates, checks .com/.com.br/.io/.app domains, verifies Instagram/X/GitHub
  usernames, and scores name quality (pronounceable, memorable, brandable).
  Use when: naming products, startups, apps, or brands. Also use when the user provides
  name candidates to evaluate, asks to check domain availability, wants name suggestions,
  or any naming-related task. Triggers on "check if a name is available", "suggest names for",
  "find a name for", "what should I call", "name ideas for", "domain available",
  "check this name", "evaluate these names".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Product Naming

Research, evaluate, and validate product/startup/app names with domain and social media availability checks.

## Workflow

```
detect entry --> [generate names] --> evaluate & filter --> output report
```

Two entry points: if the user already has candidates, skip generation and go straight to evaluation.

## Context Loading Strategy

Load references based on the detected entry point:

- **User has candidates**: load [evaluation.md](references/evaluation.md) only
- **User needs suggestions**: load [generation.md](references/generation.md) first, then [evaluation.md](references/evaluation.md)

The [tld-guide.md](references/tld-guide.md) is always loaded as part of the evaluation phase.

## Triggers

| Trigger Pattern | Entry Point | References |
|-----------------|-------------|------------|
| Suggest names, find a name, name ideas, what should I call | Generate + Evaluate | [generation.md](references/generation.md) + [evaluation.md](references/evaluation.md) |
| Check this name, is this name available, evaluate these names | Evaluate only | [evaluation.md](references/evaluation.md) |
| Check domain, domain available | Evaluate only (domain focus) | [evaluation.md](references/evaluation.md) |

Notes:

- [tld-guide.md](references/tld-guide.md) is not a direct trigger. It is loaded by [evaluation.md](references/evaluation.md) during domain checks.

## Cross-References

```
product-naming --> docs-writer (validated name feeds into PRD/Brief)
product-naming --> design-builder (chosen name informs brand/logo direction)
```

## Guidelines

**DO:**
- Use shell commands (dig, whois, curl) for domain and social media checks; fall back to web search if shell is unavailable
- Check .com and .com.br for every name (universal requirement)
- Add extra TLDs based on product type (see tld-guide.md)
- Bias invented names toward PT+EN bilingual phonetics
- Flag the strongest option as TOP PICK when one clearly stands out
- Present eliminated names with clear reasons

**DON'T:**
- Skip domain checks -- availability is critical for final decisions
- Do deep legal/trademark research -- flag obvious conflicts only
- Eliminate names solely on domain unavailability (note as caveat instead)
- Use emojis outside of status indicators (availability uses traffic light emojis only)
- Generate more than 20 candidates (keep focused)

## Output

Reports are saved as `.md` files in `.artifacts/docs/` (create the directory if needed). Each template generates a separate file:

- **Template A**: `.artifacts/docs/{product}-research.md`
- **Template B**: `.artifacts/docs/{product}-validation.md`

Two report templates in `templates/report.md`:

- **Template A (Name Research)**: full flow with candidates, availability, comparison, and eliminated names
- **Template B (Name Validation)**: per-name quality table, availability, risk assessment, and verdict

Status indicators: 🟢 disponivel  🔴 indisponivel  🟡 incerto

## Error Handling

- No product context provided: ask what the product does and who it's for
- Too many candidates (10+): batch shell commands or web searches for efficiency
- Domain check uncertain: mark as 🟡 and note it
- Shell rate-limiting: add delays between requests or switch to web search for remaining names
- No tools available (no shell, no web search): mark all availability as 🟡 Uncertain
- All candidates eliminated: suggest the user adjust constraints or generate a new batch
