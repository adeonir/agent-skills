---
paths:
  - "skills/**/*.md"
---

## One Routing Level

**Impact: HIGH**

`SKILL.md` selects the procedure; the procedure loads the material its steps need. A procedure never hands the job to another procedure, and material never points to another file.

A load is a step: the procedure says when to read the file and what it buys. A constraint two procedures need is one material file, loaded by each at the step that needs it, so a condition that only surfaces mid-procedure is still delivered.

**Incorrect:**

```markdown
<!-- references/create-pull-request.md -->
For the wording, see [message-sourcing.md](../references/message-sourcing.md).
```

**Correct:**

```markdown
<!-- references/create-pull-request.md -->
**Step 4. Load [message-sourcing.md](references/message-sourcing.md)** · the diction bar and the sourcing rule. Done when every line of the body comes from a hunk read in Step 3.
```

## Reference Header

**Impact: MEDIUM**

Open with the H1. A procedure uses the same words as the index branch that selects it, which makes the pair checkable by comparison; a material file names its topic, and its branch states when to load it. Then one sentence: the result a procedure produces, or what the material provides. A single-job skill has no branch label, so its H1 names the job and the sentence carries the payload.

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
**Step 2. Fill** the template at `assets/spec.md`; done when every placeholder carries a value.
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
