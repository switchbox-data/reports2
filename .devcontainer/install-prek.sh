#!/usr/bin/env bash
set -euo pipefail

# install-prek.sh - Install prek CLI for pre-commit hooks
#
# This script installs prek for the current user.
# The actual hook installation (prek install --install-hooks) happens
# after the container starts, when .git/ is mounted from the host.

echo "===================================================================="
echo "🪝 Installing prek CLI"
echo "===================================================================="

# Install prek
curl --proto '=https' --tlsv1.2 -LsSf \
    https://github.com/j178/prek/releases/download/v0.2.11/prek-installer.sh | sh

# Verify installation
if ! command -v prek >/dev/null 2>&1; then
    echo "❌ ERROR: prek installation failed or not in PATH" >&2
    echo "" >&2
    echo "Try adding ~/.local/bin to your PATH:" >&2
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\"" >&2
    exit 1
fi

PREK_VERSION=$(prek --version 2>&1 || echo "unknown")
echo "✅ Installed: prek ${PREK_VERSION}"
echo

echo "===================================================================="
echo "✨ prek CLI installed successfully!"
echo "===================================================================="
echo
echo "💡 To install pre-commit hooks:"
echo "   prek install --install-hooks"
