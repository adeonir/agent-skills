---
name: grill-me
description: 'Interviews the user round by round to settle every open decision in a plan, design, or idea, asking questions with a recommended answer until nothing is left assumed. Use when stress-testing a plan, resolving open decisions before a document or spec is written, or when the user says "grill me", "grill this plan", or "ask me questions until we agree". Not for generating or comparing alternatives, writing documents, or reviewing code.'
---

# Grill Me

Interview the user until every decision in the plan is settled and nothing is left silently assumed.

## Triggers

- Stress-test a plan, a decision, or an idea
- Resolve open decisions before a document or spec is written
- "grill me", "grill this plan"

## Workflow

```text
tree → ask the frontier → answers → tree
         ^____________________________|
         frontier empty → confirm → record
```

1. **Map the plan as a design tree**: every decision branches into the decisions that hang off it. The frontier is every decision whose prerequisites are settled. Ask the whole frontier as one round, then let the answers reshape the tree and ask the next frontier.
2. **Ask with the harness question tool**, at most four questions per call, continuing in further calls of the same round. Give each question two to four mutually exclusive options, the recommended answer first and marked as recommended. Ask a question with no discrete options in chat, alone. With no question tool, ask the round as a numbered list in chat, each question carrying its recommended answer.
3. **Find facts yourself.** Look up what the environment can answer, by a subagent when the reading is long, and never ask the user for it. Ask the rest of the frontier meanwhile.
4. **Close when the frontier is empty.** State the shared understanding and wait for the user to confirm it before acting on it. Then apply `domain-modeling` for every term the interview resolved, and the ADR flow of `docs-writer` for every decision that is hard to reverse, surprising without context, and the result of a real trade-off.
