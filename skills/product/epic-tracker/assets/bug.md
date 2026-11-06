ALWAYS use this exact template structure:

````markdown
## Summary

{{What is broken and who it affects. One to three sentences.}}

MUST NOT contain: conversation narrative ("as discussed", "the user reported that"), decision history, `§x.x` section numbers, document or reference codes, sibling-artifact names, a fix suggestion, or code identifiers and fix mechanism. Source links and ticket ids travel in Signals, with the verbatim errors and stack traces; `ADR-NNN` belongs to the fix and enters the bug nowhere.

## Steps to Reproduce

1. {{First action}}
2. {{Next action}}
3. {{Action where the bug shows}}

**Reproducible:** {{always | intermittently | once, as it behaved while live — plus whether it still occurs, and when it is not always, what is known about when it happened}}

## Expected Behavior

{{What should happen.}}

## Actual Behavior

{{What happens instead.}}

## Signals

{Forensic data from logs/dashboards/error reports. Populate from pasted context. Remove this section if no signals are available.}

- **Links:** {{deployment URL, error tracker issue, observability dashboard, repo URL}}
- **Identifiers:** {{request id, trace id, deployment id, commit hash, user id}}
- **First observed:** {{timestamp}}
- **Error excerpt:**

  ```text
  {{stack trace or error message verbatim}}
  ```

## Environment

{Remove this section when nothing about the running system bears on the
defect. Name what identifies the run: browser and OS for a client defect;
deploy, commit, runtime, and region for a server defect. Drop a line with
nothing to say.}

- {{Field: value}}

## Regression

{Remove this section if the bug is not known to be a regression.}

- **Introduced in:** {{release, commit, or deployment where the bug first appeared}}
- **Last known good:** {{release, commit, or deployment where it worked}}

## Workaround

{Remove this section when no mitigation is known.}

{{The known mitigation.}}

## Acceptance Criteria

- [ ] {{The steps above produce the expected behavior.}}
- [ ] {{A check that fails before the fix and passes after it covers the case. Omit when the project has no way to run one.}}

{Each line is one verifiable condition. See [ac-validation.md](../references/ac-validation.md) for the contract.}

MUST NOT contain: a requirement link, a fix mechanism, or a condition no outcome of the fix can show.

## References

{Durable pointers to what the tracker does not model, chosen for what
matters to this bug. The parent epic and every dependency are tracker
relations, not lines here. Remove the section when there is nothing to
point at; a line saying "None" states nothing and rots the same as a
stale link.

A doc link (a file in a repo, like a Design Doc) is an absolute URL or a
repo-relative path. A relative path resolves only when the tracker and the
file share a host; across hosts, use an absolute URL.}

- {{A pointer relevant to this bug: a design doc, a related issue, material the fix starts from.}}

MUST NOT contain: the parent epic or a dependency (tracker relations).
````

This is the tracker description; the dispatch inputs (title, epic id, severity, `blocked_by`, `priority`, `estimate`) travel as metadata alongside it. The body opens at `## Summary` — the tracker renders the title above the description, so no title heading belongs in the body.
