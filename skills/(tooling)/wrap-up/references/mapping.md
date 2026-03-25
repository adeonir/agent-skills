# Project Detection and System Mapping

Resolve the current working directory to a project, BM configuration, and
Obsidian folder.

## When to Use

- Always loaded first, before any other reference
- All wrap-up steps depend on the output of this resolution

## Path Detection

Extract `{category}` and `{project}` from the current working directory:

```
~/Developer/{category}/{project}/...
```

The first segment after `~/Developer/` is the category. The second segment
is the project.

Examples:
- `~/Developer/work/jaya/src/` -> category: `work`, project: `jaya`
- `~/Developer/ventures/pensefy/apps/webapp/` -> category: `ventures`, project: `pensefy`
- `~/Developer/projects/my-skills/` -> category: `projects`, project: `my-skills`

If the path does not match `~/Developer/{category}/{project}`, or if the
resolved project looks like a grouping folder (e.g. `courses`, `challenges`)
rather than an actual project, ask the user for the project name and category.

## Mapping Table

| Category  | BM Project | BM Prefix  | Obsidian Session |
|-----------|-----------|------------|-------------------------|
| work      | work      | jobs/      | Work/                   |
| freelance | work      | freelance/ | Freelance/              |
| ventures  | ventures  | products/  | Ventures/               |
| personal  | main      | personal/  | Personal/               |
| projects  | main      | projects/  | Projects/               |
| learning  | --        | --         | Learning/               |
| sandbox   | --        | --         | --                      |

Daily note (`Daily/YYYY-MM-DD.md`) always runs, regardless of mapping values.

## Resolved Paths

Given category `ventures` and project `pensefy`:

- **BM session**: `products/pensefy/sessions/YYYY-MM-DD — Description.md`
- **BM debrief**: `products/pensefy/debriefs/YYYY-MM-DD — Description.md`
- **BM decision**: `products/pensefy/decisions/Title — Theme.md`
- **Obsidian session**: `Ventures/Pensefy/YYYY-MM-DD — Description.md`
- **Obsidian decision**: `Ventures/Pensefy/Decisions/Title — Theme.md`
- **Obsidian daily**: `Daily/YYYY-MM-DD.md` (always the same)

## Rules

- BM Project `--`: skip auto-memory and BM notes entirely (session and debrief)
- Obsidian Session `--`: skip Obsidian session note
- Daily note always runs, even when all other columns are `--`
- Project name in Obsidian uses Title Case (`my-skills` -> `My Skills`)
- New project in existing category: works automatically, no config needed
- New category: add one row to the mapping table
