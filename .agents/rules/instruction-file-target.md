---
paths:
  - "skills/**"
---

## Resolve the Instruction File the Same Way Everywhere

**Impact: HIGH**

A skill that maintains an owned block in the project's instruction file uses the same target selection and the same section maintenance as every other skill. Every skill that resolves the instruction file bundles this contract as `references/instruction-file.md`, and the copies across skills stay identical; the canonical text is the one in the `git-helpers` skill. Skills that edit instruction-file content instead (extracting, trimming, placing facts) carry their own placement contracts and are outside this rule. Skills ship standalone, so the mechanism repeats as code or reference; the copies must implement the contract exactly. The canonical code lives in the `instruction_path`, `tracker_sections`, and `replace_block` functions of `tracker-config/scripts/config.py` — copy from there, rename freely, change the algorithm in all copies together.

Target selection, resolved from the repository root (`git rev-parse --show-toplevel`):

1. `CLAUDE.md` at the root.
2. `.claude/CLAUDE.md`.
3. When the chosen `CLAUDE.md` imports `AGENTS.md` — a line containing only `@AGENTS.md`, `./AGENTS.md`, or `../AGENTS.md` — resolve the import relative to the importing file and use that path.
4. Otherwise `AGENTS.md` at the root.

A target that resolves outside the repository is an error.

Section maintenance for each owned block (one section per skill, titled by the contract of the skill):

- Scan real level-two headings. A fenced example is not a heading: track CommonMark fences (up to three leading spaces, three or more markers, a closing fence matching the opening marker and length) and read nothing inside one.
- An unclosed fence is an error.
- Maintain exactly one owned section: replace its body; append at the end with a blank line separation when absent.
- Duplicate owned sections, more than one nonblank line of unrelated body content, or a target outside the repository are errors reported for manual resolution — never auto-rewritten.
- Preserve the file's CRLF/LF endings.
- On failure, leave the file untouched.

**Incorrect:**

```python
target = root / "AGENTS.md"  # every project records instructions in AGENTS.md
```

**Correct:**

```python
target = instruction_path(root)
```

## One Block Is the Whole Signature

**Impact: MEDIUM**

An owned block is a record, not a rules body: the section heading plus one sentence. The git config, environment, or script that maintains the block is the mechanism and stays out of it. If a consumer needs reconfiguration steps, the skill's own instructions carry them.

**Incorrect:**

```markdown
## Issue tracker

Tracker: Linear; team ENG; project Platform. Inspect with `git config --local --get-regexp '^tracker\.'`. Change with "configure tracker".
```

**Correct:**

```markdown
## Issue tracker

Tracker: Linear; team ENG; project Platform.
```
