#!/bin/sh
#
# Build crc32.com and publish it to the GitHub Pages repo (crc32/crc32.github.io).
#
# Usage:  ./deploy.sh ["optional commit message"]
#
# Assumes the Pages repo is checked out next to this one:
#   ~/Projects/crc32-sitefiles      (this repo: sources)
#   ~/Projects/crc32.github.io      (built site, served at crc32.com)
# Override with:  SITE_REPO=/path/to/crc32.github.io ./deploy.sh
#
# Requires: hugo (extended), uv, and Google Chrome (or Playwright's Chromium).
# The PDF résumé is regenerated from data/cv.yaml on every deploy.

# Stop on the first failing command.
set -e

# Resolve paths relative to this script so it works from any directory.
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
SITE_REPO="${SITE_REPO:-$SRC_DIR/../crc32.github.io}"

if [ ! -d "$SITE_REPO/.git" ]; then
	echo "Pages repo not found at $SITE_REPO (set SITE_REPO)." >&2
	exit 1
fi

printf "\033[0;32mBuilding site...\033[0m\n"

# Fresh build into ./public (ignored by git).
rm -rf "$SRC_DIR/public"
hugo --source "$SRC_DIR" --minify --gc

# Render the PDF résumé from the built /cv-pdf/ page with headless Chrome.
# Writes public/crossman-cv.pdf (deployed) and static/crossman-cv.pdf
# (committed below), then removes the print-only page from public/.
printf "\033[0;32mRendering PDF résumé...\033[0m\n"
uv run "$SRC_DIR/scripts/build_pdf.py"

# Copy the build over the Pages repo. Not a mirror: files that exist only in
# the Pages repo are left alone.
cp -R "$SRC_DIR/public/." "$SITE_REPO/"

msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi

# Commit and push sources (only if something changed).
git -C "$SRC_DIR" add -A
git -C "$SRC_DIR" diff --cached --quiet || git -C "$SRC_DIR" commit -m "$msg"
git -C "$SRC_DIR" push

# Commit and push the built site.
printf "\033[0;32mPublishing to %s...\033[0m\n" "$SITE_REPO"
git -C "$SITE_REPO" add -A
git -C "$SITE_REPO" diff --cached --quiet || git -C "$SITE_REPO" commit -m "$msg"
git -C "$SITE_REPO" push
