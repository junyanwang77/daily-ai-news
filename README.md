# 每日 AI 要闻 · Daily AI News

> 每天自动生成一份中文 AI 行业简报，覆盖过去 24 小时内全球最值得关注的 AI 动态，并发布为手机友好的网页。

🔗 在线阅读：https://junyanwang77.github.io/daily-ai-news/

## 特点

- **每日自动更新**：通过 GitHub Actions 定时任务，每天北京时间 9:00 左右自动生成并发布，无需人工干预
- **真实性优先**：生成简报的 Prompt 内置了严格的事实核查规则——要求交叉验证信源、标注可信度、禁止编造新闻/链接/数据，无法核实的内容会被明确标注而非编造
- **多维度解读**：不只是新闻链接堆砌，每条要闻都会说明发生了什么、为什么重要、影响谁、是否可靠
- **手机阅读友好**：自动将 Markdown 转换为卡片式排版的移动端 HTML

## 工作原理

```
GitHub Actions（定时 / 手动触发）
        │
        ▼
  claude -p 按照 prompts/daily_ai_briefing.md 的要求：
  联网搜索 → 抓取核实 → 生成当日 Markdown
        │
        ▼
  python3 make_html.py  →  生成手机阅读版 HTML
        │
        ▼
  publish.sh：更新 latest 文件与首页 index.html，
  commit + push 回本仓库
        │
        ▼
  GitHub Pages 自动发布最新页面
```

整套流程通过 [`.github/workflows/daily-ai-news.yml`](.github/workflows/daily-ai-news.yml) 编排，全部运行在 GitHub 的服务器上，不依赖任何本地设备。

## 项目结构

```
.
├── .github/workflows/daily-ai-news.yml   # 定时任务：生成 + 发布
├── prompts/daily_ai_briefing.md          # 生成简报所用的完整 Prompt
├── make_html.py                          # Markdown → 手机端 HTML 转换脚本
├── publish.sh                            # 更新 latest 文件、生成首页、commit & push
├── index.html                            # 网站首页（自动生成，指向最新一期）
├── daily-ai-briefing-YYYY-MM-DD.md       # 每日简报（Markdown 原文）
└── daily-ai-briefing-YYYY-MM-DD-mobile.html  # 每日简报（手机阅读版）
```

## 本地运行 / 自行部署

如果你想 fork 本项目，在自己的仓库里跑起同样的自动化：

### 1. 准备 Claude Code 的鉴权凭证

本项目使用 [Claude Code](https://docs.claude.com/en/docs/claude-code) CLI 生成内容。若你有 Claude Pro/Max 订阅，可在本地终端执行：

```bash
claude setup-token
```

按提示在浏览器完成授权后，会得到一个长期有效的 OAuth token。

### 2. 配置 GitHub Actions Secret

在你 fork 后的仓库中，进入 `Settings → Secrets and variables → Actions`，新增一个 Secret：

| Name | Value |
|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | 上一步得到的 token |

### 3. 启用 GitHub Pages

进入 `Settings → Pages`，Source 选择 `Deploy from a branch`，分支选 `main`，目录选 `/ (root)`。

### 4. 手动触发一次测试

进入 `Actions` 标签页，选择 `Daily AI News` workflow，点击 `Run workflow` 手动触发一次，确认能成功生成并发布。

之后每天会按 [workflow 文件](.github/workflows/daily-ai-news.yml) 中设置的 cron 时间自动运行，也可以随时手动触发。

## 本地手动生成（可选）

无需等待定时任务，也可以在本地直接生成当天简报：

```bash
claude -p "$(cat prompts/daily_ai_briefing.md)" \
  --model sonnet \
  --permission-mode bypassPermissions \
  --allowedTools "Read,Write,Bash,WebSearch,WebFetch"

bash ./publish.sh
```

## 免责声明

简报内容由 AI 自动联网搜索、核实并生成，虽然 Prompt 中内置了严格的事实核查与信源交叉验证要求，仍可能存在遗漏或误判。请将其作为信息参考，重要决策请以官方一手信息为准。
