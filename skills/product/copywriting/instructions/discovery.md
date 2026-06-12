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
- `docs/product/prd.md`, `docs/product/brief.md`, `docs/product/brainstorm.md`
  — intent and requirements when writing fresh

If found, read and extract purpose, audience, tone, and surfaces — copy-relevant
facts only; requirement IDs, milestones, sprint or release names, roadmap
language, and sibling-artifact references stay out of `copy.yaml`. Skip to the
relevant operation.

### Step 2: Classify Field

Infer from source and intent — do not ask explicitly:

- **greenfield** — no existing copy → write fresh from intent.
- **brownfield** — existing copy or a source → extract to structure it,
  refresh to tighten it, revoice to change its voice, or reconcile to sync
  implementation drift.

### Step 3: Route to Operation

| Intent | Reference |
|--------|-----------|
| Write fresh copy from intent | [write.md](write.md) |
| Structure existing content from a source | [extract.md](extract.md) |
| Tighten existing copy in the same voice | [refresh.md](refresh.md) |
| Rewrite existing copy in a new voice | [revoice.md](revoice.md) |
| Sync `copy.yaml` from a drifted implementation | [reconcile.md](reconcile.md) |

### Step 4: Fill Gaps

When context is missing, ask one question at a time: source, tone
(professional, casual, bold), which surfaces the content covers, and any
constraints (word count, mandatory sections).
