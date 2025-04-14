#!/bin/sh

# If a command fails then the deploy stops
set -e

printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Remove current public folder
rm -fR public
mkdir public

# Build the project.
hugo -t researcher # if using a theme, replace with `hugo -t <YOURTHEME>`

cp -f /Users/crc32/Projects/crc32-sitefiles/public/about/index.html /Users/crc32/Projects/crc32-sitefiles/public/
cp -R /Users/crc32/Projects/crc32-sitefiles/public/ /Users/crc32/Projects/crc32.github.io/

mv /Users/crc32/Projects/crc32.github.io/Crossman-CV.pdf /Users/crc32/Projects/crc32.github.io/crossman-cv.pdf

# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi

git commit -m "$msg"

# Push source and build repos.
git push

# push website
git -C /Users/crc32/Projects/crc32.github.io commit -a -m "update website"
git -C /Users/crc32/Projects/crc32.github.io push
