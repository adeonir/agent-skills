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

Always check .com and .com.br. Add other TLDs based on product type (see tld-guide.md). Include .app for mobile/web apps.

**Preferred method: whois (Shell)**

Always use `whois` as the primary verification tool. It provides authoritative registration status directly from registries.

```bash
# Check a single domain
whois <name>.com | grep -iE "status|not found|no match"

# Check multiple TLDs for one name
whois <name>.com | grep -iE "status|not found|no match"
whois <name>.com.br | grep -iE "status|not found"
whois <name>.io | grep -iE "status|not found|no match"
whois <name>.app | grep -iE "status|not found|no match"

# Batch multiple candidates
for name in foo bar baz; do
  echo "=== $name ==="
  echo ".com: $(whois "$name.com" 2>/dev/null | grep -iE "status|not found|no match" | head -1)"
  echo ".com.br: $(whois "$name.com.br" 2>/dev/null | grep -iE "status|not found" | head -1)"
  echo ".io: $(whois "$name.io" 2>/dev/null | grep -iE "status|not found|no match" | head -1)"
  echo ".app: $(whois "$name.app" 2>/dev/null | grep -iE "status|not found|no match" | head -1)"
done
```

**Interpretation:** "No match" / "NOT FOUND" = 🟢 Available. Any status like "clientTransferProhibited", "active", "registered" = 🔴 Taken.

**Fallback method: dig (Shell)**

Use `dig` only for quick DNS resolution checks when whois is slow or unavailable. A non-empty response means the domain resolves (likely taken), but empty response doesn't guarantee availability.

```bash
dig +short <name>.com
```

**Last resort: WebSearch**

If shell tools are unavailable, search `<name>.com available domain` or `<name>.com.br registro.br disponivel`. Look for registrar pages showing "available" or "taken". Mark as 🟡 Uncertain if results are inconclusive.

Mark each as:
- 🟢 Available
- 🔴 Taken
- 🟡 Uncertain (could not confirm)

## Social Media Username Check

| Platform | When to check |
|----------|---------------|
| Instagram | Always |
| X/Twitter | Always |
| GitHub | Dev tools / technical products |
| LinkedIn (company page) | B2B / SaaS |
| TikTok | Consumer apps |

**How to check** -- pick the first method available in your environment:

**Method 1 (Shell -- preferred):** use `curl` to check HTTP status codes.

```bash
# 200 = taken, 404 = available
curl -sI -o /dev/null -w "%{http_code}" https://www.instagram.com/<name>/
curl -sI -o /dev/null -w "%{http_code}" https://x.com/<name>
curl -sI -o /dev/null -w "%{http_code}" https://github.com/<name>

# Batch multiple candidates across platforms
for name in foo bar baz; do
  echo "--- $name ---"
  echo "IG: $(curl -sI -o /dev/null -w '%{http_code}' https://www.instagram.com/$name/)"
  echo " X: $(curl -sI -o /dev/null -w '%{http_code}' https://x.com/$name)"
done
```

Note: Instagram returns 302 for non-existent users instead of 404 -- mark 302 responses as 🟡 Uncertain.

**Method 2 (WebSearch -- fallback):** search `"<name>" site:instagram.com` or `"@<name>" twitter`.

**Method 3 (Neither available):** mark all usernames as 🟡 Uncertain and note that availability could not be verified.

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

- If checking many names (10+), batch searches or shell commands for efficiency
- If a name scores well on quality but has poor domain availability, keep it in shortlist with domain caveat
- Always end with a brief recommendation if one name clearly dominates
- Shell rate-limiting: if whois or curl commands get throttled, add a 1-2 second delay between requests (`sleep 1` in the loop) or switch to WebSearch for remaining names
