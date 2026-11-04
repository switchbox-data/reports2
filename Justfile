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

# Read-only check of the Zotero API key, the Reports collection and its data shapes
zotero-verify:
    uv run python -m lib.sources.cli zotero-verify

# Regenerate reports/references.yaml from Zotero (checks: warn or strict)
sync-bib checks="warn" path_output=path_references *flags="":
    uv run python -m lib.sources.cli sync-bib --checks {{ checks }} --path-output {{ path_output }} {{ flags }}

# Confirm every citation key used in reports exists in references.yaml
check-citekeys path_references=path_references path_reports=path_reports:
    uv run python -m lib.sources.cli check-citekeys --path-references {{ path_references }} --path-reports {{ path_reports }}

# =============================================================================
# 📥 SOURCE INGEST
# =============================================================================
# Sources (PDFs, workbooks, web pages) enter the library through ingest. Agents draft a details card, you
# approve it, then `sources-ingest` writes to Zotero, DocumentCloud / Google Drive and pub.switch.box.
# See context/code/sources_user_guide.md. Run `just sources-doctor` after setting credentials in .env.

# Ingest approved cards (YAML) into Zotero, public hosts, short links and the repo; prints one JSON object per document
sources-ingest +path_cards:
    uv run python -m lib.sources.cli ingest {{ path_cards }}

# Ingest one card, adopting an item you saved to Zotero by hand (e.g. from the Inbox)
sources-ingest-item path_card zotero_item:
    uv run python -m lib.sources.cli ingest {{ path_card }} --zotero-item {{ zotero_item }}

# Download a source's original file from Zotero next to its extract (prints the path)
fetch-source citekey:
    uv run python -m lib.sources.cli fetch {{ citekey }}

# List Zotero items waiting for ingest (add --brief for one line)
sources-pending *flags="":
    uv run python -m lib.sources.cli pending {{ flags }}

# Step checklist for one or more citation keys (green means done)
sources-status +citekeys:
    uv run python -m lib.sources.cli status {{ citekeys }}

# Is this file or URL already in the repo or the Zotero library? e.g. just sources-dedupe --path-file x.pdf
sources-dedupe *flags:
    uv run python -m lib.sources.cli dedupe {{ flags }}

# Existing spellings and short forms of an organization, e.g. just sources-org "Massachusetts DPU"
sources-org name:
    uv run python -m lib.sources.cli org "{{ name }}"

# Existing spellings of a person, e.g. just sources-person "Walsh, Michael"
sources-person name:
    uv run python -m lib.sources.cli person "{{ name }}"

# A PDF's text with [PDF p. N | printed p. M] markers and {n} margin line numbers: the scaffold an extract is written into
sources-page-skeleton path_pdf path_output:
    uv run python -m lib.sources.cli page-skeleton "{{ path_pdf }}" --path-output "{{ path_output }}"

# Check an extract's page markers and line numbers against its PDF (default: the source_file beside the extract)
sources-check-pages path_md path_pdf="":
    uv run python -m lib.sources.cli check-pages "{{ path_md }}" {{ if path_pdf != "" { "--path-pdf \"" + path_pdf + "\"" } else { "" } }}

# Page and line citation of a quote in an extract, e.g. just sources-cite context/sources/x.md "the quoted words"
sources-cite path_md quote:
    uv run python -m lib.sources.cli cite {{ quote(path_md) }} {{ quote(quote) }}

# Give old items doi.org urls (DOI) or pub.switch.box short links (DocumentCloud); dry run unless --apply
sources-backfill-links *flags:
    uv run python -m lib.sources.cli backfill-links {{ flags }}

# One-time Google login (opens a browser) that caches the token ingest uses for Drive uploads; same login as the Sheets helpers
google-login:
    uv run python -m lib.data.gsheets

# Check credentials, Zotero write access, collections, tools and push access to the short-link repo
sources-doctor:
    uv run python -m lib.sources.cli doctor

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
# ⚖️  EXPERT TESTIMONY
# =============================================================================
# Every testimony renders to Word in one standard format. Only the docket details change; they live in
# the `testimony:` block of the testimony .qmd. Render with `just testimony` from the report folder.

# Create a new testimony .qmd with every `testimony:` field in place, e.g. just new-testimony reports/md_hp_rates/expert_testimony.qmd
new-testimony path_qmd:
    uv run python -m lib.just.testimony new {{ path_qmd }}

# Check a testimony's `testimony:` fields without rendering, e.g. just check-testimony reports/md_hp_rates/expert_testimony.qmd
check-testimony path_qmd:
    uv run python -m lib.just.testimony check {{ path_qmd }}

# =============================================================================
# 🏗️  DEVELOPMENT ENVIRONMENT SETUP
# =============================================================================
# These commands help you set up your development environment

# Install uv, python packages, r packages, prek, and pre-commit hooks
install:
    @echo "🚀 Setting up development environment\n"
    @.devcontainer/install-python-deps.sh .
    @echo "🚀 Installing Playwright Chromium (web-page capture for source ingest)"
    @uv run playwright install chromium
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
