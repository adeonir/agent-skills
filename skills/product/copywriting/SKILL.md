---
name: copywriting
allowed-tools: Read Write Edit Grep Glob WebFetch Bash(python3:*)
description: "Creates and evaluates copy for brand, editorial, product, UX, conversion, and informational surfaces. Use when writing, extracting, editing, syncing, critiquing, or auditing copy. Not for visual identity, page layout, or standalone social bios."
---

# Copywriting

Owns `copy.yaml`, the structured content payload that design consumes. The same payload must work with any visual identity, so this skill carries words, not design decisions. Authoring operations change copy; judging operations report on it.

## Triggers

**Author** — produce or change copy:

- **write** ("write the headline", "new copy from this brief", "we need a value proposition") → [write.md](instructions/write.md)
- **extract** ("structure this page", "pull the copy from this URL", "turn this brief into copy.yaml") → [extract.md](instructions/extract.md)
- **refresh** ("tighten this", "the copy reads weak", "polish before handoff") → [refresh.md](instructions/refresh.md)
- **revoice** ("make it playful", "make it sound premium", "drier, less salesy") → [revoice.md](instructions/revoice.md)
- **reconcile** ("sync copy from code", "the implementation drifted") → [reconcile.md](instructions/reconcile.md)

**Judge** — a non-mutating verdict on existing copy:

- **critique** ("does this read as slop", "score the copy", "verdict before more editing") → [critique.md](instructions/critique.md)
- **audit** ("is this copy ready to ship", "defect report before handoff") → [audit.md](instructions/audit.md)

Classify the request by what it wants done to the copy, and infer from source and intent rather than asking. "Before handoff" matches two operations: a judging request with no implementation source is **audit**, while a sync request naming code or a live URL as the source of truth is **reconcile**.

## Workflow

```text
trigger → discovery (context, intent, register) → operation → copy.yaml or verdict
                                                      |
                              critique → refresh → critique again
```

Every operation starts by loading discovery. A judging verdict is applied by running the matching authoring operation, never by patching from the judgment itself.
