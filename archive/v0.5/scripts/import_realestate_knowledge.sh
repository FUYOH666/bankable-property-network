#!/usr/bin/env bash
# One-time import of RealEstate-AI knowledge_base into demo corpus.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${ROOT}/data/consult_knowledge/realestate-demo"
REPO="FUYOH666/RealEstate-AI"
SRC_PATH="knowledge_base"

FILES=(
  README.md
  Project_Overview.md
  FAQ.md
  Legal_and_Terms.md
  Investment_Guide.md
  Layouts_Guide.md
  Location_Lifestyle.md
  Sales_Process.md
  TEST_CONSTRUCTION_GROUP_Profile.md
  payment_plans.csv
  units_full_309.csv
)

mkdir -p "${DEST}"

if ! command -v gh >/dev/null 2>&1; then
  echo "gh CLI required. Install: https://cli.github.com/" >&2
  exit 1
fi

echo "Importing from ${REPO}/${SRC_PATH} → ${DEST}"

for file in "${FILES[@]}"; do
  echo "  ${file}"
  gh api "repos/${REPO}/contents/${SRC_PATH}/${file}" --jq '.content' | base64 -d > "${DEST}/${file}"
done

cat > "${DEST}/DEMO_NOTICE.md" <<'EOF'
# Demo knowledge corpus

Imported from prior art **RealEstate-AI** (`knowledge_base/`) for hackathon consultation demo only.

- Fictional project: TEST CONSTRUCTION GROUP / TEST DEVELOPER 1
- Not a live ERP feed or bank endorsement
- Re-import: `./scripts/import_realestate_knowledge.sh`
EOF

echo "Done. $(find "${DEST}" -type f | wc -l | tr -d ' ') files in ${DEST}"
