#!/bin/bash
set -e

cd "$(dirname "$0")"

echo "Current directory:"
pwd

briefing_date="${1:-$(date +%F)}"

if ! [[ "$briefing_date" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
  echo "Invalid date: $briefing_date"
  exit 1
fi

echo "Publishing briefing date: $briefing_date"

latest_html="daily-ai-briefing-${briefing_date}-mobile.html"
latest_md="daily-ai-briefing-${briefing_date}.md"

if [ ! -f "$latest_html" ]; then
  echo "Expected HTML file not found: $latest_html"
  exit 1
fi

if [ ! -f "$latest_md" ]; then
  echo "Expected Markdown file not found: $latest_md"
  exit 1
fi

compact_date=$(echo "$briefing_date" | tr -d '-')
display_year="${briefing_date:0:4}"
display_month="${briefing_date:5:2}"
display_day="${briefing_date:8:2}"
display_date="${display_year} 年 ${display_month#0} 月 ${display_day#0} 日"

echo "Updating latest files..."
cp "$latest_html" daily-ai-briefing-latest-mobile.html
cp "$latest_md" daily-ai-briefing-latest.md

archive_dir="archive/${briefing_date:0:7}"
echo "Archiving dated files into $archive_dir..."
mkdir -p "$archive_dir"
mv -f "$latest_html" "$archive_dir/"
mv -f "$latest_md" "$archive_dir/"

echo "Regenerating archive.html..."

archive_list=""
current_month=""
while IFS= read -r f; do
  fname=$(basename "$f")
  d="${fname#daily-ai-briefing-}"
  d="${d%-mobile.html}"
  y="${d:0:4}"; mo="${d:5:2}"; da="${d:8:2}"
  month_key="${y}-${mo}"
  if [ "$month_key" != "$current_month" ]; then
    if [ -n "$current_month" ]; then
      archive_list+=$'  </ul>\n</div>\n'
    fi
    archive_list+="<div class=\"month\">
  <h2>${y} 年 ${mo#0} 月</h2>
  <ul>
"
    current_month="$month_key"
  fi
  archive_list+="    <li><a href=\"./${f}?t=$(echo "$d" | tr -d '-')\">${y} 年 ${mo#0} 月 ${da#0} 日</a></li>
"
done < <(find archive -name 'daily-ai-briefing-*-mobile.html' | sort -r)
if [ -n "$current_month" ]; then
  archive_list+=$'  </ul>\n</div>\n'
fi

cat > archive.html <<HTML
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>往期回顾 · 每日 AI 要闻</title>
  <meta name="robots" content="noindex">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
      background: #f2f2f7;
      padding: 32px 16px 48px;
    }
    .wrap {
      max-width: 480px;
      margin: 0 auto;
    }
    .header {
      background: #111;
      color: #fff;
      padding: 24px 24px 22px;
      border-radius: 20px 20px 0 0;
    }
    .back {
      display: inline-block;
      color: rgba(255,255,255,.55);
      text-decoration: none;
      font-size: 13px;
      margin-bottom: 12px;
    }
    .title {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.01em;
    }
    .card {
      background: #fff;
      border-radius: 0 0 20px 20px;
      padding: 8px 24px 24px;
      box-shadow: 0 4px 24px rgba(0,0,0,.08), 0 1px 4px rgba(0,0,0,.04);
    }
    .month h2 {
      font-size: 13px;
      font-weight: 700;
      color: #999;
      letter-spacing: 0.05em;
      margin: 22px 0 6px;
    }
    .month ul { list-style: none; }
    .month li {
      border-bottom: 1px solid #f5f5f5;
    }
    .month li:last-child { border-bottom: none; }
    .month a {
      display: block;
      padding: 12px 4px;
      color: #222;
      text-decoration: none;
      font-size: 15px;
      -webkit-tap-highlight-color: transparent;
    }
    .month a:active { color: #999; }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <a class="back" href="./index.html">‹ 返回首页</a>
      <div class="title">往期回顾</div>
    </div>
    <div class="card">
$archive_list    </div>
  </div>
</body>
</html>
HTML

echo "Updating index.html to published date: $briefing_date"

cat > index.html <<HTML
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>每日 AI 要闻</title>
  <meta name="description" content="每天筛选真正值得关注的 AI 变化，用普通人也能看懂的方式解释：发生了什么、为什么重要、和你有什么关系。">
  <meta property="og:title" content="每日 AI 要闻">
  <meta property="og:description" content="每天筛选真正值得关注的 AI 变化，用普通人也能看懂的方式解释。">
  <meta property="og:type" content="website">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
      background: #f2f2f7;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 32px 16px;
    }
    .card {
      max-width: 400px;
      width: 100%;
      background: #fff;
      border-radius: 28px;
      overflow: hidden;
      box-shadow: 0 4px 24px rgba(0,0,0,.08), 0 1px 4px rgba(0,0,0,.04);
    }
    .header {
      background: #111;
      color: #fff;
      padding: 28px 28px 26px;
    }
    .badge {
      display: inline-block;
      background: rgba(255,255,255,.12);
      color: rgba(255,255,255,.8);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.1em;
      padding: 3px 10px;
      border-radius: 20px;
      margin-bottom: 14px;
      text-transform: uppercase;
    }
    .title {
      font-size: 28px;
      font-weight: 800;
      line-height: 1.2;
      letter-spacing: -0.01em;
    }
    .subtitle {
      margin-top: 8px;
      font-size: 14px;
      color: rgba(255,255,255,.55);
      line-height: 1.5;
    }
    .body {
      padding: 22px 28px 28px;
    }
    .list {
      list-style: none;
      margin-bottom: 22px;
    }
    .list li {
      font-size: 14px;
      color: #444;
      line-height: 1.6;
      padding: 8px 0;
      border-bottom: 1px solid #f5f5f5;
      display: flex;
      gap: 10px;
      align-items: flex-start;
    }
    .list li:last-child { border-bottom: none; }
    .list li::before {
      content: "";
      display: block;
      width: 5px;
      height: 5px;
      background: #ccc;
      border-radius: 50%;
      margin-top: 8px;
      flex-shrink: 0;
    }
    .btn {
      display: block;
      padding: 15px;
      background: #111;
      color: #fff;
      text-decoration: none;
      text-align: center;
      font-weight: 700;
      font-size: 15px;
      border-radius: 14px;
      margin-bottom: 16px;
      -webkit-tap-highlight-color: transparent;
    }
    .btn-secondary {
      background: #f2f2f7;
      color: #111;
    }
    .footer {
      text-align: center;
      color: #bbb;
      font-size: 12px;
      line-height: 1.8;
    }
    .footer strong { color: #777; }
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="badge">Daily AI Briefing</div>
      <div class="title">每日 AI 要闻</div>
      <div class="subtitle">每天一份，看懂 AI 行业真正在发生什么</div>
    </div>
    <div class="body">
      <ul class="list">
        <li>筛选过去 24 小时最重要的 AI 动态</li>
        <li>解释发生了什么、为什么重要、谁会受影响</li>
        <li>涵盖模型发布、产品更新、开源项目与监管变化</li>
        <li>提供对普通人、开发者、创业者的具体分析</li>
      </ul>
      <a class="btn" href="./daily-ai-briefing-latest-mobile.html?t=$compact_date">阅读最新一期</a>
      <a class="btn btn-secondary" href="./archive.html">查看往期回顾</a>
      <div class="footer">
        最新一期：<strong>$display_date</strong><br>
        每日自动生成 · 内容仅供信息参考
      </div>
    </div>
  </div>
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

commit_msg="Update daily AI briefing $briefing_date"
git commit -m "$commit_msg"
git push

echo "Published successfully."
