# Contributing to Switchbox Reports

This guide explains Switchbox's internal development workflow. We follow a structured process to ensure all work is tracked, tickets are clear, PRs don't grow stale, and code quality remains high.

We use [Linear](https://linear.app/) for issue management, which automatically syncs to GitHub Issues for public transparency. Create and manage issues in Linear, then work with branches and PRs in GitHub.

### How Linear and GitHub Work Together

- **Issues**: Created and managed in Linear, automatically sync to GitHub (public)
- **Branches**: Created from GitHub issues
- **Pull Requests**: Created and reviewed on GitHub (public)
- **Status updates**: Updates in Linear sync to GitHub automatically
- **Closing**: Merging a PR closes issues in both Linear and GitHub

**What's Public**: All issues, PRs, and code are publicly visible on GitHub. Private information (Project, Milestone fields) stays in Linear only.

## 📋 Table of Contents

- [Types of Issues](#types-of-issues)
- [Getting Started](#getting-started)
- [Doing the Work](#doing-the-work)
- [Getting Review](#getting-review)
- [Wrapping Up](#wrapping-up)
- [Quick Reference](#quick-reference)
- [Need Help?](#need-help)

---

## 🎫 Types of Issues

**All work is tracked with issues, no exceptions.** We use issues for three main types of work:

### 1. 💻 Code
Any report-related task delivered via commits and pull requests.

**Examples**:
- Data engineering (fetching, cleaning, processing data)
- Data analysis (statistical modeling, calculations)
- Report writing (Quarto notebooks, visualizations)
- Infrastructure improvements (CI/CD, tooling)

**Deliverables**: Code in a PR, tests, documentation

**Workflow**: Issues → Branches → Commits → PRs → Review → Merge

### 2. 📚 Research
Work that requires investigation, reading, or conceptual thinking to advance a project.

All Research issue started with a **question**.

**Examples**:
- Reading academic papers or technical reports
- Reviewing regulatory dockets or policy documents
- Thinking through methodological approaches
- Investigating data sources or APIs
- Evaluating technical options

**Deliverables**: Comments on the issue that:
- Answer a research question
- Summarize findings or key insights
- Provide recommendations
- Document decisions with rationale

**Public visibility**: 📚 Research findings are publicly visible on GitHub - they provide valuable context that helps others understand our methodology and decision-making.

**Workflow**: Issues → Research → Document findings in issue comments (public) → Close issue

### 3. 📋 Other
Any other project-related tasks that aren't 💻 Code or 📚 Research.

**Examples**:
- Writing grant proposals or project plans
- Producing graphics for presentations
- Preparing report releases and announcements
- Coordinating with external partners
- Internal project management tasks

**Deliverables**: Varies - Google Docs, slide decks, published announcements, coordinated events, etc.

**Public visibility**: These issues are visible on GitHub, though external deliverables (like Google Docs) may be private.

**Workflow**: Issues → Do the work → Document deliverables in issue → Close issue

---

**Note**: The sections on branches, PRs, commits, and code review primarily apply to **💻 Code** issues. 📚 Research and 📋 Other issues follow a simpler workflow focused on documenting outputs.

---

## 🚀 Getting Started

### Viewing Issues and Work

Use our private [Linear workspace](https://linear.app/switchbox-data) to view and manage issues. Linear provides our Kanban board and project tracking.

**Public View**: All issues are also visible on [GitHub Issues](https://github.com/switchbox-data/reports2/issues) for transparency.

**Issue Statuses**:
- 📋 **Backlog**: Issues for future sprints
- ⭕ **To Do**: Issues for the current sprint
- 🔄 **In Progress**: Currently being worked on
- 👀 **Under Review**: Needs or is undergoing review
- ✅ **Done**: Closed (merged PR or completed manually for non-code tasks)

🚨 **IMPORTANT**: Keep your issue statuses updated as you progress through these stages! This is critical for team visibility and project tracking. Update the status in Linear whenever you move between stages - it syncs to GitHub automatically for public transparency.

### Creating an Issue

1. Open the [Linear workspace](https://linear.app/switchbox-data)
2. Create a new issue
3. Fill out all required fields (see below)
4. The issue will automatically sync to GitHub for public visibility

### Issue Fields (Switchbox Team)

All fields below are **required** except **Priority** and **How** (when trivial). These fields apply to **all issue types** (💻 Code, 📚 Research, and 📋 Other).

#### Title
**Format**: `[project_code] Brief description` (e.g., `[ny_aeba] Add winter peak analysis`)

Short, scannable summary of the issue.

#### What
**Purpose**: Answer "what is this even about?"

High-level description of what you're building, changing, or deciding. Keep it concise but clear enough that anyone can understand the scope at a glance.

**Example**: "Add winter peak demand forecast visualizations to the NY AEBA report"

#### Why
**Purpose**: Explain context, importance, and value

This is where you justify the work. Answer:
- Why is this important?
- What value does it deliver, or what problem does it solve?
- What will it enable or unblock?

**Example**: "Winter peak demand is a critical metric for grid planning. Adding these visualizations will help policymakers understand the impact of building electrification on winter grid capacity, which is essential for infrastructure planning decisions."

#### How (optional when trivial)
**Purpose**: Provide implementation details or discussion context

**For tech/manual tasks**: Enumerate the steps
- Break down complex work into smaller steps
- Identify technical decisions or trade-offs
- List dependencies or prerequisites

**For decision/discussion issues**: Provide context and framing
- Background information needed for the decision
- Options to consider
- Criteria for evaluation
- Stakeholders to consult

**When to skip**: If the "what" is self-explanatory and the implementation is straightforward, you can leave this blank.

**Example (💻 Code issue)**:
```
1. Create new notebook: notebooks/winter_peak_forecast.qmd
2. Load hourly demand data from S3
3. Calculate peak demand by season and scenario
4. Create line chart with confidence intervals
5. Embed chart in index.qmd using {{< embed >}} syntax
```

**Example (📚 Research issue requiring discussion)**:
```
We need to decide whether to use ASHRAE climate zones or IECC climate zones
for categorizing building performance. ASHRAE is more granular (8 zones) but
IECC is more commonly used in policy (3 zones). Consider: audience familiarity,
data availability, and alignment with other reports.
```

#### Deliverables
**Purpose**: Define specific, verifiable outputs

🎯 **CRITICAL**: List concrete deliverables as specifically as possible. This defines "done."

**Why this matters**: Clear deliverables are essential for async remote work. They let anyone know:
- ✅ Exactly when the issue is complete
- 🔍 Exactly what to look for when reviewing
- 🚫 Without specific deliverables, teammates get blocked and have to ping you with questions instead of moving forward independently

**Examples**:
- ✅ "PR that adds winter peak forecast visualization to NY AEBA report"
- ✅ "Tests for peak demand calculation function"
- ✅ "Comment in this issue documenting our climate zone decision with rationale"
- ✅ "Google Doc at `Projects/ny_aeba/paperwork` that containers our proposal"
- ✅ "Updated `data/` directory with cleaned NYC building dataset"
- ❌ "Finish the analysis" (too vague)
- ❌ "Make it better" (not measurable)

#### Assignee
**Required**: No

Person responsible for the work. Select in Linear; automatically syncs with GitHub username.

Fill in if possible, only leave blank if the person doing the work isn't known yet.

#### Status
**Required**: Yes

Current state of the issue. Options:
- **Backlog**: Future work
- **To Do**: Current sprint
- **In Progress**: Actively working
- **Under Review**: Awaiting or in review
- **Done**: Complete

Defaults to **Backlog**. Status syncs to GitHub automatically.

#### Priority
**Required**: No (not currently enforced)

Indicates urgency/importance. Use to help prioritize work.

#### Project
**Required**: Yes

The Linear project this issue belongs to.

**For reports repo**: Should match the project directory name in `reports/` (e.g., "ny_aeba" for `reports/ny_aeba_grid/`)

**Note**: This field is visible in Linear but not synced to GitHub.

#### Milestone
**Required**: When applicable (strongly encouraged)

Internal project management milestone this work contributes to.

Milestones group related issues across projects (e.g., "Q1 2025 Reports Launch", "Data Infrastructure v2").

🗺️ **Why milestones matter**: Milestones are our X-ray of the project. They let us:
- 📊 See the big pieces we need to complete and by when
- 🔍 See the details of what's needed to achieve the milestone (by viewing associated issues)
- 🧭 Make sense of a pile of issues by organizing them around major goals
- 📈 Track progress toward the milestone at a glance

**Associate issues with milestones whenever possible** - it's critical for planning and visibility.

**Note**: This field is visible in Linear but not synced to GitHub.

### What's Publicly Visible on GitHub

When issues sync to GitHub, the public can see:
- Title
- What, Why, How, Deliverables (in issue description)
- Assignee
- Status
- Labels
- Issue type (💻 Code, 📚 Research, or 📋 Other)
- **For 📚 Research issues**: Comments with findings and sources (valuable for transparency)
- **For 💻 Code issues**: Linked branches, PRs, and all code changes

**Not visible on GitHub** (Linear-only):
- Project field
- Milestone field
- Internal Linear discussions

### Requesting Issue Review (Optional)

Sometimes, we assign an issue to someone without specifying exactly **How** they're going to do the work, or what they're going to **Deliver**. The assignee is responsible for figuring these things out and updating the ticket.

Occasionally, the **How** and **Deliverables** will need review before they get to work—spending days working on the wrong thing is much less efficient than ask for a review!

In these cases, if your issue needs review before starting work:

1. Assign a reviewer in Linear
2. Update status to reflect it needs review
3. Notify them on Slack in the relevant project channel
4. Get review
5. Update the issue as needed
6. Start work

### Starting Work

Once your ready to get started working on the issue:

**For 💻 Code Issues**:

1. **Create a branch from the GitHub issue**:
   - 💡 **Note**: Branch creation happens in GitHub, not Linear
   - Go to the synced issue on [GitHub](https://github.com/switchbox-data/reports2/issues)
   - Find **Development** on the right sidebar
   - Click **Create a branch**
   - This will automatically generate a branch name, based on the issue title
   - This also automatically links the branch to the issue

2. **Update status in Linear**:
   - Drag the issue from `To Do` to `In Progress`
   - Status syncs to GitHub automatically (publicly visible)

3. **Pull the branch locally** and start working:
   ```bash
   git fetch origin
   git checkout <branch-name>
   ```

**For 📚 Research & 📋 Other Issues**:

1. **Update status to `In Progress`** in Linear (syncs to GitHub)

2. **Start working** - no branch needed, just begin your research or task

---

## 💻 Doing the Work

This section covers workflows for different issue types.

### For 💻 Code Issues: Create a PR Early

_**This section applies to 💻 Code issues only.** 📚 Research and 📋 Other issues don't use branches or PRs._

**After your first commit**, immediately create a Pull Request:

1. Push your branch and open a PR on GitHub
2. **Title**: 🚨 **CRITICAL** - Must start with `[project_code]` (just copy from the linked issue's title, which should include this)
   - **Why**: When the PR is squashed and merged to main, the PR title becomes the merge commit message
   - **Impact**: Since `reports2` contains many projects, this tagging is essential for making sense of commit history on main
   - **Example**: `[ny_aeba] Add winter peak demand analysis`
   - ✅ This lets anyone read the commit history and immediately know: "This commit is about the ny_aeba project"
3. **Description**: Add any context _not in the issue_:
   - Implementation decisions you made
   - Trade-offs or alternatives considered
   - Anything that might not be obvious to reviewers

**Why create PRs early?**
- Makes work-in-progress visible to the team
- Allows for early feedback if direction needs adjustment
- Shows activity even if work isn't complete
- PRs stay in draft status until you request review

**Note**: The linked issue will **auto-close** when the PR is merged.

#### Pre-Commit Checklist (💻 Code Issues Only)

Before committing changes to 💻 Code issues, ensure these three standards are met:

**1. ✨ Code Quality**

**Why this matters**: Keeping the codebase clean keeps the team productive. Clean, well-formatted code is easier to read, review, and maintain.

Run quality checks:

```bash
just check
```

**Requirements**:
- ✅ No linter errors or warnings
- ✅ All checks must pass (green)

🔒 **Automatic enforcement**: Pre-commit hooks will block commits that don't pass quality checks. See the [README](README.md) for details.

**2. ✅ Tests**

**Why this matters**: Tests ensure our reports are correct. Testing must happen continuously as you develop (not at the end) through automated tests and code review (see below).

Run tests:

```bash
just test
```

**Requirements**:
- ✅ Write tests for new functionality in the `tests/` directory
- ✅ All tests must pass

**3. 🔄 Reproducibility**

**Why this matters**: Reproducibility ensures:
1. 👥 Other team members can use and build on your work
2. ⏰ We (and you!) can use this in 6 months
3. 🌍 Anyone external can run and build off our work

**For reports**: Ensure the report renders successfully and reproducibly:

```bash
# Clear cache and render report (run from report directory)
just render
```

**Requirements**:
- ✅ All data is pulled from S3 (see [README](README.md) for S3 data conventions)
- ✅ No reliance on local files in `data/` or `cache/` that others won't have (unless generated by the notebooks as part of the reproducible process)
- ✅ Report renders without errors

#### Making Commits (💻 Code Issues Only)

Here are best practices for commits.

**Keep commits atomic**:
- Small, focused commits are easier to review
- Each commit should represent one logical change
- [Read more about atomic commits](https://dev.to/samuelfaure/how-atomic-git-commits-dramatically-increased-my-productivity-and-will-increase-yours-too-4a84)

**Write good commit messages**:
- Start with a verb, using the imperative ("Add feature" not "Added feature")
- First line: concise summary (<50 characters)
- Blank line, then detailed explanation if needed
- [Read more about commit messages](https://cbea.ms/git-commit/)

**Commit frequently**:
- Commit at least once per work session
- If work is incomplete, prefix message with `WIP: `
- Example: `WIP: Add data loading logic`
- 🚨 **VERY IMPORTANT**: Push your commits regularly! If you don't commit and push frequently, nobody else can see what you've worked on. This blocks teammates who might be waiting on your work or need to coordinate with you.

**Keep PRs short-lived**:
- PRs should be merged _within the sprint_
- If dragging on, the scope is probably too large
- Consider breaking into smaller PRs

### For 📚 Research Issues: Document Your Findings

📚 Research issues don't require branches or PRs. Instead, document your findings directly in the issue as comments.

**Why we document in issue comments**: This creates a public archive of what we're learning and why we made certain decisions. Future readers (including your future self) can understand our reasoning and methodology.

**Write self-contained documentation**: Document findings to a high standard with all context necessary to understand the issue standalone. This serves three critical purposes:
1. 🚫 **Unblocks reviewers** - they don't need to ping you for clarification
2. ⏰ **Future understanding** - you and the team can understand it in 6 months
3. 🌍 **External transparency** - anyone outside can follow our thinking and methodology

**As you work**:
1. **Update status in Linear** regularly (syncs to GitHub - publicly visible)
3. **Cite sources** - link to papers, documents, or data sources

**When complete**:
1. **Write a summary comment** that includes:
   - **Answer to the original question**: high level answer that summarizes learnings, or proposes recommendation
   - **Rationale** (if applicable) - if answer is a recommendation, argument or evidence in support
   - **Key findings** (if applicable) - if answer is summarizing learnings, a deeper expalantion of we learned?
   - **Implications** (if applicable) - what should we do differently based on this information?
   - **Sources cited** - links to all materials reviewed

2. **Tag relevant team members** who need to see the findings and **Move to "Under Review"**

4. **Close the issue** reviewers close the issue once they have reviewed and commented

**Example 1: Research question that requires a decision**:
```
**Question**: Should we use ASHRAE or IECC climate zones?

**Answer**: Use IECC climate zones (3 zones)

**Rationale**:
- IECC zones are standard in building energy codes and policy
- Our audience (policymakers) is more familiar with IECC
- ResStock data is already categorized by IECC zones
- ASHRAE's 8 zones would require data transformation with no clear benefit

**Sources**:
- IECC 2021 Climate Zone Map: https://...
- ResStock documentation: https://...
- Conversation with [Name] on [date]
```

**Example 2: Research question about understanding a paper**:
```
**Question**: What are the key takeaways from "Cold Climate Air Source Heat Pump
Performance" (Metzger et al., 2023)?

**Answer**: Modern air-source heat pumps perform significantly better in cold climates
than older models, but performance varies substantially based on temperature and backup
heat configuration. This has important implications for how we model ASHP performance.

**Key Findings**:
- Modern ASHPs maintain 200%+ COP down to -15°F (vs. 150% in older models)
- Performance degradation is primarily due to defrost cycling, not compressor efficiency
- Backup resistance heat engagement varies significantly by thermostat configuration:
  - Dual-fuel setups: backup at 25-35°F
  - Heat pump-only: backup only at equipment limits (-15 to -20°F)
- Field performance matches lab ratings within 10% for temps above 5°F

**Implications**:
- We should model ASHP performance using temperature-dependent COP curves, not fixed values
- Thermostat/backup heat strategy is a critical modeling parameter
- Our current assumption of 250% average COP may overestimate cold-climate performance

**Sources**:
- Metzger, I., et al. (2023). "Cold Climate Air Source Heat Pump Performance"
  https://doi.org/10.1016/j.energy.2023.xxxxx
- Supplementary data files: https://...
```

### For 📋 Other Issues: Document Deliverables

**As you work**:
1. **Update status in Linear** regularly (syncs to GitHub)
2. **Communicate** about blockers or dependencies via Slack

**When complete**:
1. **Document deliverables** in the issue (publicly visible on GitHub):
   - Link to final Google Docs, slides, or other materials
   - 💡 **Note**: Many of these deliverables will be internal/private (Google Drive docs, internal slides, etc.)


---

## 👀 Getting Review

### Code Review (💻 Code Issues Only)

#### Preparing for Code Review
Before requesting review:

1. **Resolve merge conflicts**:
   ```bash
   git fetch origin main
   git merge origin/main
   # Resolve any conflicts
   git push
   ```

2. **Ensure all checks pass**:
   - ✅ All CI checks are green
   - ✅ No test failures
   - ✅ No linting errors

3. **Update status**:
   - In Linear, move issue from `In Progress` to `Under Review` (syncs to GitHub)

4. **Request review**:
   - Select a **Reviewer** on the GitHub PR
   - Notify them on Slack in the relevant channel

#### Code Review Process

1. **Reviewer examines the PR**:
   - Checks code quality, logic, and adherence to standards
   - Tests functionality if needed
   - Leaves comments and/or requests changes

2. **Address feedback**:
   - Make requested changes
   - Push new commits to the same branch
   - Respond to comments
   - Notify reviewer on Slack

3. **Iterate if needed**:
   - Process may repeat 1-2 times
   - Stay responsive to keep the PR moving

### Peer Review (📚 Research & 📋 Other Issues)

Most 📚 Research Issues must be reviewed (the point is to learn or decide something, and usually to disseminate it).
Only some 📋 Other Issues need review. Use your judgement.

For these deliverables:

1. **Update status**: Move issue to `Under Review` in Linear (syncs to GitHub)
2. **Request review**: Assign reviewer in Linear and notify on Slack
3. **Implement feedback** and notify reviewer
4. **Iterate** as needed

## 🎯 Wrapping Up
### Merging and Closing

**For 💻 Code Issues** - Once the PR is approved:

1. **Merge to main**:
   - Use GitHub's interface to merge (not terminal!)
   - Choose "Squash and merge" or "Create a merge commit" based on team preference
   - This automatically closes the linked GitHub issue

2. **Delete the branch**:
   - GitHub will prompt you to delete the branch after merging
   - Click **Delete branch** to keep the repository tidy
   - ⚠️ **Important**: Always delete merged branches! Otherwise you'll end up with dozens of stale branches cluttering the repository

3. **Issue closes automaticalli**:
   - GitHub issue closes automatically
   - Linear issue status syncs to `Done` automatically

**For 📚 Research & 📋 Other Issues** - Once deliverables are complete and reviewed:

1. **Close the issue manually**:
   - Move status to `Done` in Linear (syncs to GitHub)


---


## 🎯 Quick Reference

**💻 Code Issue Lifecycle**:
```
Create Issue (Linear) → Syncs to GitHub (public) → [Optional: Issue Review] →
Create Branch (GitHub) → Move to In Progress (Linear) →
Do Work → Commit & Push Regularly → Create PR (GitHub) → Code Review →
Merge to Main (GitHub) → Issue Auto-Closes (Linear + GitHub) → Delete Branch ⚠️
```

**📚 Research Issue Lifecycle**:
```
Create Issue (Linear) → Syncs to GitHub (public) → [Optional: Issue Review] →
Move to In Progress → Do Research → Document Findings in Issue (public) →
Peer Review (required for most) → Close Issue Manually
```

**📋 Other Issue Lifecycle**:
```
Create Issue (Linear) → Syncs to GitHub (public) → [Optional: Issue Review] →
Move to In Progress → Do Work → Document Deliverables in Issue →
Peer Review (only if needed) → Close Issue Manually
```

---

## 🎯 Quick Reference

### 🚨 Critical Reminders (Don't Skip These!)

- 🚨 **Update issue status** regularly in Linear (critical for team visibility!)
- 🚨 **Commit & push frequently** (teammates can't see your work otherwise!)
- 🚨 **Delete branches after merging** (avoid clutter!)
- 🎯 **Specific deliverables** in issues (unblocks async work!)
- 📊 **Associate issues with milestones** (project X-ray!)

### Before Every Commit (💻 Code Issues)

- ✨ **Quality**: `just check` (enforced by pre-commit hooks 🔒)
- ✅ **Tests**: `just test` + write tests for new functionality
- 🔄 **Reproducibility** (reports only): `just render` (ensure report renders without errors)

### Before Requesting Code Review (💻 Code Issues)

- ✅ No merge conflicts
- ✅ All CI checks passing (GitHub Actions)
- ✅ Tests written for new functionality
- ✅ Issue status updated to "Under Review" in Linear
- ✅ PR title starts with `[project_code]` 🚨

### Before Requesting Peer Review (📚 Research / 📋 Other Issues)

- ✅ Findings/deliverables documented in issue (self-contained, high standard)
- ✅ Relevant links and sources included
- ✅ Issue status updated to "Under Review" in Linear

### Best Practices by Issue Type

**For 💻 Code Issues**:
- **Start with small PRs** - easier to review, faster to merge
- **Commit & push frequently** - don't lose work, make progress visible, unblock teammates
- **Test in a clean environment** - catches reproducibility issues early
- **Keep PRs short-lived** - merge within the sprint

**For 📚 Research Issues**:
- **Document as you go** - add interim findings as comments (publicly visible)
- **Cite your sources** - link to papers, docs, or conversations
- **Write self-contained summaries** - high standard with full context (unblocks reviewers, helps future readers)
- **Be transparent** - research is public, share your thinking and reasoning

**For All Issue Types** (💻📚📋):
- **Communicate blockers** - team can help unblock you via Slack
- **Review the issue before starting** - make sure you understand the "why"
- **Keep status updated in Linear** (syncs to GitHub for public visibility)
- **Update regularly** - weekly progress updates at minimum
- **Ask questions early** - don't spin your wheels alone

---

## 🆘 Need Help?

- **Slack**: Ask in the relevant project channel
- **Stuck on a review?** Ping your reviewer directly
- **Technical blockers?** Schedule a pairing session
- **Process questions?** Ask in #engineering
- **Public questions?** Comment on the GitHub issue (publicly visible)

Remember: This workflow exists to help us ship quality work efficiently. If something isn't working, let's discuss and improve it!
