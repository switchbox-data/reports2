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

# Create pak lockfile from project dependencies (only if it doesn't exist)
$pkgLockPath = Join-Path $projectRoot "pkg.lock"
if (-not (Test-Path $pkgLockPath)) {
    Write-Host "🔧 Creating pak lockfile from project dependencies..." -ForegroundColor Cyan
    try {
        Rscript -e "setwd('$projectRoot'); pak::lockfile_create()"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Pak lockfile created successfully" -ForegroundColor Green
        } else {
            throw "Creation failed"
        }
    } catch {
        Write-Host "❌ Error: Failed to create pak lockfile" -ForegroundColor Red
        exit 2
    }
} else {
    Write-Host "ℹ️  Pak lockfile already exists, skipping creation" -ForegroundColor Blue
}

# Install packages from lockfile
if (Test-Path $pkgLockPath) {
    Write-Host "📦 Installing packages from pak lockfile..." -ForegroundColor Cyan

    try {
        Rscript -e "setwd('$projectRoot'); pak::lockfile_install(lockfile = 'pkg.lock')"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Packages installed successfully from pak lockfile" -ForegroundColor Green
        } else {
            throw "Installation failed"
        }
    } catch {
        Write-Host "❌ Error: Failed to install packages from pak lockfile" -ForegroundColor Red
        Write-Host "Please check the pkg.lock file and try again" -ForegroundColor Yellow
        exit 2
    }
} else {
    Write-Host "❌ Error: Pak lockfile was not created" -ForegroundColor Red
    exit 2
}

Write-Host "🎉 R environment check completed successfully" -ForegroundColor Green
