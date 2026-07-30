# 🛠️ LeetSync Automated Documentation & Portfolio Setup Guide

This guide explains how the non-intrusive documentation automation works alongside **LeetSync**, how to configure your GitHub repository, and how to troubleshoot common setup scenarios.

---

## 🏗️ Repository Architecture & ASCII Mockups

### 1. Initial State (LeetSync Only)
When LeetSync syncs solutions from LeetCode, it pushes problem folders directly into the repository root:

```
leetcode-solutions/
├── 1-two-sum/
│   ├── README.md
│   └── two-sum.java
├── 2-add-two-numbers/
│   ├── README.md
│   └── add-two-numbers.java
├── 20-valid-parentheses/
│   ├── README.md
│   └── valid-parentheses.java
└── 347-top-k-frequent-elements/
    ├── README.md
    └── top-k-frequent-elements.java
```

> [!IMPORTANT]
> **LeetSync Integrity Guarantee**: The automation **NEVER** moves, renames, or deletes any solution folders or files inside `<id>-<slug>/`. All problem folders remain exactly where LeetSync expects them.

---

### 2. Automated State (After GitHub Actions Runs)
Upon receiving a push, the GitHub Actions workflow runs Python scripts to generate root documentation, pattern pages, statistics, and metadata cache:

```
leetcode-solutions/
├── .cache/
│   └── leetcode_cache.json              <-- Caches LeetCode API metadata
├── .github/
│   └── workflows/
│       └── update-index.yml             <-- Automated GitHub Actions workflow
├── docs/
│   ├── Arrays.md                        <-- Topic pattern page
│   ├── Backtracking.md
│   ├── BinarySearch.md
│   ├── BST.md
│   ├── DynamicProgramming.md
│   ├── Easy.md                          <-- Difficulty filter page
│   ├── Graph.md
│   ├── HashMap.md
│   ├── Hard.md
│   ├── Medium.md
│   ├── SlidingWindow.md
│   ├── Strings.md
│   ├── TwoPointers.md
│   └── ... (25+ topic pages)
├── scripts/
│   ├── common.py                        <-- Core scanner & API client
│   ├── generate_patterns.py             <-- docs/ builder
│   ├── generate_readme.py               <-- README.md portfolio builder
│   ├── generate_stats.py                <-- stats/ analytics builder
│   ├── run_all.py                       <-- Master pipeline runner
│   └── requirements.txt                 <-- Python dependencies
├── stats/
│   └── progress.md                      <-- Mermaid charts & timeline analytics
├── 1-two-sum/                           <-- Solution folder (UNTOUCHED)
├── 2-add-two-numbers/                   <-- Solution folder (UNTOUCHED)
├── SETUP.md                             <-- Setup documentation
└── README.md                            <-- Master portfolio dashboard
```

---

## 🔄 How LeetSync & The Automation Work Together

```
┌─────────────────┐       Push Solution      ┌─────────────────────────┐
│  LeetCode.com   │ ───────────────────────> │  GitHub Repository      │
└─────────────────┘       (LeetSync)         └────────────┬────────────┘
                                                          │
                                                    Triggers Workflow
                                                          │
                                                          ▼
                                             ┌─────────────────────────┐
                                             │ GitHub Actions Workflow │
                                             └────────────┬────────────┘
                                                          │
                                                 Runs python scripts/
                                                          │
                                                          ▼
                                             ┌─────────────────────────┐
                                             │ Updates README.md       │
                                             │ Updates docs/*.md       │
                                             │ Updates stats/          │
                                             └─────────────────────────┘
```

1. **LeetSync Action**: You solve a problem on LeetCode. The LeetSync Chrome extension / GitHub integration pushes the solution code and problem `README.md` into `<id>-<slug>/`.
2. **Push Event Trigger**: The push to `main` triggers `.github/workflows/update-index.yml`.
3. **Metadata Resolution**: `scripts/common.py` checks `.cache/leetcode_cache.json`. If missing, it queries the LeetCode GraphQL API for difficulty and topic tags.
4. **Documentation Regeneration**: `generate_readme.py`, `generate_patterns.py`, and `generate_stats.py` update `README.md`, `docs/*.md`, and `stats/progress.md`.
5. **Auto Commit**: The workflow commits and pushes the updated documentation files with `[skip ci]` to prevent infinite workflow loops.

---

## 🚀 Setup & Installation Instructions

### Step 1: Enable GitHub Actions Permissions
For the workflow to push generated documentation back to your repository:

1. Navigate to your repository on GitHub.
2. Go to **Settings** > **Actions** > **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests**.
6. Click **Save**.

---

### Step 2: (Optional) Personal Access Token (PAT)
If your repository rules enforce branch protection or require explicit authentication:

1. Go to GitHub **Settings** > **Developer Settings** > **Personal Access Tokens** > **Tokens (classic)**.
2. Generate a new token with `repo` scope.
3. In your repository, go to **Settings** > **Secrets and variables** > **Actions**.
4. Click **New repository secret**.
5. Name: `PAT_TOKEN`, Value: `<your-token>`.
6. Update `.github/workflows/update-index.yml` token line to: `token: ${{ secrets.PAT_TOKEN }}`.

*(Note: Default `GITHUB_TOKEN` works automatically out of the box for standard repositories!)*

---

### Step 3: Test Locally (Optional)
You can run the documentation generator on your local machine anytime:

```bash
# Install dependencies
pip install -r scripts/requirements.txt

# Run full documentation pipeline
python scripts/run_all.py
```

---

## ❓ Troubleshooting & Common Issues

### Issue 1: GitHub Actions failed with "Permission Denied" during push
- **Cause**: Workflow permissions are set to Read-Only by default.
- **Solution**: Follow **Step 1** above to set Workflow Permissions to **Read and write permissions**.

### Issue 2: Workflow is triggering infinite loops
- **Cause**: The workflow push triggers another workflow push.
- **Solution**: The workflow includes `[skip ci]` in the commit message and specifies `paths-ignore` for `README.md`, `docs/**`, and `stats/**`. Ensure these settings remain intact in `.github/workflows/update-index.yml`.

### Issue 3: Problem folders are not recognized
- **Cause**: Folder name does not follow `<id>-<slug>` format (e.g. `1-two-sum`).
- **Solution**: LeetSync automatically creates folders in `<id>-<slug>` format. Ensure folder names match the pattern `^(\d+)-(.+)$`.

### Issue 4: LeetCode API Rate Limits / Failure
- **Cause**: Network issues or temporary LeetCode API throttling.
- **Solution**: The generator includes retry logic, local HTML fallback parsing from local problem `README.md`, and caches all successful responses in `.cache/leetcode_cache.json`.
