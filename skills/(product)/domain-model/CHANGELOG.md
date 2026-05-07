---
name: domain-model
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-05-07

### Changed

- BR, FR, EC id format aligned to dash-separated with no padding (`BR-1`, `FR-1`, `EC-1`) following the PRD source convention; placeholder shape standardized to `BR-N` / `FR-N` / `EC-N`

## 2026-05-06

### Added

- Initial release with discovery, entities, relationships, rules, and
  output phases.
- Update mode trigger enabling spec-driven to route domain gaps back for
  refinement via knowledge.md queue.
- `domain.md` template with entity invariants, lifecycle, BR coverage
  table, and Processed Gaps historical record.
- Bounded context grouping and context map as handoff contract for
  system-design.
- Future integration point documented in output.md for knowledge.md
  Domain Gaps section.
