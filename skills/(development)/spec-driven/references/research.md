# Research

Research technologies and cache findings for reuse across features.

## Tools

Use available documentation lookup and web search tools to research technologies.
The agent discovers and uses whatever tools are available in the environment.

## Cache Location

Research files are stored at `.artifacts/research/{topic}.md`.

## Cache File Structure

Research files must include YAML frontmatter with metadata:

```yaml
---
topic: totp-authentication
researched_at: 2024-01-15
version: "1.0.0"
sources_hash: "abc123def456"
ttl_days: 90
keywords:
  - totp
  - 2fa
  - authentication
---
```

## Cache Check Process

Before researching, always check for existing cache:

```bash
if [ -f ".artifacts/research/{topic}.md" ]; then
  researched_at=$(grep "researched_at:" .artifacts/research/{topic}.md | head -1 | cut -d: -f2 | tr -d ' ')
  ttl_days=$(grep "ttl_days:" .artifacts/research/{topic}.md | head -1 | cut -d: -f2 | tr -d ' ')
  # Calculate age and check if still valid
fi
```

## Invalidation Rules

Cache is automatically invalidated when:

1. **TTL expired**: Days since research > ttl_days
2. **Source 404**: Main documentation URL returns 404
3. **Version mismatch**: Spec mentions different version than cached
4. **Breaking changes**: Changelog indicates breaking changes since research date

## Cache Reuse Strategy

### Exact Match

Topic in spec matches cached topic exactly:
- Reuse cache if valid

### Partial Match

Topic is related to cached topic:
- Check keywords overlap
- Review cache content for relevance
- Extend cache if applicable

### No Match

No relevant cache exists:
- Conduct new research
- Save with proper metadata

## Research Process

1. **Check Cache** - Look for `.artifacts/research/{topic}.md`
2. **Extract Topics** - From spec.md: technologies, APIs, services
3. **Research** - Official docs first, best practices, gotchas
4. **Synthesize** - Organize: must-know, architectural impact, warnings

## Research File Template

```markdown
---
topic: {kebab-case-topic}
researched_at: {YYYY-MM-DD}
version: "{x.y.z}"
sources_hash: "{hash}"
ttl_days: 90
keywords:
  - {keyword1}
  - {keyword2}
---

# {Topic Title}

> Researched: {YYYY-MM-DD}

## Summary

{2-3 sentences of key findings}

## Key Information

- {bullet points}

## Implementation Notes

- {specific guidance}

## Gotchas

- {warnings}

## Recommendations

{specific suggestions}

## Uncertainties

{topics needing verification}

## Sources

- [{title}]({url})
```

## Rules

1. **Always check cache first**: Before webfetch, check .artifacts/research/
2. **Include metadata**: Every research file must have YAML frontmatter
3. **Respect TTL**: Don't use expired cache without verification
4. **Version matters**: If spec mentions version, verify cache matches
5. **Update, don't duplicate**: Refresh existing files instead of creating new ones
6. **Be targeted**: Only research what's relevant to the feature
7. **Cite sources**: Include URLs for verification
