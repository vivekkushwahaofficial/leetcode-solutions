"""
common.py - Core data models, LeetCode API integration, caching, and problem discovery utilities.
"""

from dataclasses import dataclass, field
import datetime
import json
import logging
import os
import re
import subprocess
import time
from typing import Dict, List, Optional, Set
import urllib.request
import urllib.error
import ssl

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("LeetSyncAuto")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
CACHE_DIR = os.path.join(REPO_ROOT, ".cache")
CACHE_FILE = os.path.join(CACHE_DIR, "leetcode_cache.json")
LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"

# Tag to Document Filename Mapping
TAG_TO_DOC_NAME: Dict[str, str] = {
    "Array": "Arrays",
    "String": "Strings",
    "Hash Table": "HashMap",
    "Sliding Window": "SlidingWindow",
    "Two Pointers": "TwoPointers",
    "Binary Search": "BinarySearch",
    "Stack": "Stack",
    "Queue": "Queue",
    "Linked List": "LinkedList",
    "Tree": "Tree",
    "Binary Search Tree": "BST",
    "Heap (Priority Queue)": "Heap",
    "Graph": "Graph",
    "Trie": "Trie",
    "Greedy": "Greedy",
    "Backtracking": "Backtracking",
    "Dynamic Programming": "DynamicProgramming",
    "Bit Manipulation": "BitManipulation",
    "Math": "Math",
    "Prefix Sum": "PrefixSum",
    "Intervals": "Intervals",
    "Matrix": "Matrix",
    "Recursion": "Recursion",
    "Binary Tree": "BinaryTree",
    "Union Find": "UnionFind",
    "Monotonic Stack": "MonotonicStack",
    "Topological Sort": "TopologicalSort",
    "Depth-First Search": "Tree",
    "Breadth-First Search": "Tree",
}

# Required doc pages that must exist (even if 0 problems yet)
REQUIRED_PATTERNS: List[str] = [
    "Arrays", "Strings", "HashMap", "SlidingWindow", "TwoPointers",
    "BinarySearch", "Stack", "Queue", "LinkedList", "Tree", "BST",
    "Heap", "Graph", "Trie", "Greedy", "Backtracking",
    "DynamicProgramming", "BitManipulation", "Math", "PrefixSum",
    "Intervals", "Matrix", "Recursion", "BinaryTree", "UnionFind",
    "MonotonicStack", "TopologicalSort"
]

@dataclass
class ProblemInfo:
    id: int
    folder_name: str
    slug: str
    title: str
    difficulty: str  # Easy, Medium, Hard
    tags: List[str] = field(default_factory=list)
    solution_file: Optional[str] = None
    date_added: str = ""  # YYYY-MM-DD

    @property
    def leetcode_url(self) -> str:
        return f"https://leetcode.com/problems/{self.slug}/"

    @property
    def difficulty_badge(self) -> str:
        if self.difficulty == "Easy":
            return "![Easy](https://img.shields.io/badge/-Easy-brightgreen)"
        elif self.difficulty == "Medium":
            return "![Medium](https://img.shields.io/badge/-Medium-orange)"
        elif self.difficulty == "Hard":
            return "![Hard](https://img.shields.io/badge/-Hard-red)"
        return f"![{self.difficulty}](https://img.shields.io/badge/-{self.difficulty}-blue)"


class LeetCodeCache:
    """Manages local metadata caching for LeetCode problems to eliminate redundant network calls."""
    
    def __init__(self, cache_file: str = CACHE_FILE):
        self.cache_file = cache_file
        self.cache: Dict[str, dict] = {}
        self.load_cache()

    def load_cache(self) -> None:
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                logger.info(f"Loaded {len(self.cache)} problems from cache ({self.cache_file}).")
            except Exception as e:
                logger.warning(f"Failed to load cache file: {e}. Starting fresh.")
                self.cache = {}
        else:
            self.cache = {}

    def save_cache(self) -> None:
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.cache, f, indent=2, sort_keys=True)
            logger.info(f"Saved {len(self.cache)} entries to cache ({self.cache_file}).")
        except Exception as e:
            logger.error(f"Failed to save cache file: {e}")

    def get(self, slug: str) -> Optional[dict]:
        return self.cache.get(slug)

    def set(self, slug: str, data: dict) -> None:
        self.cache[slug] = data


