# Project Conventions

## Repo Structure

- Monorepo with multiple report projects under `reports/<project_code>/`
- Shared libraries in `lib/`
- Python tests in `tests/`
- Published HTML reports in `docs/` (committed to main, served via GitHub Pages)
- Data lives on S3 (`s3://data.sb/`), never committed to git

## Language Preferences

- **Python (polars)**: Default choice for data analysis, data engineering, fetch scripts, numerical simulations
- **R (tidyverse)**: Acceptable for visualization or when R libraries are specifically needed
- Do NOT use pandas for analysis; use polars with lazy evaluation
- In R, prefer arrow lazy datasets; only `collect()` to tibble when a library requires it

## Task Runner

- Use `just` for all commands (defined in root `Justfile` and per-report `Justfile`s)
- `just check` — lint, format, type-check (ruff, ty, prek hooks)
- `just test` — run pytest with doctests
- `just render` — render a Quarto report (run from report directory)
- `just clean` — remove caches and generated files

## Code Quality (required before every commit)

- Run `just check` — no linter errors, no type errors, no warnings
- Run `just test` — all tests pass; write tests for new Python functionality
- Pre-commit hooks enforce: ruff-check, ruff-format, ty-check, trailing whitespace,
  end-of-file newline, YAML/JSON/TOML validation, no large files (>600KB),
  no merge conflict markers

## Commits

- Atomic: one logical change per commit
- Message format: imperative verb, <50 char summary (e.g., "Add winter peak analysis")
- WIP commits prefixed with `WIP:`

## Branches and PRs

- PR title MUST start with `[project_code]` (e.g., `[ny_aeba] Add peak analysis`)
  — this becomes the squash-merge commit message on main
- Create PRs early (draft is fine)
- PRs should merge within the sprint; break large work into smaller PRs
- Delete branches after merging

## Report Structure (Quarto)

- Each report: `reports/<project_code>/`
  - `index.qmd` — narrative report (text + embedded charts)
  - `notebooks/analysis.qmd` — data analysis (prefer single notebook)
  - `_quarto.yml` — Quarto config
  - `docs/` — rendered output (gitignored in report dirs)
- Data flows from `notebooks/analysis.qmd` → `index.qmd` via:
  - R: `save()`/`load()` for variables
  - Quarto `{{< embed >}}` for charts
- Render with `just render` from the report directory

## Data Conventions (S3)

- Path format: `s3://data.sb/<org>/<dataset>/<filename_YYYYMMDD.parquet>`
- Prefer Parquet format
- Filenames: lowercase with underscores, end with `_YYYYMMDD` (download date)
- Use lazy evaluation (polars `scan_parquet` / arrow `open_dataset`) and filter before collecting

## Dependencies

- Python: `uv add <package>` (updates pyproject.toml + uv.lock); never use `pip install`
- R: add to `DESCRIPTION` Imports, then `just install`
- Commit lock files (uv.lock) and DESCRIPTION when adding dependencies

## Report Naming

- Format: `state_topic` (e.g., `ny_aeba`, `ri_hp_rates`)
- Reuse existing topic names across states for consistency

## MCP Tools

### Context7

When writing or modifying code that uses a library, use the Context7 MCP server to fetch
up-to-date documentation for that library. Do not rely on training data for API signatures,
function arguments, or usage patterns — always resolve against Context7 first.

### Linear

When a task involves creating, updating, or referencing issues, use the Linear MCP server
to interact with our Linear workspace directly. See the ticket conventions below.

## New Issue Checklist

All work is tracked with Linear issues (which sync to GitHub Issues automatically).
When asked to create or update a ticket, use the Linear MCP tools.
Every new issue MUST satisfy all of the following before it is created:

- [ ] **Type** is one of: **Code** (delivered via commits/PRs), **Research** (starts with
      a question, findings documented in issue comments), or **Other** (proposals, graphics,
      coordination — deliverables vary).
- [ ] **Title** follows the format `[project_code] Brief description`
      (e.g., `[ny_aeba] Add winter peak analysis`).
- [ ] **What** is filled in: a concise, high-level description of what is being built,
      changed, or decided. Anyone should be able to understand the scope at a glance.
- [ ] **Why** is filled in: context, importance, and value — why this matters, what
      problem it solves, and what it unblocks.
- [ ] **How** is filled in (skip only when the What is self-explanatory and
      implementation is trivial):
  - For Code issues: numbered implementation steps, trade-offs, dependencies.
  - For Research issues: background context, options to consider, evaluation criteria.
- [ ] **Deliverables** lists concrete, verifiable outputs that define "done":
  - Code: "PR that adds …", "Tests for …", "Updated `data/` directory with …"
  - Research: "Comment in this issue documenting … with rationale and sources"
  - Other: "Google Doc at …", "Slide deck for …", link to external deliverable
  - Never vague ("Finish the analysis") or unmeasurable ("Make it better").
- [ ] **Project** is set and matches the report directory name in `reports/`
      (e.g., `ny_aeba`).
- [ ] **Status** is set. Default to **Backlog**. Options: Backlog, To Do, In Progress,
      Under Review, Done.
- [ ] **Milestone** is set when one applies (strongly encouraged — milestones are how we
      track progress toward major goals).
- [ ] **Assignee** is set if the person doing the work is known.
- [ ] **Priority** is set when urgency/importance is clear.

### Status Transitions

Keep status updated as work progresses — this is critical for team visibility:

- **Backlog** → **To Do**: Picked for the current sprint
- **To Do** → **In Progress**: Work has started (branch created for code issues)
- **In Progress** → **Under Review**: PR ready for review, or findings documented
- **Under Review** → **Done**: PR merged (auto-closes), or reviewer approves and closes
