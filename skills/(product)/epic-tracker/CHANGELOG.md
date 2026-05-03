---
name: epic-tracker
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-05-03

### Added

- Issue artifact type for internal work items (infra, refactor, tooling, research) with optional epic parent, checklist, and rabbit holes
- Adapter mapping for the issue type across all trackers (Linear: label `task`, GitHub: label `task`, Jira: native Task issue type)
- `create_issue` operation in the sync operations table
- CLI detection in bootstrap alongside MCP; integration method persisted as `via: mcp | cli` in config

### Changed

- Tracker integration is tracker-first when configured: artifacts pushed directly to the tracker with no local markdown file created
- Save and Sync steps in core refs merged into a single conditional step routing to tracker or markdown based on config
- Markdown output is the fallback path only, used when no tracker is configured or user declines to push
- Push Direction in sync accepts draft content directly without a pre-saved markdown file; surfaces tracker URL to the user on success when no local file exists
- Release discovery fetches stories from the tracker when configured instead of scanning markdown files

## 2026-04-29

### Added

- Optional tracker integration covering Linear, GitHub Issues, GitHub Projects (sub-issues default + classic fallback), and Jira; markdown stays the source of truth when no tracker is configured
- `sync.md` reference orchestrating push and pull between markdown artifacts and external trackers; runs bootstrap on first use, dispatches to the matching adapter, surfaces conflicts, updates frontmatter on success
- Three adapters (`adapters/linear.md`, `adapters/github.md`, `adapters/jira.md`) translating generic operations into tracker-specific primitives
- Tracker config at `.artifacts/epics/.config.yml` capturing `kind`, workspace, repo, project_number, projects_mode, base_url, project_key
- Optional `tracker` block in artifact frontmatter (id, url, last_synced) populated after sync push
- Direct triggers for "sync to tracker", "push to linear/github/jira", "pull from tracker", "configure tracker"
- Per-session push cache: ask once whether to push, remember the answer for the rest of the session
- Tracker primitive mapping table in SKILL.md covering Epic, Story, Bug, and Release across all four trackers

### Changed

- Workflow expanded to `discover -> create -> sync* -> track -> handoff`; sync is gated by config and asked per session
- `status.md` reads from the tracker when configured, falls back to markdown cache when MCP unavailable
- `handoff.md` surfaces tracker URLs from frontmatter and routes status updates through `status.md` (which dispatches to sync when needed)
- Core refs (`epic.md`, `story.md`, `bug.md`, `release.md`) gained a Sync step that delegates to `sync.md` when config is present
- Templates carry an optional `tracker` frontmatter block as commented schema; populated by sync after first push
- Release maps adaptively per tracker: Linear Cycle, GitHub Release tag, Jira Fix Version (no forced single concept)
- SKILL.md cross-references diagram covers core refs -> sync -> adapters and status -> sync read paths
- Guidelines updated: tracker is source of truth for status when configured; markdown is fallback; conflicts surface explicitly with tracker winning by default and user override allowed

## 2026-04-23

### Changed

- Triggers "overview", "status", "start story", and "create bug" removed (collided with spec-driven and project-index)
- "Not for" routing added to spec-driven ("implement story S###") and project-index (project-wide overview)

## 2026-04-22

### Changed

- Story files now use a zero-padded 3-digit numeric prefix (`001-story-name.md`) for visual ordering in file explorers
- Epic checklist entries updated to linked format when story is created

## 2026-04-20

### Changed

- Pair every Guideline DON'T with a concrete DO in SKILL.md and epic.md

## 2026-03-25

### Added

- Initial skill creation with SKILL.md, references, and templates
- Epic, story, bug, and release artifact types
- Discover phase checks for existing PRD/brief before creating epics
- Status tracking in frontmatter for all artifacts
- Handoff reference for spec-driven bridge
- Overview reads artifacts directly (no index file)
