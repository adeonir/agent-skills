---
paths:
  - "skills/**/*.md"
---

## One Level, One Selector

**Impact: HIGH**

Every supporting file sits one hop from `SKILL.md`, and the index is the only selector: a reference never links to another reference.

A constraint two procedures need is its own reference, announced in the index with a condition that covers both jobs.

**Incorrect:**

```markdown
<!-- references/create-pull-request.md -->
Read [message-sourcing.md](../references/message-sourcing.md) before writing the body.
```

**Correct:**

```markdown
<!-- SKILL.md -->
- **Wording** — a commit, pull request, or merge is about to write text → [message-sourcing.md](references/message-sourcing.md) · the diction bar and the sourcing rule
```

## Reference Header

**Impact: MEDIUM**

Open with the H1, using the same words as the index entry, then one sentence: the result a procedure produces, or what the material provides. The index states the condition; the file states the payload.

**Incorrect:**

```markdown
# Commit

## When to Use

Load this when the user asks to commit.
```

**Correct:**

```markdown
# Commit

Creates a conventional commit from the actual changes.
```

## Procedure Ends Where the Job Ends

**Impact: MEDIUM**

Every step declares its input, action, and completion condition. A check that can fail carries a line saying where to return. The file ends at its outcome and never hands over the next job.

**Incorrect:**

```markdown
## Next Steps

After generating the spec, run the design phase.
```

**Correct:**

```markdown
2. **Fill** the template at `assets/spec.md`; done when every placeholder carries a value.
```

## Scripts and Tool Calls

**Impact: MEDIUM**

A script takes input from arguments, including every path, and reports through the exit code: `0` for success, non-zero with an actionable message on stderr. A mutation is idempotent or refuses a second run. The step anchors its completion condition to the exit code, so a broken script fails loudly.

Name every MCP tool as `Server:tool_name`.

**Incorrect:**

```markdown
Run the validator and check that the output looks right. Call create_issue.
```

**Correct:**

```markdown
Run `python3 scripts/validate_fields.py fields.json`; done when it exits `0`, and a non-zero exit lists the offending field and returns to step 2. Call GitHub:create_issue.
```

## Assets Hold Data

**Impact: MEDIUM**

A copyable template lives in `assets/`, named for the artifact it produces, with its rigidity stated on the first line: `Use this template as written:` or `Adapt this template to the case:`. The step says whether it reads or fills the asset. The procedure stays in the reference.

**Incorrect:**

```text
skill-name/templates/spec.md
```

**Correct:**

```text
skill-name/assets/spec.md
```

```markdown
Use this template as written:

## Summary
{{...}}
```
