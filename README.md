# 每日 AI 要闻 · Daily AI News

由 Codex 联网核查并生成中文 AI 简报，覆盖过去24小时的重要动态，发布为手机友好的网页。

在线阅读：https://junyanwang77.github.io/daily-ai-news/

## 当前自动化：ChatGPT 订阅

2026-11-11 起改用 Mac 上 Codex CLI 的 ChatGPT 登录额度，每天北京时间 **08:40** 生成、独立复核并发布。电脑必须开机、联网且用户已登录。错过时间后，登录/唤醒时补检查当天任务；关机期间无法生产，不自动补往期。订阅额度不足或登录过期时停止，不回退到 API。

旧 GitHub 工作流只显示迁移提示，**不再调用模型或 API**，cron-job.org 的旧触发不会消耗 API 余额。GitHub Pages 仍在 push 后部署。ChatGPT 登录凭证只留本机，不上传到公开仓库或 Actions Secret。参考 [官方认证文档](https://learn.chatgpt.com/docs/auth)。

### 安装与管理

在项目目录执行：

```bash
codex login                             # 选择 ChatGPT；已登录无需重复
python3 scripts/subscription_daily.py --check
python3 scripts/subscription_daily.py --install
python3 scripts/subscription_daily.py --status
```

安装的 macOS LaunchAgent 每15分钟检查一次当天是否需要生产，08:40 到时也会触发。同一天最多自动尝试一次，避免故障反复消耗订阅额度。修复失败原因后执行 `python3 scripts/subscription_daily.py --retry` 显式重试；`--draft-only` 生成并复核但不发布。已有当天归档时不再生成。

- 运行记录、日志和中间稿：`~/Library/Application Support/daily-ai-news/YYYY-MM-DD/`
- 定时配置：`~/Library/LaunchAgents/com.wangyuan.daily-ai-news.subscription.plist`
- 不必打开 Codex 窗口，但须保留 CLI、ChatGPT 登录和本机 GitHub 推送权限。
- 停用定时任务：`launchctl bootout gui/$(id -u)/com.wangyuan.daily-ai-news.subscription`

### 生产流程

检查 ChatGPT 登录 → 独立临时克隆 → Codex 订阅推荐模型实时搜索生成 → 新会话逐条打开原文复核 → 输出限制和结构校验 → 生成 HTML → 更新首页与归档 → 推送 → GitHub Pages 部署。

不固定旧 API 型号：Codex 根据订阅权限选择推荐模型，每次实际型号记在 generate.log 和 review.log 的开头。

两次模型调用均强制 ChatGPT 身份、移除 API 环境变量、忽略个人模型配置，使用 workspace-write 沙箱。日志不包含登录凭证。模型不负责提交或发布；脚本只在校验通过后执行发布。无法联网、无合格候选、缺失文件或修改已有文件时停止，不覆盖上一期。原文复核仍由模型执行，不能保证杜绝事实错误。

封面统一标注“由 Codex 自动生成”。

## 项目结构

| 文件 | 用途 |
|---|---|
| `scripts/subscription_daily.py` | 本机订阅生产与定时任务管理 |
| `prompts/daily_ai_briefing.md` | 内容规范与事实核查要求 |
| `prompts/subscription_generate.md` | 生成阶段指令 |
| `prompts/subscription_review.md` | 独立复核指令 |
| `make_html.py` | Markdown 转手机端 HTML |
| `validate_briefing.py` | 结构与字段校验 |
| `check_generated_briefing.py` | 文件范围和发布条件检查 |
| `publish.sh` | 更新最新一期、首页和归档，提交并推送 |
| `.github/workflows/daily-ai-news.yml` | 旧触发入口迁移提示，不调用 API |
| `archive/YYYY-MM/` | 已发布的历史简报 |

## 历史迁移

原 Claude 订阅流程已停用。2026-11-05 至 11-10 曾使用 Codex GitHub Action + OpenAI API 生成和复核，API 单独计费；2026-11-11 改为本机 ChatGPT 订阅。旧 API Secret 不再被任何生产步骤引用。

## 免责声明

简报由 AI 联网搜索、核查并生成，仍可能存在遗漏或误判。请作为信息参考，重要决策以官方一手信息为准。
