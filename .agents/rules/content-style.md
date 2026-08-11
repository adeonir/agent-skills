## Content Style

**Impact: MEDIUM**

Write skills and rules in clear, consistent English so agents can apply the repository's authoring conventions without extra interpretation.

### Principles

- Write repository files in English.
- Never use emoji.
- Never hard wrap the body. One paragraph is one line, one bullet is one line.
- Write the frontmatter `description` on one line. Quote the value that carries a colon.
- Write the frontmatter `description` in third person.
- Put the key use case first in the `description`, and cap it at 1024 characters.
- Write a slot inside a path or a command as `<what goes here>`: `src/skills/<group>/<name>/SKILL.md`.
- Write a slot the reader fills inside a template as `[what goes here]`.
- Write the name of a skill or a rule in backticks: `spec-memory`.
- Write only what the agent does not already know. Cut the line it would follow without being told, such as what a pull request is.
- State what to do. Never narrate how or why, in a skill or in a rule.
- Write the body in the imperative: "Read the issue through the tracker's MCP server", never "The issue is read through the tracker's MCP server". The `description` is the one field in third person.
- Keep a reason only when it decides something: a cost the agent has to weigh, or the condition that selects between two options.
- Give exact instructions where a wrong move is expensive and the sequence matters. Name the goal where many routes work.
- For a workflow, offer one default and one escape hatch. A body that lays out three routes makes the agent pick again on every run.
- Use one term per concept across the whole file. Never alternate between "endpoint", "route" and "path" for the same thing.
- Make every example a real path, command or type from the domain. Never `foo`, `bar` or `doSomething`.
- Leave the example out where the domain carries none. The line asks for the real case over the placeholder, never for an invented case over no case: a fabricated example is read as a fact about the tree the reader is in.
- State the rule, then show the case. Never restate the rule after the example.
- Never write dated content: no "until August", no "in the current version", no deadline.
- Say what to do before saying what to avoid. Name what to avoid only when it is a mistake someone makes.
