"""
run_all.py - Master coordinator script that scans problems once and executes all documentation generators.
"""

import sys
import os
from common import scan_problems, logger
from generate_readme import generate_readme
from generate_patterns import generate_patterns
from generate_stats import generate_stats

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logger.info(f"Starting LeetSync documentation generator in: {repo_root}")

    # Step 1: Scan and resolve problem metadata
    problems = scan_problems(repo_root)
    logger.info(f"Loaded {len(problems)} total problems.")

    # Step 2: Generate root README.md
    generate_readme(repo_root, problems)

    # Step 3: Generate docs/ pages
    generate_patterns(repo_root, problems)

    # Step 4: Generate stats/progress.md
    generate_stats(repo_root, problems)

    logger.info("All documentation and statistics successfully generated!")

if __name__ == "__main__":
    main()
