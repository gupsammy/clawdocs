# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`clawdocs` is a single-file Python CLI (`./clawdocs`) that fetches OpenClaw documentation as markdown for LLM agent consumption. There is no build step, no package manager, and no runtime dependencies beyond the Python standard library.

## Running and testing

Run the CLI directly:
```
./clawdocs telegram
./clawdocs get channels/telegram --json
./clawdocs search cron --slugs-only
./clawdocs list --prefix channels/
```

Run all tests (integration tests that invoke the binary as subprocess):
```
python3 tests/test_clawdocs.py
```

Run a single test class or method:
```
python3 -m unittest tests.test_clawdocs.TestGet.test_get_exact_slug -v
python3 -m unittest tests.test_clawdocs.TestGet -v
```

## Architecture

The entire implementation lives in the `clawdocs` executable. There are no modules to import.

**Subcommand injection**: `main()` pre-processes `sys.argv` to inject `"fetch"` when the first positional argument isn't a known subcommand (`fetch`, `get`, `search`, `list`). This makes `clawdocs telegram` equivalent to `clawdocs fetch telegram`.

**4-step resolution chain** (in `_resolve`):
1. Exact index path match — no network
2. Path suffix / title match against index — no network
3. Semantic search via `openclaw docs <query>` subprocess — one network call
4. Fuzzy `difflib` fallback against index paths and titles — no network

**Index loading**: `_find_index` checks `CLAWDOCS_INDEX` env var first, then two hardcoded candidate paths under `~/.openclaw/`. An empty index degrades gracefully (skips steps 1, 2, 4; step 3 still works).

**Cache**: `_cache_path` stores fetched pages at `~/.cache/clawdocs/<slug>.md` (override with `CLAWDOCS_CACHE_DIR`). A path-traversal guard ensures resolved paths stay inside the cache base.

**Output modes**: plain text with colored `--- clawdocs: slug ---` header (default), `--json`, `--no-header` (content only), `--plain` (no ANSI).

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Not found |
| 2 | Network error |
| 3 | Ambiguous (reserved) |
| 4 | Usage error |

## Environment variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `CLAWDOCS_INDEX` | (see candidate paths in source) | Path to `openclaw-docs-index.json` |
| `CLAWDOCS_CACHE_DIR` | `~/.cache/clawdocs` | Cache directory |
| `CLAWDOCS_TIMEOUT` | `20` | HTTP timeout in seconds |
| `NO_COLOR` | unset | Disable ANSI color output |
