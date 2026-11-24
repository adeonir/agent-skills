# Refresh

Tighten and improve existing copy in `copy.yaml` in the same voice. Brownfield: when the content is sound but the writing is loose, run focused editing passes and patch the payload in place.

## Load first

Read [discovery.md](discovery.md) before starting — it settles the existing context, the confirmed intent and voice, and the register this operation must respect.

## Workflow

### Step 1: Read Current Copy

Parse `docs/product/copy.yaml`. If either block is missing or inferred, use discovery before editing.

### Step 2: Run the Sweeps

Apply [../references/editing-sweeps.md](editing-sweeps.md) per content part: clarity → voice consistency → reader value → prove it → specificity → reader pull → reader confidence, then the quick-pass word/sentence/paragraph checks. Apply the function-specific meaning of each sweep. Pull proof guidance from [../references/voice.md](voice.md); the dead-word and dead-structure catalogue is in [../references/anti-patterns.md](anti-patterns.md). The voice pass checks *consistency* only; never change the voice. For microcopy (labels, errors, states, navigation), also run the clarity method in [../references/ux-writing.md](ux-writing.md).

### Step 3: Patch copy.yaml

Apply the edits in place. Preserve the content tree paths and the voice; never change the voice or reorganize the structure. If discovery confirmed missing or inferred metadata, add the confirmed root intent and voice in the same patch.

### Step 4: Self-Check

Before finishing, check the content tree, design leakage, core message, and voice. Run the validator for the first two:

```bash
python3 <this-skill>/scripts/validate_copy.py docs/product/copy.yaml
```

Resolve any real flag. Judge false positives, such as a product named "Grid".

### Step 5: Report

Report the path, what changed in one to three sentences, and any open item `copy.yaml` carries. Never paste the file. Then, per part, quote the original line and the tightened line with a one-line reason. Group by `copy.yaml` content path.

## Guidelines

**DO:**

- Enhance, do not rewrite: preserve the intent, core message, and author's voice
- One focused dimension per pass; loop back after edits
- Make every vague claim specific or cut it

**DON'T:**

- Change the surface function or add function-specific parts that were not requested
- Restructure the content tree
- Embed visual decisions in `copy.yaml`
- Invent proof to satisfy a sweep; soften the claim instead

## Error Handling

- `copy.yaml` missing: nothing to refresh; route to extract or write first
- Copy is already tight: report `no edits needed` and stop
- A claim needs proof the user lacks: soften the claim, flag it, do not fabricate
