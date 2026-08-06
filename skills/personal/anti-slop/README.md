# Anti Slop

Edits drafts into sharper, more human prose — or names the AI tells without touching a word.

## What It Does

```mermaid
flowchart TD
    IN[draft: file path or pasted text] --> READ[read the full draft]
    READ --> VOICE[core point + 3-5 voice signals]
    VOICE --> MODE{edit or detect}
    MODE -->|detect| SCAN[scan against the slop catalog]
    SCAN --> REPORT[pattern, quoted line, fix]
    MODE -->|edit| CUT[apply principles, cut catalog patterns]
    CUT --> CHECK[run the self-check]
    CHECK -->|fail| CUT
    CHECK -->|pass| OUT[edited draft + What changed]
```

| Mode | Output |
|------|--------|
| edit | The full edited draft plus a What changed list |
| detect | One line per pattern found: name, quoted line, fix — nothing rewritten |

## Usage

```text
Clean up this draft, keep it sounding like me
Make this post less AI-sounding
Edit docs/notes/launch.md
Does this read as AI slop?
Scan this for AI tells, do not rewrite it
```

## Output

Pasted text comes back in the reply. A file path is edited in place, with What changed reported in the reply.

The draft's language sets the output language — the skill's word lists are English, and against a draft in another language it matches the shape and cuts the equivalent word.

## FAQ

**Does detect tell me whether AI wrote the piece?** No. It names patterns and quotes the lines that carry them. Detectors guess; named patterns are evidence you can check yourself.

**Will it flatten my voice?** The edit keeps distinctive vocabulary, cadence, bluntness, humor, and digressions. Cutting is proportional to the actual slop, so a rough draft with a real voice still sounds like the same person.
