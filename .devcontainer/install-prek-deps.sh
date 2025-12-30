#!/usr/bin/env bash
set -euo pipefail

# install-prek-deps.sh - Install prek pre-commit hooks
#
# Requirements:
#   - prek must be installed
#   - .pre-commit-config.yaml file must exist

echo "===================================================================="
echo "🪝 Installing prek pre-commit hooks from .pre-commit-config.yaml"
echo "===================================================================="
echo

# Find the git repository root and cd there
# This works in both devcontainers and on laptops
if ! REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null); then
    echo "❌ ERROR: Not in a git repository" >&2
    exit 1
fi
cd "${REPO_ROOT}"
echo "📁 Working in repository: ${REPO_ROOT}"
echo

# Check if .pre-commit-config.yaml exists
PRECOMMIT_CONFIG=".pre-commit-config.yaml"
if [ -f "${PRECOMMIT_CONFIG}" ]; then
    echo "✅ Found .pre-commit-config.yaml: $(realpath "${PRECOMMIT_CONFIG}")"
else
    echo "❌ ERROR: .pre-commit-config.yaml is necessary but not found in $(pwd)" >&2
    exit 1
fi
echo

# Check if prek is installed
echo "📦 Checking for prek..."
echo
if command -v prek >/dev/null 2>&1; then
    PREK_VERSION=$(prek --version 2>&1)
    echo "✅ Using: ${PREK_VERSION}"
else
    echo "❌ ERROR: prek is not installed" >&2
    echo "Expected location: ${HOME}/.local/bin/prek" >&2
    echo "" >&2
    echo "Install prek first by running: .devcontainer/install-prek.sh" >&2
    exit 1
fi
echo

# Check if pre-commit hooks are already installed
PRECOMMIT_HOOK=".git/hooks/pre-commit"
HOOKS_ALREADY_INSTALLED=false

if [ -f "${PRECOMMIT_HOOK}" ]; then
    # Check if it's a prek-managed hook
    if grep -q "prek" "${PRECOMMIT_HOOK}" 2>/dev/null; then
        HOOKS_ALREADY_INSTALLED=true
        echo "ℹ️  Pre-commit hooks already installed, checking for updates..."
    fi
fi

# Install prek pre-commit hooks
if [ "$HOOKS_ALREADY_INSTALLED" = true ]; then
    echo "📥 Updating prek pre-commit hooks..."
else
    echo "📥 Installing prek pre-commit hooks..."
fi

PREK_OUTPUT=$(prek install --install-hooks 2>&1)
echo "$PREK_OUTPUT"
echo

# Parse prek output to show what happened
# Count total hooks from .pre-commit-config.yaml (look for "- id:" pattern)
TOTAL_HOOKS=$(grep -c "^\s*- id:" .pre-commit-config.yaml 2>/dev/null || echo "0")
# Ensure it's a single integer
TOTAL_HOOKS=$(echo "$TOTAL_HOOKS" | head -1 | tr -d ' ')

if [ "$HOOKS_ALREADY_INSTALLED" = true ]; then
    if [ "$TOTAL_HOOKS" -gt 0 ] 2>/dev/null; then
        echo "✅ ${TOTAL_HOOKS} pre-commit hooks already installed"
    else
        echo "✅ Pre-commit hooks already installed"
    fi
else
    if [ "$TOTAL_HOOKS" -gt 0 ] 2>/dev/null; then
        echo "✅ Installed ${TOTAL_HOOKS} pre-commit hooks"
    else
        echo "✅ Pre-commit hooks installed"
    fi
fi
echo

echo "===================================================================="
echo "✨ prek pre-commit hooks installed successfully!"
echo "===================================================================="
echo
echo
