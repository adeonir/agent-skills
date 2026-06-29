# Discovery

Establishes content context and routes to the right operation.

## When to Use

Load at the start of every copywriting operation, before the routed work
begins — never invoked directly.

## Workflow

### Step 1: Check Existing Context

Look for:

- `docs/design/copy.yaml` — existing content payload (signals brownfield)
- Source on hand: URL, brief (PDF/DOCX), codebase, screenshot, or raw paste
- `docs/product/prd.md`, `docs/product/PRODUCT.md`, `docs/product/brainstorm.md`
  — intent, positioning, and requirements when writing fresh

If found, read and extract purpose, audience, tone, register (brand or product),
brand personality, copy anti-references, and surfaces — copy-relevant facts only;
requirement IDs, milestones, sprint or release names, roadmap language, and
sibling-artifact references stay out of `copy.yaml`. Skip to the relevant operation.

### Step 2: Classify the Request

Infer from source and intent — do not ask explicitly. First fork on what the
request wants done to the copy:

- **author** — produce or change copy. Then split by field:
  - **greenfield** — no existing copy → write fresh from intent.
  - **brownfield** — existing copy or a source → extract to structure it,
    refresh to tighten it, revoice to change its voice, or reconcile to sync
    implementation drift.
- **judge** — a non-mutating verdict on existing copy, no change applied →
  critique for a quality / slop verdict that loops to refresh, or audit for a
  ship-readiness defect report before handoff.

### Step 3: Route to Operation

| Intent | Reference |
|--------|-----------|
| Write fresh copy from intent | [write.md](write.md) |
| Structure existing content from a source | [extract.md](extract.md) |
| Tighten existing copy in the same voice | [refresh.md](refresh.md) |
| Rewrite existing copy in a new voice | [revoice.md](revoice.md) |
| Sync `copy.yaml` from a drifted implementation | [reconcile.md](reconcile.md) |
| Judge copy quality — is this slop, score it, verdict before more editing | [critique.md](critique.md) |
| Pre-ship quality pass on `copy.yaml` before handoff | [audit.md](audit.md) |

Disambiguation — "before handoff" matches two operations. A judge request with
no implementation source → **audit** (quality verdict on the copy itself). A
sync request naming code or a live URL as the source of truth → **reconcile**
(drift check against the implementation).

### Step 4: Fill Gaps

When context is missing, ask one question at a time: source, the surfaces the
copy covers (landing, dashboard, form…) and their register (from `PRODUCT.md`'s
default when present, else brand or product — usually inferable from the
surface), and any constraints (word count, mandatory sections).
