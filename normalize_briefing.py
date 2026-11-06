#!/usr/bin/env python3
import datetime
import pathlib
import re
import sys


def normalize_statuses(markdown):
    return re.sub(
        r'(?m)^([-*][ \t]+(?:\*\*)?核查状态(?:\*\*)?[ \t]*[：:][ \t]*)已打开原文正文核查[ \t]*$',
        r'\1部分核实（已打开原文正文核查）',
        markdown,
    )


def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 normalize_briefing.py YYYY-MM-DD')
    briefing_date = sys.argv[1]
    if datetime.date.fromisoformat(briefing_date).isoformat() != briefing_date:
        raise SystemExit('Invalid briefing date')
    markdown_path = pathlib.Path(f'daily-ai-briefing-{briefing_date}.md')
    if markdown_path.is_symlink():
        raise SystemExit('Refusing symlink output')
    original = markdown_path.read_text(encoding='utf-8')
    normalized = normalize_statuses(original)
    if normalized != original:
        markdown_path.write_text(normalized, encoding='utf-8')
        print('Normalized source-open status to partial verification; factual claims unchanged')


if __name__ == '__main__':
    main()
