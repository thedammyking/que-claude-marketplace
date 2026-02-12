# claude-skills-loader

A Claude Code plugin that auto-discovers `SKILL.md` files in any project and registers them as native Claude Code skills via symlinks.

## What It Does

When a Claude Code session starts (or is resumed, cleared, or compacted), this plugin recursively scans the current project directory for `SKILL.md` files. Each discovered skill directory is symlinked into the plugin's own `skills/` directory, making it available through Claude Code's native Skill tool.

This means you can drop a `SKILL.md` file into any directory of your project, and it will automatically become a registered skill without any manual configuration.

## Installation

1. Add the marketplace:

   ```
   /plugin marketplace add thedammyking/que-claude-marketplace
   ```

2. Install the plugin:

   ```
   /plugin install claude-skills-loader@que-claude-marketplace
   ```

## How It Works

1. A **SessionStart hook** fires on `startup`, `resume`, `clear`, or `compact` events.
2. The hook script (`session-start.sh`) runs asynchronously to avoid blocking session initialization.
3. It scans the project root recursively (up to **5 levels deep**) for files named `SKILL.md`.
4. Old symlinks in the plugin's `skills/` directory are cleaned up (only symlinks are removed, never real files or directories).
5. Each discovered `SKILL.md`'s parent directory is symlinked into `plugins/claude-skills-loader/skills/`.
6. Claude Code then picks up the symlinked skills as if they were native plugin skills.

## Scan Exclusions

The following directories are excluded from the scan to keep it fast and avoid false positives:

- `node_modules`
- `.git`
- `dist`
- `build`
- `.next`
- `.turbo`
- `coverage`
- `.cache`

## Collision Handling

If two or more `SKILL.md` files live in directories with the **same name** (e.g., `packages/foo/utils/SKILL.md` and `apps/bar/utils/SKILL.md`), the plugin detects the collision and uses the full relative path with `/` replaced by `--`:

```
skills/
  packages--foo--utils -> /absolute/path/to/packages/foo/utils
  apps--bar--utils     -> /absolute/path/to/apps/bar/utils
```

This ensures every discovered skill gets a unique link name.

## SKILL.md Format

Each `SKILL.md` file must include YAML frontmatter with at least `name` and `description` fields:

```markdown
---
name: my-skill
description: A brief description of what this skill does
---

# My Skill

Instructions for Claude when this skill is invoked...
```

## Max Depth

The scan searches up to **5 directory levels deep** from the project root. Skills nested deeper than that will not be discovered. This limit keeps the scan performant on large monorepos.
