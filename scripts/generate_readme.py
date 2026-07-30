"""
generate_readme.py - Generates the root portfolio README.md file.
"""

import os
from typing import List, Dict
from common import ProblemInfo, TAG_TO_DOC_NAME, REQUIRED_PATTERNS, logger

def generate_progress_bar(solved: int, total_goal: int = 3500, length: int = 25) -> str:
    """Generates a text-based progress bar."""
    pct = (solved / total_goal) * 100 if total_goal > 0 else 0
    filled = int(round(length * solved / total_goal))
    bar = "█" * filled + "░" * (length - filled)
    return f"`[{bar}] {solved}/{total_goal} ({pct:.1f}%)`"

def build_readme_content(problems: List[ProblemInfo]) -> str:
    """Constructs the complete README.md content."""
    total_solved = len(problems)
    easy_count = sum(1 for p in problems if p.difficulty == "Easy")
    medium_count = sum(1 for p in problems if p.difficulty == "Medium")
    hard_count = sum(1 for p in problems if p.difficulty == "Hard")

    # Map problem tags to doc pattern names
    pattern_counts: Dict[str, int] = {p: 0 for p in REQUIRED_PATTERNS}
    for p in problems:
        for tag in p.tags:
            doc_name = TAG_TO_DOC_NAME.get(tag)
            if doc_name and doc_name in pattern_counts:
                pattern_counts[doc_name] += 1

    progress_bar = generate_progress_bar(total_solved)

    # Sort problems for Recently Solved (latest added first, fallback to highest ID)
    recent_problems = sorted(problems, key=lambda p: (p.date_added, p.id), reverse=True)[:10]

    lines = []
    lines.append("<div align=\"center\">")
    lines.append("")
    lines.append("# ⚡ LeetCode Solutions Portfolio")
    lines.append("")
    lines.append("### Automated, Structured & Pattern-Categorized Algorithm Solutions")
    lines.append("")
    lines.append(f"![Total Solved](https://img.shields.io/badge/Total%20Solved-{total_solved}-blue?style=for-the-badge&logo=leetcode)")
    lines.append(f"![Easy](https://img.shields.io/badge/Easy-{easy_count}-brightgreen?style=for-the-badge)")
    lines.append(f"![Medium](https://img.shields.io/badge/Medium-{medium_count}-orange?style=for-the-badge)")
    lines.append(f"![Hard](https://img.shields.io/badge/Hard-{hard_count}-red?style=for-the-badge)")
    lines.append("![Auto Updated](https://img.shields.io/badge/Status-Auto%20Updated-success?style=for-the-badge&logo=githubactions)")
    lines.append("")
    lines.append("</div>")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📌 Table of Contents")
    lines.append("- [📚 All Problems (Sorted Numerically)](docs/AllProblems.md)")
    lines.append("- [📊 Progress Overview](#-progress-overview)")
    lines.append("- [🎯 Difficulty Breakdown](#-difficulty-breakdown)")
    lines.append("- [🧩 Pattern & Topic Index](#-pattern--topic-index)")
    lines.append("- [🕒 Recently Solved Problems](#-recently-solved-problems)")
    lines.append("- [📈 Detailed Statistics & Analytics](#-detailed-statistics--analytics)")
    lines.append("- [⚙️ Workflow & Automation](#%EF%B8%8F-workflow--automation)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📊 Progress Overview")
    lines.append("")
    lines.append(f"**LeetCode Journey Target Progress:** {progress_bar}")
    lines.append("")
    lines.append("| Metric | Count | Percentage | Documentation |")
    lines.append("| :--- | :---: | :---: | :---: |")
    easy_pct = (easy_count / total_solved * 100) if total_solved > 0 else 0
    med_pct = (medium_count / total_solved * 100) if total_solved > 0 else 0
    hard_pct = (hard_count / total_solved * 100) if total_solved > 0 else 0
    lines.append(f"| 🟢 **Easy** | {easy_count} | {easy_pct:.1f}% | [View Easy Solutions](docs/Easy.md) |")
    lines.append(f"| 🟠 **Medium** | {medium_count} | {med_pct:.1f}% | [View Medium Solutions](docs/Medium.md) |")
    lines.append(f"| 🔴 **Hard** | {hard_count} | {hard_pct:.1f}% | [View Hard Solutions](docs/Hard.md) |")
    lines.append(f"| 🏆 **Total** | **{total_solved}** | **100.0%** | [All Problems Index](docs/AllProblems.md) | [Full Stats](stats/progress.md) |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🎯 Difficulty Breakdown & Index")
    lines.append("")
    lines.append("Quickly browse or filter solutions by problem number and difficulty:")
    lines.append("")
    lines.append("- 📚 **[All Problems Index](docs/AllProblems.md)** - Master list of all solved problems sorted numerically by Problem ID (1, 2, 3...).")
    lines.append("- 🟢 **[Easy Problems](docs/Easy.md)** - Fundamental data structures, basic syntax, and array/string manipulations.")
    lines.append("- 🟠 **[Medium Problems](docs/Medium.md)** - Two pointers, sliding window, binary search, tree traversals, and dynamic programming foundations.")
    lines.append("- 🔴 **[Hard Problems](docs/Hard.md)** - Advanced graph algorithms, complex dynamic programming, segment trees, and hard constraint optimizations.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🧩 Pattern & Topic Index")
    lines.append("")
    lines.append("Explore problems grouped by algorithmic pattern and data structure:")
    lines.append("")
    lines.append("| Pattern / Topic | Problems Solved | Document Link |")
    lines.append("| :--- | :---: | :---: |")

    for pat in REQUIRED_PATTERNS:
        cnt = pattern_counts.get(pat, 0)
        lines.append(f"| 🏷️ **{pat}** | {cnt} | [View {pat} Solutions](docs/{pat}.md) |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 🕒 Recently Solved Problems")
    lines.append("")
    lines.append("| # | Problem Title | Difficulty | Solution | Date Added |")
    lines.append("| :---: | :--- | :---: | :---: | :---: |")

    for p in recent_problems:
        sol_link = f"[Solution]({p.solution_file})" if p.solution_file else f"[Folder]({p.folder_name}/)"
        folder_link = f"[{p.id}. {p.title}]({p.folder_name}/)"
        lines.append(f"| {p.id} | {folder_link} | {p.difficulty_badge} | {sol_link} | {p.date_added} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 📈 Detailed Statistics & Analytics")
    lines.append("")
    lines.append("For interactive Mermaid charts, timeline metrics, weekly/monthly growth tracking, visit the dedicated statistics page:")
    lines.append("➡️ **[View Complete Progress & Analytics (stats/progress.md)](stats/progress.md)**")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## ⚙️ Workflow & Automation")
    lines.append("")
    lines.append("This repository is integrated with **LeetSync** and powered by custom **GitHub Actions**:")
    lines.append("1. **LeetSync Push**: Automatically pushes newly solved LeetCode solutions into standard `<id>-<slug>/` directories.")
    lines.append("2. **Metadata Fetching**: Uses LeetCode GraphQL API to resolve tags, difficulty, and metadata without manual input.")
    lines.append("3. **Idempotent Regeneration**: Automatically updates `README.md`, `docs/`, and `stats/progress.md` upon every push without modifying solution code.")
    lines.append("")
    lines.append("<div align=\"center\">")
    lines.append("<br>")
    lines.append("<i>Generated automatically by GitHub Actions workflow. Built with Python 3.12.</i>")
    lines.append("</div>")
    lines.append("")

    return "\n".join(lines)


def generate_readme(repo_root: str = ".", problems: List[ProblemInfo] = None) -> None:
    """Generates and writes root README.md."""
    if problems is None:
        from common import scan_problems
        problems = scan_problems(repo_root)

    content = build_readme_content(problems)
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Successfully generated root README.md with {len(problems)} problems.")


if __name__ == "__main__":
    generate_readme(".")
