#!/bin/bash
set -e

cd "$HOME/Documents/daily-ai-news"

echo "Current directory:"
pwd

echo "Finding latest dated briefing files..."

latest_html=$(ls -t daily-ai-briefing-20*-mobile.html 2>/dev/null | head -1)
latest_md=$(ls -t daily-ai-briefing-20*.md 2>/dev/null | head -1)

if [ -z "$latest_html" ]; then
  echo "No dated mobile HTML briefing found."
  exit 1
fi

if [ -z "$latest_md" ]; then
  echo "No dated Markdown briefing found."
  exit 1
fi

html_date=$(echo "$latest_html" | sed -E 's/daily-ai-briefing-([0-9]{4}-[0-9]{2}-[0-9]{2})-mobile.html/\1/')
md_date=$(echo "$latest_md" | sed -E 's/daily-ai-briefing-([0-9]{4}-[0-9]{2}-[0-9]{2}).md/\1/')

echo "Latest HTML: $latest_html"
echo "Latest MD: $latest_md"
echo "HTML date: $html_date"
echo "MD date: $md_date"

if [ "$html_date" != "$md_date" ]; then
  echo "HTML date and Markdown date do not match. Stop publishing."
  exit 1
fi

compact_date=$(echo "$html_date" | tr -d '-')

echo "Updating latest files..."
cp "$latest_html" daily-ai-briefing-latest-mobile.html
cp "$latest_md" daily-ai-briefing-latest.md

echo "Updating index.html to published date: $html_date"

cat > index.html <<HTML
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>每日 AI 要闻</title>
  <style>
    body {
      margin: 0;
      padding: 24px 16px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f6f7f9;
      color: #111;
      line-height: 1.75;
    }
    main {
      max-width: 720px;
      margin: 0 auto;
      background: #fff;
      border-radius: 18px;
      padding: 24px;
      box-shadow: 0 8px 30px rgba(0,0,0,.06);
    }
    h1 {
      font-size: 30px;
      margin: 0 0 12px;
      letter-spacing: -0.02em;
    }
    p {
      font-size: 16px;
      margin: 12px 0;
    }
    a {
      color: #0b57d0;
      word-break: break-all;
    }
    .button {
      display: block;
      margin: 18px 0;
      padding: 14px 16px;
      border-radius: 12px;
      background: #111;
      color: #fff;
      text-decoration: none;
      text-align: center;
      font-weight: 600;
    }
    .muted {
      color: #666;
      font-size: 14px;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <main>
    <h1>每日 AI 要闻</h1>

    <p>每天筛选真正值得关注的 AI 变化，用普通人也能看懂的方式解释：发生了什么、为什么重要、和你有什么关系。</p>

    <p>这份简报不是简单搬运新闻，而是帮你从 AI 行业的模型发布、产品更新、开源项目、商业动态和监管变化中，挑出最值得关注的内容。</p>

    <p>内容包括：今日最重要的 AI 动态、对普通人的影响、对学习者和开发者的建议、对创业者的启发，以及我的判断。</p>

    <a class="button" href="./$latest_html?t=$compact_date">阅读最新 AI 要闻</a>

    <p class="muted">当前最新一期：$html_date。每日自动生成并持续更新，内容仅供学习、观察和信息参考。</p>
  </main>
</body>
</html>
HTML

echo "Git status before commit:"
git status --short

git add .

if git diff --cached --quiet; then
  echo "No changes to commit."
  exit 0
fi

commit_msg="Update daily AI briefing $html_date"
git commit -m "$commit_msg"
git push

echo "Published successfully."
