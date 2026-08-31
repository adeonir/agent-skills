# Discovery

Establishes the content context every copywriting operation works from.

## When to Use

Loaded at the start of every operation, before the work begins. It settles what already exists, the intent and voice the work must respect, and the gaps worth asking about.

## Check Existing Context

Look for:

- `docs/design/copy.yaml`: existing content payload (signals brownfield)
- Source on hand: URL, brief (PDF/DOCX), codebase, screenshot, or raw paste
- `docs/product/PRD.md`, `docs/product/PRODUCT.md`, `docs/product/brainstorm.md`: intent, positioning, and requirements when writing fresh

If found, read and extract purpose, audience, tone, surface function, register (brand or product), brand personality, copy anti-references, and surfaces: copy-relevant facts only; requirement IDs, milestones, sprint or release names, roadmap language, and sibling-artifact references stay out of `copy.yaml`. An `intent` or `voice` block with `status: confirmed` is a decision already made: hold it, never re-derive it from the copy or ask for it again. A block with `status: inferred` is provisional; confirm it before authoring.

## Establish Intent, Register, and Surface

Set the intent before choosing patterns or the register. Once confirmed, it is the first gate every pattern, edit, and verdict passes — including its constraints, such as a ban on sales language.

`intent.function` is the reader's job for that surface; classify it with [surface-functions.md](surface-functions.md), and never infer conversion from a page name alone. Intent also records the purpose, reader goal, and functional constraints, such as a ban on sales language. Use one function per surface when possible; a mixed surface may override the root intent per surface or part.

**Register** is the posture, either **brand** (the words are the product) or **product** (the words serve the task). It sets the voice: read the matching [brand.md](brand.md) or [product.md](product.md) first. **Surface** is the granular type the copy serves, named by context — landing, dashboard, form, empty-state. A surface sits under a register, and the content tree is named by context rather than forced into a fixed list. Storefronts straddle: catalog copy is brand, checkout and account copy is product.

`voice` carries tone and style; [voice.md](voice.md) owns how the register sets it.

## The Artifact

The skill owns `docs/design/copy.yaml`: a context-named content tree whose surfaces and parts mirror the source. It carries `intent` (purpose, reader goal, function, and functional constraints) and `voice` (the stylistic direction). Every later operation reads both before drafting or judging.

An authoring operation changes content only after the user confirms the proposed edits, and changes intent or voice only after the user confirms a new intent or voice. Before saving, self-check that the tree is well-formed and carries no design decisions — no colors, fonts, or layout. The content stays swappable: any `copy.yaml` must work independent of visual styling.

## Fill Gaps

When authoring has no confirmed intent or voice, interview before drafting. Establish intent — purpose, reader goal, function, and functional constraints — then voice: stylistic direction and avoided words. Propose concise blocks when the request makes values clear; otherwise ask. A user request that changes purpose or functional limits changes intent; a request that changes style changes voice. The next authoring patch adds confirmed root blocks to a legacy `copy.yaml`; a judging operation instead states its inference and writes nothing.

Batch independent low-stakes gaps — source, word count, mandatory sections — in one turn. Keep dependent picks in order: surface, intent, register, then voice.
