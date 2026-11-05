# FLOWS.md — {{product name}}

Here is a sensible default format, but use your best judgment:

---

```markdown
---
product: [name]
platform: [any target — e.g. website, mobile app, desktop, PWA]
updated: [date]
---

# FLOWS — [product name]

One flow per task. Priority flows carry full branch coverage; the rest are happy-path-only until promoted.

## Priority

1. [Flow name] — [value it carries]
2. [Flow name] — [value it carries]

## Flow: [name]

**Goal:** [complete checkout from the product screen]
**Entry:** [first-open | deep link | from Flow: browse]
**Type:** [onboarding/auth | task | conversion | settings]

[wireflow diagram — mermaid flowchart, one diagram, labeled arrows]

**Dead ends:**

| State | Exit to |
|-------|---------|
| [card rejected] | [payment screen with error message] |
| [timeout] | [return to cart] |

**Connects:** starts from [flow], hands off on [terminal state] to [flow].

## Connect Map

[macro diagram or list: every hand-off, in both directions — which flow ends where, which flow receives it]

## Unset

[TBD items the discovery interview left open]
```

---

One `## Flow:` section per task, in priority order — never a merged or shared section. A flow not yet drafted keeps its section with `**Goal:** TBD` and the reason, so the file maps the whole app even while partially planned.
