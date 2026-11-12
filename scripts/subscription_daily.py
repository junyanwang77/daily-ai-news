#!/usr/bin/env python3
"""Local, subscription-only briefing production. Never falls back to API auth."""
import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STATE = Path.home() / 'Library/Application Support/daily-ai-news'
LABEL = 'com.wangyuan.daily-ai-news.subscription'
REMOTE = 'https://github.com/junyanwang77/daily-ai-news.git'
TZ = ZoneInfo('Asia/Shanghai')


def clean_env():
    env = os.environ.copy()
    for key in list(env):
        if key.startswith('OPENAI_') or key in {
            'CODEX_API_KEY', 'CODEX_ACCESS_TOKEN', 'ANTHROPIC_API_KEY',
        }:
            env.pop(key)
    env['TZ'] = 'Asia/Shanghai'
    env['GIT_TERMINAL_PROMPT'] = '0'
    return env


def run(args, cwd=ROOT, capture=False, timeout=120):
    return subprocess.run(args, cwd=cwd, env=clean_env(), check=True,
                          text=True, capture_output=capture, timeout=timeout)


def require_chatgpt():
    result = run(['codex', 'login', 'status'], capture=True)
    status = result.stdout + result.stderr
    if 'Logged in using ChatGPT' not in status:
        raise RuntimeError('需要 codex login 的 ChatGPT 登录；拒绝 API 登录。')


def save_status(path, **values):
    values['updated_at'] = dt.datetime.now(TZ).isoformat()
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(values, ensure_ascii=False, indent=2) + '\n')
    temp.replace(path)


def install():
    require_chatgpt()
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    agent = Path.home() / 'Library/LaunchAgents' / f'{LABEL}.plist'
    agent.parent.mkdir(parents=True, exist_ok=True)
    bins = [str(Path(shutil.which(name)).parent) for name in ('codex', 'node', 'git')]
    task_path = ':'.join(dict.fromkeys(bins + ['/opt/homebrew/bin', '/usr/bin', '/bin', '/usr/sbin', '/sbin']))
    config = {
        'Label': LABEL,
        'ProgramArguments': [sys.executable, str(Path(__file__).resolve())],
        'WorkingDirectory': str(ROOT),
        'EnvironmentVariables': {'PATH': task_path, 'TZ': 'Asia/Shanghai'},
        'RunAtLoad': True,
        'StartInterval': 900,
        'StartCalendarInterval': {'Hour': 8, 'Minute': 40},
        'StandardOutPath': str(STATE / 'scheduler.log'),
        'StandardErrorPath': str(STATE / 'scheduler-error.log'),
        'ProcessType': 'Background',
    }
    with agent.open('wb') as output:
        plistlib.dump(config, output)
    domain = f'gui/{os.getuid()}'
    subprocess.run(['launchctl', 'bootout', f'{domain}/{LABEL}'], capture_output=True)
    run(['launchctl', 'bootstrap', domain, str(agent)])
    print(f'已安装：{agent}；北京时间08:40，登录/唤醒后每15分钟检查补跑。')


def assert_outputs(work, date):
    run(['git', 'diff', '--exit-code'], cwd=work)
    run(['git', 'diff', '--cached', '--exit-code'], cwd=work)
    run([sys.executable, 'check_generated_briefing.py', date], cwd=work)
    run([sys.executable, 'validate_briefing.py', date], cwd=work)


def model_step(work, date, stage, folder):
    require_chatgpt()
    prompt = (ROOT / f'prompts/subscription_{stage}.md').read_text().replace('{date}', date)
    args = ['codex', '-a', 'never', 'exec', '--ignore-user-config',
            '-c', 'forced_login_method="chatgpt"', '-c', 'model_provider="openai"',
            '-c', 'web_search="live"', '-c', 'model_reasoning_effort="medium"',
            '--sandbox', 'workspace-write',
            '--cd', str(work), '--color', 'never', '-']
    with (folder / f'{stage}.log').open('w') as log:
        subprocess.run(args, input=prompt, text=True, env=clean_env(),
                       stdout=log, stderr=subprocess.STDOUT, check=True,
                       cwd=work, timeout=1800)


