# Discovery

Establishes content context and routes to the right operation.

## When to Use

Load at the start of every copywriting operation, before the routed work begins: never invoked directly.

## Workflow

### Step 1: Check Existing Context

Look for:

- `docs/design/copy.yaml`: existing content payload (signals brownfield)
- Source on hand: URL, brief (PDF/DOCX), codebase, screenshot, or raw paste
- `docs/product/PRD.md`, `docs/product/PRODUCT.md`, `docs/product/brainstorm.md`: intent, positioning, and requirements when writing fresh

If found, read and extract purpose, audience, tone, surface function, register (brand or product), brand personality, copy anti-references, and surfaces: copy-relevant facts only; requirement IDs, milestones, sprint or release names, roadmap language, and sibling-artifact references stay out of `copy.yaml`. An `intent` or `voice` block with `status: confirmed` is a decision already made: hold it, never re-derive it from the copy or ask for it again. A block with `status: inferred` is provisional; confirm it before authoring. Skip to the relevant operation.

### Step 2: Classify the Request

Infer from source and intent: do not ask explicitly. First fork on what the request wants done to the copy:

- **author**: produce or change copy. Then split by field:
  - **greenfield**: no existing copy → write fresh from intent.
  - **brownfield**: existing copy or a source → extract to structure it, refresh to tighten it, revoice to change its voice, or reconcile to sync implementation drift.
- **judge**: a non-mutating verdict on existing copy, no change applied → critique for a quality / slop verdict that loops to refresh, or audit for a ship-readiness defect report before handoff.

For authoring and judging, establish the intent before choosing patterns or the register. Intent records the purpose, reader goal, function, and functional constraints; voice records stylistic direction. Read [surface-functions.md](../references/surface-functions.md) when the reader's job or the applicable pattern is unclear. Never infer conversion from a page name alone.

### Step 3: Route to Operation

| Intent | Reference |
|--------|-----------|
| Write fresh copy from intent | [write.md](write.md) |
| Structure existing content from a source | [extract.md](extract.md) |
| Tighten existing copy in the same voice | [refresh.md](refresh.md) |
| Rewrite existing copy in a new voice | [revoice.md](revoice.md) |
| Sync `copy.yaml` from a drifted implementation | [reconcile.md](reconcile.md) |
| Judge copy quality: is this slop, score it, verdict before more editing | [critique.md](critique.md) |
| Pre-ship quality pass on `copy.yaml` before handoff | [audit.md](audit.md) |

Disambiguation: "before handoff" matches two operations. A judge request with no implementation source → **audit** (quality verdict on the copy itself). A sync request naming code or a live URL as the source of truth → **reconcile** (drift check against the implementation).

### Step 4: Fill Gaps

When authoring has no confirmed intent or voice, interview before drafting. Establish intent: purpose, reader goal, function, and functional constraints: then voice: stylistic direction and avoided words. Propose concise blocks when the request makes values clear; otherwise ask. A user request that changes purpose or functional limits changes intent; a request that changes style changes voice. The next authoring patch adds confirmed root blocks to a legacy `copy.yaml`; a judge operation instead states its inference and writes nothing. Batch independent low-stakes gaps: source, word count, mandatory sections: in one turn. Keep dependent picks in order: surface, intent, register, then voice.
