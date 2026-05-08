# Docs Writer

Generates structured product and technical documents through guided discovery.

## What It Does

Routes document creation requests to type-specific workflows, each with
appropriate discovery depth:

```mermaid
flowchart TD
    T[Trigger] --> R{Document type}
    R -->|PRD| PRD[PRD workflow]
    R -->|Design Doc| DD[Design Doc workflow]
    R -->|TDD| TDD[TDD workflow]
    PRD --> B[Brief generated alongside]
    PRD --> P[prd.md]
    B --> BR[brief.md]
    DD --> D[design.md]
    TDD --> T2[tdd.md]
```

| Type | Workflow | Output |
|------|----------|--------|
| **PRD** | discovery → validation → synthesis → drafting | `prd.md` |
| **Brief** | generated alongside PRD (no standalone trigger) | `brief.md` |
| **Design Doc** | discovery → analysis → drafting (informal trade-off discussion) | `design.md` |
| **TDD** | discovery → analysis → drafting (auto-sized core/medium/large) | `tdd.md` |

## Usage

```
create PRD for my project
create design doc for API gateway
create TDD for payment service
write requirements for the new feature
```

The skill detects the document type from the trigger and loads the
appropriate workflow.

## Output

All documents are saved to:

```
.artifacts/docs/{type}.md
```

## FAQ

**Q: When should I use a Design Doc vs a TDD?**
A: Design Docs are informal documents focused on trade-offs and
decision-making for ambiguous problems. TDDs are prescriptive plans for
specific components — they tell the team exactly what to build, with
what stack, and how to deploy. A project can have both: a Design Doc
for system-level decisions and TDDs for component-level technical
planning.

**Q: Why is the Brief generated alongside the PRD?**
A: The Brief is a 1-page narrative summary of the PRD. It distills
discovery into a story readable in under a minute, while the PRD
remains the specification. Having a separate trigger and discovery
phase would duplicate work — the data is already collected during the
PRD workflow.

**Q: How does TDD auto-sizing work?**
A: TDDs scale by project complexity: Core (7 sections, single service),
Medium (12 sections, multiple integrations or data modeling), Large
(15 sections, cross-team or production-critical). Critical sections
(Security, Deployment, Monitoring) are promoted regardless of size when
the project is payment/auth/PII, a production service, a migration, or
infrastructure.

**Q: What if the user has no PRD when starting a Design Doc or TDD?**
A: Both workflows can start from scratch. When a PRD exists at
`.artifacts/docs/prd.md`, the workflows extract product context as
starting input. Without one, the discovery phase covers both product
context and technical design.
