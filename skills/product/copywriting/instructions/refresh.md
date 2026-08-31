# Refresh

Tighten and improve existing copy in `copy.yaml` in the same voice. Brownfield: when the content is sound but the writing is loose, run focused editing passes and patch the payload in place.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the existing context, the confirmed intent and voice, and the register this operation must respect.

Not for: changing the voice (a different job; refresh keeps the voice), structuring net-new content (see [extract.md](extract.md) or [write.md](write.md)), or syncing from code (see [reconcile.md](reconcile.md)).

## Workflow

### Step 1: Read Current Copy

Parse `docs/design/copy.yaml`. Note the established intent and voice; refresh preserves both. If either block is missing or inferred, use discovery before proposing edits.

### Step 2: Run the Sweeps

Apply [../references/editing-sweeps.md](../references/editing-sweeps.md) per content part: clarity → voice consistency → reader value → prove it → specificity → reader pull → reader confidence, then the quick-pass word/sentence/paragraph checks. Check the intent constraints before each sweep; do not introduce a forbidden technique to improve another dimension. Apply the function-specific meaning of each sweep. Pull proof guidance from [../references/voice.md](../references/voice.md); the dead-word and dead-structure catalogue is in [../references/anti-patterns.md](../references/anti-patterns.md). The voice pass checks *consistency* only; never change the voice. For microcopy (labels, errors, states, navigation), also run the clarity method in [../references/ux-writing.md](../references/ux-writing.md).

### Step 3: Propose Edits

Per part, quote the current line, propose the tightened line, give a one-line reason. Group by `copy.yaml` content path.

### Step 4: Confirm Before Write

Present the edits inline. User approves, rejects, or edits each row. No silent writes. If the user rejects every row, stop with `no edits applied`.

### Step 5: Patch copy.yaml

Apply approved edits in place. Preserve the content tree paths and the voice; never change the voice or reorganize the structure. If discovery confirmed missing or inferred metadata, add the confirmed root intent and voice in the same patch.

### Step 6: Self-Check

Before finishing, check the content tree, design leakage, core message, and voice. Run the validator for the first two:

```bash
python3 <this-skill>/scripts/validate_copy.py docs/design/copy.yaml
```

Resolve any real flag. Judge false positives, such as a product named "Grid".

## Guidelines

**DO:**

- Enhance, do not rewrite: preserve the intent, core message, and author's voice
- One focused dimension per pass; loop back after edits
- Make every vague claim specific or cut it
- Confirm each edit; the author owns the copy

**DON'T:**

- Change the voice (contrasts: refresh keeps it; changing voice is a separate job)
- Change the surface function or add function-specific parts that were not requested
- Restructure the content tree (contrasts: patch values, not shape)
- Embed visual decisions in `copy.yaml` (contrasts: content-only)
- Invent proof to satisfy a sweep (contrasts: soften the claim instead)

## Error Handling

- `copy.yaml` missing: nothing to refresh; route to extract or write first
- Copy is already tight: report `no edits needed` and stop
- A claim needs proof the user lacks: soften the claim, flag it, do not fabricate
- User rejects every edit: leave the file untouched, report what was rejected
