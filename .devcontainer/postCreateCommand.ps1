# This script is for Windows native development (outside of devcontainer)

# Install uv
Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression

# Install Dependencies
uv sync --group dev

# Install prek pre-commit hooks
Invoke-RestMethod https://github.com/j178/prek/releases/download/v0.2.11/prek-installer.ps1 | Invoke-Expression

# Install pre-commit hooks
prek install --install-hooks


# Check R environment and restore if needed
& .\.devcontainer\checkREnvironment.ps1
