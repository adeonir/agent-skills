# Guidelines Audit

Audit code changes for compliance with project guideline files.

## Purpose

Verify changes follow explicit rules documented in project guideline files
(CLAUDE.md, AGENTS.md, and similar).

## Process

### Step 1: Find Guideline Files

Search from the git repository root, not the current directory:

```bash
git rev-parse --show-toplevel 2>/dev/null
```

Then search for guideline files within the repository:

```bash
find "$(git rev-parse --show-toplevel)" \( -name "CLAUDE.md" -o -name "AGENTS.md" \) -type f 2>/dev/null
```

IMPORTANT: Only use guideline files found inside the project repository.
Do NOT read files from the user home directory (e.g. ~/.claude/CLAUDE.md)
as those are personal global settings, not project guidelines.

### Step 2: Read Guidelines

Extract explicit rules from all discovered project guideline files.

### Step 3: Review Diff

Check each change against the extracted guidelines.

### Step 4: Score Violations

Only report violations with >= 80 confidence.

## Confidence Scoring

| Score | Action |
|-------|--------|
| >= 80 | Report violation |
| 50-79 | Investigate more |
| < 50 | Do not report |

## What to Check

- Explicit coding standards in guideline files
- Naming conventions if specified
- Architecture patterns if documented
- Forbidden practices if listed

## What NOT to Report

- Inferred or implied guidelines
- Style preferences not documented
- Best practices not mentioned in guideline files

## Output Format

```markdown
## Guidelines Compliance

- **[{score}] [{file}:{line}]** Guideline violation
  - **Source**: "{guideline file where the rule was found}"
  - **Guideline**: "{exact quote from the guideline file}"
  - **Violation**: What the code does wrong
  - **Fix**: How to comply

## Summary

X guidelines checked | Y violations found
```

## Rules

- Quote exact guideline being violated
- Reference the source guideline file (CLAUDE.md, AGENTS.md, etc.)
- Be specific about the violation
- Provide actionable fix
- If no guideline files found, report that and skip audit
