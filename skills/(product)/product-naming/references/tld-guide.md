# TLD Guide

Reference for domain extension selection during name evaluation.

## Universal (always check)

| TLD | Notes | Price |
|-----|-------|-------|
| .com | Globally trusted, first choice | ~$10-15/year |
| .com.br | Required for Brazilian products; needs CNPJ or CPF; authoritative source is registro.br | ~R$40/year |

## Brazilian

| TLD | Use case | Price |
|-----|----------|-------|
| .app.br | Mobile apps with Brazilian focus; requires CPF/CNPJ | ~R$40/year |
| .net.br | Generic alternative | ~R$40/year |
| .org.br | Nonprofits and communities | ~R$40/year |

## Tech / Startup

| TLD | Use case | Price |
|-----|----------|-------|
| .io | SaaS and dev tools | ~$30-50/year |
| .app | Mobile and web apps | ~$15-20/year |
| .dev | Developer tools | ~$12-15/year |
| .ai | AI products | ~$30-80/year |
| .co | Clean .com alternative | ~$25-30/year |

## Creative / Other

| TLD | Use case | Price |
|-----|----------|-------|
| .xyz | Modern and cheap | ~$10-15/year |
| .so | Minimal, growing in use | ~$25-35/year |

## Selection Logic

1. Always check .com + .com.br
2. Add TLDs based on product category:
   - Dev tool: +.io, +.dev
   - AI product: +.ai, +.io
   - Mobile app: +.app, +.app.br
   - SaaS/B2B: +.io, +.co
   - Consumer app: +.app, +.co
3. Add .xyz or .so only if the user expresses interest in creative/alternative extensions

## How to Check

See [evaluation.md](evaluation.md) -- Domain Availability Check section for environment-adaptive methods (shell commands, web search fallback).
