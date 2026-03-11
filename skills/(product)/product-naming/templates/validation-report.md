---
name: {{product-name}}
type: validation
created: {{YYYY-MM-DD}}
---

# Validation Report Template

Phase 2 output: availability summary across domains, social media, and trademark, with recommendation and next steps.

## Template: Product Naming -- Validation

```markdown
# Product Naming -- Validation

## Context

- Product: {{one-sentence description}}
- Audience: {{target audience}}
- Names validated: {{comma-separated list of names checked}}
- Research report: {{path to research report, or "N/A" if standalone}}

---

## Availability Summary

### Domains

<!-- Add or remove TLD columns based on product type. See tld-guide.md. -->
<!-- Always include .com and .com.br. Add others per selection logic. -->

| Name | .com | .com.br | {{TLD}} | {{TLD}} | Est. Cost |
|------|------|---------|---------|---------|-----------|
| **{{Name}}** | 🟢 | 🟢 | 🟢 | 🟢 | ~${{total}}/year |
| **{{Name}}** | 🔴 | 🟢 | 🟢 | 🟢 | ~${{total}}/year |

> 🟢 Available  🔴 Taken  🟡 Uncertain/Verify
> Prices from tld-guide.md. Estimate covers available TLDs only.

### Social Media

<!-- Always check IG and X. Add platform columns by product type. -->
<!-- GH for dev tools, LinkedIn for B2B/SaaS, TikTok for consumer apps. -->

| Name | IG | X | {{Platform}} |
|------|-----|---|-------------|
| **{{Name}}** | 🟢 | 🟡 | 🟢 |
| **{{Name}}** | 🔴 | 🟢 | 🟢 |

### Trademark

| Name | INPI (BR) | USPTO (US) | Risk |
|------|-----------|------------|------|
| **{{Name}}** | 🟢 No conflicts | 🟢 No conflicts | None |
| **{{Name}}** | 🟡 Similar in class {{N}} | 🟢 No conflicts | Low |

> Preliminary search only. Recommend professional trademark verification for final pick.

---

## Recommendation

### Primary: {{Name}}

{{Why this is the best choice -- 2-3 sentences covering availability, quality, and trademark status}}

### Alternatives (if primary unavailable)

| Priority | Name | Key Trade-off |
|----------|------|---------------|
| 2nd | {{Name}} | {{concern}} |
| 3rd | {{Name}} | {{concern}} |

---

## Next Steps

1. {{Action item: register domain}}
2. {{Action item: secure social media handles}}
3. {{Action item: professional trademark search}}
4. {{Action item: additional steps as needed}}
```

---

## Guidelines

- Availability Summary: Always include .com and .com.br; add TLD columns per tld-guide.md selection logic
- Social Media: Always check IG and X; add platform columns by product type (GH for dev tools, LinkedIn for B2B, TikTok for consumer)
- Estimated cost: Sum available TLD prices from tld-guide.md; show per-year estimate
- Trademark: Always include disclaimer about professional verification
- Recommendation: Pick one primary name; list 1-2 alternatives with trade-offs
- Next Steps: Actionable items the user can execute immediately
- Research reference: Link to the research report if one exists; write "N/A" for standalone validation
