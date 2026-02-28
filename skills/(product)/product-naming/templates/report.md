# Report Templates

Two templates based on entry point. Use the one that matches the user's request.

---

## Template A: Name Research

Use when the user needs name suggestions (generate + evaluate flow).

```markdown
# Product Naming

## Context

- **Product**: {one-sentence description}
- **Audience**: {target audience}
- **Tone**: {vibe/tone}
- **Style**: {naming style preferences or "none specified"}

---

## Candidates

Validated against existing products in the market.

{For each viable name, one section:}

### {Name}

> "{root word}" ({language}: {meaning}) + "{suffix}"

{1-2 sentence description: what it evokes, tone, how it works in PT+EN.}

**Risk:** {Risk level and justification. "None" if completely clean.}

---

## Full Evaluation

### Top Pick

> **{Name}** -- {Short justification: why this is the best candidate.}

### Availability

> Status: 🟢 disponivel  🔴 indisponivel  🟡 incerto

| Name | Highlight | .com | .com.br | {extra TLDs} | IG | X | GH |
|---|---|---|---|---|---|---|---|
| **{Name}** | {quality note} | 🟢 | 🔴 | 🟡 | 🟢 | 🟢 | 🔴 |

### Comparison

| Name | Tone | Memorability | Pronunciation PT+EN | Spelling | Risk |
|---|---|---|---|---|---|
| **{Name}** | {tone description} | {High/Very high} | {assessment} | {assessment} | {Very low/Low/Medium/High} |

---

## Eliminated

{For each eliminated name, one line:}

- ~~{Name}~~ -- {elimination reason}
```

---

## Template B: Name Validation

Use when the user already has one or more names to evaluate.

```markdown
# Name Validation

## Context

- **Product**: {one-sentence description or "not specified"}
- **Names evaluated**: {list of names}

---

{For each name, one section:}

## {Name}

### Quality

| Criteria | Rating | Notes |
|---|---|---|
| Pronounceable (PT+EN) | {Good/Fair/Poor} | {assessment} |
| Memorable | {Good/Fair/Poor} | {assessment} |
| Spellable | {Good/Fair/Poor} | {assessment} |
| Unique | {Good/Fair/Poor} | {assessment} |
| Scalable | {Good/Fair/Poor} | {assessment} |

### Availability

> Status: 🟢 disponivel  🔴 indisponivel  🟡 incerto

| Name | Highlight | .com | .com.br | {extra TLDs} | IG | X | GH |
|---|---|---|---|---|---|---|---|
| **{Name}** | {quality note} | 🟢 | 🔴 | 🟡 | 🟢 | 🟢 | 🔴 |

### Risk

{For each risk found, one bullet. "None identified." if clean.}

- **{risk type}**: {context} -- {impact}
- **{risk type}**: {context} -- {impact}

---

{If multiple names were evaluated:}

## Verdict

> **{Name}** -- {contextual assessment: viable for what stage, key trade-offs, and one concrete next step.}

{If only one name: skip this section. The single-name evaluation above is the full report.}
```
