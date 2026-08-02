# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A fully automated daily Chinese-language AI news briefing. A GitHub Actions workflow generates a new briefing every day, converts it to a mobile-friendly HTML page, validates it, and publishes it to GitHub Pages — no manual steps required in normal operation.

## Commands

Generate today's briefing locally (same command the workflow runs):

```bash
claude -p "$(cat prompts/daily_ai_briefing.md)" \
  --model sonnet \
  --permission-mode bypassPermissions \
  --allowedTools "Read,Write,Bash,WebSearch,WebFetch"
```

Validate a generated briefing before publishing:

```bash
python3 validate_briefing.py YYYY-MM-DD
```

Regenerate the mobile HTML from an existing Markdown file:

```bash
python3 make_html.py YYYY-MM-DD
```

Publish (updates latest files, archives dated files, regenerates `index.html`/`archive.html`, commits, pushes):

```bash
bash ./publish.sh [YYYY-MM-DD]   # defaults to today
```

There is no build step, package manager, or lint/test framework — `validate_briefing.py` is the correctness check that stands in for tests, and it must pass before `publish.sh` runs.

## Architecture

```
cron-job.org (external, 08:40 Beijing time)
        │  calls workflow_dispatch via GitHub API
        ▼
.github/workflows/daily-ai-news.yml
        │  skips entirely if archive/YYYY-MM/daily-ai-briefing-YYYY-MM-DD.md already exists
        ▼
claude -p prompts/daily_ai_briefing.md   →  daily-ai-briefing-YYYY-MM-DD.md
        │
        ▼
python3 make_html.py YYYY-MM-DD          →  daily-ai-briefing-YYYY-MM-DD-mobile.html
        │
        ▼
python3 validate_briefing.py YYYY-MM-DD  →  fails the run if structure/fields are wrong
        │
        ▼
bash publish.sh YYYY-MM-DD               →  updates *-latest.* , moves dated files into
                                             archive/YYYY-MM/, regenerates index.html and
                                             archive.html, commits + pushes
        │
        ▼
GitHub Pages serves the updated site
```

Key things a future change needs to respect:

- **The trigger is intentionally not GitHub's native `schedule:`.** It was replaced with an external cron-job.org call to `workflow_dispatch` because GitHub's own schedule delay proved unreliable. Don't "fix" this back to a `schedule:` trigger without knowing that history.
- **The workflow is idempotent by design**: it checks whether today's archived `.md` already exists and skips generation if so, so it's safe to trigger manually without producing duplicates.
- **`prompts/daily_ai_briefing.md` is the actual spec**, not just a prompt — it dictates the exact two-file output contract (Markdown must be written first, then `make_html.py` must be run to produce the HTML — the HTML is never to be hand-written), and explicitly forbids the generation step from modifying `README.md`, `index.html`, or `publish.sh`. Those three files are only ever touched by `publish.sh` itself (index.html) or by a human (README.md).
- **`validate_briefing.py` enforces the contract from the prompt**: required sections (先说结论 / 今日最值得关注的...件事 / 对普通人的影响 / 对学习者·开发者的影响 / 对创业者的影响 / 我的判断 / 来源链接 / 核查说明), and per-news-item required fields (来源, 链接, 核查状态 ∈ {已核实, 部分核实, 未完全核实}, 发生了什么, 为什么重要, 影响对象, 重要性评分 ∈ [1,10], 可信度 ∈ {高, 中, 低}). A day with zero verifiable news items is treated as valid (it means nothing checked out, not a failure) — validation only enforces structure, not that news exist.
- **Authentication**: both local runs and the GitHub Action need `CLAUDE_CODE_OAUTH_TOKEN` (obtained via `claude setup-token`); in CI it's read from the `CLAUDE_CODE_OAUTH_TOKEN` repository secret.
- **`publish.sh` derives the archive/index layout by scanning `archive/*/daily-ai-briefing-*-mobile.html` on every run** — it doesn't keep a separate manifest, so archive.html is always regenerated from whatever files actually exist on disk.