def fetch_leetcode_graphql(slug: str) -> Optional[dict]:
    """Fetches problem metadata from official LeetCode GraphQL API."""
    query = """
    query getQuestionDetail($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            difficulty
            topicTags {
                name
                slug
            }
        }
    }
    """
    payload = json.dumps({"query": query, "variables": {"titleSlug": slug}}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://leetcode.com"
    }

    ctx = ssl.create_default_context()
    req = urllib.request.Request(LEETCODE_GRAPHQL_URL, data=payload, headers=headers)

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                if response.status == 200:
                    res_data = json.loads(response.read().decode("utf-8"))
                    question = res_data.get("data", {}).get("question")
                    if question:
                        return {
                            "id": int(question.get("questionFrontendId", 0) or question.get("questionId", 0)),
                            "title": question.get("title", slug.replace("-", " ").title()),
                            "difficulty": question.get("difficulty", "Easy"),
                            "tags": [tag["name"] for tag in question.get("topicTags", [])]
                        }
        except Exception as e:
            logger.warning(f"GraphQL request attempt {attempt + 1} failed for '{slug}': {e}")
            time.sleep(1)

    return None


def get_git_commit_date(folder_path: str) -> str:
    """Returns YYYY-MM-DD date of when the folder was created/committed in git history, or file mtime."""
    try:
        cmd = ["git", "log", "--diff-filter=A", "--follow", "--format=%cd", "--date=short", "-1", "--", folder_path]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        output = res.stdout.strip()
        if output:
            return output
        
        # Fallback to latest commit if creation commit not found
        cmd_latest = ["git", "log", "-1", "--format=%cd", "--date=short", "--", folder_path]
        res_latest = subprocess.run(cmd_latest, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        output_latest = res_latest.stdout.strip()
        if output_latest:
            return output_latest
    except Exception:
        pass

    # File system fallback
    try:
        mtime = os.path.getmtime(folder_path)
        return datetime.date.fromtimestamp(mtime).isoformat()
    except Exception:
        return datetime.date.today().isoformat()


def scan_problems(repo_root: str = REPO_ROOT) -> List[ProblemInfo]:
    """Scans repository root directory for problem folders in `<id>-<slug>` format."""
    cache = LeetCodeCache()
    problems: List[ProblemInfo] = []
    ignored = {".git", ".github", ".cache", "docs", "stats", "scripts", "node_modules"}

    for item in os.listdir(repo_root):
        folder_path = os.path.join(repo_root, item)
        if not os.path.isdir(folder_path) or item in ignored:
            continue

        match = re.match(r"^(\d+)-(.+)$", item)
        if not match:
            continue

        problem_id = int(match.group(1))
        slug = match.group(2)

        # Detect solution code file in folder
        solution_file = None
        code_exts = (".java", ".py", ".cpp", ".c", ".js", ".ts", ".go", ".rs", ".kt", ".cs", ".swift")
        try:
            for fname in os.listdir(folder_path):
                if fname.lower() != "readme.md" and fname.endswith(code_exts):
                    solution_file = f"{item}/{fname}"
                    break
        except Exception:
            pass

        date_added = get_git_commit_date(folder_path)

        # Retrieve metadata from cache or API
        cached_data = cache.get(slug)
        if cached_data:
            info = ProblemInfo(
                id=cached_data.get("id", problem_id),
                folder_name=item,
                slug=slug,
                title=cached_data.get("title", slug.replace("-", " ").title()),
                difficulty=cached_data.get("difficulty", "Easy"),
                tags=cached_data.get("tags", []),
                solution_file=solution_file,
                date_added=date_added
            )
        else:
            logger.info(f"Fetching metadata for '{slug}' via LeetCode API...")
            api_data = fetch_leetcode_graphql(slug)
            if api_data:
                title = api_data["title"]
                difficulty = api_data["difficulty"]
                tags = api_data["tags"]
                cache.set(slug, {
                    "id": api_data["id"],
                    "title": title,
                    "difficulty": difficulty,
                    "tags": tags
                })
            else:
                title = slug.replace("-", " ").title()
                difficulty = "Easy"
                tags = []
                cache.set(slug, {
                    "id": problem_id,
                    "title": title,
                    "difficulty": difficulty,
                    "tags": tags
                })

            info = ProblemInfo(
                id=problem_id,
                folder_name=item,
                slug=slug,
                title=title,
                difficulty=difficulty,
                tags=tags,
                solution_file=solution_file,
                date_added=date_added
            )

        problems.append(info)

    cache.save_cache()
    # Sort deterministically by problem ID
    problems.sort(key=lambda p: p.id)
    logger.info(f"Discovered {len(problems)} problem folders.")
    return problems
