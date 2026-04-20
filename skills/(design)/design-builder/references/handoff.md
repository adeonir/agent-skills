# Handoff

Package design artifacts and intent into a single bundle for external
consumption (another agent, developer, or tool that does not have direct
access to this repo).

## When to Use

- Another agent or developer will implement the design without repo access
- Passing the approved design to Claude Code as a one-shot instruction
- Archiving an approved design for future reference

Handoff is optional. Most projects do not need it — `spec-driven` already
reads the artifacts directly from `.artifacts/design/`.

## Prerequisites

- `design.json` validated
- `structure.md` approved
- `preview/` with the approved final HTML (recommended, not mandatory)
- `copy.yaml` if content was extracted (optional)

## Workflow

### Step 1: Collect Artifacts

Gather from `.artifacts/design/`:

- `design.json` (tokens)
- `structure.md` (layout decisions)
- `copy.yaml` (content, if present)
- `preview/*/final.html` or the chosen variant (if present)
- `design.pen` if Pencil was used (referenced, not embedded)

### Step 2: Capture Intent

Ask the user if intent is not already covered by a PRD, brief, or brainstorm
artifact:

1. What is the primary user outcome this design should produce?
2. What were the non-negotiable decisions during design?
   (e.g., "primary CTA must be above fold", "no modal for sign-up")
3. What is explicitly out of scope for the implementer?

If prior artifacts exist, extract intent from them and confirm with the user
before writing the handoff.

### Step 3: Generate handoff.md

**USE TEMPLATE:** `templates/handoff.md`

Assemble the bundle. The output is a single markdown file with:

- Project summary and intent
- Pointers to each artifact (paths, not embedded copies)
- Key design decisions with rationale
- Explicit non-goals
- Implementation framing without prescribing a specific stack

### Step 4: Save and Present

Save to `.artifacts/design/handoff.md`.

Present the single-instruction format the consumer can paste:

```
Implement the design in .artifacts/design/handoff.md.
Tokens: design.json. Structure: structure.md. Content: copy.yaml.
Visual reference: preview/*/final.html.
```

## Guidelines

**DO:**
- Point to artifacts, never embed them (keeps the bundle in sync with source)
- Capture intent explicitly — the consumer needs to know why, not only what
- List explicit non-goals to prevent scope creep during implementation
- Keep the implementation framing framework-agnostic

**DON'T:**
- Inline the full `design.json` or `structure.md` into the handoff (contrasts: point to files)
- Skip intent capture (contrasts: capture intent explicitly)
- Prescribe a specific framework or library (contrasts: keep framing agnostic)
- Treat the handoff as a frozen snapshot — if source changes, regenerate (contrasts: keep bundle pointing to live files)

## Error Handling

- No `design.json`: handoff is premature. Run extract design first
- No `structure.md`: handoff is premature. Run structure first
- No preview approved: warn that the handoff lacks a visual reference; proceed only if confirmed
- Intent unclear after discovery: ask the user directly, do not fabricate

## Next Steps

After handoff, suggest:

- "Share the handoff with the implementer"
- "If edits come back from implementation, run sync to propagate back to design.json and structure.md"
