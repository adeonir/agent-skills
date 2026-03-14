---
name: docs-writer
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-14

### Changed

- Replace Pitch with Epic (deliverable feature slice linked to PRD milestones)
- Replace Scope with Issue (enriched work item with Context field)
- Add Rabbit Holes to Brief Risks section
- Remove `type` field from all template frontmatters
- Update cross-references and triggers

## 2026-03-11

### Added

- TDD (Technical Design Document) type with reference and template
- 15 sections organized by sizing (core/medium/large) with critical sections by project type
- Auto-sizing logic based on discovery signals
- Document count updated from 8 to 9 types

## 2026-03-10

### Changed

- Break frontmatter description into multi-line YAML to avoid obfuscation alerts in security audits

## 2026-03-09

### Changed

- Adopt Shape Up naming: User Story -> Pitch, Task -> Scope, Issue -> Bug
- Pitch uses narrative format (problem + solution), replaces "As a... I want..." agile format
- Scope defines technical work slice with in/out, no acceptance criteria (validation at pitch level)
- Bug simplified to essential fields: description (expected/actual), steps to reproduce, environment, workaround
- Issue subtypes (feature, discussion) removed -- Bug is a standalone type
- Replace TDD with Design Doc following a broader technical design approach
- Update cross-references: Pitch -> Scope relationship, Design Doc -> ADR
- Update triggers, discovery patterns, and output filenames

## 2026-03-02

### Changed

- TDD template restructured from 16 to 9 sections following AWS design doc pattern
- Remove Context & Background, Scope of Impact, Technical Design, Failure Modes & Recovery, Performance Considerations, Observability & Monitoring, Migration / Rollout Plan
- Tech Stack becomes standalone section with category tables (Frontend, Backend, Shared) without justification column
- Alternatives Considered changes format from Pros/Cons to Decision/Choice/Over/Why
- Security section expanded to Security & Compliance (includes regulatory requirements)
- Architecture section focuses on three Mermaid diagrams: High-Level Design, System Context, Data Flow
- Add `updated` field to frontmatter
- TDD reference updated: discovery topics reorganized from 3 generic to 3 focused (Requirements & Stack, Architecture & Integrations, Security/Compliance/Testing)
- TDD reference schema table updated to match new 9-section template

## 2026-02-27

### Changed

- Deduplicate quality standards table (keep in SKILL.md, remove from prd.md)
- Simplify task template to match reference fields (remove Technical Details, Files to Modify, Approach, Notes)
- Enhance description with adjacent trigger contexts for better skill matching
- TDD template restructured from 14 to 16 sections: add frontmatter (status/date), Scope of Impact, Observability & Monitoring; rename Error Handling to Failure Modes & Recovery; add Do Nothing to Alternatives; add rollback triggers to Migration/Rollout
- ADR template restructured from 7 to 8 sections: add MADR 4.0 frontmatter (status/date/deciders), add Confirmation section for decision validation
- RFC template restructured from 11 to 12 sections: add frontmatter (status/date/authors), add Prior Art section, split Drawbacks into Accepted Trade-offs and Open Risks
- Issue template: remove severity from frontmatter (keep priority only), add Reproduction Link, Last Working Version, and Workaround fields for bugs, rename Proposed Solution to Proposed Fix
- User Story template restructured from 8 to 7 sections: remove Definition of Done (team-level concern), simplify AC from Given/When/Then to checklist format, merge Design/UI Reference and Related into unified References section
- Update TDD, ADR, RFC, Issue, User Story reference docs to match new template schemas
- Standardize reference section naming: Process to Workflow, Rules to Guidelines
- Standardize reference closing sections order: Guidelines, Error Handling, Output
- Add When to Use section to all reference files
- Convert SKILL.md Guidelines to DO/DON'T format
- Add Context Loading Strategy to SKILL.md
- Reorder Cross-References before Guidelines in SKILL.md
- Merge Integration with Other Skills into Cross-References notes

## 2026-02-26

### Changed

- Restructure PRD template from 12 to 11 sections
- Add User Journeys section (product-level flows with pre/post-conditions)
- Add Business Rules section (functional constraints with IDs)
- Add Edge Cases section (exception scenarios with IDs)
- Remove Value Proposition, Competitive Landscape (covered by Brief)
- Remove User Stories (derived later in spec-driven from journeys)
- Remove Technical Specifications (covered by TDD)
- Add discovery topic 5: Journeys & Constraints
- Update PRD-to-spec integration via milestones

## 2026-02-25

### Changed

- Replace fixed discovery stages with adaptive deepening across all document types
- Apply adaptive discovery to remaining types (adr, issue, rfc, tdd, user-story)

## 2026-02-20

### Changed

- Output directory migrated from `.specs/docs/` to `.artifacts/docs/`
- All document types now save to unified `.artifacts/docs/` location

## 2026-02-19

### Changed

- Output filenames simplified from `{type}-{project-name}` to `{type}` only

## 2026-02-17

### Changed

- Remove frontmatter and title placeholders from document templates

## 2026-02-13

### Added

- Brief document type with reference and template (lightweight project brief)
- Document count updated from 7 to 8 types

### Changed

- Refine discovery questions and PRD reference structure
- Update PRD template with improved frontmatter metadata

## 2026-02-11

### Added

- Docs Writer skill with generalized document generation for 7 types
- Router/dispatcher pattern in SKILL.md (detects document type from trigger, loads reference on-demand)
- `discovery.md` shared reference with common interview patterns across all types
- PRD type with 3-phase workflow (discovery, analysis, drafting)
- User Story type with agile format (discovery, drafting, WHEN/THEN/SHALL acceptance criteria)
- Task type for sprint execution items (direct drafting, structured fields)
- Issue type for bug reports, feature requests, discussions (classification, drafting, 3 subtypes)
- RFC type for Request for Comments (discovery, analysis, drafting, status lifecycle)
- ADR type for Architecture Decision Records (discovery, drafting, sequential numbering)
- TDD type for Technical Design Documents (discovery, analysis, drafting)
- Templates for all document types in `templates/`
- Cross-references with spec-driven and design-builder skills
