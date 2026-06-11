#!/bin/bash
set -e

cd "$HOME/Documents/daily-ai-news"

echo "Current directory:"
pwd

echo "Finding latest briefing files..."

latest_html=$(ls -t daily-ai-briefing-*-mobile.html 2>/dev/null | head -1)
latest_pdf=$(ls -t daily-ai-briefing-*-mobile.pdf 2>/dev/null | head -1)
latest_md=$(ls -t daily-ai-briefing-20*.md 2>/dev/null | head -1)

if [ -z "$latest_html" ]; then
  echo "No mobile HTML briefing found."
  exit 1
fi

if [ -z "$latest_pdf" ]; then
  echo "No mobile PDF briefing found."
  exit 1
fi

echo "Latest HTML: $latest_html"
echo "Latest PDF: $latest_pdf"
echo "Latest MD: $latest_md"

cp "$latest_html" daily-ai-briefing-latest-mobile.html
cp "$latest_pdf" daily-ai-briefing-latest-mobile.pdf

if [ -n "$latest_md" ]; then
  cp "$latest_md" daily-ai-briefing-latest.md
fi

echo "Git status before commit:"
git status --short

git add .

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

commit_msg="Update daily AI briefing $(date '+%Y-%m-%d %H:%M')"
git commit -m "$commit_msg"

git push

echo "Published successfully."
