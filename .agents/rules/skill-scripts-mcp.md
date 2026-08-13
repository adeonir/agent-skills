---
paths:
  - "skills/**/*.md"
---

## Resolve Bundled Scripts From the Skill Directory

**Impact: MEDIUM**

When a skill runs its own bundled script, write the path as `<this-skill>/scripts/<name>` and resolve `<this-skill>` to the directory the `SKILL.md` was read from before running the command. Never write `${CLAUDE_SKILL_DIR}` or a bare relative path. If the host does not expose the path the `SKILL.md` was read from, stop and report an environment problem.

**Incorrect:**

```bash
python ${CLAUDE_SKILL_DIR}/scripts/extract.py "$@"
```

**Correct:**

```bash
python <this-skill>/scripts/extract.py "$@"
```

## Qualify MCP Tool Names

**Impact: MEDIUM**

Reference every MCP tool by its qualified `Server:tool_name`. Without the server prefix, the call is ambiguous when two servers expose the same tool name, and the agent may invoke the wrong one.

**Incorrect:**

```text
Call create_issue to open the ticket.
```

**Correct:**

```text
Call GitHub:create_issue to open the ticket.
```

## No Voodoo Constants

**Impact: MEDIUM**

Every numeric constant in a bundled script carries a comment justifying its value. An unexplained constant is one the next author cannot safely change and one the model cannot reason about.

**Incorrect:**

```python
chunk = data[:512]
```

**Correct:**

```python
chunk = data[:512]  # 512: provider embedding token limit per request
```

## Scripts Solve, Don't Punt

**Impact: MEDIUM**

A bundled script handles its own errors with explicit fallbacks (try/except, default values) instead of surfacing a raw exception for the agent to resolve. The script is the deterministic layer; punting defeats its purpose.

**Incorrect:**

```python
data = json.load(open(path))
```

**Correct:**

```python
try:
    data = json.load(open(path))
except (OSError, json.JSONDecodeError):
    data = {}
```
