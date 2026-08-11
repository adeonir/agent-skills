## File and Directory Casing

**Impact: MEDIUM**

Fixed files use UPPERCASE names (`SKILL.md`, `README.md`); skill directories and reference files use kebab-case; sub-directories stay lowercase (`references/`, `scripts/`). Consistent casing keeps paths predictable across skills.

**Incorrect:**

```text
skills/engineering/GitHelpers/References/Quick_Mode.md
```

**Correct:**

```text
skills/engineering/git-helpers/references/quick-mode.md
```

## Slash Command Equals Name

**Impact: LOW**

The slash command always equals the skill `name`; do not invent aliases. The harness derives the command from the name, so an alias is a second source that drifts.

**Incorrect:**

```yaml
name: git-helpers
aliases: [gh, commit-helper]
```

**Correct:**

```yaml
name: git-helpers
```
