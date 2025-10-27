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

# Run code quality tools
check:
    echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    uv lock --locked
    echo "🚀 Linting, formatting, and type checking code"
    prek run -a
    echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Test the code with pytest
test:
    echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --doctest-modules

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
    echo "🚀 Creating virtual environment using uv"
    .devcontainer/postCreateCommand.sh

# Clean generated files and caches
clean:
    rm -rf .pytest_cache .ruff_cache tmp notebooks/.quarto
