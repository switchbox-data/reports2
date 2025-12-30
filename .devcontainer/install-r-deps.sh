#!/usr/bin/env bash
set -euo pipefail

# install-r-deps.sh - Install R package dependencies from DESCRIPTION file
#
# This script uses pak to install all R packages listed in the DESCRIPTION file.
# Works on laptops, servers, and in devcontainers.
#
# Usage:
#   ./install-r-deps.sh [path/to/DESCRIPTION]
#
# Requirements:
#   - R must be installed
#   - pak must be installed
#   - DESCRIPTION file must exist

DESCRIPTION_PATH="${1:-./DESCRIPTION}"

echo "===================================================================="
echo "📊 Installing R dependencies from DESCRIPTION"
echo "===================================================================="
echo

# Check if R is installed
if command -v R >/dev/null 2>&1; then
    R_VERSION=$(R --version | head -1)
    echo "✅ Using: ${R_VERSION}"
else
    echo "❌ ERROR: R is not installed" >&2
    echo "" >&2
    echo "Please install R before running this script." >&2
    exit 1
fi
echo

# Check if DESCRIPTION file exists
if [ -f "${DESCRIPTION_PATH}" ]; then
    echo "✅ Found DESCRIPTION file: $(realpath "${DESCRIPTION_PATH}")"
else
    echo "❌ ERROR: DESCRIPTION file is necessary but not found at ${DESCRIPTION_PATH}" >&2
    echo "" >&2
    echo "Usage: $0 [path/to/DESCRIPTION]" >&2
    echo "Default: ./DESCRIPTION" >&2
    exit 1
fi
echo

# Detect platform and set appropriate repository
OS_TYPE=$(uname -s)
if [ "$OS_TYPE" = "Linux" ]; then
    REPO_ARGS="repos = c(CRAN = 'https://cran.rstudio.com/', P3M = 'https://p3m.dev/cran/__linux__/noble/latest')"
    echo "🐧 Detected Linux - using P3M for fast binary package installs"
else
    REPO_ARGS="repos = c(CRAN = 'https://cran.rstudio.com/')"
    echo "🍎 Detected macOS - using CRAN to install packages from source"
fi
echo

# Check if pak is installed
echo "📦 Checking for pak package manager..."
echo
if Rscript -e "if (!requireNamespace('pak', quietly = TRUE)) quit(status = 1)" 2>/dev/null; then
    PAK_VERSION=$(Rscript -e "cat(paste('pak', as.character(packageVersion('pak'))))" 2>/dev/null)
    echo "✅ Using: ${PAK_VERSION}"
else
    echo "❌ ERROR: pak is not installed" >&2
    echo "" >&2
    echo "Install pak with: R -e \"install.packages('pak')\"" >&2
    exit 1
fi
echo

# Get the directory containing DESCRIPTION
DESC_DIR=$(dirname "${DESCRIPTION_PATH}")

# Install dependencies and capture output
echo "📥 Installing R dependencies from DESCRIPTION..."
PAK_OUTPUT=$(Rscript -e "
options(${REPO_ARGS})
result <- pak::local_install_deps(
  root = '${DESC_DIR}',
  dependencies = TRUE,
  upgrade = FALSE,
  ask = FALSE
)
" 2>&1)

echo "$PAK_OUTPUT"
echo

# Parse pak output to show what happened
# Pak summary format: "✔ N deps: kept X, upd Y, added Z, dld W [time]"
if echo "$PAK_OUTPUT" | grep -q "deps:"; then
    # Extract counts from the summary line
    SUMMARY_LINE=$(echo "$PAK_OUTPUT" | grep "deps:" | tail -1)

    KEPT_COUNT=$(echo "$SUMMARY_LINE" | grep -o "kept [0-9]\+" | grep -o "[0-9]\+" || echo "0")
    ADDED_COUNT=$(echo "$SUMMARY_LINE" | grep -o "added [0-9]\+" | grep -o "[0-9]\+" || echo "0")
    UPDATED_COUNT=$(echo "$SUMMARY_LINE" | grep -o "upd [0-9]\+" | grep -o "[0-9]\+" || echo "0")

    # Calculate total installed (added + updated)
    INSTALLED_TOTAL=$((ADDED_COUNT + UPDATED_COUNT))

    # Build the message
    if [ "$INSTALLED_TOTAL" -gt 0 ] && [ "$KEPT_COUNT" -gt 0 ]; then
        echo "✅ Installed ${INSTALLED_TOTAL} R packages, ${KEPT_COUNT} already up to date"
    elif [ "$INSTALLED_TOTAL" -gt 0 ]; then
        echo "✅ Installed ${INSTALLED_TOTAL} R packages"
    elif [ "$KEPT_COUNT" -gt 0 ]; then
        echo "✅ ${KEPT_COUNT} R packages already up to date"
    else
        echo "✅ R packages ready"
    fi
else
    echo "✅ R dependencies processed"
fi
echo

echo "===================================================================="
echo "✨ R dependencies installed successfully!"
echo "===================================================================="
echo
echo
