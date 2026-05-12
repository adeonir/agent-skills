# Integrations

Generate `.agents/codebase/integrations.md` — external services, environment variables, and configuration touchpoints.

## When to Use

- Sub-agent dispatched during codebase summary fan-out
- User explicitly asks to refresh `integrations.md` after adding/removing external dependencies

## Scope

All external touchpoints: API calls, database connections, third-party SDKs, environment variables, file system operations. Both functional integrations (used in code) and configured integrations (declared in env files).

## Reading Priorities

1. `.env.example`, `.env.sample`, or equivalent — declared environment variables
2. Config files (`config/`, `.config.{js,ts}`, etc.)
3. API/HTTP client wrappers
4. Database setup files (ORM config, connection pool, migrations)
5. Third-party SDK initializations (auth, payments, analytics, telemetry)

Prefer AST-aware tooling (e.g., `smart-explore`) over full `Read` when scanning client wrappers or SDK setup files larger than 300 lines.

## Source Boundary

List only services with current evidence in code or config. A planned integration mentioned in `.artifacts/` but not yet wired does not appear here.

If an environment variable is declared in `.env.example` but never read, document it but flag the unused state.

## Output

Save to `.agents/codebase/integrations.md`. On re-run, follow [merge-policy.md](merge-policy.md).

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: active
sources:
  - {{file-path-actually-read}}
  - {{file-path-actually-read}}
---

# Integrations

| Service | Purpose | Auth Method | Config |
|---------|---------|-------------|--------|
| {{service}} | {{purpose}} | {{API key/OAuth/token/none}} | {{env var or config file}} |

## Environment Variables

| Variable | Service | Required |
|----------|---------|----------|
| {{VAR_NAME}} | {{service}} | {{yes/no}} |
````

## Guidelines

- Document auth method per service (API key, OAuth, JWT, none)
- Mark variables as required only when the code throws or fails without them
- One row per distinct service — combine related vars under the same row
- Populate `sources:` with every file actually read; empty list is not acceptable
