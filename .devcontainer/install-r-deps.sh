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

# Check if R is installed
if ! command -v R >/dev/null 2>&1; then
    echo "❌ ERROR: R is not installed" >&2
    echo "" >&2
    echo "Please install R before running this script." >&2
    exit 1
fi

# Check if DESCRIPTION file exists
if [ ! -f "${DESCRIPTION_PATH}" ]; then
    echo "❌ ERROR: DESCRIPTION file not found at ${DESCRIPTION_PATH}" >&2
    echo "" >&2
    echo "Usage: $0 [path/to/DESCRIPTION]" >&2
    echo "Default: ./DESCRIPTION" >&2
    exit 1
fi

echo "===================================================================="
echo "📊 Installing R dependencies from DESCRIPTION"
echo "===================================================================="
echo "📄 DESCRIPTION file: ${DESCRIPTION_PATH}"
echo

# Print R version
R_VERSION=$(R --version | head -1)
echo "✅ Using: ${R_VERSION}"
echo

# Create the R script to run
R_SCRIPT=$(cat <<'RSCRIPT'
# Set repositories
# P3M provides pre-compiled binaries for both ARM and x_86 on Ubuntu 24.04 (faster installs)
options(repos = c(
  CRAN = 'https://cran.rstudio.com/',
  P3M = 'https://p3m.dev/cran/__linux__/noble/latest'
))

# Check if pak is installed
if (!requireNamespace("pak", quietly = TRUE)) {
  stop("pak is not installed. Install it first with: install.packages('pak')")
}

# Install dependencies from DESCRIPTION
cat("📥 Installing dependencies from:", dirname("DESCRIPTION_PATH_PLACEHOLDER"), "\n")
pak::local_install_deps(
  root = dirname("DESCRIPTION_PATH_PLACEHOLDER"),
  dependencies = TRUE,
  upgrade = FALSE,
  ask = FALSE
)

cat("\n✅ Done! All R dependencies installed.\n")
RSCRIPT
)

# Replace the placeholder with actual path
R_SCRIPT="${R_SCRIPT//DESCRIPTION_PATH_PLACEHOLDER/$DESCRIPTION_PATH}"

# Run the R script
echo "📥 Installing dependencies..."
echo "$R_SCRIPT" | R --vanilla --quiet --no-save

echo "===================================================================="
echo "✨ R dependencies installed successfully!"
echo "===================================================================="
