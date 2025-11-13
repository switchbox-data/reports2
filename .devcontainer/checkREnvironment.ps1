# R Environment Check Script for Windows
# This script validates that R, pkgdepends, and pak are installed
# and creates/installs packages from pak lockfile

Write-Host "🔍 Checking R environment..." -ForegroundColor Cyan

# Check if R is installed
try {
    $rPath = Get-Command R -ErrorAction Stop
    Write-Host "✅ R is installed at: $($rPath.Source)" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: R is not installed" -ForegroundColor Red
    Write-Host "Please install R from https://cran.r-project.org/bin/windows/base/" -ForegroundColor Yellow
    exit 1
}

# Get project root directory
$scriptPath = $PSScriptRoot
$projectRoot = Split-Path (Split-Path $scriptPath -Parent) -Parent

# Check if pkgdepends is installed, install if missing
try {
    R --slave -e "library(pkgdepends)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pkgdepends is already installed" -ForegroundColor Green
    } else {
        throw "pkgdepends not found"
    }
} catch {
    Write-Host "📦 pkgdepends package is not installed, installing..." -ForegroundColor Yellow
    try {
        Rscript -e "source('$projectRoot\.Rprofile', local = TRUE); install.packages('pkgdepends')"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ pkgdepends installed successfully" -ForegroundColor Green
        } else {
            throw "Installation failed"
        }
    } catch {
        Write-Host "❌ Error: Failed to install pkgdepends package" -ForegroundColor Red
        exit 1
    }
}

# Check if pak is installed, install if missing
try {
    R --slave -e "library(pak)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pak is already installed" -ForegroundColor Green
    } else {
        throw "pak not found"
    }
} catch {
    Write-Host "📦 pak package is not installed, installing..." -ForegroundColor Yellow
    try {
        Rscript -e "source('$projectRoot\.Rprofile', local = TRUE); install.packages('pak', repos = sprintf('https://r-lib.github.io/p/pak/stable/%s/%s/%s', .Platform`$pkgType, R.Version()`$os, R.Version()`$arch))"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ pak installed successfully" -ForegroundColor Green
        } else {
            throw "Installation failed"
        }
    } catch {
        Write-Host "❌ Error: Failed to install pak package" -ForegroundColor Red
        exit 1
    }
}

# Create temporary pak lockfile to scan project dependencies
Write-Host "🔧 Scanning project for R package dependencies..." -ForegroundColor Cyan
$pkgLockPath = Join-Path $projectRoot "pkg.lock"

try {
    Rscript -e "setwd('$projectRoot'); pak::lockfile_create(lockfile = 'pkg.lock')"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Project dependencies scanned successfully" -ForegroundColor Green

        # Install packages from temporary lockfile
        Write-Host "📦 Installing packages from scanned dependencies..." -ForegroundColor Cyan
        try {
            Rscript -e "setwd('$projectRoot'); pak::lockfile_install(lockfile = 'pkg.lock')"
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Packages installed successfully" -ForegroundColor Green
            } else {
                throw "Installation failed"
            }
        } catch {
            Write-Host "❌ Error: Failed to install packages" -ForegroundColor Red
            # Clean up lockfile even on failure
            if (Test-Path $pkgLockPath) {
                Remove-Item $pkgLockPath -Force
            }
            exit 2
        }

        # Clean up temporary lockfile
        Write-Host "🧹 Cleaning up temporary lockfile..." -ForegroundColor Cyan
        if (Test-Path $pkgLockPath) {
            Remove-Item $pkgLockPath -Force
            Write-Host "✅ Temporary lockfile removed" -ForegroundColor Green
        }
    } else {
        throw "Scan failed"
    }
} catch {
    Write-Host "❌ Error: Failed to scan project dependencies" -ForegroundColor Red
    # Clean up lockfile if it was partially created
    if (Test-Path $pkgLockPath) {
        Remove-Item $pkgLockPath -Force
    }
    exit 2
}

Write-Host "🎉 R environment check completed successfully" -ForegroundColor Green
