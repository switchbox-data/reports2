# =============================================================================
# ⭐ DEFAULT
# =============================================================================

# If you run `just`, you see all available commands
default:
    @just --list

# =============================================================================
# 🔍 CODE QUALITY & TESTING
# =============================================================================
# These commands check your code quality and run tests

# Run code quality tools (same as CI)
check:
    echo "🚀 Checking lock file consistency with 'pyproject.toml'"
    XDG_CACHE_HOME="${XDG_CACHE_HOME:-.cache}" UV_CACHE_DIR="${UV_CACHE_DIR:-.cache/uv}" uv lock --locked
    echo "🚀 Linting, formatting, and type checking code"
    XDG_CACHE_HOME="${XDG_CACHE_HOME:-.cache}" UV_CACHE_DIR="${UV_CACHE_DIR:-.cache/uv}" PREK_HOME="${PREK_HOME:-.cache/prek}" uv run prek run -a

# Prepare and cache prek hook environments ahead of time
prepare-hooks:
    echo "🚀 Preparing prek hook environments"
    XDG_CACHE_HOME="${XDG_CACHE_HOME:-.cache}" UV_CACHE_DIR="${UV_CACHE_DIR:-.cache/uv}" PREK_HOME="${PREK_HOME:-.cache/prek}" uv run prek prepare-hooks

# Check for obsolete dependencies
check-deps:
    echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Run tests
test:
    echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --doctest-modules tests/

# =============================================================================
# 📚 BIBLIOGRAPHY
# =============================================================================
# reports/references.yaml is generated from the Zotero "Reports" collection.
# None of these recipes write to Zotero.

path_references := "reports/references.yaml"
path_reports := "reports"
path_csl := "reports/chicago-author-date-switchbox.csl"

# Read-only check of the Zotero API key, the Reports collection and its data shapes
zotero-verify:
    uv run python -m lib.sources.cli zotero-verify

# Regenerate reports/references.yaml from Zotero (checks: warn or strict)
sync-bib checks="warn" path_output=path_references *flags="":
    uv run python -m lib.sources.cli sync-bib --checks {{ checks }} --path-output {{ path_output }} {{ flags }}

# Confirm every citation key used in reports exists in references.yaml
check-citekeys path_references=path_references path_reports=path_reports:
    uv run python -m lib.sources.cli check-citekeys --path-references {{ path_references }} --path-reports {{ path_reports }}

# Regenerate the Switchbox CSL style from pandoc's default Chicago author-date style
make-csl path_output=path_csl:
    uv run python -m lib.sources.make_csl --path-output {{ path_output }}

# =============================================================================
# 🏗️  NEW QUARTO REPORT
# =============================================================================

# Create a new Quarto report from the switchbox-data/report_template
new-report:
    @read -p "Enter the name of the directory to create for the project: " dir_name && \
    mkdir -p reports/$dir_name && \
    cd reports/$dir_name && \
    QUARTO_TEMPLATE_TRUST=true quarto use template switchbox-data/report_template --no-prompt

# =============================================================================
# 🏗️  DEVELOPMENT ENVIRONMENT SETUP
# =============================================================================
# These commands help you set up your development environment

# Install uv, python packages, r packages, prek, and pre-commit hooks
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
# Authenticate with AWS via SSO (for manual AWS CLI usage like S3 access)

# Automatically configures SSO if not already configured
aws:
    .devcontainer/devpod/aws.sh

# Your workspace files persist between sessions; container state resets each time.

# Launch devcontainer locally with Docker
up-local rebuild="":
    .devcontainer/devpod/up-local.sh {{ rebuild }}

# Launch devcontainer on AWS EC2, using the specified machine type
up-aws MACHINE_TYPE="t3.xlarge" rebuild="":
    @bash .devcontainer/devpod/up-aws.sh {{ MACHINE_TYPE }} {{ rebuild }}

# Show active EC2 instances running devcontainers, and commands to delete them
up-aws-list:
    @bash .devcontainer/devpod/up-aws-list.sh
