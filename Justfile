# =============================================================================
# ⭐ DEFAULT
# =============================================================================
# If you run `just` you should get the options available, not a full install of the package

default:
    @just --list


# =============================================================================
# 🔍 CODE QUALITY & TESTING
# =============================================================================
# These commands check your code quality and run tests

# Run code quality tools (same as CI)
check:
    echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    uv lock --locked
    echo "🚀 Linting, formatting, and type checking code"
    prek run -a

# Check for obsolete dependencies
check-deps:
    echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Test the code with pytest
test:
    echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --doctest-modules tests/

# =============================================================================
# 🏗️  NEW QUARTO REPORT
# =============================================================================
# These commands help you create a new Quarto report
new_report:
  @read -p "Enter the name of the directory to create for the project: " dir_name && \
  mkdir -p reports/$dir_name && \
  cd reports/$dir_name && \
  QUARTO_TEMPLATE_TRUST=true quarto use template switchbox-data/report_template --no-prompt


# =============================================================================
# 🏗️  DEVELOPMENT ENVIRONMENT SETUP
# =============================================================================
# These commands help you set up your development environment

# Install the virtual environment and install the pre-commit hooks
install:
    @echo "🚀 Setting up development environment\n"
    @.devcontainer/install-python-deps.sh .
    @.devcontainer/install-r-deps.sh ./DESCRIPTION
    @.devcontainer/install-prek.sh
    @.devcontainer/install-prek-deps.sh
    @echo "✨ Development environment ready!\n"

# Clean generated files and caches
clean:
    rm -rf .pytest_cache .ruff_cache tmp notebooks/.quarto

# =============================================================================
# 🔍 AWS
# =============================================================================
# These commands help you login to AWS

aws:
    aws sso login

# =============================================================================
# 🚀 DEVPOD
# =============================================================================
# Launch a devcontainer on AWS via DevPod, using prebuilt image from GHCR

devpod:
    devpod up github.com/switchbox-data/reports2 \
      --prebuild-repository ghcr.io/switchbox-data/reports2
