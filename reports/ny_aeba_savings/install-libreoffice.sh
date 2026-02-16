#!/usr/bin/env bash
# install-libreoffice.sh — Installs LibreOffice Calc if not already present.
# This is a report-specific dependency used for Excel workbook recalculation
# during testing. It is NOT a project-wide requirement.
set -euo pipefail

if command -v libreoffice &>/dev/null; then
  echo "LibreOffice is already installed: $(libreoffice --version)"
  exit 0
fi

echo "LibreOffice not found. Attempting to install..."

# Detect package manager
if command -v apt-get &>/dev/null; then
  echo "Detected Debian/Ubuntu. Installing libreoffice-calc via apt-get..."
  sudo apt-get update -qq
  sudo apt-get install -y -qq libreoffice-calc >/dev/null 2>&1
elif command -v dnf &>/dev/null; then
  echo "Detected Fedora/RHEL. Installing libreoffice-calc via dnf..."
  sudo dnf install -y -q libreoffice-calc
elif command -v pacman &>/dev/null; then
  echo "Detected Arch Linux. Installing libreoffice-still via pacman..."
  sudo pacman -S --noconfirm libreoffice-still
else
  echo "ERROR: Unsupported platform. Could not find apt-get, dnf, or pacman."
  echo "Please install LibreOffice manually and ensure 'libreoffice' is on PATH."
  exit 1
fi

# Verify installation
if command -v libreoffice &>/dev/null; then
  echo "LibreOffice installed successfully: $(libreoffice --version)"
else
  echo "ERROR: Installation appeared to succeed but 'libreoffice' is not on PATH."
  exit 1
fi
