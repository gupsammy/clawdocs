# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-02-23

### Added
- Add `clawdocs update` subcommand — fetches `llms.txt` and `sitemap.xml` from
  `docs.openclaw.ai` and writes a merged index to `~/.local/share/clawdocs/index.json`
- Install script now runs `clawdocs update` automatically on first install
- Warn on stderr when the local index is older than 14 days (run `clawdocs update`)
- Index resolution now checks the clawdocs-native data dir first, eliminating the
  hard dependency on the docclaw skill

## [0.1.0] - 2026-02-23

### Added
- Initial clawdocs CLI for fetching OpenClaw documentation as markdown for agent consumption
- Install script and GitHub release workflow

### Security
- Harden cache path traversal protection and reject full URL slugs
