# Research Cache

The shape of a `.artifacts/research/{topic}.md` entry: a finding that outlives the design that produced it.

## When to Use

When reading the cache as the bottom rung of the verification ladder, and when writing a finding — documentary or observed — that could answer the same question for a later feature.

## What the Cache Is For

A finding is cached so the next design reads it instead of re-deriving it: no re-fetching a doc, no re-running a spike. Reuse is the only reason the file exists — a finding scoped so tightly to one feature that nothing else could ask it again is not cached at all; it lands in `design.md` and dies with the feature.

A documentary finding (what the docs state for the installed version) and an observed finding (what a spike proved against this environment) share one file, because they answer the same shape of question and are read from the same rung. Only their `source` differs.

The spike's code is never cached. The spike is disposable by construction; what survives is the observation it produced.

## Falsifiability

A cached finding is a claim about a world that changes. The dependency is upgraded, the config is rewritten, the runtime moves — and the observation that was true becomes a lie that reads exactly like the truth. **A cache that cannot be falsified is a trap, not a shortcut**: it is worse than no cache, because re-deriving costs time while trusting a stale finding costs a wrong design.

So every entry records the basis it was observed under, and the reader checks that basis before trusting the finding. `verified-against` carries it: the dependency and version from the manifest, the config file, or the environment the observation depended on.

A topic file holds findings that share one basis. When a finding's basis differs, it belongs to a different topic file — that keeps the void-check a single comparison rather than a per-finding audit.

## Reading

Compare `verified-against` with the project's current state before using any finding in the file.

- **Basis matches** — the finding stands. Use it, and cite the file path in the `Source` cell of the Decisions row or Risks entry it settles.
- **Basis diverges** — every finding in the file is void. Do not weigh it, do not treat it as a hint, do not "probably still true" it. Re-verify from the ladder and overwrite the file with the new observation and the new basis.

A void entry is not a weaker entry. It carries no evidential weight at all, and reasoning from it is how a stale finding survives into a design.

**`updated` never grounds that judgment.** A recent date is not evidence the finding still holds — a lockfile bumped this morning voids an observation written last night, and a basis nothing has touched in a year still stands. Read the date for context (how long this has gone unexercised, whether the topic is worth revisiting) and decide trust from `verified-against` alone. Trusting a finding because it looks recent is the exact reasoning the void rule exists to stop.

## Template

ALWAYS use this exact template structure.

```markdown
---
topic: {topic}
verified-against: {dependency@version | config path | environment}
source: docs | spike | mixed
created: {YYYY-MM-DD}              # the topic file's first write; never rewritten
updated: {YYYY-MM-DD}              # the observation's write; context, never grounds for trust
---

# {Topic}

## Findings

| Claim | Observation | Source |
|-------|-------------|--------|
| {the question the finding answers} | {what was found, stated so it can be contradicted} | {official doc deep-link, or `spike`} |

## Preconditions            <!-- conditional: only when a finding is a cost, not an answer -->
{An observation that the mechanism needs environment or infra setup to exercise. The setup cost is the finding; the next design inherits it instead of paying to rediscover it.}
```

MUST NOT contain: the spike's code, the deliberation that produced the finding, feature slugs, `AC-N` references, task IDs, or anything scoped to the design that happened to write it. The cache belongs to the project, not to a feature.

## Writing

Write the observation so a later reader can contradict it. "The batch API works" survives any evidence; "the batch API rejects a mixed-statement array with `D1_ERROR`" is a claim the next run either reproduces or refutes.

An `UNVERIFIED` decision is cached the same way, with what was attempted recorded as the observation — the next design inherits the dead end instead of walking into it, which is a finding as real as an answer.

Overwrite a stale file rather than appending to it. A cache that accumulates every basis it ever had becomes a history nobody can read, and the void-check degrades into archaeology. An overwrite bumps `updated` and leaves `created` untouched — `created` dates the topic, `updated` dates the observation, and it is the observation a reader is weighing.
