# syntax=docker/dockerfile:1.4

FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# ============================================================================
# ROOT USER SECTION
# ============================================================================
# All commands in this section run as root (Dockerfile default).
# This section installs system-level tools and devcontainer features.
# This mirrors what happens when you use "features" in devcontainer.json:
# features are installed as root during the image build phase.
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
# Note: Don't use r-rig feature for rmarkdown/languageserver/vscDebugger/rmarkdown/httpgd -
#       they have outdated detection and install from source (slow)
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/r-rig:1" \
    version=4.4 \
    pakVersion=stable \
    installRadian=true

# Install R packages needed by toolchain
# httpgd: Interactive plot viewer (archived from CRAN, requires source build from GitHub)
# pkgdepends: Required by pak, binary install from P3M
# rmarkdown: Required for Quarto R documents, binary install from P3M
# languageserver: VSCode autocomplete / go-to-definition / hover docs, binary install from P3M
# vscDebugger: R debugger for VSCode RDebugger extension, binary install from P3M
# Note: Uses P3M mirror for fast binary installs on Ubuntu 24.04
RUN /tmp/install-feature.sh "ghcr.io/rocker-org/devcontainer-features/r-packages:1" \
    packages="github::nx10/httpgd, pkgdepends, rmarkdown, languageserver, github::ManuelHentschel/vscDebugger" \
    cranMirror="https://p3m.dev/cran/__linux__/noble/latest" \
    installSystemRequirements=true

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

# Install zsh with plugins and clone custom plugin repositories
# The zsh feature enables plugins in .zshrc.
# Built-in plugins (git, colored-man-pages, colorize, history) are included with oh-my-zsh and don't need separate installation.
# Custom plugins (zsh-autosuggestions, fast-syntax-highlighting, zsh-autocomplete) need their repositories cloned to
# ~/.oh-my-zsh/custom/plugins/, which is done via install-ohmyzsh-plugins.sh.
COPY .devcontainer/install-ohmyzsh-plugins.sh /tmp/install-ohmyzsh-plugins.sh
RUN chmod +x /tmp/install-ohmyzsh-plugins.sh && \
    /tmp/install-feature.sh "ghcr.io/nils-geistmann/devcontainers-features/zsh:0" \
        plugins="git colored-man-pages colorize history zsh-autosuggestions fast-syntax-highlighting zsh-autocomplete" && \
    /tmp/install-ohmyzsh-plugins.sh

# ============================================================================
# VSCODE USER SECTION
# ============================================================================
# Switch to vscode user for installing R and Python dependencies.
# This is necessary because:
#   1. The r-rig feature (installed as root above) installs pak for the vscode user
#      in /home/vscode/R, not for root. R packages need to be installed as vscode
#      to access pak and write to vscode's R library.
#   2. Python venv and packages should be owned by vscode (the user who will
#      actually run the code), not root.
#   3. prek should be installed for vscode user (who runs pre-commit hooks).
#   4. This mirrors the container runtime: the devcontainer runs as vscode user,
#      not root, so dependencies should be installed as vscode during build.
#
# ============================================================================
USER vscode

# Install prek CLI for pre-commit hooks
# Note: The actual hook installation (prek install --install-hooks) happens in postCreateCommand
# because it needs to write to .git/hooks/, which is mounted from the host after container starts
COPY --chown=vscode:vscode .devcontainer/install-prek.sh /tmp/install-prek.sh
RUN chmod +x /tmp/install-prek.sh && \
    /tmp/install-prek.sh

# Install R dependencies from DESCRIPTION
# This layer rebuilds when DESCRIPTION changes
# Note: --chown is still needed even though USER is vscode, because COPY always copies files as root:root by default.
# Without --chown, vscode user can read but not write to these files.
# Note: Files copied to /tmp (not /workspace) since they're just build-time inputs.
# The actual project files will be mounted at /workspaces/reports2 at runtime.
COPY --chown=vscode:vscode .devcontainer/install-r-deps.sh /tmp/install-r-deps.sh
COPY --chown=vscode:vscode DESCRIPTION /tmp/DESCRIPTION
RUN chmod +x /tmp/install-r-deps.sh && \
    /tmp/install-r-deps.sh /tmp/DESCRIPTION

# Install Python dependencies from pyproject.toml + uv.lock
# This layer rebuilds when either file changes
# Note: --chown ensures vscode user owns these files (COPY defaults to root:root ownership)
# Note: Files copied to /tmp (not /workspace) since they're just build-time inputs.
# The actual project files will be mounted at /workspaces/reports2 at runtime.
COPY --chown=vscode:vscode .devcontainer/install-python-deps.sh /tmp/install-python-deps.sh
COPY --chown=vscode:vscode pyproject.toml uv.lock /tmp/
RUN chmod +x /tmp/install-python-deps.sh && \
    /tmp/install-python-deps.sh /tmp

# Configure Git to trust all directories (needed for CI and when mounting repos)
# This prevents "dubious ownership" errors when the vscode user accesses repos
# owned by different users (e.g., when GitHub Actions mounts the workspace).
RUN git config --global --add safe.directory '*'

# Set working directory for development
WORKDIR /workspaces/reports2
