# Name Evaluation

Reference for Phase 2: evaluating and filtering name candidates.

## When to Use

Always. Whether names were generated or provided by the user, every candidate goes through this evaluation.

## Workflow

For each candidate, run these checks in order:

1. Domain availability
2. Social media username availability
3. Name quality analysis

Then produce the output report.

## Domain Availability Check

**LOAD:** [tld-guide.md](tld-guide.md) for the full TLD reference.

Always check .com and .com.br. Add other TLDs based on product type (see tld-guide.md).

**How to check**: use web search for `<name>.com available domain` or `<name>.com.br registro.br disponivel`. Look for registrar pages showing "available" or "taken".

Mark each as:
- 🟢 Available
- 🔴 Taken
- 🟡 Uncertain (could not confirm)

## Social Media Username Check

Check relevant platforms using web search: `site:instagram.com/<name>` or `"@<name>" instagram`.

| Platform | When to check |
|----------|---------------|
| Instagram | Always |
| X/Twitter | Always |
| GitHub | Dev tools / technical products |
| LinkedIn (company page) | B2B / SaaS |
| TikTok | Consumer apps |

Mark each as: 🟢 Available, 🔴 Taken, 🟡 Uncertain

## Name Quality Analysis

Evaluate each name on:

- **Pronounceable**: works in both PT and EN without breaking?
- **Memorable**: easy to recall after hearing once?
- **Spellable**: can someone type it correctly after hearing it?
- **Unique**: stands out in its category?
- **Scalable**: still makes sense if the product pivots or grows?
- **Trademark risk**: sounds too close to a known brand? (quick search, flag obvious conflicts)

## Output Format

### Shortlist

One line per viable name:

```
Name -- [brief quality note] | Domains: .com 🟢 .com.br 🟢 .io 🔴 | Social: IG 🟢 X 🟢
```

Flag the strongest option with "TOP PICK" if one clearly stands out.

Example:
```
Flowly -- Fluido, memorizavel, soa bem em PT e EN | Domains: .com 🔴 .com.br 🟢 .io 🟢 | Social: IG 🟢 X 🟡
Nuvio -- Inventado, leve, escalavel | Domains: .com 🟢 .com.br 🟢 .io 🟢 | Social: IG 🟢 X 🟢 -- TOP PICK
```

### Eliminated

One line per eliminated name with reason:

```
Name -- [elimination reason]
```

Common elimination reasons:
- Dominio .com tomado + username IG tomado
- Dificil de pronunciar em ingles ou portugues
- Muito generico / sem personalidade
- Conflito com marca conhecida: [brand name]
- Spelling confuso (dupla interpretacao)

## Edge Cases

- If checking many names (10+), batch web searches for efficiency
- If a name scores well on quality but has poor domain availability, keep it in shortlist with domain caveat
- Always end with a brief recommendation if one name clearly dominates
