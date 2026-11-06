# Handoff

Capture conversation state so another session can resume.

## What It Does

```mermaid
flowchart TD
    A[save] --> B[Consolidated HANDOFF.md]
    B --> A
    B --> C[load]
    C --> D[next session resumes]
    B -.-> E[clear]
```

| Operation | Output |
|-----------|--------|
| save | Consolidates the existing handoff with the current conversation and work state, one block per topic |
| load | Reads the handoff, checks claims that may have changed, and resumes from its context |
| clear | Writes empty content to the file (opt-in, separate operation) |

## Usage

```text
save context
dump conversation
checkpoint this
session handoff
save handoff
resume session
load handoff
continue from last
clear handoff
reset handoff
/handoff
/handoff auth race fix
/handoff load
/handoff clear
```

## Output

```text
.artifacts/HANDOFF.md      # one current, consolidated handoff, one block per topic
```

Save consolidates it on each run and clear empties it. An empty file reads as no handoff.

## Requirements

Python 3 (standard library only) for the format and secret check save runs on the written file.

## FAQ

**Q: Does save discard the previous handoff?** A: No. Save reads the existing handoff and consolidates it with the current conversation. Relevant information remains; superseded and redundant content is removed.

**Q: Does load auto-clear the handoff?** A: No. Load reads the handoff; clear is a separate explicit operation.

**Q: Does the handoff prescribe what to do next?** A: No. The next session infers what to do from the context and current state of each topic.

**Q: What if the file is absent?** A: Load reports that no handoff exists. Clear no-ops silently. Save creates the file.

**Q: How does this differ from end-of-session note persistence?** A: End-of-session flows write a narrative of what happened into a durable memory system. The handoff skill carries the live context, rationale, and work state needed to resume. An end-of-session flow may consume and clear the handoff after it persists the content.

**Q: What is a topic?** A: A subject the next session can resume without the others. Each topic has its own block in the file, so work on one subject does not overwrite another's.

**Q: Can I name the topic a save belongs to?** A: Yes. Pass the topic as an argument: `/handoff auth race fix`. Save writes the conversation's work into the block with that heading, or opens one. Without an argument, save picks the topic from the conversation. `load` and `clear` are the only arguments that select another operation.
