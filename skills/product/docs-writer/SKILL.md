---
name: docs-writer
description: "Product and technical document creation through guided discovery, including PRDs, positioning docs, Design Docs, and ADRs. Use when defining requirements, strategy, trade-offs, or architecture decisions. Not for UI design, implementation specs, or meeting notes."
---

# Docs Writer

## Triggers

| Type | Load |
|------|------|
| PRD — product requirements | [prd.md](instructions/prd.md) |
| PRODUCT — strategic positioning and identity | [product.md](instructions/product.md) |
| Design Doc — lean technical design and trade-offs | [design.md](instructions/design.md) |
| ADR — single architecture decision record | [adr.md](instructions/adr.md) |

Detect the document type from the trigger. If ambiguous, ask the user.

## Workflow

```text
trigger → detect type → load instruction → check disk → drafting
  document exists → update the requested parts
  document absent → full discovery
  ADR → create a numbered record or update the requested record
```
