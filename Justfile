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
# Automatically configures SSO if not already configured
aws:
    #!/usr/bin/env bash
    set -euo pipefail

    # Check for AWS CLI (silent if installed, error if not)
    if ! command -v aws >/dev/null 2>&1; then
        echo "❌ ERROR: AWS CLI is not installed" >&2
        echo "" >&2
        echo "Install AWS CLI first:" >&2
        echo "  https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html" >&2
        echo "" >&2
        exit 1
    fi

    # Check if credentials are already valid (early exit if so)
    # Test with an actual EC2 API call since DevPod uses EC2
    if aws sts get-caller-identity &>/dev/null && \
       aws ec2 describe-instances --max-results 5 &>/dev/null; then
        echo "✅ AWS credentials are already valid"
        echo
        exit 0
    fi

    # Credentials are not valid, so we need to configure and/or login
    # Load AWS SSO configuration from shell script (needed for session name)
    CONFIG_FILE=".secrets/aws-sso-config.sh"
    if [ -f "$CONFIG_FILE" ]; then
        # shellcheck source=.secrets/aws-sso-config.sh
        . "$CONFIG_FILE"
    fi
    # Check if SSO is already configured for the default profile
    # (default profile is used when --profile is not specified)
    NEEDS_CONFIG=false
    if ! aws configure get sso_start_url &>/dev/null || \
       ! aws configure get sso_region &>/dev/null; then
        NEEDS_CONFIG=true
    fi

    if [ "$NEEDS_CONFIG" = true ]; then
        echo "🔧 AWS SSO not configured. Setting up SSO configuration..."
        echo

        # Load AWS SSO configuration from shell script
        CONFIG_FILE=".secrets/aws-sso-config.sh"
        if [ ! -f "$CONFIG_FILE" ]; then
            echo "❌ ERROR: Missing AWS SSO configuration file" >&2
            echo "" >&2
            echo "   The file '$CONFIG_FILE' is required but not found." >&2
            echo "   Please ask a team member for this file and place it in the .secrets/ directory." >&2
            echo "" >&2
            exit 1
        fi

        # Source the configuration file
        # shellcheck source=.secrets/aws-sso-config.sh
        . "$CONFIG_FILE"


        # Configure default profile with SSO settings
        aws configure set sso_start_url "$SSO_START_URL"
        aws configure set sso_region "$SSO_REGION"
        aws configure set sso_account_id "$SSO_ACCOUNT_ID"
        aws configure set sso_role_name "$SSO_ROLE_NAME"
        aws configure set region "$SSO_REGION"
        aws configure set output "json"

        echo "✅ AWS SSO configuration complete"
        echo
    fi

    # Run SSO login (handles browser authentication)
    # Use profile-based login since we configure SSO settings directly on the profile
    echo "🔓 Starting AWS SSO login..."
    echo
    aws sso login
    echo
# Your workspace files persist between sessions; container state resets each time.

# Launch devcontainer locally with Docker
up-local rebuild="":
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

    REBUILD="{{ rebuild }}"

    # Warn user if rebuilding
    if [ -n "${REBUILD}" ]; then
        echo "⚠️  WARNING: You are about to rebuild the devcontainer image and relaunch the container."
        echo "   This will reset the container state (runtime package installs will be lost)."
        echo "   Workspace files will persist."
        echo
    fi

    if ! devpod provider list 2>/dev/null | grep -q "^docker\s"; then
        devpod provider add docker 2>/dev/null || true
    fi

    # Use prebuilt images from GHCR (built by CI/CD) for fast startup
    if [ -n "${REBUILD}" ]; then
        devpod up . \
          --id "reports2-docker" \
          --provider docker \
          --prebuild-repository ghcr.io/switchbox-data/reports2 \
          --ide cursor \
          --recreate
    else
        devpod up . \
          --id "reports2-docker" \
          --provider docker \
          --prebuild-repository ghcr.io/switchbox-data/reports2 \
          --ide cursor
    fi

# Launch devcontainer on AWS EC2, using the specified machine type
up-aws MACHINE_TYPE="t3.xlarge" rebuild="": aws
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

    # Convert just variable to bash
    MACHINE_TYPE="{{ MACHINE_TYPE }}"
    REBUILD="{{ rebuild }}"

    # Detect if "rebuild" was passed as MACHINE_TYPE (common mistake: just up-aws rebuild)
    # If so, treat it as the rebuild flag and use default machine type
    if [ "${MACHINE_TYPE}" = "rebuild" ]; then
        MACHINE_TYPE="t3.xlarge"
        REBUILD="rebuild"
    fi

    # Warn user and get confirmation if rebuilding
    if [ -n "${REBUILD}" ]; then
        echo "==========================================================================="
        echo "⚠️  WARNING: You are about to rebuild the devcontainer image and relaunch the container."
        echo "   This action will wipe any uncommitted files on the server."
        echo "==========================================================================="
        echo
        read -p "Do you really want to proceed? (yes/no): " CONFIRM
        if [ "${CONFIRM}" != "yes" ]; then
            echo "Aborted."
            exit 0
        fi
        echo
    fi

    # Replace dots with dashes for provider name
    PROVIDER_NAME="aws-${MACHINE_TYPE//./-}"

    # Add DevPod AWS provider if needed (silent if already exists)
    # Using skevetter's fork which has important fixes: https://github.com/skevetter/devpod-provider-aws
    if devpod provider add github.com/skevetter/devpod-provider-aws \
      --name "${PROVIDER_NAME}" \
      --option AWS_AMI="ami-05134c8ef96964280" \
      --option AWS_DISK_SIZE="100" \
      --option AWS_INSTANCE_TYPE="${MACHINE_TYPE}" \
      --option AWS_REGION="us-west-2" \
      --option AWS_VPC_ID="vpc-0d19afce59d2395d9" >/dev/null 2>&1; then
        echo "➕ Added DevPod AWS provider '${PROVIDER_NAME}' with machine type ${MACHINE_TYPE}"
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

    # Use prebuilt images from GHCR (built by CI/CD) for fast startup
    if [ -n "${REBUILD}" ]; then
        devpod up . \
          --id "${WORKSPACE_ID}" \
          --provider "${PROVIDER_NAME}" \
          --prebuild-repository ghcr.io/switchbox-data/reports2 \
          --ide cursor \
          --recreate
    else
        devpod up . \
          --id "${WORKSPACE_ID}" \
          --provider "${PROVIDER_NAME}" \
          --prebuild-repository ghcr.io/switchbox-data/reports2 \
          --ide cursor
    fi
    echo

    echo "========================================================================"
    echo "✨ Successfully connected to devcontainer on '${WORKSPACE_ID}'"
    echo "========================================================================"
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
