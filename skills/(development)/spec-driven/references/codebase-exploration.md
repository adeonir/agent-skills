# Codebase Exploration Patterns

Patterns for analyzing existing code for a specific feature.

## When to Use

- During design (design.md)
- Need to understand patterns for a specific feature
- Finding similar existing features
- Understanding integration points

## Scope

**Feature-specific analysis** - Focused on what you need for this feature:
- Similar existing features
- Reusable components
- Integration patterns
- Testing approaches

For **general codebase mapping**, use the project-index skill (creates `.agents/codebase/` docs).

## Tools

Use available semantic analysis, code search, and file reading tools to explore the codebase.
The agent discovers and uses whatever tools are available in the environment.

## Workflow

### Phase 1: Discovery

1. **Find Documentation**

   Look for README.md, CLAUDE.md, CONTRIBUTING.md, package.json, tsconfig.json in the project.

2. **Find Source Files**

   Find files related to the feature being built, plus test files.

3. **Read Documentation**

   Read 2-3 documentation files to understand project structure, architecture patterns, and coding conventions.

### Phase 2: Pattern Extraction

4. **Identify Reference Files**

   Find 2-3 existing features similar to what needs to be built. Check imports, exports, and file organization.

5. **Read Reference Files**

   Read 3-5 essential files and extract:
   - Naming conventions (functions, classes, variables)
   - Import/export patterns
   - Error handling approach
   - Type definitions style
   - Testing patterns

6. **Extract Code Patterns**

   Document specific patterns with file:line references:
   ```
   Pattern: Function naming
   - Project uses: camelCase for functions
   - Example: src/utils/helpers.ts:15

   Pattern: Error handling
   - Project uses: Custom error classes
   - Example: src/errors/index.ts:23
   ```

7. **Map Dependencies**

   For key files, identify imports (dependencies) and what imports from them (dependents).

### Phase 3: Architecture Analysis

8. **Trace Entry Points**

   Where would the feature integrate: API routes, UI components, CLI commands, event handlers.

9. **Follow Data Flow**

   Trace: Input validation -> Business logic -> Data transformation -> Output/response.

10. **Identify Layers**

    Map architecture layers: Presentation, Business logic, Data access, External services.

### Phase 4: Member Enumeration

Before closing Architecture Analysis, list every entity, projection, contract, DTO, view model, or type the feature will read from or write to. For each one, enumerate every exposed member with a `file:line` anchor. Sampling is not allowed -- a type either has all its members listed or it is not yet explored.

11. **Identify Touched Types**

    From the feature requirements and the data flow traced in Phase 3, list every entity, projection, DTO, contract, view model, response shape, and persisted type the feature will consume or emit.

12. **Enumerate Members Exhaustively**

    For each touched type, open its definition and list every exposed member (field, property, method, or contract element) with `file:line`. If a member is itself a composite type the feature also touches, recurse.

13. **Anchor Absence Claims**

    For every claim of the form "already returns X", "no additional join needed", "signature unchanged", "contract already covers this", attach the `file:line` of the member that backs the claim. Unanchored absence claims are rejected.

**Exit criterion:** No claim about an existing type's contents stands without (a) a full member list with `file:line` and (b) anchors on every absence assertion.

### Phase 5: Consolidation

14. **Summarize Conventions**

    Create comprehensive convention table with file:line references.

15. **List Essential Files**

    Categorize as: Reference (patterns to follow), Modify (existing files to change), Dependencies (files to import).

## Output Template

**USE TEMPLATE:** `templates/exploration.md`

After exploration, document findings following the template structure.

## Integration with Design

Use findings in design.md:
- Reference files to follow
- Patterns to use
- Code to reuse

After exploration, if `.agents/codebase/` exists, new findings are persisted back to it (see design.md Step 5: Persist Codebase Discoveries). This ensures patterns discovered during one feature's design are available to future features without rediscovery.

## Guidelines

**DO:**
- Read file content to extract actual patterns -- not just list files
- Include file:line references for every pattern
- Cover naming, imports, error handling, types, testing
- Follow the exploration template structure
- Focus on patterns most relevant to the feature being built
- Enumerate every exposed member of every type the feature touches -- cite file:line for each
- Anchor every "no change" or "already exposes" claim to a file:line in the member list

**DON'T:**
- List files without reading their content
- Omit file:line references for discovered patterns
- Skip areas like error handling or testing conventions
- Sample members of a touched type -- enumerate them exhaustively
- Claim a type "already returns" or "already covers" something without citing file:line
