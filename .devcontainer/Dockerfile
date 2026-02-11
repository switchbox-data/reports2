# syntax=docker/dockerfile:1.4

FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# ============================================================================
# All commands run as root. The devcontainer also runs as root (remoteUser).
# This eliminates permission issues between build-time and run-time users.
# ============================================================================

# Copy devcontainer-feature installer script
COPY .devcontainer/install-feature.sh /tmp/install-feature.sh
RUN chmod +x /tmp/install-feature.sh

# Install Python
# os-provided: workaround to avoid compiling Python from source
RUN /tmp/install-feature.sh "ghcr.io/devcontainers/features/python:1" \
    version=os-provided \
    installTools=false

# Install R via rig package manager
# pak: fast installs of R packages
# radian: enhanced R console with multiline editing and syntax highlighting
# USERNAME=root: install pak for root user (default auto-detects vscode user from base image)
# Note: Don't use r-rig feature for rmarkdown/languageserver/vscDebugger/rmarkdown/httpgd -
#       they have outdated detection and install from source (slow)
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/r-rig:1" \
    version=4.4 \
    pakVersion=stable \
    installRadian=true \
    USERNAME=root && \
    # Remove rig zsh completions to avoid compinit security warnings (we don't use them)
    rm -rf /usr/local/share/zsh 2>/dev/null || true

# Install R packages needed by toolchain
# httpgd: Interactive plot viewer (archived from CRAN, requires source build from GitHub)
# pkgdepends: Required by pak, binary install from P3M
# rmarkdown: Required for Quarto R documents, binary install from P3M
# languageserver: VSCode autocomplete / go-to-definition / hover docs, binary install from P3M
# vscDebugger: R debugger for VSCode RDebugger extension, binary install from P3M
# USERNAME=root: install packages for root user
# Note: Uses P3M mirror for fast binary installs on Ubuntu 24.04
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/r-packages:1" \
    packages="github::nx10/unigd, github::nx10/httpgd, pkgdepends, rmarkdown, languageserver, github::ManuelHentschel/vscDebugger" \
    cranMirror="https://p3m.dev/cran/__linux__/noble/latest" \
    installSystemRequirements=true \
    USERNAME=root

# Install AWS CLI
RUN /tmp/install-feature.sh "ghcr.io/devcontainers/features/aws-cli:1" \
    version=2.27.4

# Install GitHub CLI
RUN /tmp/install-feature.sh "ghcr.io/devcontainers/features/github-cli:1"

# Install just CLI
RUN /tmp/install-feature.sh "ghcr.io/guiyomh/features/just:0.1.0" \
    version=1.42.4

# Install Quarto CLI
# installChromium: for Mermaid diagrams
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/quarto-cli:1" \
    version=1.8.26 \
    installChromium=true

# Install additional apt packages (needed by quarto)
# python3-tk: Required for matplotlib to work with quarto
# chromium-browser: Shared library dependencies for Chromium, required for Mermaid diagrams in quarto (must be combined with installChromium=true above)
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/apt-packages:1" \
    packages="python3-tk, chromium-browser"

# Install zsh with plugins and custom plugin repositories
# The zsh feature installs oh-my-zsh for root user and enables plugins in .zshrc.
# Built-in plugins (git, colored-man-pages, colorize, history) are included with oh-my-zsh.
# Custom plugins (zsh-autosuggestions, fast-syntax-highlighting, zsh-autocomplete) need to be cloned separately.
COPY .devcontainer/install-ohmyzsh-plugins.sh /tmp/install-ohmyzsh-plugins.sh
RUN chmod +x /tmp/install-ohmyzsh-plugins.sh && \
    /tmp/install-feature.sh "ghcr.io/nils-geistmann/devcontainers-features/zsh:0" \
        plugins="git colored-man-pages colorize history zsh-autosuggestions fast-syntax-highlighting zsh-autocomplete" \
        theme="bira" && \
    /tmp/install-ohmyzsh-plugins.sh

# Install prek CLI for pre-commit hooks
# Note: The actual hook installation (prek install --install-hooks) happens in postCreateCommand
# because it needs to write to .git/hooks/, which is mounted from the host after container starts
COPY .devcontainer/install-prek.sh /tmp/install-prek.sh
RUN chmod +x /tmp/install-prek.sh && \
    /tmp/install-prek.sh

# Install R dependencies from DESCRIPTION
# This layer rebuilds when DESCRIPTION changes
COPY .devcontainer/install-r-deps.sh /tmp/install-r-deps.sh
COPY DESCRIPTION /tmp/DESCRIPTION
RUN chmod +x /tmp/install-r-deps.sh && \
    /tmp/install-r-deps.sh /tmp/DESCRIPTION

# Install Python dependencies from pyproject.toml + uv.lock
# This layer rebuilds when either file changes
# Note: venv is installed to /opt/venv (not workspace) to avoid being shadowed by mounted code
COPY .devcontainer/install-python-deps.sh /tmp/install-python-deps.sh
COPY pyproject.toml uv.lock /tmp/
# Set UV_PROJECT_ENVIRONMENT to install venv to /opt/venv
# This ensures uv commands (uv add, uv run, etc.) always use this location
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN mkdir -p /opt/venv && \
    chmod +x /tmp/install-python-deps.sh && \
    /tmp/install-python-deps.sh /tmp

# Add uv/uvx to PATH (installed to /root/.local/bin)
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory for development
WORKDIR /workspaces/reports2
