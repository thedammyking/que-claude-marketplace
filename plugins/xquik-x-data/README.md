# xquik-x-data

A Claude Code plugin that adds the `xquik-x-data` skill for X/Twitter public data workflows with Xquik.

## Installation

1. Add the marketplace:

   ```
   /plugin marketplace add thedammyking/que-claude-marketplace
   ```

2. Install the plugin:

   ```
   /plugin install xquik-x-data@que-claude-marketplace
   ```

## What It Adds

The bundled skill helps Claude:

- Find Xquik source-truth docs before writing API or MCP examples.
- Keep API keys in environment variables instead of prompts or source files.
- Use Xquik REST API, MCP, webhooks, and SDK routes only when the docs support them.
- Avoid claims about private data access, quotas, pricing, or unsupported workflows.

## Source Truth

- Docs: https://docs.xquik.com
- REST API: https://docs.xquik.com/api-reference/overview
- MCP: https://docs.xquik.com/mcp/overview
- Source: https://github.com/Xquik-dev/x-twitter-scraper
