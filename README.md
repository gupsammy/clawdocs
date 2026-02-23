<div align="center">

<h1>clawdocs</h1>
<p>Fetch OpenClaw docs as markdown — agent-first.<br>One call from topic → full page content. Pure HTTP, no LLM required.</p>

![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
[![GitHub Release](https://img.shields.io/github/v/release/gupsammy/clawdocs?style=flat-square)](https://github.com/gupsammy/clawdocs/releases/latest)

</div>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

`clawdocs` resolves any OpenClaw topic — a keyword, partial title, or exact slug — to its full markdown documentation page in a single command. Built for LLM agents that need live docs fed into context without extra tooling or dependencies.

## ✨ Features

- **Smart 4-step resolution** — exact index match → path/title match → semantic search via `openclaw docs` → fuzzy difflib fallback, each step progressively broader
- **Subcommand injection** — `clawdocs telegram` just works; no subcommand keyword required
- **Zero dependencies** — pure Python standard library, no `pip install` step
- **Structured JSON output** — slug, url, title, confidence, match method, related slugs, section headings, and full content in one object
- **Local cache** — fetched pages cached at `~/.cache/clawdocs/` for instant re-reads
- **Self-contained index** — `clawdocs update` fetches and builds the local index from `docs.openclaw.ai`; no external skill required
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
CLAWDOCS_VERSION=v0.2.0 curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/install.sh | sh
```

Browse all releases at [github.com/gupsammy/clawdocs/releases](https://github.com/gupsammy/clawdocs/releases).

### Usage

```bash
# First-time setup — build local docs index (no external tool needed)
clawdocs update

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
| `CLAWDOCS_INDEX` | (auto-resolve) | Override index JSON path directly |
| `CLAWDOCS_DATA_DIR` | `~/.local/share/clawdocs` | Where `clawdocs update` writes `index.json` |
| `CLAWDOCS_CACHE_DIR` | `~/.cache/clawdocs` | Directory for cached markdown pages |
| `CLAWDOCS_TIMEOUT` | `20` | HTTP fetch timeout in seconds |
| `NO_COLOR` | unset | Set to any value to disable ANSI color output |

Index resolution order (first found wins): `CLAWDOCS_INDEX` env → `$CLAWDOCS_DATA_DIR/index.json` → docclaw skill path → openclaw node path.

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
| `--dry-run` | Show what `update` would write without writing it |

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
- [ ] MCP server mode — expose `clawdocs` as an MCP tool for Claude Desktop and other MCP clients

## ❓ FAQ

### Does clawdocs require OpenClaw to be installed?

Only for the semantic search step (step 3 of the resolution chain). If `openclaw` is not on your PATH, steps 1, 2, and 4 — index-based and fuzzy matching — still work. Step 3 is silently skipped rather than crashing.

### How do I get the local docs index?

Run `clawdocs update`. It fetches `llms.txt` and `sitemap.xml` from `docs.openclaw.ai` and writes a merged index to `~/.local/share/clawdocs/index.json`. The install script does this automatically on first install. If your index is more than 14 days old, `clawdocs` will remind you to refresh it. You can also point to any compatible index file via `CLAWDOCS_INDEX`.

### Can I use clawdocs inside an LLM agent tool call?

Yes — that's the primary design goal. Use `--no-header -q` for raw markdown content and `--json` for a structured payload. The exit-code contract (0 = success, 1 = not found, 2 = network error) is stable and safe to branch on in agent logic.

## 📄 License

MIT © [gupsammy](https://github.com/gupsammy)
