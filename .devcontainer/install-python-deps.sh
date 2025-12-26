#!/usr/bin/env bash
set -euo pipefail

# install-python-packages.sh - Install Python dependencies using uv
#
# Usage:
#   ./install-python-packages.sh [path/to/workspace]
#
# This script:
# 1. Checks if Python is installed
# 2. Installs uv package manager
# 3. Installs Python dependencies from pyproject.toml + uv.lock
#
# Requirements:
#   - Python must be installed
#   - pyproject.toml and uv.lock must exist in the workspace directory

WORKSPACE_PATH="${1:-.}"

echo "===================================================================="
echo "🐍 Installing Python dependencies"
echo "===================================================================="
echo "📄 Workspace: ${WORKSPACE_PATH}"
echo

# Check if Python is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ ERROR: Python is not installed" >&2
    echo "" >&2
    echo "Please install Python before running this script:" >&2
    echo "  • Ubuntu/Debian: sudo apt-get install python3" >&2
    echo "  • macOS: brew install python3" >&2
    exit 1
fi

# Print Python version
PYTHON_VERSION=$(python3 --version)
echo "✅ Found: ${PYTHON_VERSION}"
echo

# Install uv package manager
echo "📦 Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
echo

# Verify installation by checking if uv works
if ! UV_VERSION=$(uv --version 2>&1); then
    echo "❌ ERROR: uv installation failed or uv command not found" >&2
    exit 1
fi

echo "✅ Installed: ${UV_VERSION}"
echo

# Change to workspace directory
cd "${WORKSPACE_PATH}"

# Install Python dependencies
echo "📥 Installing Python dependencies from pyproject.toml + uv.lock..."
uv sync --group dev
echo

echo "===================================================================="
echo "✨ Python dependencies installed successfully!"
echo "===================================================================="
