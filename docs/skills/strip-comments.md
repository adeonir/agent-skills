# Strip Comments

Deletes comments that narrate, excuse, or warn around code, then fixes the code those comments were covering.

## What It Does

| Phase | Output |
|---|---|
| Hunt | A sub-agent deletes the comments in scope and flags the code behind each excuse as `MUST KILL` |
| Audit | Deletions, keeps, and flags checked against the diff; missed suppressions added |
| Fix | Smallest root-cause fix in scope for each flag |
| Constraints | Offer to encode `do not remove` notes as a type, check, test, or lint rule |

## Usage

```text
strip the comments from this diff
clean the comments out of src/auth
remove the workaround comments and fix what they cover
```

## FAQ

**Q: Which comments survive?** A: License headers, notes on behavior forced by an external dependency, faulty or style-only lint suppressions, public API doc comments, and issue or RFC links that explain a constraint the code cannot express.

**Q: Does the sub-agent change my code?** A: No. It edits comments only; the fixes happen in the main session, and a design choice waits for your approval.
