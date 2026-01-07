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
    uv lock --locked
    echo "🚀 Linting, formatting, and type checking code"
    prek run -a

# Check for obsolete dependencies
check-deps:
    echo "🚀 Checking for obsolete dependencies: Running deptry"
    uv run deptry .

# Run tests
test:
    echo "🚀 Testing code: Running pytest"
    uv run python -m pytest --doctest-modules tests/

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
aws:
    aws sso login

# =============================================================================
# 🚀 LAUNCH DEV ENVIRONMENT
# =============================================================================
# Launch the development environment from your current branch.
# Your workspace files persist between sessions; container state resets each time.

# Launch devcontainer locally with Docker
up-local:
    #!/usr/bin/env bash
    set -euo pipefail

    # Check for DevPod CLI (silent if installed, error if not)
    if ! command -v devpod >/dev/null 2>&1; then
        echo "❌ ERROR: DevPod CLI is not installed" >&2
        echo "" >&2
        echo "Install skevetter fork of DevPod first:" >&2
        echo "  https://github.com/skevetter/devpod/releases" >&2
        echo "" >&2
        exit 1
    fi

    if ! devpod provider list 2>/dev/null | grep -q "^docker\s"; then
        devpod provider add docker 2>/dev/null || true
    fi
    devpod up . \
      --id "reports2-docker" \
      --provider docker \
      --prebuild-repository ghcr.io/switchbox-data/reports2 `# Use prebuilt images from GHCR (built by CI/CD) for fast startup` \
      --ide cursor \
      --recreate  # Always restart container fresh, ensuring env matches current branch (workspace files still persist)

# Launch devcontainer on AWS EC2, using the specified machine type
up-aws MACHINE_TYPE="t3.xlarge":
    #!/usr/bin/env bash
    set -euo pipefail

    # Check for DevPod CLI (silent if installed, error if not)
    if ! command -v devpod >/dev/null 2>&1; then
        echo "❌ ERROR: DevPod CLI is not installed" >&2
        echo "" >&2
        echo "Install skevetter fork of DevPod first:" >&2
        echo "  https://github.com/skevetter/devpod/releases" >&2
        echo "" >&2
        exit 1
    fi

    # Check for AWS CLI (silent if installed, error if not)
    if ! command -v aws >/dev/null 2>&1; then
        echo "❌ ERROR: AWS CLI is not installed" >&2
        echo "" >&2
        echo "Install AWS CLI first:" >&2
        echo "  https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html" >&2
        echo "" >&2
        exit 1
    fi

    # Check AWS credentials and log in if needed (silent if already logged in)
    if ! aws sts get-caller-identity &>/dev/null; then
        echo "❌ AWS credentials are not valid or have expired"
        echo "🔓 Starting AWS SSO login..."
        echo
        aws sso login
        echo
        echo "✅ AWS login successful"
        echo
    fi

    # Convert just variable to bash, then replace dots with dashes for provider name
    MACHINE_TYPE="{{ MACHINE_TYPE }}"
    PROVIDER_NAME="aws-${MACHINE_TYPE//./-}"

    # Add DevPod AWS provider if needed (silent if already exists)
    # Using skevetter's fork which has important fixes: https://github.com/skevetter/devpod-provider-aws
    if devpod provider add github.com/skevetter/devpod-provider-aws \
      --name "${PROVIDER_NAME}" \
      --option AWS_AMI="ami-05134c8ef96964280" \
      --option AWS_DISK_SIZE="100" \
      --option AWS_INSTANCE_TYPE="{{ MACHINE_TYPE }}" \
      --option AWS_REGION="us-west-2" \
      --option AWS_VPC_ID="vpc-0d19afce59d2395d9" >/dev/null 2>&1; then
        echo "➕ Added DevPod AWS provider '${PROVIDER_NAME}' with machine type {{ MACHINE_TYPE }}"
        echo
    fi

    # Create unique workspace ID using provider name
    WORKSPACE_ID="reports2-${PROVIDER_NAME}"

    # Check if workspace already exists
    if devpod list --output json 2>/dev/null | jq -e --arg id "${WORKSPACE_ID}" '.[] | select(.id == $id)' >/dev/null 2>&1; then
        echo "============================================================================"
        echo "🔄 EC2 instance '${WORKSPACE_ID}' found, reconnecting to devcontainer"
        echo "============================================================================"
        echo
        echo "   This may take a moment..."
    else
        echo "==========================================================================="
        echo "🚀 Launching new EC2 instance '${WORKSPACE_ID}' to run devcontainer"
        echo "==========================================================================="
        echo
        echo "   This may take a few minutes..."
    fi
    echo
    devpod up . \
      --id "${WORKSPACE_ID}" \
      --provider "${PROVIDER_NAME}" \
      --prebuild-repository ghcr.io/switchbox-data/reports2 `# Use prebuilt images from GHCR (built by CI/CD) for fast startup` \
      --ide cursor \
      --recreate  # Always restart container fresh, ensuring env matches current branch (workspace files still persist)
    echo

    echo "========================================================================"
    echo "✨ Successfully connected to devcontainer on '${WORKSPACE_ID}'"
    echo "========================================================================"
    echo
    echo

# Show active EC2 instances running devcontainers, and commands to delete them
up-aws-list:
    #!/usr/bin/env bash
    set -euo pipefail

    # Check for DevPod CLI (silent if installed, error if not)
    if ! command -v devpod >/dev/null 2>&1; then
        echo "❌ ERROR: DevPod CLI is not installed" >&2
        echo "" >&2
        echo "Install skevetter fork of DevPod first:" >&2
        echo "  https://github.com/skevetter/devpod/releases" >&2
        echo "" >&2
        exit 1
    fi

    instances=$(devpod list --output json 2>/dev/null | jq -r '.[] | select(.provider.name | startswith("aws-")) | "  \(.id)\n    Provider: \(.provider.name)\n    Status: \(.status // "unknown")\n    IDE: \(.ide.name // "none")\n    └─ To delete: devpod delete \(.id)"' || echo "")
    if [ -z "$instances" ]; then
        echo "Active EC2 instances: None"
        echo ""
        echo "Use just up-aws to launch an the reports2 devcontainer on an EC2 instance."
    else
        echo "Active EC2 instances:"
        echo ""
        echo "$instances"
        echo ""
        echo "Copy and run a delete command above to terminate an instance."
    fi
