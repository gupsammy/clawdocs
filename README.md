<div align="center">

<h1>clawdocs</h1>
<p>Fetch OpenClaw docs as markdown — agent-first.<br>One call from topic → full page content. Pure HTTP, no LLM required.</p>

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

</div>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

`clawdocs` resolves any OpenClaw topic — a keyword, partial title, or exact slug — to its full markdown documentation page in a single command. Built for LLM agents that need live docs fed into context without extra tooling or dependencies.

## ✨ Features

- **Smart 4-step resolution** — exact index match → path/title match → semantic search via `openclaw docs` → fuzzy difflib fallback, each step progressively broader
- **Subcommand injection** — `clawdocs telegram` just works; no subcommand keyword required
- **Zero dependencies** — pure Python standard library, no `pip install` step
- **Structured JSON output** — slug, url, title, confidence, match method, related slugs, section headings, and full content in one object
- **Local cache** — fetched pages cached at `~/.cache/clawdocs/` for instant re-reads
- **Offline-friendly** — index-based lookups (steps 1, 2, 4) work without network access; degrades gracefully when index is absent
- **Agent-optimized output** — `--no-header -q` strips all wrapper text, leaving clean markdown ready to embed in context windows

## 🚀 Install

**Prerequisites:** Python 3.8+ (no packages needed).

**One-line install (macOS / Linux):**

```bash
curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/install.sh | sh
```

Installs to `~/.local/bin/clawdocs`. Override the directory with `INSTALL_DIR`:

```bash
INSTALL_DIR=/usr/local/bin curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/install.sh | sh
```

**Manual one-liner (no install script):**

```bash
mkdir -p ~/.local/bin
curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/clawdocs -o ~/.local/bin/clawdocs
chmod +x ~/.local/bin/clawdocs
```

**Pin to a specific version:**

```bash
CLAWDOCS_VERSION=v0.1.0 curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/install.sh | sh
```

### Usage

```bash
# Smart fetch — keyword, partial title, or exact slug
clawdocs telegram

# Direct fetch by exact slug (no resolution step)
clawdocs get channels/telegram

# Search and list matches
clawdocs search cron --slugs-only

# List all slugs in a section
clawdocs list --prefix channels/

# Clean content only — pipe directly into an LLM context
clawdocs telegram --no-header -q

# Structured JSON for programmatic use
clawdocs get channels/telegram --json

# Use the 2nd search result instead of the 1st
clawdocs telegram --top 2

# Grep into a page
clawdocs get channels/telegram --no-header | grep "dmPolicy"
```

**Default output:**

```
--- clawdocs: channels/telegram ---
url: https://docs.openclaw.ai/channels/telegram
confidence: exact (index exact path)
related: channels/whatsapp, channels/slack, channels/email
covers: Bot setup, Webhook configuration, Message types

# Telegram Channel
...
--- end: channels/telegram ---
```

## ⚙️ Configuration

### Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLAWDOCS_INDEX` | `~/.openclaw/workspace/skills/docclaw/references/openclaw-docs-index.json` | Path to the local docs index JSON |
| `CLAWDOCS_CACHE_DIR` | `~/.cache/clawdocs` | Directory for cached markdown pages |
| `CLAWDOCS_TIMEOUT` | `20` | HTTP fetch timeout in seconds |
| `NO_COLOR` | unset | Set to any value to disable ANSI color output |

### Flags (all subcommands)

| Flag | Description |
|------|-------------|
| `--json` | Emit structured JSON to stdout |
| `--plain` | Plain text output, no ANSI codes |
| `--no-header` | Content only — omit the `--- clawdocs: slug ---` wrapper |
| `--no-color` | Disable ANSI colors (runtime override) |
| `-q / --quiet` | Suppress all stderr diagnostics |
| `--timeout S` | HTTP timeout in seconds |
| `--no-cache` | Bypass local cache and force a fresh fetch |
| `--strict` | Exit 1 on low-confidence matches or slugs absent from index |
| `--index PATH` | Override index file path (or use `CLAWDOCS_INDEX`) |
| `--out FILE` | Write output to a file instead of stdout |
| `--top N` | Use the Nth search result instead of the 1st (fetch/search only) |

### Exit codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Not found |
| `2` | Network error |
| `3` | Ambiguous (reserved) |
| `4` | Usage error |

## 🗺 Roadmap

- [ ] `--watch` mode — poll for doc updates and re-fetch on change
- [ ] Multi-slug batch fetch in a single call
- [ ] Shell completions for bash and zsh
- [ ] `clawdocs update-index` command to refresh the local index without reinstalling docclaw
- [ ] MCP server mode — expose `clawdocs` as an MCP tool for Claude Desktop and other MCP clients

## ❓ FAQ

### Does clawdocs require OpenClaw to be installed?

Only for the semantic search step (step 3 of the resolution chain). If `openclaw` is not on your PATH, steps 1, 2, and 4 — index-based and fuzzy matching — still work. Step 3 is silently skipped rather than crashing.

### How do I get the local docs index?

The index ships with the [docclaw skill](https://openclaw.ai). Installing docclaw places the index at `~/.openclaw/workspace/skills/docclaw/references/openclaw-docs-index.json`, which `clawdocs` looks for automatically. You can point to any compatible index via the `CLAWDOCS_INDEX` environment variable.

### Can I use clawdocs inside an LLM agent tool call?

Yes — that's the primary design goal. Use `--no-header -q` for raw markdown content and `--json` for a structured payload. The exit-code contract (0 = success, 1 = not found, 2 = network error) is stable and safe to branch on in agent logic.

## 📄 License

MIT © [gupsammy](https://github.com/gupsammy)
