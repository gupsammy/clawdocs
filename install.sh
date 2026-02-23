#!/usr/bin/env sh
# install.sh — Install clawdocs
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/gupsammy/clawdocs/main/install.sh | sh
#
# Environment overrides:
#   INSTALL_DIR        Target directory          (default: ~/.local/bin)
#   CLAWDOCS_VERSION   Specific version to pin   (default: latest release)

set -e

REPO="gupsammy/clawdocs"
BINARY="clawdocs"
INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/bin}"

# ── helpers ────────────────────────────────────────────────────────────────────

say()  { printf '  %s\n' "$*"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$*"; }
err()  { printf '\033[31merror:\033[0m %s\n' "$*" >&2; exit 1; }
warn() { printf '\033[33mwarning:\033[0m %s\n' "$*" >&2; }

# Download a URL to stdout; tries curl then wget.
fetch() {
    _url="$1"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$_url"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- "$_url"
    else
        err "curl or wget is required but neither was found"
    fi
}

# Download a URL to a file path.
fetch_to() {
    _url="$1"; _dest="$2"
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$_url" -o "$_dest"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO "$_dest" "$_url"
    else
        err "curl or wget is required but neither was found"
    fi
}

# ── python check ───────────────────────────────────────────────────────────────

check_python() {
    if ! command -v python3 >/dev/null 2>&1; then
        err "Python 3.8+ is required. Install it from https://python.org"
    fi
    if ! python3 -c "import sys; assert sys.version_info >= (3, 8)" 2>/dev/null; then
        _found=$(python3 --version 2>&1)
        err "Python 3.8+ is required but found: $_found. Install from https://python.org"
    fi
    ok "python3 $(python3 --version 2>&1 | cut -d' ' -f2)"
}

# ── version resolution ─────────────────────────────────────────────────────────

resolve_version() {
    # Explicit env override wins.
    if [ -n "${CLAWDOCS_VERSION:-}" ]; then
        ok "version $CLAWDOCS_VERSION (pinned)" >&2
        echo "$CLAWDOCS_VERSION"
        return
    fi

    # Ask GitHub Releases API for the latest tag.
    _api="https://api.github.com/repos/$REPO/releases/latest"
    _resp=$(fetch "$_api" 2>/dev/null || true)
    _tag=$(printf '%s' "$_resp" \
        | grep '"tag_name"' \
        | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/' \
        | head -1)

    if [ -n "$_tag" ]; then
        ok "version $_tag (latest release)" >&2
        echo "$_tag"
    else
        # No release yet — fall back to main branch.
        ok "version main (no release found, using main branch)" >&2
        echo ""
    fi
}

# ── download URL construction ──────────────────────────────────────────────────

build_url() {
    _ver="$1"
    if [ -n "$_ver" ]; then
        echo "https://github.com/$REPO/releases/download/$_ver/$BINARY"
    else
        echo "https://raw.githubusercontent.com/$REPO/main/$BINARY"
    fi
}

# ── PATH check ─────────────────────────────────────────────────────────────────

check_path() {
    _dir="$1"
    case ":${PATH}:" in
        *":$_dir:"*) ;;
        *)
            warn "$_dir is not in your PATH."
            warn "Add the following line to your shell config (~/.zshrc, ~/.bashrc, etc.):"
            warn "  export PATH=\"$_dir:\$PATH\""
            warn "Then restart your shell or run: source ~/.zshrc"
            ;;
    esac
}

# ── main ───────────────────────────────────────────────────────────────────────

printf '\nInstalling clawdocs...\n\n'

check_python

VERSION=$(resolve_version)
URL=$(build_url "$VERSION")

say "downloading $(printf '%s' "$URL" | sed 's|.*/||')"
mkdir -p "$INSTALL_DIR"
fetch_to "$URL" "$INSTALL_DIR/$BINARY"
chmod +x "$INSTALL_DIR/$BINARY"

printf '\n'
ok "installed to $INSTALL_DIR/$BINARY"
printf '\n'

check_path "$INSTALL_DIR"

printf '\nRun: clawdocs --version\n\n'
