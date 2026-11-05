#!/usr/bin/env python3
import datetime
import pathlib
import subprocess
import sys


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 check_generated_briefing.py YYYY-MM-DD')
    briefing_date = sys.argv[1]
    if datetime.date.fromisoformat(briefing_date).isoformat() != briefing_date:
        raise SystemExit('Invalid briefing date')
    markdown_path = pathlib.Path(f'daily-ai-briefing-{briefing_date}.md')
    html_path = pathlib.Path(f'daily-ai-briefing-{briefing_date}-mobile.html')
    for output_path in (markdown_path, html_path):
        if output_path.is_symlink() or not output_path.is_file() or output_path.stat().st_size == 0:
            raise SystemExit(f'Missing, empty or unsafe output: {output_path}')
    markdown_text = markdown_path.read_text(encoding='utf-8')
    if '未能联网获取实时新闻' in markdown_text:
        raise SystemExit('Offline briefing must not replace the published edition')
    untracked = subprocess.check_output(
        ['git', 'ls-files', '--others', '--exclude-standard', '-z']
    ).decode().split('\0')
    unexpected = set(filter(None, untracked)) - {str(markdown_path), str(html_path)}
    if unexpected:
        raise SystemExit(f'Unexpected generated files: {sorted(unexpected)}')
    print(f'OK: {briefing_date} output contract checked')


if __name__ == '__main__':
    main()
