const fs = require("fs");
const path = require("path");

const ROOT = path.join(__dirname, "..");
const STATS_DIR = path.join(ROOT, "stats");

// Get all problem folders
const folders = fs.readdirSync(ROOT).filter((item) => {
  const full = path.join(ROOT, item);
  return fs.statSync(full).isDirectory() && /^\d+-/.test(item);
});

const dashboard = {
  totalSolved: folders.length,
  easy: 0,
  medium: 0,
  hard: 0,
  lastUpdated: new Date().toISOString().split("T")[0],
  platform: "LeetCode",
};

const problems = [];
const missingReadmes = [];

folders.forEach((folder) => {
  const id = Number(folder.split("-")[0]);

  const title = folder
    .replace(/^\d+-/, "")
    .replace(/-/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());

  const readme = path.join(ROOT, folder, "README.md");

  let difficulty = "Unknown";

  if (!fs.existsSync(readme)) {
    missingReadmes.push(folder);
  } else {
    const text = fs.readFileSync(readme, "utf8");

    const match = text.match(/Difficulty-(Easy|Medium|Hard)/i);

    if (match) {
      difficulty = match[1];

      switch (difficulty.toLowerCase()) {
        case "easy":
          difficulty = "Easy";
          dashboard.easy++;
          break;

        case "medium":
          difficulty = "Medium";
          dashboard.medium++;
          break;

        case "hard":
          difficulty = "Hard";
          dashboard.hard++;
          break;
      }
    }
  }

  problems.push({
    id,
    title,
    difficulty,
  });
});

// Sort latest first
problems.sort((a, b) => b.id - a.id);

// Write JSON files
fs.writeFileSync(
  path.join(STATS_DIR, "dashboard.json"),
  JSON.stringify(dashboard, null, 2)
);

fs.writeFileSync(
  path.join(STATS_DIR, "problems.json"),
  JSON.stringify(problems, null, 2)
);

console.log("✅ dashboard.json updated");
console.log("✅ problems.json updated");
console.log(dashboard);

if (missingReadmes.length > 0) {
  console.log("\n⚠ Missing README files:");
  missingReadmes.forEach((folder) => {
    console.log(` - ${folder}`);
  });
}