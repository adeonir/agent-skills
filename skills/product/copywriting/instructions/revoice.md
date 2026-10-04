# Revoice

Rewrite existing copy in `copy.yaml` into a new voice while keeping the message. Brownfield: when the content is right but the tone should change (more playful, more formal, more premium), recast each line and patch the payload in place. The verbal analogue of a rebrand: same message, new voice.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the existing context, the confirmed intent and voice, and the register this operation must respect.

Not for: tightening in the same voice (see [refresh.md](refresh.md)), writing net-new copy (see [write.md](write.md)), or syncing from code (see [reconcile.md](reconcile.md)).

## Workflow

### Step 1: Read Current Copy

Parse `docs/product/copy.yaml`. Note the current intent and voice; revoice replaces the voice only.

### Step 2: Establish Target Voice

Get the target from the user: a stated direction ("more playful", "luxury", "drier") or a sample to match. Hold the surface's **intent** and **register** (brand or product; [../references/brand.md](../references/brand.md) / [../references/product.md](../references/product.md)); they bound how far the voice can move. Then set the axes from [../references/voice.md](../references/voice.md). Confirm it back in one line before recasting.

### Step 3: Recast Each Part

Rewrite each line into the target voice, preserving the message, every claim, and the structure. Change *how* it is said, never *what*. Do not introduce dead adjectives (see [../references/anti-patterns.md](../references/anti-patterns.md)) or drop proof (see [../references/voice.md](../references/voice.md)).

### Step 4: Patch copy.yaml

Apply the rewrites in place. Preserve the content tree paths and every claim; only the voice changes. Update the `voice` block to the target voice with `status: confirmed` in the same patch. If discovery established missing or inferred metadata, add the confirmed root intent and voice in the same patch.

### Step 5: Self-Check

Before finishing, check that every original claim remains, the content tree is well-formed, and no design leaked into it. Run the validator for the last two:

```bash
python3 <this-skill>/scripts/validate_copy.py docs/product/copy.yaml
```

Resolve any real flag. Judge false positives, such as a product named "Grid".

### Step 6: Report

Report the path, what changed in one to three sentences, and any open item `copy.yaml` carries. Never paste the file. Then, per content path, show the original line → the revoiced line + a one-line note.

## Guidelines

**DO:**

- Change the voice, keep the message and surface function: same claims, same structure
- Set and confirm the target voice before recasting
- Hold the new voice consistently across every part

**DON'T:**

- Add or drop claims (contrasts: revoice changes tone, not substance)
- Change the surface function or introduce conversion, marketing, or task elements that were not present
- Restructure the content tree (contrasts: patch values, not shape)
- Reintroduce dead adjectives or marketing clichés (contrasts: see anti-patterns.md)
- Embed visual decisions in `copy.yaml` (contrasts: content-only)

## Error Handling

- `copy.yaml` missing: nothing to revoice; route to extract or write first
- Target voice unclear: ask for a descriptor or a sample to match before recasting
- A claim cannot survive the new voice honestly: keep the claim, flag the tension
