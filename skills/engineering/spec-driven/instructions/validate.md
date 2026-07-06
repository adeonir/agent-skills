# Validate / UAT

User-facing acceptance testing after a passing technical audit. Owned by the main agent, not the auditor subagent. Appends `## Visual Evidence` to the existing `validation.md` — never a separate file.

## When to Use

Only when the feature is `user-facing: true` (spec frontmatter) and the audit has returned PASS. Non-user-facing features skip this entirely. Also runs when the user asks to run UAT, do manual testing, or validate flows on a feature.

## Workflow

1. **Confirm the gate** — `spec.md user-facing: true` and audit status PASS. Otherwise stop; there is nothing to validate.
2. **Load references** — the `spec.md` visual references and user stories define the flows and states to exercise.
3. **Exercise the flows** — walk each user-facing flow and capture evidence per screen and state into `.artifacts/specs/{slug}/evidences/`. If a browser-automation MCP is available (e.g. `Playwright:browser_navigate`, `Playwright:browser_take_screenshot`), use it to navigate, screenshot, and check accessibility and responsiveness. If none is available, fall back to guiding the user through the flow and collecting their screenshots. Detect availability before calling; never assume the MCP is present.
4. **Append `## Visual Evidence`** to `validation.md` using the table below.
5. **Get explicit user approval** — UAT does not self-approve. Only after the user confirms does `spec.md` move to `status: done`; on that flip, clear `.artifacts/STATE.md` per [memory.md](../references/memory.md) — the feature is no longer active.

## Template: `## Visual Evidence`

ALWAYS use this exact section structure, appended to the feature's `validation.md`:

```markdown
## Visual Evidence
| Screen | State | Evidence | Result |
|--------|-------|----------|--------|
| checkout | error | `evidences/checkout-error.png` | PASS |
| checkout | success | `evidences/checkout-success.png` | PASS |
```

MUST NOT contain: a new `validation.md` file (this appends to the existing one), code fixes, or automatic status transition — `done` waits for explicit user approval.
