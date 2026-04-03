# reports2

Switchbox is a nonprofit think tank that produces rigorous, accessible data on U.S. state climate policy for advocates, policymakers, and the public. Find out more at [www.switch.box](www.switch.box)

This repository contains Switchbox's reports. We use a modern stack that uses both **Python** and **R**.

## 📋 Table of Contents

- [Overview](#-overview)
- [Why Open Source?](#-why-open-source)
- [Repo Structure](#-repo-structure)
- [Available Commands](#-available-commands) <!-- markdownlint-disable-line MD051 -->
- [Quick Start](#-quick-start)
- [Creating a New Report](#-creating-a-new-report)
- [Development Workflow](#-development-workflow)
- [Understanding Quarto Reports](#-understanding-quarto-reports)
- [Publishing Web Reports](#-publishing-web-reports)
- [Managing Dependencies](#-managing-dependencies)
- [When to Use Python vs. R](#-when-to-use-python-vs-r)
- [Working with Data](#-working-with-data)
- [Code Quality & Testing](#-code-quality--testing)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Cleaning Up](#-cleaning-up)
- [Additional Resources](#-additional-resources)

---

## 🎯 Overview

- **Quarto Reports**: All reports written in [Quarto](https://quarto.org/) (located in `reports/` directory)
- **Cloud Data**: The data used in our reports is stored in an S3 bucket (`s3://data.sb/) on AWS
- **Bilingual Analytics**: Reports use both Python (polars) and R (tidyverse)
- **Fast Package Management**:
  - Python: [uv](https://github.com/astral-sh/uv) for lightning-fast dependency resolution
  - R: [pak](https://pak.r-lib.org/) with [P3M](https://p3m.dev/) for fast binary package installation
- **Reproducible Development Environment**: Uses devcontainers via DevPod (see [Quick Start](#-quick-start))
- **Task Runner**: [just](https://github.com/casey/just) for convenient command execution
- **Code Quality**: Modern linting and formatting with [ruff](https://github.com/astral-sh/ruff) (Python) and [air](https://github.com/posit-dev/air) (R), automated via [prek](https://github.com/j178/prek) pre-commit hooks

## 🌍 Why Open Source?

The reports (on [our website](https://switch.box)) are shared under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/), and the code behind them (contained in this repo) is released under the [MIT License](LICENSE).

We do this for two reasons:

### 1. 🔍 Transparency

As a research group, our work is frequently cited in the press and aims to shape the policy conversation. Given the public nature of our work, we believe everyone has the right to see exactly how we produce our findings—going well beyond vague methodology sections.

### 2. 🔬 Open Science

We believe the clean energy transition will happen faster if energy researchers (particularly those working in the nonprofit sector) embrace open data and open source code, so they can build on each other's work rather than reinventing the wheel.

## 📁 Repo Structure

Here is an initial overview of our repo. The rest of this README.md will walk through it in detail:

```text
reports2/
├── .devcontainer/          # Dev container configuration
├── docs/                   # Published HTML reports (hosted via GitHub Pages at switchbox-data.github.io/reports2)
├── lib/                    # Shared libraries and utilities
├── reports/                # Switchbox report projects (source code for reports on our website)
│   ├── ct_hp_rates/        # Individual Quarto projects for each report
│   ├── il_lea/
│   └── ...
├── tests/                  # Python test suite
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── DESCRIPTION             # R dependencies
├── pyproject.toml          # Python dependencies and tool configuration
├── uv.lock                 # Locked Python dependencies
└── Justfile                # Command runner recipes
```

## 🛠️ Available Commands

To make the core tasks in this repo visible and easy to use, we've automated them using the just command runner.

Here is an initial overview of those tasks. The rest of this README.md will explain when these commands should be used.

**Two places to use `just`**: Commands are available in the **repository root** (for development environment and testing) and in **individual report directories** (for rendering reports). These commands are defined in `Justfile`s in each location - see the [root Justfile](Justfile) and individual report Justfiles (e.g., `reports/ny_aeba_grid/Justfile`).

To wiew all available commands in either of these locations:

```bash
just --list
```

**Repository root commands:**

- `just install` - Set up development environment
- `just check` - Run quality checks
- `just check-deps` - Check for obsolete dependencies with [deptry](https://github.com/fpgmaas/deptry)
- `just test` - Run test suite
- `just new_report` - Create a new Quarto report in `reports/`
- `just aws` - Authenticate with AWS SSO
- `just up-local [rebuild]` - Launch dev environment locally (use `rebuild` to update dev environment)
- `just up-aws [MACHINE_TYPE] [rebuild]` - Launch dev environment on AWS EC2 (use `rebuild` to update dev environment)
- `just up-aws-list` - Show active EC2 instances (for cleanup)
- `just clean` - Remove generated files and caches

**Report directory commands** (`reports/<project_code>/`):

- `just render` - Render HTML version of report using Quarto
- `just draft` - Render Word document for content reviews using Quarto
- `just typeset` - Render ICML for InDesign typesetting using Quarto
- `just publish` - Copy rendered HTML version of report from project `docs/` to root `docs/` for web publishing
- `just clean` - Remove generated files and caches

## 🚀 Quick Start

If you want to rerun and edit the code that generates our reports, this section shows you how to get started.

### Option 1: Devcontainer on your laptops

Devcontainers make it easy to use Docker images to package and run an entire development environment. This means you don't have to install all the software required to render our reports by hand. It also means that you get the exact same dev environment as everyone else, guaranteeing that everything Just Works.

Using this repo's devcontainer on your laptop is therefore the easiest and fastest way to get started. You'll need to install some software first:

1. Prerequisites:
   - Install [VS Code](https://code.visualstudio.com/) or [Cursor](https://www.cursor.com/), which can use devcontainers seamlessly
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop), which will actually run the devcontainer
   - Install latest release of [DevPod (skevetter fork)](https://github.com/skevetter/devpod/releases), which makes it easier to work with devcontainers (we use this fork because it has important fixes)
     - If you use MacOS, it may not let you open DevPod. Go to `System Settings > Privacy & Security > Security` to enable the app.
     - Make sure you enable the Devpod cli.
   - Install [just](https://github.com/casey/just) to run commands
   - Make sure Docker Desktop is running in the background

2. Launch:

   ```bash
   just up-local
   ```

**How local Devcontainers work:**

Think of your local devcontainer as a **virtal machine** that runs on your laptop, and that VS Code/Cursor can connect to seamlessly, as if you were just running them on your local files. The reports2 repo is automatically synced between your laptop and the container: any changes you make to the files in the container will be reflected on your laptop, and vice versa.

First time you run `just up-local`, Devpod:

- Pulls a prebuilt devcontainer image matching your current local branch/commit (~30x)
- If for some reason a prebuilt image isn't available, it builds from scratch (~8 min first time)
- **Note**: if you're already familiar with using local devcontainers in VS Code/Cursor, the reason we use Devpod to run them instead is because it allows us to use prebuilt devcontainer images rather than building them from scratch on your laptoo
- Starts a new Docker container on your laptop using this prebuilt image
- Mounts your working directory / the reports2 repo into the container
- Launches Cursor and connects it to the container via (local) SSH

After a few minutes of inactivity, Devpod will stop the container. However, an uncommitted files you had in the container persist on your laptop directory (because it was mounted into the container). To restart the container...

Subsequent times you run `just up-local`, Devpod:

- Restarts the container using the same prebuilt image that was used when you first created it
- Re-mounts your working directory / the reports2 repo into the container
- Connects you to this new container running on your laptop
- Your uncommitted files are still there (they're in your laptop directory, which is mounted into the container)
- Inside the container, you can switch branches, pull changes, etc. — it's just a regular devcontainer (but note that if you switch to a branch that contains a different devcontainer definition, it won't automatically update anything.)
- **Important**: When you restart and reconnect to the devcontainer by running `just up-local` again, the devcontainer stays same as it was when you first ran `just up-local`: it isn't automatically rebuilt—even if the commit that's now checked out on your laptop contains a different devcontainer definition—unless you tell Devpod to do this explicitly.

**When you need to rebuild the devcontainer:**

The dev environment is "frozen" to whatever was on your local branch when you first ran `just up-local`. To update it:

1. On your laptop, checkout the branch/commit with the dev environment you want:

   ```bash
   git checkout feature-branch
   git pull
   ```

2. Launch the devcontainer using the rebuild flag:

   ```bash
   just up-local rebuild
   ```

   This will:
   - Shut down the old container (if still running)
   - **Your uncommitted files persist on your laptop** (unlike AWS, where they'd be overwritten)
   - Download the prebuilt image corresponding to the commit you have checked out
   - Spin up a new container based on that prebuilt image
   - Mount your local files back into the new container
   - Connect your code editor to the container via (local) SSH

3. **After rebuilding**, running `just up-local` (without the flag) just reconnects you to the the rebuilt devcontainer

**To persist new packages:**
Add them to `pyproject.toml` (Python) or `DESCRIPTION` (R), commit the changes, let CI/CD build the devcontainer image, then run `just up-local rebuild` to use this prebuilt image. (That way, the image gets built once and used by all, rather than everyone needing to rebuild it locally.)

### Option 2: Devcontainer on an AWS EC2 instance

Our data lives on S3, so running a devcontainer locally means waiting for data to download from S3 before report code can be run. For faster data access (and faster computers), you can run the exact same devcontainer on an EC2 instance in AWS (in `us-west-2`, near our S3 data):

1. Prerequisites:
   - Install [DevPod (skevetter fork)](https://github.com/skevetter/devpod/releases) (we use this fork because it has important fixes)
   - AWS CLI installed
   - AWS credentials configured (see [AWS Configuration](#-aws-configuration))

2. Launch:

   ```bash
   # Default instance (t3.xlarge: 4 vCPU, 16GB RAM)
   just up-aws

   # Heavy workloads (t3.2xlarge: 8 vCPU, 32GB RAM)
   just up-aws t3.2xlarge

   # Memory-intensive work (r6i.xlarge: 4 vCPU, 32GB RAM)
   just up-aws r6i.xlarge
   ```

**How Devcontainers on AWS EC2 instances work:**

Think of your Devpod AWS instance as a **persistent server** that runs your devcontainer, much as your laptop would. Here's how they work:

First time you run `just up-aws`, Devpod:

- Creates a new EC2 instance (takes a few minutes)
- Uploads the reports2 git repo on your laptop to the instance
- Inspects the current branch/commit (that you had checked out on your laptop, now on the server), determine which prebuilt devcontainer image corresponding to this commit, and pulls it from GitHub Container Registry (GHCR)
- Starts a new container on the instance using this prebuilt image
- Connects your local code editor to this container via SSH

You'll get charged for the time that the instance is running. After you disconnect from the container, the instance will actually get paused, so you'll no longer be charged for compute—only for the hard drive, which persists. To wake the server back up, and reconnect your code editor to the container:

Subsequent times you run `just up-aws`, Devpod:

- Starts the instance again, and unpauses the container
- Reconnects your local coder editor to the container on the instance, via SSH (takes ~30 seconds)
- ✅ Uncommitted files stay on the server between sessions (because the hard drive persists)
- ✅ You can switch branches, pull changes, work normally — it's just a regular server, but using our devcontainer environment
- **Important**: The dev environment (packages, tools) stays static — it won't automatically update when you change branches

**When you need to update the dev environment:**

The dev environment (Python packages, R packages, tools) is "frozen" to whatever was on your local branch when you first created the EC2 instance. To update it:

1. On your laptop, checkout the branch/commit that contains the dev environment you want:

   ```bash
   git checkout feature-branch
   git pull
   ```

2. Rebuild the server devcontainer:

   ```bash
   just up-aws rebuild
   ```

   ⚠️ **Warning**: Devpod will:

   - Keep using the current instance, but destroy the container
   - Upload the reports2 git repo on your laptop to the instance again, _overwriting the repo that was alread there_
   - **This means you'll lose any uncommitted work on the server** (save/commit first!)
   - Inspect the current branch/commit (that you had checked out on your laptop, now on the server), determine which prebuilt devcontainer image corresponding to this commit, and pull it from GitHub Container Registry (GHCR)
   - Start a new container on the instance using this prebuilt image
   - Connect your local code editor to this new container via SSH

   **Note**: Unlike `up-local rebuild` (where uncommitted files persist on your laptop), `up-aws rebuild` overwrites everything on the server. Always commit or stash your work before rebuilding on AWS.

**Managing AWS instances:**

After you've created an instance via `just up-aws`, the instance persist indefinity, though they are paused after a period of inactivity. Paused instances are less expensive then running ones, but they still cost money.

**Cost considerations:**

- **Compute costs**: You only pay for compute time when the instance is running. DevPod automatically stops instances after inactivity (default: 10 minutes), so you're not charged for compute when paused.
- **Storage costs**: You pay for EBS storage (~$8/month for 100GB) even when the instance is stopped.
- **Total cost**: Depends on usage, but typically much less than running 24/7. For example, running 2 hours/day costs ~$10/month compute + ~$8/month storage = ~$18/month.

To see what instances are already running:

```bash
# See what's running
just up-aws-list

# Shows output like:
#   reports2-aws-t3-xlarge (Running)
#   └─ To delete: devpod delete reports2-aws-t3-xlarge
```

To delete the instance, copy and paste delete command shown. The instance terminates immediately.

### Option 3: Manual Installation (Without Dev Container)

We strongly recommend using devcontainers (either locally or in the cloud), because all the software is already packaged up in a Docker image for you. But if you prefer to install the software directly on your laptop:

1. Install Prerequisites:
   - Python 3.9+
   - R 4.0+
   - `pak` package for R
   - [just](https://github.com/casey/just)
   - quarto

2. Run install script:

   ```bash
   just install
   ```

   This command:
   - Installs `uv`
   - Uses `uv` to create a virtualenv and install python packages to it
   - Uses `pak` to install R packages listed in `DESCRIPTION` file
   - Installs pre-commit hooks with `prek`

## 📝 Creating a New Report

To create a new Quarto report from the Switchbox template:

```bash
just new_report
```

You'll be prompted to enter a report name.

**Naming convention**: Use `state_topic` format (e.g., `ny_aeba`, `ri_hp_rates`). If we've used a topic before in other states (like `hp_rates`), reuse it to maintain consistency across reports.

This will:

- Create `reports/<state_topic>/`

- Initialize it with the [switchbox-data/report_template](https://github.com/switchbox-data/report_template)
- Set up the necessary Quarto configuration files

## 🔄 Development Workflow

We follow a structured development process to ensure all work is tracked, organized, and reviewed. This workflow keeps PRs from growing stale, maintains code quality, and ensures every piece of work is tied to a clear ticket.

**Our workflow:**

1. **All work starts with a GitHub Issue** - Captured in our Kanban board with clear "What", "Why", "How", and "Deliverables"

2. **Issues are reviewed before work begins** - Ensures alignment before coding starts
3. **Branches are created from issues** - Automatic linking between code and tickets
4. **PRs are created early** - Work-in-progress is visible and reviewable
5. **Code is reviewed before merging** - Quality checks and peer review catch issues
6. **PRs are short-lived** - Merged within a week to keep momentum

This process ensures:

- 📝 Every feature/fix has documentation (the issue)
- 🔗 Code changes are traceable to requirements
- 👀 Work is visible and reviewable at all stages
- ✅ Code is reviewed early and often

**For complete details on our workflow**, including how to create issues, request reviews, and merge PRs, see **[CONTRIBUTING.md](CONTRIBUTING.md)**.

## 📄 Understanding Quarto Reports

### What is Quarto?

[Quarto](https://quarto.org/) is a scientific publishing system that lets you combine **narrative text** with **executable code**. This approach, called [literate programming](https://en.wikipedia.org/wiki/Literate_programming), means your analysis and narrative live together in one document.

**Simple example:**

````markdown
## Heat Pump Adoption

Total residential heat pumps installed in Rhode Island:

```{r}
total_installs <- sum(resstock_data$heat_pump_count)
print(total_installs)
```

This represents `{r} pct_electric`% of all heating systems statewide.
````

The code executes when you render the document, weaving results directly into your narrative. [Learn more about Quarto](https://quarto.org/docs/get-started/).

### Our Opinionated Approach

We use Quarto in a specific way, defined by our [report template](https://github.com/switchbox-data/report_template). Our reports are based on Quarto's [Manuscript project type](https://quarto.org/docs/manuscripts/), which is designed for scientific and technical publications.

### Report Structure

After running `just new_report`, you'll have this structure:

```text
reports/your-report/
├── index.qmd              # The actual report (narrative + embedded results)
├── notebooks/
│   └── analysis.qmd       # The underlying analysis (data wrangling + analysis + visualization)
├── _quarto.yml            # Quarto project configuration (set up by template)
├── Justfile               # Commands to render the report
└── docs/                  # Generated output (HTML, DOCX, ICML, PDF) - gitignored, do not commit
```

**Key files**:

- **`index.qmd`**: Your report's narrative. This is what readers see. Contains text, embedded charts, and inline results.
- **`notebooks/analysis.qmd`**: Your data analysis. Data loading, cleaning, modeling, and creating visualizations.
  - **Prefer a single `analysis.qmd` notebook** for simplicity and clarity
  - If you need multiple notebooks, **check with the team first** to discuss organization
- **`_quarto.yml`**: Quarto configuration - [YAML front matter](https://quarto.org/docs/authoring/front-matter.html), format settings, and stylesheet references (all set up by the template)

### Data Flow: Analysis → Report

We keep analysis separate from narrative. Here's how data flows from `notebooks/analysis.qmd` to `index.qmd`:

#### 1. Export Variables from Analysis (R)

In `notebooks/analysis.qmd`, export objects to a local RData file (gitignored, do not commit):

```r
# Do your analysis
total_savings <- calculate_savings(data)
growth_rate <- 0.15

# Export variables for the report
save(total_savings, growth_rate, file = "report_vars.RData")
```

Then load them in `index.qmd`:

```r
# Load analysis results
load("report_vars.RData")
```

**Note**: The `.RData` file is gitignored - only the code that generates it is versioned.

#### 2. Embed Charts from Analysis

For visualizations, use Quarto's [embed syntax](https://quarto.org/docs/authoring/notebook-embed.html) to pull charts from `notebooks/analysis.qmd` into `index.qmd`:

In `notebooks/analysis.qmd`, create a labeled code chunk:

````markdown
```{r}
#| label: fig-energy-savings
#| fig-cap: "Annual energy savings by upgrade"

ggplot(data, aes(x = upgrade, y = savings)) +
  geom_col() +
  theme_minimal()
```
````

In `index.qmd`, embed it:

```markdown
{{< embed notebooks/analysis.qmd#fig-energy-savings >}}
```

The chart appears in your report without duplicating code!

### Report Output Formats

Our template includes `just` commands for different outputs:

```bash
just render    # Generate HTML for web publishing (static site)
just draft     # Generate Word doc for content reviews with collaborators
just typeset   # Generate ICML for creating typeset PDFs in InDesign
```

**When to use each:**

- **HTML** (`just render`): Publishing our reports as interactive web pages
- **DOCX** (`just draft`): Sharing drafts for content review and feedback
- **ICML** (`just typeset`): Professional typesetting in Adobe InDesign for PDF export

The template automatically configures these formats with our stylesheets and branding.

## 🌐 Publishing Web Reports

Once your report is ready to be published, you'll want to get it to the web so others can access it. This section walks through how our web hosting works and the steps to publish.

### How Web Reports Work

When you run `just render` in your report directory (e.g., `reports/ny_aeba_grid/`), Quarto generates a complete static website in the `docs/` subdirectory:

```text
reports/ny_aeba_grid/
└── docs/                      # Generated by Quarto (gitignored in report dirs)
    ├── index.html             # Main HTML file
    ├── img/                   # Images
    ├── index_files/           # Supporting files
    ├── notebooks/             # Embedded notebook outputs
    └── site_libs/             # JavaScript, CSS, etc.
```

**Why this matters**: The entire `docs/` directory is self-contained. You can copy it anywhere, open `index.html`, and the report will work perfectly - all assets are bundled together.

💡 **Development Tip**: Use this during development! Run `just render` frequently and open `reports/<project_code>/docs/index.html` in your browser to see exactly how your report will look when published to the web. This lets you iterate on design and layout before publishing.

### How We Host Reports

We use [GitHub Pages](https://pages.github.com/) to host our reports automatically:

1. **Any files in the root `docs/` directory on the `main` branch** are automatically published to `https://switchbox-data.github.io/reports2/`

2. **To publish a report**, we copy the rendered report from `reports/<project_code>/docs/` to the root `docs/<project_code>/` directory

3. **URLs**: A report at `docs/ny_aeba_grid/index.html` becomes accessible at:
   - [https://switchbox-data.github.io/reports2/ny_aeba_grid/](https://switchbox-data.github.io/reports2/ny_aeba_grid/)
   - [https://www.switch.box/aeba-grid](https://www.switch.box/aeba-grid) (our web admin embeds it in an iframe - you don't need to worry about this)

📂 **See what's published**: Check the [docs/](https://github.com/switchbox-data/reports2/tree/main/docs) directory to see currently published reports.

💡 **Key insight**: Publishing = rendering your report ➡️ copying to `docs/<project_code>/` ➡️ merging to `main`

### Publishing Step-by-Step

Follow these steps to publish or update a web report:

#### 1. Prepare Your Report

- Finish your work following the development workflow (create issue, work in a branch, etc.)
- Make sure your PR is ready to merge
- Open your devcontainer terminal

#### 2. Navigate to Your Report Directory

```bash
cd reports/<project_code>
```

#### 3. Verify Render Configuration

Check that all notebooks needed for the report are listed in `_quarto.yml` under `project > render`:

```yaml
project:
  render:
    - index.qmd
    - notebooks/analysis.qmd
```

**Why**: Quarto only renders files you explicitly list, ensuring you have control over what gets published.

#### 4. Clear Cache and Render

```bash
# Clear any cached content
just clean

# Render the HTML version
just render
```

This creates fresh output in `reports/<project_code>/docs/`.

#### 5. Copy to Publishing Directory

```bash
# Copy rendered report to root docs/ directory
just publish
```

**What this does**: Copies all files from `reports/<project_code>/docs/` to `docs/<project_code>/`. If files already exist at `docs/<project_code>/`, they're deleted first to ensure a clean publish.

#### 6. Return to Repository Root

```bash
cd ../..
```

#### 7. Stage the Published Files

```bash
git add -f docs/
```

**Why `-f` (force)?** The `docs/` directory is gitignored in report directories to prevent accidental commits during development. The `-f` flag overrides this, allowing you to commit to the root `docs/` directory intentionally.

#### 8. Commit and Push

```bash
git commit -m "Publish new version of <project_code> report"
git push
```

**Important**: Pushing to your branch does NOT publish the report yet - it must be merged to `main` first.

#### 9. Merge to Main

- Go to your PR on GitHub
- Merge it to `main`

#### 10. Verify Deployment

- GitHub automatically triggers a "pages build and deployment" workflow
- Check [Actions](https://github.com/switchbox-data/reports2/actions) to see the workflow run
- Once the workflow is green (✓), your report is live at `https://switchbox-data.github.io/reports/<project_code>/`

### Adding a PDF Link

Once you have a final PDF version (typically typeset in InDesign), you can add a download link to the web report:

#### 1. Get the PDF

- Download the final PDF from Google Drive: `Projects > <project_code> > final`
- Ensure it's named `switchbox_<project_code>.pdf` (rename if needed)

#### 2. Add to Report Directory

Place the PDF in your report root:

```text
reports/<project_code>/
├── switchbox_<project_code>.pdf   # ← Add here
├── index.qmd
└── ...
```

#### 3. Update YAML Front Matter

Add or uncomment this in `index.qmd`'s YAML header:

```yaml
other-links:
  - text: PDF
    icon: file-earmark-pdf
    href: switchbox_<project_code>.pdf
```

**What this does**: Adds a PDF download button to your web report's navigation.

#### 4. Re-render and Publish

```bash
# Re-render with PDF link
just render

# Verify the PDF link appears and works locally

# Publish the update
just publish
cd ../..
git add -f docs/
git commit -m "Add PDF link to <project_code> report"
git push
```

Then merge to `main` following steps 9-10 above.

## 📦 Managing Dependencies

### Python Dependencies

**Adding a Python package:**

```bash
uv add <package-name>
```

This command:

- Adds the package to `pyproject.toml`
- Updates `uv.lock` with resolved dependencies
- Installs the package in your virtual environment

**Example:**

```bash
uv add polars  # Add polars as a dependency
uv add --dev pytest-mock  # Add as a dev dependency
```

**⚠️ Important**: Do NOT use `pip install` to add packages. Using `pip install` will install the package locally but will not update `pyproject.toml` or `uv.lock`, meaning others won't get your dependencies. Always use `uv add`.

#### How Your Python Package Persists

_In dev container_:

- When you run `uv add package-name`, packages are installed to `/opt/venv/` inside the container
- They stay in the container, and are not exported to your local filesystem. So if you restart the container, the package will be gone!
- To make your new package persist, you need to add it to the image itself, by committing `pyproject.toml` and `uv.lock` and pushing to Github
- If you're using devcontainers locally, run `just up-local rebuild` after CI/CD builds the new image, and your package will be permanently installed within the devcontainer
- If you're using devcontainers on AWS, run `just up-aws rebuild` after CI/CD builds the new image, and your package will be permanently installed within the devcontainer
- **Bottom line**: Run `uv add`, commit `pyproject.toml` and `uv.lock`, let CI/CD build the new devcontainer image that contains these packages, then run `just up-local rebuild` or `just up-aws rebuild` to use this new image

_On regular laptop_:

- When you run `uv add package-name`, packages are installed to `.venv/`, which persists in your local workspace
- Packages remain installed between sessions
- No reinstallation needed unless you delete `.venv/` or run `uv sync` after changes

#### How Others Get Your Python Package

_In dev container_:

1. You commit both `pyproject.toml` and `uv.lock`, and push to Github

2. Others pull your changes
3. They rebuild their container:
   - If they're using devcontainers locally, they run `just up-local rebuild` on their laptop after pulling your changes, and their laptop will automatically download a new devcontainer image (built by CI/CD) that contains all packages in `uv.lock` (including your new one), and spin up a new devcontainer based on this image
   - If they're using devcontainers on AWS, they run `just up-aws rebuild` on their laptop after pulling your changes, and the instance will automatically download a new image (built by CI/CD) that contains all packages in `uv.lock` (including your new one), and spin up a new devcontainer based on this image

_On regular laptop_:

1. You commit both `pyproject.toml` and `uv.lock` to git
2. Others pull your changes
3. They must manually run `uv sync` to install the new dependency

### R Dependencies

R dependency management works differently, you have to manually update a file that lists packages, then install them.

**Adding a new R package:**

1. **Add it to `DESCRIPTION`** in the `Imports` section:

   ```text
   Imports:
       dplyr,
       ggplot2,
       arrow
   ```

2. **Install it** by running:

   ```bash
   just install
   ```

#### How Your R Package Persists

_In dev container_:

- If you install a package directly with `pak::pak("dplyr")`, the package is installed temporarily in the container
- It will be gone when the container restarts!
- If you add it to `DESCRIPTION` and run `just install`, as documented above, the package will also install temporarily
- However, if you then commit `DESCRIPTION` and push to Github...
- If you're using devcontainers locally, run `just up-local rebuild` after CI/CD builds the new image, and every package in `DESCRIPTION` (including your new one) will be permanently installed within the devcontainer
- If you're using devcontainers on AWS, run `just up-aws rebuild` after CI/CD builds the new image, and every package in `DESCRIPTION` (including your new one) will be permanently installed within the devcontainer
- **Bottom line**: Add packages to `DESCRIPTION`, commit this file, let CI/CD build the new devcontainer image that contains these packages, then run `just up-local rebuild` or `just up-aws rebuild` on your laptop to use this new image

_On regular laptop_:

- Packages are saved to your global R library (typically `~/R/library/`)
- Packages remain installed between sessions
- No reinstallation needed unless you uninstall them or use a different R version

#### How Others Get Your R Package

_In dev container_:

1. You add a package to `DESCRIPTION`, commit it, and push to GitHub

2. Others pull your changes
3. They rebuild their container:
   - If they're using devcontainers locally, they run `just up-local rebuild` on their laptop after pulling your changes, and their laptop will automatically download a new devcontainer image (built by CI/CD) that contains all packages in `DESCRIPTION` (including your new one), and spin up a new devcontainer based on this image
   - If they're using devcontainers on AWS, they run `just up-aws rebuild` on their laptop after pulling your changes, and the instance will automatically download a new image (built by CI/CD) that contains all packages in `DESCRIPTION` (including your new one), and spin up a new devcontainer based on this image

_On regular laptop_:

1. You add a package to `DESCRIPTION` and commit it to git

2. Others pull your changes
3. They manually install dependencies:

   ```bash
   just install
   ```

   Or in an R session:

   ```r
   pak::local_install_deps()  # Installs all dependencies from DESCRIPTION
   ```

## 🔀 When to Use Python vs. R

Both languages are available, but we have clear preferences based on the type of work:

### Use R (with tidyverse) for

- **Data analysis** - Exploratory data analysis, statistical analysis
- **Data modeling** - Statistical models, regression, forecasting
- **Data visualization** - Creating charts and graphs for reports
- **Default choice** - Unless there's a specific reason to use Python, prefer R for these tasks

### Use Python for

- **Data engineering** - Scripts that fetch, process, and upload data to S3
- **Numerical simulations** - Generating synthetic data, Monte Carlo simulations
- **Library requirements** - When a specific Python library is needed

### Why this split?

- **R/tidyverse excels** at interactive analysis and producing publication-quality visualizations
- **Python excels** at scripting, automation, and computational tasks
- Our reports are written in Quarto, which works seamlessly with both languages
- You can use both in the same report when needed, but prefer consistency within a single analysis

## 📊 Working with Data

### 🔑 AWS Configuration

Data for analyses is stored on S3. Ensure you have:

- AWS credentials configured in `~/.aws/credentials`
- Default region set to `us-west-2`

The dev container automatically mounts your local AWS credentials.

### Reading Data from S3

**All data lives in S3** - we do not store data files in this git repository. Our primary data bucket is `s3://data.sb/`, and we also use public open data sources from other S3 buckets.

We prefer **Parquet files** in our data lake for efficient columnar storage and compression.

**Using Python (with [polars](https://pola.rs/) / [arrow](https://arrow.apache.org/docs/python/))**

```python
import polars as pl

# Scan multiple parquet files from S3 (lazy - doesn't load data yet)
lf = pl.scan_parquet("s3://data.sb/eia/heating_oil_prices/*.parquet")

# Apply transformations and aggregations (still lazy)
# By using parquet and arrow with lazy execution, we limit how much data is downloaded
result = (
    lf.filter(pl.col("state") == "RI")
    .group_by("year")
    .agg(pl.col("price").mean().alias("avg_price"))
)

# 💡 TIP: Stay in lazy execution as long as possible - do all filtering, grouping, and aggregations
# before calling collect(). This allows Polars to optimize the query plan and minimize data transfer.

# Collect to download subset of parquet data, perform aggregation, and load into memory
# Result is a Polars DataFrame (columnar, Arrow-based format)
df = result.collect()

# To convert to row-oriented format, use to_pandas() to get a pandas DataFrame
# ⚠️ WARNING: We do NOT use pandas for analysis - only use if a library requires pandas DataFrame
pandas_df = result.collect().to_pandas()
```

**Using R (with [dplyr](https://dplyr.tidyverse.org/) / [arrow](https://arrow.apache.org/docs/r/))**

```r
library(arrow)
library(dplyr)

# Scan multiple parquet files from S3 (lazy - doesn't load data yet)
lf <- open_dataset("s3://data.sb/eia/heating_oil_prices/*.parquet")

# Apply transformations and aggregations (still lazy)
# By using parquet and arrow with lazy execution, we limit how much data is downloaded
result <- lf |>
  filter(state == "RI") |>
  group_by(year) |>
  summarize(avg_price = mean(price))

# 💡 TIP: Stay in lazy execution as long as possible - do all filtering, grouping, and aggregations
# before calling compute(). This allows Arrow to optimize the query plan and minimize data transfer.

# Compute to download subset of parquet data, perform aggregation, and load into memory
# Result is an Arrow Table (columnar, Arrow-based format - same as Python polars)
df <- result |> compute()

# Or use collect() to convert to tibble (row-oriented, standard R data frame)
# ⚠️ WARNING: stay in arrow whenever possible — only use if a library requires tibbles
tibble_df <- result |> collect()
```

#### Performance Considerations

**Initial downloads can be slow** depending on:

- File size
- Your internet connection
- Distance from the S3 region (us-west-2)

**Options to improve performance:**

1. **Cache locally**: Download files once and cache in `data/` (gitignored)
2. **Run dev containers in the cloud**: See [Option 2: Devcontainer on an AWS EC2 instance](#option-2-devcontainer-on-an-aws-ec2-instance) for launching devcontainers on AWS in `us-west-2 region`, same as the data bucket
3. **Use partitioned datasets**: Only read the partitions you need

**When reports execute**: Data is downloaded from S3 at runtime. The first run may be slower, but subsequent runs can use cached data if you've set up local caching.

### Writing Data to S3

⚠️ **Note**: We have naming conventions but the upload process is still being standardized.

#### Naming and Organization Conventions

**Directory structure:**

```text
s3://data.sb/<org>/<dataset>/<filename_YYYYMMDD.parquet>
```

- **Org**: Organization producing the data (e.g., `nrel`, `eia`, `fred`)
- **Dataset**: Name of the dataset (e.g., `heating_oil`, `resstock`, `inflation_factors`)
  - Always use a dataset directory, even if there's only one file
  - **Prefer official data product names** when they exist (e.g., EIA's "State Energy Data System", Census Bureau's "American Community Survey")
  - If the official name is long, use a clear abbreviated version in lowercase with underscores
- **Filename**: Descriptive name for the specific file
  - **Do NOT include** the org name or dataset name (already in the path)
  - **Do include** geographic scope, time granularity, or other distinguishing info about the contents of the file
  - **Must end with** `_YYYYMMDD` reflecting when the data was downloaded
- **Naming style**: Everything lowercase with underscores
  - Good: `eia/heating_oil_prices/ri_monthly_20240315.parquet`
  - Bad: `EIA/Heating-Oil_ri_eia_prices_2024-03-15.parquet`

**Why timestamps matter:**

- **Versioning**: New snapshots get new dates (e.g., `ri_monthly_20240415.parquet`)

- **Reproducibility**: Old code using `ri_monthly_20240315.parquet` continues to work
- **Traceability**: Know exactly when data was retrieved

**Example structure:**

```text
s3://data.sb/

├── eia/
│   ├── heating_oil_prices/
│   │   ├── ri_monthly_20240315.parquet
│   │   └── ct_monthly_20240315.parquet
│   └── propane/
│       └── ri_monthly_20240315.parquet
├── nrel/
│   └── resstock/
│       └── 2024_release2_tmy3/...
└── fred/
    └── inflation_factors/
        └── monthly_20240301.parquet
```

#### Uploading Data

**Preferred method**: Use scripted downloads via `just` commands

Check the `lib/` directory for existing data fetch scripts:

- `lib/eia/fetch_delivered_fuels_prices_eia.py`
- `lib/eia/fetch_eia_state_profile.py`

These scripts should:

1. Download data from the source
2. Process and save as Parquet
3. Upload to S3 with proper naming (including date)
4. Be runnable via `just` commands for reproducibility

**Manual uploads** (when necessary):

```bash
# Using AWS CLI
aws s3 cp local_file.parquet s3://data.sb/<org>/<dataset>/<filename_YYYYMMDD.parquet>

# Example: uploading heating oil data for Rhode Island
aws s3 cp ri_monthly_20240315.parquet s3://data.sb/eia/heating_oil/ri_monthly_20240315.parquet
```

⚠️ **Before uploading**: Coordinate with the team to ensure:

- Naming follows conventions
- Path doesn't conflict with existing data
- Date reflects actual download/creation date

## 🔍 Code Quality & Testing

### Pre-commit Hooks

**What are pre-commit hooks?** Pre-commit hooks are automated scripts that run every time you make a git commit. They catch issues (formatting, linting, syntax errors) _before_ code enters the repository, ensuring consistent code quality across the team. This saves time in code review and prevents broken code from being committed.

**Why we use them**: By automatically formatting and checking code at commit time, we ensure that all code in the repository meets our quality standards without requiring manual intervention. Everyone's code is formatted consistently, and common errors are caught immediately.

Pre-commit hooks are managed by [prek](https://github.com/j178/prek) and configured in `.pre-commit-config.yaml`.

**Configured hooks:**

- **ruff-check**: Lints Python code with auto-fix

- **ruff-format**: Formats Python code
- **ty-check**: Type checks Python code using [ty](https://github.com/astral-sh/ty)
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml/json/toml**: Validates config file syntax
- **check-added-large-files**: Prevents commits of files >600KB
- **check-merge-conflict**: Detects merge conflict markers
- **check-case-conflict**: Prevents case-sensitivity issues

**Note on R formatting**: We don't yet have the [air](https://github.com/posit-dev/air) formatter for R integrated with pre-commit hooks. Instead, use air's editor integration via the [Posit.air-vscode extension](https://marketplace.visualstudio.com/items?itemName=Posit.air-vscode), which is pre-installed in the dev container. Air will automatically format your R code in the editor.

Hooks run automatically on `git commit`. To run manually:

```bash
prek run -a  # Run all hooks on all files
```

### Run Quality Checks

```bash
just check
```

This command performs (same as CI):

1. **Lock file validation**: Ensures `uv.lock` is consistent with `pyproject.toml`
2. **Pre-commit hooks**: Runs all configured hooks including type checking (see above)

**Optional - Check for obsolete dependencies:**

```bash
just check-deps
```

Runs [deptry](https://github.com/fpgmaas/deptry) to check for unused dependencies in `pyproject.toml`.

### Run Tests

```bash
just test
```

Runs the Python test suite with pytest (tests in `tests/` directory), including doctest validation.

**Note on R tests**: We don't currently have R tests or a testing framework configured for R code. Only Python tests are run by `just test` and in CI.

## 🚦 CI/CD Pipeline

The repository uses [GitHub Actions](https://docs.github.com/en/actions) to automatically run quality checks and tests on your code. **The CI runs the exact same `just` commands** you use locally, in the same devcontainer environment, ensuring perfect consistency.

### What Runs and When

The workflow runs **two jobs in parallel** for speed:

**On Pull Requests** (opened, updated, or marked ready for review):

1. **quality-checks**: Runs `just check` (lock file validation + pre-commit hooks)
2. **tests**: Runs `just test` (pytest test suite)

**On Push to `main`:**

- Same checks and tests as pull requests (both jobs run in parallel)

### Devcontainer in CI/CD

On every commit to `main` or a pull request, GitHub Actions actually **builds the devcontainer image**, and publishes it to [GitHub Container Registry (GHCR)](https://github.com/switchbox-data/reports2/pkgs/container/reports2), for use by:

1. **CI/CD**: **quality-checks** and **tests** jobs run inside the devcontainer
2. **DevPod**: Users can [launch devcontainers locally or on AWS](#option-1-devcontainer-on-your-laptops) using the prebuilt image, so they don't have to wait for the image to build from scratch—since CI/CD has already built it

To avoid long build times on every commit to main or a PR branch, we use a **two-tier caching strategy:**

1. **Image caching**: If `.devcontainer/Dockerfile`, `pyproject.toml`, `uv.lock`, and `DESCRIPTION` haven't changed, the devcontainer image build is skipped, and the most recent image (in GHCR) is reused (~30 seconds)
2. **Layer caching**: If any of these files changed, the image is rebuilt, but only affected layers rebuild while the others are pulled from GHCR cache (incremental builds, ~2-5 minutes)

Once built, the AMD and ARM versions of the image is pushed to [GHCR](https://github.com/switchbox-data/reports2/pkgs/container/reports2)**, where the AMD version is immediately available as `ghcr.io/switchbox-data/reports2:latest`.

The quality-checks and tests jobs then **pull the prebuilt AMD image** and run `just check` and `just test` inside it.

**Bottom line**: Every commit that modifies the devcontainer or dependencies triggers an automatic devcontainer image build. This ensures CI uses the correct environment, and anyone (including Devpod users) can use the fully built devcontainer (on both AMD and ARM computers) without building it from scratch.

### Why CI/CD matters

- **Code quality**: Every PR must pass all code quality checks and tests before it can be merged
- **Safety net**: Even if someone skips code quality pre-commit checks locally, CI catches code quality issues before they are merged to main
- **Perfect Consistency**: CI literally runs `just check` and `just test` inside of the devcontainer - exactly what you run locally — and devcontainer is rebuilt when its definition changes
- **Speed**: Devcontainer is only rebuilt when necessary, so quality checks and tests usually run immediately, and they run in parallel, making CI faster

You can see the workflow configuration in `.github/workflows/data-science-main.yml`.

## 🧹 Cleaning Up

Remove generated files and caches:

```bash
just clean
```

This removes:

- `.pytest_cache`
- `.ruff_cache`
- `tmp/`
- `notebooks/.quarto`

## 📚 Additional Resources

### Development Environment

- [Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [just Documentation](https://just.systems/)
- [Quarto Documentation](https://quarto.org/)
- [prek Documentation](https://github.com/j178/prek) - Pre-commit hook manager

### Python Tools

- [uv Documentation](https://docs.astral.sh/uv/) - Package manager
- [ruff Documentation](https://docs.astral.sh/ruff/) - Linter and formatter
- [ty Documentation](https://docs.astral.sh/ty/) - Type checker
- [deptry Documentation](https://github.com/fpgmaas/deptry) - Dependency checker
- [Polars Documentation](https://pola.rs/) - Fast DataFrame library
- [PyArrow Documentation](https://arrow.apache.org/docs/python/) - Python bindings for Apache Arrow

### R Tools

- [pak Documentation](https://pak.r-lib.org/) - Package manager
- [air Documentation](https://docs.posit.dev/air/) - Linter and formatter
- [dplyr Documentation](https://dplyr.tidyverse.org/) - Data manipulation grammar
- [arrow Documentation](https://arrow.apache.org/docs/r/) - R bindings for Apache Arrow
