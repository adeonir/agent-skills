# Skill Pattern

The canonical form every skill in this repository is built to. It builds on the [Agent Skills](https://agentskills.io) specification and is stricter than it in a few places.

## Baseline

Build every skill to the specification. A rule in `.agents/rules/` adds a requirement the specification leaves open or tightens a limit it sets, staying consistent with the specification and holding one structure for each thing.

Treat the format as portable. Behavior that makes a skill work belongs in `SKILL.md` and `references/`; behavior that involves one host belongs in that host's metadata. A conformant skill keeps working when a host ignores a host-specific field.

Keep one level of guidance: every supporting file sits one hop from `SKILL.md`, and a file under `references/` refers by path to its scripts and assets.

## The skill directory

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── agents/
    └── openai.yaml
```

`references/` holds every supporting file. The distinction between a procedure and reference material is real and lives in the file's first two lines.

The skill directory holds these five entries. The human-facing page lives in `docs/`, described under [Documentation](#documentation).

Scope the skill to one job: one request in, one outcome out. Add a mode, a phase, or a depth setting to that job when the outcome stays the same.

Make the skill a router when the requests it answers produce distinct end-to-end outcomes, or when its procedure would exceed the body limit. Route each job to one file under `references/`.

## SKILL.md

### Frontmatter

The frontmatter carries the fields the specification defines:

| Field | Rule |
|-------|------|
| `name` | Same as the folder: 1 to 64 characters, lowercase letters, digits, and single hyphens, beginning and ending with a letter or digit. Unique across the library and distinct from a host's built-in command. |
| `description` | Third person, plain text, at or below 1024 characters. Primary use case first, then the skill's scope and its boundary against adjacent work, in the words a user types. |
| `metadata` | Additional properties, such as `inspired-by`. See [Attribution](#attribution). |
| `compatibility` | Environment requirements: runtime, packages, network. Required when the skill has any. |
| `allowed-tools` | Optional. Every step runs when a host withholds these tools. |

Treat the set of descriptions as one budget, because every host loads all of them at startup. Keep the total inside the smallest host budget the repository targets, which is 8000 characters by default in Codex. When the total exceeds it, shorten descriptions or remove skills.

Keep `description` and `## Triggers` apart: the description states the skill's scope at the library level, the index chooses the branch inside the skill.

### Opening

Open with the H1, then one sentence stating what the skill covers, then either `## Triggers` for a router or `## Workflow` for a single job.

Put the index directly after the opening: after compaction the host reattaches the top of the file, so keep the list near the top.

A router routes. The procedure and the rules that shape its output live in the file it points to.

### Index

Give every file under `references/` exactly one entry, in this shape:

```text
- **<branch>** — <the situation that makes it relevant> → [references/<file>.md](references/<file>.md) · <what loading it buys>
```

```markdown
## Triggers

- **Commit** — the user asks to commit staged or unstaged changes → [references/commit.md](references/commit.md) · staging rules and the message bar
- **Create pull request** — a branch is ready for review → [references/create-pull-request.md](references/create-pull-request.md) · body structure and evidence
- **Merge pull request** — a pull request is ready to land → [references/merge-pull-request.md](references/merge-pull-request.md) · merge method, state checks, and cleanup
- **Wording** — any branch above is about to write text → [references/message-sourcing.md](references/message-sourcing.md) · where the words come from
```

Test each condition by asking whether the agent can choose from the entry itself, at the moment the request arrives, because the index is read once. A situation passes the test; a topic label sends the agent into the file to find out.

A single-job skill carries its procedure in `## Workflow` and places each entry in the step that loads the file, in the same shape. The entry is what the step says to load before relying on it.

Three completeness rules: every supporting file has one entry, every entry states a condition, and every procedure lives in the file a router points to.

### Length

Keep the body at or below 150 lines. Move detail into the file that needs it.

## references/

### Header

Open with the H1. A procedure reuses the words of the index branch that selects it, which makes the pair checkable by comparison; a material file names its topic, and its branch states when to load it. Then one sentence: the result a procedure produces, or what the material provides. A single-job skill has no branch label, so its H1 names the job and the sentence carries the payload.

### Procedure

```markdown
# Commit

Creates a conventional commit from the actual changes.

## Workflow

Progress:
- [ ] Step 1: Stage the files
- [ ] Step 2: Write the message from the diff
- [ ] Step 3: Verify

**Step 1. Stage.** Stage by name the files that belong to this change. Done when `git diff --cached` shows exactly the intended set; when an unrelated file slipped in, return to this step.

**Step 2. Write the message.** Write from the staged diff, taking the words from the hunks. Done when every line traces back to a hunk.
```

Declare the input, the action, and the completion condition in every step. Number each step as `Step N` in the checklist and `**Step N. Name.**` in the body. Give a check that can fail a line that says where to go back. End where the job ends.

### Material

Use free sections. Put a `## Contents` list at the top of any file above 100 lines, so a partial read still shows the full scope.

### Naming

Keep files directly under `references/`, in kebab case, named for the job or the topic they hold. Keep the tree flat under `references/`.

## scripts/

Bundle a script when at least one of these holds:

- the operation is deterministic and repeatable;
- a wrong result is expensive or irreversible;
- the agent regenerates the same code on every run.

Use prose for every other operation.

### Interface

1. Take input from arguments, paths included.
2. Report through the exit code: `0` for success, non-zero with an actionable message on stderr for failure.
3. Resolve the expected errors itself, with a message that says what to do next.
4. Justify every constant in a comment.
5. Be self-contained, or declare the dependency in `compatibility`.
6. Treat the given paths as its whole writable surface.
7. Make a mutation idempotent, or refuse a second run.

### Invocation

State the exact command, the input, and what each exit code means, then anchor the step's completion condition to the exit code.

```markdown
**Step 3. Validate.** Run `python3 scripts/validate_fields.py fields.json`. Done when it exits `0`; a non-zero exit lists the offending field and returns to Step 2.
```

Run a script by default. Read it when the algorithm itself is what the agent must adapt, and say so: "See `scripts/<name>.py` for the extraction algorithm".

## assets/

An asset is data a procedure reads or fills.

- Name it for the artifact it produces: `design.template.md`.
- State its rigidity on the first line, above the template body: `Use this template as written:` for an exact structure, or `Adapt this template to the case:` for a default to adapt.
- Have the step say whether it reads or fills the asset, and what to substitute.
- Keep the steps in the file that uses the asset.
- Keep a short template that every run uses inline in the procedure. Move it to `assets/` when it is long or needed on some runs, and announce it in the index.

## Host metadata

`agents/openai.yaml` holds what the host displays and enforces: `interface.display_name`, `interface.short_description`, `policy`, and `dependencies.tools`.

Claude Code reads its invocation flag, `disable-model-invocation`, from the `SKILL.md` frontmatter; that is the one field outside the specification. Allow implicit invocation by default, and reserve explicit invocation for a skill with a side effect — a deploy, a send, a merge, a publication. Declare it per host: `disable-model-invocation: true` for Claude Code, `policy.allow_implicit_invocation: false` for Codex.

Treat file-scoped activation, argument hints, and isolated context as convenience. A portable skill works when a host withholds them.

## Documentation

Documentation serves the human reader; the agent reads `SKILL.md` and `references/`. The page for a skill is generated from the skill and lives outside this pattern.

The repository index holds exactly the set of skills on disk.

Keep one value per concept: `display_name` is the page H1 and the label in the index; `short_description` is the tagline and the index one-liner; prose uses `display_name`, and the folder name stays the machine identity.

Keep each fact in a machine-readable field so the page mirrors it: requirements from `compatibility` and `dependencies`, integration from the skills the description and triggers name, output from the paths the steps declare. Installation lives in `skills.sh`.

## Attribution

Record an inspiration in `metadata.inspired-by`, one entry per origin, in the form `<skill name> — <url>`:

```yaml
metadata:
  inspired-by:
    - "<skill name> — <url>"
```

Attribution is a courtesy and fits in the frontmatter.

A copied passage creates a license obligation, recorded in `license` or in a `LICENSE` file when the notice must travel with the text.

## Conformance

Two states, one target. A skill is **conformant** when it matches this pattern and passes the deterministic checks. A skill is **ready** when it also passes its evaluations.

Run the deterministic checks before the judgment review, because they are cheap and can invalidate the review. Run the judgment review once over the whole skill, then apply one edit pass.