def produce(retry=False, draft_only=False):
    now = dt.datetime.now(TZ)
    date = now.date().isoformat()
    if (now.hour, now.minute) < (8, 40):
        print('等待北京时间08:40。')
        return
    STATE.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (STATE / 'production.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print('另一生产任务正在运行。')
            return
        day = STATE / date
        day.mkdir(exist_ok=True)
        status_path = day / 'status.json'
        if status_path.exists() and not retry:
            previous = json.loads(status_path.read_text())
            # No model has run during preflight. Retrying on the next timer tick
            # cannot duplicate subscription usage, unlike generate/review failures.
            if not (previous.get('state') == 'failed' and previous.get('stage') == 'preflight'):
                print(status_path.read_text())
                return
            print('生成前检查失败，自动重试；尚未消耗模型额度。')
        if status_path.exists() and json.loads(status_path.read_text()).get('state') == 'published':
            print('今天已经发布，不重复消耗订阅额度。')
            return
        folder = day / now.strftime('%H%M%S-%f')
        folder.mkdir()
        work = folder / 'workspace'
        stage = 'preflight'
        try:
            require_chatgpt()
            save_status(status_path, date=date, state='running', stage=stage, logs=str(folder))
            run(['git', 'clone', '--depth', '1', REMOTE, str(work)])
            archive = work / f'archive/{date[:7]}/daily-ai-briefing-{date}.md'
            if archive.exists():
                save_status(status_path, date=date, state='published', detail='远程已归档，无需再生成。')
                return
            for stage in ('generate', 'review'):
                save_status(status_path, date=date, state='running', stage=stage, logs=str(folder))
                model_step(work, date, stage, folder)
                if stage == 'review':
                    run([sys.executable, 'normalize_briefing.py', date], cwd=work)
                    run([sys.executable, 'make_html.py', date], cwd=work)
                assert_outputs(work, date)
                shutil.copy2(work / f'daily-ai-briefing-{date}.md', folder / f'{stage}.md')
            if draft_only:
                save_status(status_path, date=date, state='validated_draft', logs=str(folder))
                return
            stage = 'publish'
            save_status(status_path, date=date, state='running', stage=stage, logs=str(folder))
            run(['git', 'config', 'user.name', 'daily-ai-news-bot'], cwd=work)
            run(['git', 'config', 'user.email', 'actions@users.noreply.github.com'], cwd=work)
            run(['bash', './publish.sh', date], cwd=work, timeout=180)
            commit = run(['git', 'rev-parse', 'HEAD'], cwd=work, capture=True).stdout.strip()
            save_status(status_path, date=date, state='published', commit=commit, logs=str(folder))
        except Exception as error:
            (folder / 'failure.txt').write_text(f'{stage}: {error}\n')
            save_status(status_path, date=date, state='failed', stage=stage,
                        error=str(error), logs=str(folder))
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--status', action='store_true')
    parser.add_argument('--check', action='store_true', help='Check login and executables without a model call')
    parser.add_argument('--retry', action='store_true', help='Explicitly retry a failed/validated draft today')
    parser.add_argument('--draft-only', action='store_true')
    args = parser.parse_args()
    if args.install:
        install()
    elif args.status:
        paths = sorted(STATE.glob('*/status.json'))[-7:]
        for path in paths:
            print(path.read_text())
        if not paths:
            print('尚无本机生产记录。')
    elif args.check:
        for name in ('codex', 'git', 'node'):
            if not shutil.which(name):
                raise RuntimeError(f'找不到 {name}')
        require_chatgpt()
        print('OK: ChatGPT 登录；运行时强制订阅身份，移除 API 环境变量，不做 API 回退。')
    else:
        produce(retry=args.retry, draft_only=args.draft_only)


if __name__ == '__main__':
    main()
