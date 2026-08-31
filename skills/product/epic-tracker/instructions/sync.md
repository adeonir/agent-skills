# Sync

Change status, read delivery state, reparent an artifact, edit its dependencies, or configure the tracker.

## Load first

Read [tracker.md](../references/tracker.md) — the config, the bootstrap, the dispatch flows, and the adapter operations every step below goes through. Without a tracker configured, its bootstrap runs first and nothing else proceeds until it completes.

## Status change

A bare status change ("mark done", "cancel this", "move to in-progress") is an update like any other, and takes the same guard:

1. `fetch_artifact` to read the current status, and the artifact's type.
2. When the tracker's status already differs from what the user expects, surface it and confirm before proceeding — someone moved it.
3. Closing an **epic** — `done` or `cancelled` — is a claim about its whole subtree, so read the subtree first: `list_artifacts` filtered to that epic. When any child is not closed, surface how many and in which status, and confirm before proceeding. Never close or cancel a child to make the epic's status true; each child is its own decision, taken on its own artifact. A story, bug, or task closes without this read — nothing hangs under it.
4. Call `update_status` with the new value.

## Status and Overview

Reading delivery state is a tracker query, not a stored report:

- **List** ("list epics", "what's in progress", "show the stories in this epic") → `list_artifacts` with the matching filter. Present the results; write nothing.
- **Status change** ("mark done", "cancel this", "won't fix") → the Status change flow above.
- **Reparent** ("move this to epic X", "reparent this story") → settle the milestone guard **before** moving. `set_parent` replaces the parent link, so once it runs the artifact no longer points at the epic the guard compares against.
  1. `fetch_artifact` on the artifact — its current parent and its current milestone. This is the refetch every write already owes.
  2. When it has a parent, `fetch_artifact` on that epic for the milestone the artifact should be carrying. A match is ordinary inheritance. Anything else — a different milestone, or one on an artifact that was standalone — is state the skill did not put there, so it is confirmed before being replaced, exactly as a body the tracker moved underneath is.
  3. `set_parent` with the target `epic_id`, resolved through the loaded reference's Resolving the Parent Epic when the request names an epic by title or names none.
  4. `fetch_artifact` on the target epic and dispatch `set_milestone` with the milestone it carries — none clears the artifact's milestone — so it follows its epic under the milestone grouping.
- **Dependency change** ("block this on ENG-42", "unblock this", "this depends on X") → `set_dependencies` with the artifact's full `blocked_by` list, plus `update_artifact` carrying the re-rendered `## Dependencies` section, under the same refetch guard as any other write (see the loaded reference's Dependencies).

Each needs an adapter, so this ref is loaded for them even though no artifact is being drafted.
