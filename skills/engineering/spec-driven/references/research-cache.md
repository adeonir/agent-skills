# Research Cache

The shape of a `.artifacts/research/<topic>.md` entry: a finding that outlives the design that produced it.

## When to Use

When reading the cache as the first evidence a question is put to, and when writing a finding — documentary or observed — that could answer the same question for a later feature.

## Reading

Compare `verified-against` with the project's current state before using any finding in the file.

- **Basis matches** — the finding stands. Use it, and cite the file path in the `Source` cell of the Decisions row or Risks entry it settles.
- **Basis diverges** — every finding in the file is void: it carries no evidential weight, not even as a hint. Re-verify with the cheapest observation that answers the question and overwrite the file with the new observation and the new basis.

Decide trust from `verified-against` alone, never from `updated`: a lockfile bumped this morning voids an observation written last night.

## Writing

Cache only a finding a later feature could ask again; one scoped to this feature lands in `design.md` alone. A documentary finding (what the docs state for the installed version) and an observed one (what a command proved against this environment) share the file; only `source` differs. Keep findings that share one basis in one topic file, and put a finding with another basis in another file.

Write the observation so a later reader can contradict it: "the batch API rejects a mixed-statement array with `D1_ERROR`", never "the batch API works". Cache an `UNVERIFIED` decision the same way, with what was attempted as the observation. Cache the observation, never the command that produced it.

Overwrite a stale file rather than appending to it; the overwrite bumps `updated` and leaves `created` untouched.

## Template

ALWAYS use this exact template structure.

```markdown
---
topic: <topic>
verified-against: [dependency@version | config path | environment]
source: docs | observed | mixed
created: [YYYY-MM-DD]              # the topic file's first write; never rewritten
updated: [YYYY-MM-DD]              # the observation's write; context, never grounds for trust
---

# [Topic]

## Findings

| Claim | Observation | Source |
|-------|-------------|--------|
| [the question the finding answers] | [what was found, stated so it can be contradicted] | [official doc deep-link, or where the observation was made] |

## Preconditions            <!-- conditional: only when a finding is a cost, not an answer -->
[An observation that the mechanism needs environment or infra setup to exercise. The setup cost is the finding; the next design inherits it instead of paying to rediscover it.]
```

MUST NOT contain: the deliberation that produced the finding, conversation narrative ("as discussed", "the user confirmed", "we agreed"), feature slugs, `AC-N.M` references, task IDs, or anything scoped to the design that happened to write it.
