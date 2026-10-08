# Anti-Slop

Edits drafts into clear, natural prose, or names AI-writing patterns without changing the draft.

## What It Does

```mermaid
flowchart TD
    IN[draft: file path or pasted text] --> READ[read the full draft]
    READ --> VOICE[register + voice signals]
    VOICE --> MODE{edit or detect}
    MODE -->|detect| SCAN[scan catalog and context]
    SCAN --> REPORT[pattern, quoted line, fix]
    MODE -->|edit| CUT[apply principles and cut supported patterns]
    CUT --> CHECK[run the self-check]
    CHECK -->|fail| CUT
    CHECK -->|pass| OUT[mode-specific output]
```

| Mode | Output |
|------|--------|
| edit | The full edited pasted draft plus What changed; file mode writes the file and reports its path, a summary of the edit, open items, and What changed |
| detect | One line per pattern found: name, quoted line, fix — nothing rewritten |
| embedded | Final edited text only, ready for another workflow |

## Usage

```text
Clean up this draft, keep it sounding like me
Make this post less AI-sounding
Remove the AI-writing patterns from docs/notes/launch.md
Does this read as AI slop?
Scan this for AI tells, do not rewrite it
```

## Output

Pasted text comes back in the reply. A file path is edited in place; the reply reports the path, a short summary of the edit, any open item, and What changed, never the edited file. Embedded text comes back without a preamble or change log. File mode changes prose only and preserves code, data, frontmatter, links, identifiers, and document structure.

## FAQ

**Q: Does it work in languages other than English?** A: Yes. It writes in the draft's language. The word lists are English, but the skill matches the same patterns in other languages.

**Q: Does detect tell me whether AI wrote the piece?** A: No. It names patterns and quotes the lines that carry them. It does not identify the author.

**Q: Will it flatten my voice?** A: The edit keeps distinctive words, rhythm, bluntness, humor, and digressions. It cuts only what the draft needs, so the result still sounds like the same person.

**Q: Does it add opinions or personality?** A: Not by default. Technical, reference, legal, and factual prose stays neutral and precise. Personal and editorial prose can keep personality when the source supports it.

**Q: Does one word or dash prove AI writing?** A: No. Findings require context or a pattern cluster.
