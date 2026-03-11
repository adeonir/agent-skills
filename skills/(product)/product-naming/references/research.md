# Name Research

Reference for Phase 1: discovering context, analyzing competitors, generating name candidates, and scoring quality.

## When to Use

The user asks for name suggestions, ideas, or help coming up with a name. Also use when the user provides candidates and wants quality evaluation (skip generation, go to scoring).

## Workflow

1. Complete discovery questions
2. Analyze competitor landscape
3. Generate candidates spread across multiple styles
4. Score candidates on quality criteria
5. Suggest variations for top candidates
6. Present the full list to the user before proceeding

## Discovery

Ask (if not already clear from context):

1. What does the product do? (one sentence)
2. Who is the target audience?
3. What's the vibe/tone? (e.g., professional, playful, technical, minimal)
4. Any style preferences? (e.g., real words, invented words, compound words, abbreviations)
5. Any names to avoid or themes that feel wrong?

## Competitor Analysis

Before generating names, research the competitive landscape:

1. Search for products in the same niche or category
2. List 3-5 main competitors and their naming patterns
3. Identify naming conventions in the space (e.g., "-ify" pattern in productivity tools)
4. Note names to avoid due to similarity or confusion risk
5. Look for gaps -- naming styles not yet used in the category

Present a brief competitor summary before generating candidates.

## Generation Styles

Generate 10-20 diverse candidates across these styles:

### Real words

Evocative nouns or verbs that work in both Portuguese and English (e.g., Notion, Stripe, Linear). Prefer words with shared or neutral meaning across both languages.

### Compound words

Two combined concepts (e.g., Cloudflare, Snapchat). Try PT+EN and EN+EN combinations.

### Invented / phonetic

Coined words with strong phonetics -- easy to say in both PT and EN.

Phonetic guidelines:
- Avoid sounds that break badly in one language ("th" is hard in PT, "lh/nh" is hard in EN)
- Prefer open syllables (ending in vowels): Nuvio, Fluxo, Cario, Velto
- Short: 2-3 syllables max
- Vowel-rich names sound friendly; consonant-heavy names sound technical
- Test mentally: does it sound good said by a Brazilian and by an American?

### Portmanteaus

Blend two words by merging overlapping sounds or syllables (e.g., Pinterest = pin + interest, Groupon = group + coupon). Works well when both source words are recognizable.

### Truncation with modern suffixes

Take a meaningful root word and truncate or modify it, then add a modern suffix (e.g., Airtable = air + table, Webflow = web + flow). Common suffixes: -o, -a, -ly, -fy, -io, -er, -ai.

### Prefixed / suffixed

Common patterns: -ly, -ify, -hub, -lab, get-, go-, use-, my-

### Acronyms

Only if they form a real-sounding word. Forced acronyms are worse than no acronym.

## Name Variations

For each strong candidate (top 3-5), suggest variations:

- With/without suffix (e.g., Flux vs Fluxo vs Fluxly)
- Vowel swap (e.g., Cario vs Curio vs Corio)
- Abbreviation (e.g., TaskFlow vs TFlow)
- Prefix addition (e.g., GoFlux, UseFlux)
- Domain-friendly spelling (e.g., GetNuvio if nuvio.com is likely taken)

Present variations alongside the original so the user can pick the strongest form.

## Quality Scoring

Evaluate each candidate on these criteria:

- **Pronounceable**: works in both PT and EN without breaking?
- **Memorable**: easy to recall after hearing once?
- **Spellable / Dictable**: can someone type it correctly after hearing it? Simulate the "phone test" -- imagine spelling the name over a phone call or podcast. If it requires "that's with a K, not a C" or "no hyphen", it fails.
- **Unique**: stands out in its category? (cross-reference competitor analysis)
- **Scalable**: still makes sense if the product pivots or grows?
- **Trademark risk**: sounds too close to a known brand? Flag obvious conflicts based on agent judgment -- no external research needed here.

Use [Good] / [Fair] / [Poor] for each criterion.

## Output

**USE TEMPLATE:** `templates/research-report.md`

Present results to the user. End the report suggesting the user can proceed to validation for domain, social media, and trademark checks. If the user wants to proceed, load [validation.md](validation.md).

## Error Handling

- No product context provided: ask what the product does and who it's for
- User provides too many candidates (10+): evaluate in batches, prioritize by initial impression
- All candidates eliminated: suggest the user adjust constraints or generate a new batch
- Competitor search returns no results: note the niche may be new, proceed with generation
- Evaluate-only entry point: skip competitor analysis and variations, go straight to quality scoring
