#!/usr/bin/env bash
set -euo pipefail

# ---- EDIT THESE BEFORE RUNNING ----
REPO_ROOT="${REPO_ROOT:-$(pwd)}"   # Use current directory as default
ZIP_PATH="${ZIP_PATH:-$HOME/Downloads/ai-seo-kit-v1.zip}"            # <- change if needed
SITE_SUBDIR="seo-portfolio"  # keep unless your site directory differs
# -----------------------------------

if [ ! -f "$ZIP_PATH" ]; then
  echo "ERROR: ZIP not found at $ZIP_PATH"
  echo "Place the ai-seo-kit-v1.zip at that path or edit ZIP_PATH in this script."
  exit 1
fi

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "ERROR: $REPO_ROOT is not a git repo. Set REPO_ROOT to your local repo root."
  exit 1
fi

cd "$REPO_ROOT"
echo "Repo root: $(pwd)"
ts=$(date +"%Y%m%d-%H%M%S")
BRANCH="agent/integrate-ai-seo-kit-$ts"

# Safety: show plan and prompt
cat <<PLAN

Plan
----
1) Create branch: $BRANCH
2) Unpack kit from: $ZIP_PATH
3) Copy:
   - ZIP -> $SITE_SUBDIR/public/downloads/
   - product & buy pages -> $SITE_SUBDIR/src/pages/products/
   - posts -> $SITE_SUBDIR/src/content/blog/
   - scripts & templates -> $SITE_SUBDIR/scripts/ or $SITE_SUBDIR/content/ai-seo-kit/
4) Commit & run: npm ci && npm run build && npm run preview (background)
5) Run scripts/check-performance.sh (if exists)
6) If anything fails: use the printed revert commands.

Press Enter to continue or Ctrl-C to cancel.
PLAN

read -r _

# 1) Create branch
git checkout -b "$BRANCH"

TMPDIR="$(mktemp -d)"
echo "Using temp dir $TMPDIR"
unzip -q "$ZIP_PATH" -d "$TMPDIR"

# Paths inside zip were ai_seo_kit_v1 and ai_seo_kit_pages in our build
KIT_DIR="$TMPDIR/ai_seo_kit_v1"
PAGES_DIR="$TMPDIR/ai_seo_kit_pages"

# Ensure target dirs exist in site
mkdir -p "$SITE_SUBDIR/public/downloads"
mkdir -p "$SITE_SUBDIR/src/pages/products"
mkdir -p "$SITE_SUBDIR/src/content/blog"
mkdir -p "$SITE_SUBDIR/scripts"
mkdir -p "$SITE_SUBDIR/content/ai-seo-kit"

# 2) Copy files
echo "Copying ZIP to public/downloads..."
cp -v "$ZIP_PATH" "$SITE_SUBDIR/public/downloads/"

if [ -d "$PAGES_DIR" ]; then
  echo "Copying product pages..."
  cp -v "$PAGES_DIR/ai-seo-kit.md" "$SITE_SUBDIR/src/pages/products/ai-seo-kit.md" || true
  cp -v "$PAGES_DIR/buy-ai-seo-kit.md" "$SITE_SUBDIR/src/pages/products/buy-ai-seo-kit.md" || true

  echo "Copying posts..."
  mkdir -p "$SITE_SUBDIR/src/content/blog"
  if [ -d "$PAGES_DIR/posts" ]; then
    cp -v "$PAGES_DIR/posts/"*.md "$SITE_SUBDIR/src/content/blog/" || true
  fi
fi

if [ -d "$KIT_DIR" ]; then
  echo "Copying kit assets and templates..."
  cp -vr "$KIT_DIR/templates" "$SITE_SUBDIR/content/ai-seo-kit/" || true
  cp -v "$KIT_DIR/review-response-generator.js" "$SITE_SUBDIR/scripts/review-response-generator.js" || true
  cp -v "$KIT_DIR/json-ld-snippets.json" "$SITE_SUBDIR/content/ai-seo-kit/json-ld-snippets.json" || true
  cp -v "$KIT_DIR/sample-frontmatter.md" "$SITE_SUBDIR/content/ai-seo-kit/sample-frontmatter.md" || true
  cp -v "$KIT_DIR/30-day-playbook.md" "$SITE_SUBDIR/content/ai-seo-kit/30-day-playbook.md" || true
fi

# 3) Stage + commit
git add -A
git commit -m "chore: add AI SEO Kit (product pages, posts, templates, downloads)" || true

echo "Committed changes on branch $BRANCH"

# 4) Install & build (if site has package.json in seo-portfolio dir)
if [ -d "$SITE_SUBDIR" ] && [ -f "$SITE_SUBDIR/package.json" ]; then
  echo "Installing npm deps (this may take a minute)..."
  (cd "$SITE_SUBDIR" && npm ci)
  echo "Building site..."
  (cd "$SITE_SUBDIR" && npm run build)
  echo "Starting preview (background on port 4321)..."
  (cd "$SITE_SUBDIR" && npm run preview -- --port 4321 >/tmp/astro-preview.log 2>&1 &) || true
else
  echo "Warning: no package.json found in $SITE_SUBDIR — skip build step."
fi

# 5) Run perf check script if present in repo root
if [ -f "scripts/check-performance.sh" ]; then
  echo "Running scripts/check-performance.sh..."
  bash scripts/check-performance.sh || echo "Perf script returned non-zero (check logs)"
else
  echo "No scripts/check-performance.sh; skip perf check."
fi

# 6) Output verification instructions
cat <<VERIFY

DONE (branch: $BRANCH)

Quick verification steps:
1) Open local preview:
   http://localhost:4321/products/ai-seo-kit
   - Confirm H1 reads "AI SEO Kit for Freelancers"
   - Confirm first 100 words mention "AI SEO Kit" or "AI SEO"

2) Confirm zip download exists:
   $SITE_SUBDIR/public/downloads/$(basename "$ZIP_PATH")

3) Open one blog post:
   http://localhost:4321/blog/30-day-ai-seo-playbook
   - Confirm post loads and links to /products/ai-seo-kit

4) If preview not running, run manually from repo:
   cd $SITE_SUBDIR
   npm run preview -- --port 4321

If anything is wrong and you want to revert to main:
   git checkout main
   git branch -D $BRANCH
   git reset --hard origin/main

If you want a PR created and you use gh CLI:
   gh pr create --title "Add AI SEO Kit" --body "Add product + content" --base main --head $BRANCH

VERIFY

# Cleanup temp
rm -rf "$TMPDIR"
echo "Temp cleaned."