#!/usr/bin/env bash
set -euo pipefail

# R Environment Check Script
# This script validates that R, renv, and pak are installed
# and restores the renv environment from lockfile if present

echo "🔍 Checking R environment..."

# Check if R is installed
if ! command -v R >/dev/null 2>&1; then
    echo "❌ Error: R is not installed"
    echo "Please install R before continuing."
    exit 1
fi

echo "✅ R is installed"

# Fix R library permissions on Linux in devcontainer
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🔧 Fixing R library permissions..."
    sudo chown -R vscode:staff /usr/local/lib/R/site-library 2>/dev/null || true
fi

# Get project root directory
PROJECT_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"

# Check if pkgdepends is installed, install if missing
if ! R --slave -e "library(pkgdepends)" >/dev/null 2>&1; then
    echo "📦 pkgdepends package is not installed, installing..."
    if Rscript -e "source('$PROJECT_ROOT/.Rprofile', local = TRUE); install.packages(\"pkgdepends\")"; then
        echo "✅ pkgdepends installed successfully"
    else
        echo "❌ Error: Failed to install pkgdepends package"
        exit 1
    fi
else
    echo "✅ pkgdepends is already installed"
fi

# Check if pak is installed, install if missing
if ! R --slave -e "library(pak)" >/dev/null 2>&1; then
    echo "📦 pak package is not installed, installing..."
    if Rscript -e "source('$PROJECT_ROOT/.Rprofile', local = TRUE); install.packages(\"pak\", repos = sprintf(\"https://r-lib.github.io/p/pak/stable/%s/%s/%s\", .Platform\$pkgType, R.Version()\$os, R.Version()\$arch))"; then
        echo "✅ pak installed successfully"
    else
        echo "❌ Error: Failed to install pak package"
        exit 1
    fi
else
    echo "✅ pak is already installed"
fi

# Create temporary pak lockfile to scan project dependencies
echo "🔧 Scanning project for R package dependencies..."
LOCKFILE="$PROJECT_ROOT/pkg.lock"
if Rscript -e "setwd('$PROJECT_ROOT'); pak::lockfile_create(lockfile = 'pkg.lock')"; then
    echo "✅ Project dependencies scanned successfully"

    # Install packages from temporary lockfile
    echo "📦 Installing packages from scanned dependencies..."
    if Rscript -e "setwd('$PROJECT_ROOT'); pak::lockfile_install(lockfile = 'pkg.lock')"; then
        echo "✅ Packages installed successfully"
    else
        echo "❌ Error: Failed to install packages"
        # Clean up lockfile even on failure
        rm -f "$LOCKFILE"
        exit 2
    fi

    # Clean up temporary lockfile
    echo "🧹 Cleaning up temporary lockfile..."
    rm -f "$LOCKFILE"
    echo "✅ Temporary lockfile removed"
else
    echo "❌ Error: Failed to scan project dependencies"
    # Clean up lockfile if it was partially created
    rm -f "$LOCKFILE"
    exit 2
fi

echo "🎉 R environment check completed successfully"
