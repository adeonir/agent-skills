# Refresh

Tighten and improve existing copy in `copy.yaml` — in the same voice.
Brownfield: when the content is sound but the writing is loose, run focused
editing passes and patch the payload in place.

## When to Use

- User wants existing `copy.yaml` copy tightened, sharpened, or polished
- Copy reads weak, wordy, vague, or buries the value
- Content has gone stale (outdated numbers, dated examples) and needs a refresh
- After a draft, before handoff — a quality pass on the words

Not for: changing the voice (that is a different job — refresh keeps the voice),
structuring net-new content (see [extract.md](extract.md) or
[write.md](write.md)), or syncing from code (see [reconcile.md](reconcile.md)).

## Workflow

### Step 1: Read Current Copy

Parse `docs/design/copy.yaml`. Note the established voice — refresh preserves
it.

### Step 2: Run the Sweeps

Apply [../references/editing-sweeps.md](../references/editing-sweeps.md) per
content part: clarity → voice consistency → so-what → prove-it → specificity →
emotion → zero-risk, then the quick-pass word/sentence/paragraph checks. Pull
proof and dead-adjective guidance from
[../references/voice.md](../references/voice.md). The voice pass checks
*consistency* only — never change the voice.

### Step 3: Propose Edits

Per part, quote the current line, propose the tightened line, give a one-line
reason. Group by `copy.yaml` content path.

### Step 4: Confirm Before Write

Present the edits inline. User approves, rejects, or edits each row. No silent
writes. If the user rejects every row, stop with `no edits applied`.

### Step 5: Patch copy.yaml

Apply approved edits in place. Preserve the content tree paths and the voice;
never change the voice or reorganize the structure.

### Step 6: Self-Check

Before done: well-formed content tree, no design leakage, core message and
voice intact.

## Guidelines

**DO:**

- Enhance, do not rewrite — preserve the core message and the author's voice
- One focused dimension per pass; loop back after edits
- Make every vague claim specific or cut it
- Confirm each edit; the author owns the copy

**DON'T:**

- Change the voice (contrasts: refresh keeps it; changing voice is a separate job)
- Restructure the content tree (contrasts: patch values, not shape)
- Embed visual decisions in `copy.yaml` (contrasts: content-only)
- Invent proof to satisfy a sweep (contrasts: soften the claim instead)

## Error Handling

- `copy.yaml` missing: nothing to refresh — route to extract or write first
- Copy is already tight: report `no edits needed` and stop
- A claim needs proof the user lacks: soften the claim, flag it, do not fabricate
- User rejects every edit: leave the file untouched, report what was rejected
