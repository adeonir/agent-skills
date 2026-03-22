# Test-Driven Development

Write the test first, then the implementation.

## When to Use

Loaded during execute when the project has test infrastructure:

- `.agents/codebase/testing.md` exists, OR
- Test command found in package.json, Makefile, or equivalent, OR
- Test files found in the project

Not a gate -- a technique. If the project has no tests, execute continues
normally without loading this reference.

## Workflow

### Red

Write a failing test that describes the expected behavior. The test should:

- Describe WHAT should happen, not HOW it is implemented
- Fail for the right reason (missing functionality, not syntax error)
- Be the simplest test that captures the requirement

```bash
# Run tests -- expect failure
{test command}
```

### Green

Write the minimal code to make the test pass. Nothing more.

- Do not add extra functionality
- Do not handle edge cases not covered by the test
- Do not refactor yet

```bash
# Run tests -- expect pass
{test command}
```

### Refactor

Clean up the code while keeping all tests green.

- Extract shared logic
- Improve naming
- Remove duplication
- Run tests after each change

```bash
# Run tests -- must stay green
{test command}
```

### Repeat

Write the next failing test for the next piece of behavior. Continue
the red-green-refactor cycle until the task is complete.

## Behavior vs Implementation

Follow the project's established approach:

| Approach | Test describes | Example |
|----------|---------------|---------|
| Behavior | What the user/system sees | "when user submits form, show success message" |
| Implementation | How the code works internally | "function returns object with status field" |

Read `.agents/codebase/testing.md` or existing test files to determine which
approach the project uses. Match it exactly.

**Default to behavior tests** when no clear convention exists -- they are more
resilient to refactoring.

## Matching Project Patterns

Before writing any test, check how existing tests are structured:

- describe/it nesting and naming conventions
- Mocking approach (what is mocked, how)
- Fixture and helper patterns
- Setup/teardown patterns
- File naming and location conventions

Match these exactly. A test that works differently from every other test in
the project is harder to maintain.

## Guidelines

**DO:**
- Write the test before the implementation
- Keep each red-green-refactor cycle small (one behavior at a time)
- Match the project's test patterns and conventions
- Run tests after every change (red, green, refactor)

**DON'T:**
- Write all tests upfront before any implementation
- Test implementation details when the project tests behavior
- Skip the refactor step
- Add production code without a failing test first

## Error Handling

- No test infrastructure in project: skip TDD, execute normally
- Test patterns unclear: read 2-3 existing test files before writing new ones
- Test framework not installed: inform user, suggest setup
