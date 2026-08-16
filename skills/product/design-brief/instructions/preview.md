# Preview

Render document and styleguide views from one DESIGN.md, collect feedback in batches, and apply only confirmed deltas.

## When to Use

Use after a root `DESIGN.md` exists when the user wants to inspect, comment on, tune, or explicitly export its visual views.

## Prerequisites

Load [validate.md](validate.md). Stop on `failed` or `not audited`; allow `passed with warnings` and keep its warnings visible. Load [anti-patterns.md](../references/anti-patterns.md) for rendered-output rules.

Before writing transient files, ensure `.artifacts` is locally excluded:

```bash
grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude
```

## Views

Render both transient files under `.artifacts/design/preview/` from the current root `DESIGN.md`:

- `design.html` — a readable document view of the frontmatter and body. Escape embedded HTML so source content cannot execute.
- `styleguide.html` — a visual identity view for colors, typography, spacing, radii, components, depth prose, shape prose, motion prose, responsive prose, and downstream guidance.

Use the frontmatter as the normative value source. Render every specimen through CSS custom properties rather than literals. A literal token value may appear only as its label. Show a quiet placeholder when an official group is omitted deliberately.

Add IDs matching the canonical body sections so the server sidebar can navigate both views. Add `data-tune-swatch`, `data-token`, `data-var`, `data-pair`, and `data-original` to tunable color specimens.

## Server

Start the bundled server:

```bash
bun run <this-skill>/scripts/preview-server.ts --session .artifacts/design/preview
```

The server provides:

- `/design` and `/styleguide` from the two transient files.
- Top-level tabs for switching views.
- A sidebar for canonical section navigation.
- Comment mode with a queue that survives view switches.
- An inspector sidebar for temporary color tuning.
- Live reload and append-only events at `.artifacts/design/preview/.events`.

The server stays local to `127.0.0.1` and serves only files inside the session directory.

## Feedback Round

1. The user activates Comment mode, selects an element, writes a comment, and adds it to the queue.
2. The user may switch views and add more comments. Each item records `view`, `selector`, and `text`.
3. Inspector edits update the rendered custom property only. Each adjustment records `token`, `old`, `new`, and `view`.
4. Send records one `feedback` event with all queued comments and adjustments. It does not write `DESIGN.md`.
5. Read the batch and map each item to a frontmatter group or prose section. A composed instruction may combine aspects named in several comments; reconcile it into one coherent identity instead of pasting incompatible systems together.
6. Present the proposed patch list in chat and wait for explicit confirmation.
7. After confirmation, patch frontmatter first and then only affected prose. Report old and new values.
8. Regenerate both transient views, run semantic contrast, then run full validation. Errors block completion; warnings remain visible.

Conversational tweaks follow the same propose → confirm → apply flow. No interaction writes the identity immediately.

## Explicit HTML Export

Do not create persistent HTML during normal preview. When the user explicitly requests export, write the current views to:

- `docs/design/design.html`
- `docs/design/styleguide.html`

Use a user-supplied destination when provided. Exported files contain no feedback chrome, event client, or server dependency.

## Rendered Review

Run only anti-pattern rules whose Surface is `rendered-output` or `both`. Keep qualitative anti-slop review separate from deterministic findings.

## Error Handling

- Missing root `DESIGN.md`: route to design.
- Missing transient view: regenerate both from the same source before starting the server.
- Comment without selector: ask the user to select the element again.
- Adjustment for an unknown token: propose adding or remapping the token; do not apply automatically.
- Empty feedback batch: report no requested change.
- Port in use: rely on the server's bounded port retry or pass another explicit port.
