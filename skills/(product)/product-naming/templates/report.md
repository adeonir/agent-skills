---
name: {{product-name}}
type: {{research | validation}}
created: {{YYYY-MM-DD}}
---

# Report Template

Unified template for both research (generate + evaluate) and validation (evaluate only) workflows.

## Template: Product Naming Report

```markdown
# Product Naming

## Context

- Product: {{one-sentence description}}
- Audience: {{target audience}}
- Tone: {{vibe/tone}}
- Style: {{naming style preferences}}
- Entry Point: {{Research (generated) | Validation (provided)}}

---

## Shortlist -- Viable Candidates

### {{Name}} {{TOP PICK if applicable}}

> "{{root word}}" ({{language}}: {{meaning}}) + "{{suffix}}"

{{2-3 sentences: what it evokes, tone, how it works in PT+EN, key strengths}}

Quality Score: Pronunciation: [Good] | Memorable: [Good] | Scalable: [Good]

Risk: {{None / Low / Medium / High}} -- {{justification}}

---

## Availability Summary

| Name | .com | .com.br | .io | .app | IG | X | GH |
|------|------|---------|-----|------|----|---|----|
| **{{Name}}** | 🟢 | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 🟢 |
| **{{Name}}** | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 🟢 |

> 🟢 Available  🔴 Taken  🟡 Uncertain/Verify

---

## Recommendation

### 1st Primary: {{Name}}
{{Why this is the best choice -- 2-3 sentences}}

Next Steps:
1. {{Action item}}
2. {{Action item}}

### 2nd Alternatives (if primary unavailable)
| Priority | Name | Key Trade-off |
|----------|------|---------------|
| 2nd | {{Name}} | {{concern}} |
| 3rd | {{Name}} | {{concern}} |

---

## Eliminated

| Name | Motivo |
|------|--------|
| ~~{{Name}}~~ | {{reason: domain taken / hard to pronounce / generic / trademark conflict}} |
| ~~{{Name}}~~ | {{reason}} |
```

---

## Guidelines

- TOP PICK: Flag only one name as the strongest option when there's a clear winner
- Quality Score: Use [Good] / [Fair] / [Poor] for each criterion
- Risk: Keep it brief but specific -- mention concrete issues (e.g., ".com taken by competitor", "pronunciation ambiguous in EN")
- Eliminated: Group all eliminated names in one table at the end; reason can be domain conflict OR quality issue
- Availability Summary: Always include .com and .com.br; add .io for tech products; check IG/X always, GH for dev tools
