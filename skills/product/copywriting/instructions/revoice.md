# Revoice

Rewrite existing copy in `copy.yaml` into a new voice — keeping the message. Brownfield: when the content is right but the tone should change (more playful, more formal, more premium), recast each line and patch the payload in place. The verbal analogue of a rebrand: same message, new voice.

## When to Use

- User wants existing copy in a different voice or tone ("make it playful", "make it sound premium", "drier, less salesy")
- A rebrand or audience shift means the words should sound different
- The message is fine, the personality is not

Not for: tightening in the same voice (see [refresh.md](refresh.md)), writing net-new copy (see [write.md](write.md)), or syncing from code (see [reconcile.md](reconcile.md)).

## Workflow

### Step 1: Read Current Copy

Parse `docs/design/copy.yaml`. Note the current voice — you are replacing it.

### Step 2: Establish Target Voice

Get the target from the user (stated — "more playful", "luxury", "drier" — or a sample to match). Hold the surface's **register** (brand or product — [../references/brand.md](../references/brand.md) / [../references/product.md](../references/product.md)); it bounds how far the voice can move — a product surface stays calm and instructional even when revoiced. Then set the axes from [../references/voice.md](../references/voice.md). Confirm it back in one line before recasting.

### Step 3: Recast Each Part

Rewrite each line into the target voice, preserving the message, every claim, and the structure. Change *how* it is said, never *what*. Do not introduce dead adjectives (see [../references/anti-patterns.md](../references/anti-patterns.md)) or drop proof (see [../references/voice.md](../references/voice.md)).

### Step 4: Confirm Before Write

Per content path, show the current line → the revoiced line + a one-line note. User approves, rejects, or edits each. No silent writes. If the user rejects every row, stop with `no changes applied`.

### Step 5: Patch copy.yaml

Apply approved rewrites in place. Preserve the content tree paths and every claim; only the voice changes.

### Step 6: Self-Check

Before done: every claim from the original is still present (none added, none lost), no design leakage, well-formed content tree. Run the deterministic floor for the last two:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_copy.py docs/design/copy.yaml
```

Resolve any flags (advisory — judge false positives like a product named "Grid").

## Guidelines

**DO:**

- Change the voice, keep the message — same claims, same structure
- Set and confirm the target voice before recasting
- Hold the new voice consistently across every part
- Confirm each rewrite; the author owns the copy

**DON'T:**

- Add or drop claims (contrasts: revoice changes tone, not substance)
- Restructure the content tree (contrasts: patch values, not shape)
- Reintroduce dead adjectives or marketing clichés (contrasts: see anti-patterns.md)
- Embed visual decisions in `copy.yaml` (contrasts: content-only)

## Error Handling

- `copy.yaml` missing: nothing to revoice — route to extract or write first
- Target voice unclear: ask for a descriptor or a sample to match before recasting
- A claim cannot survive the new voice honestly: keep the claim, flag the tension
- User rejects every rewrite: leave the file untouched, report what was rejected
