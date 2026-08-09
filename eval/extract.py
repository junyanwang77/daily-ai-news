#!/usr/bin/env python3
"""
把 archive/ 下所有历史简报抽取成结构化数据集，供后续评估使用。

这一步只做"抽取"，不做任何判断——判断留给 stats.py（离线指标）
和 check_links.py（联网核验）。

字段解析直接复用 validate_briefing.py 的 parse_fields，保证评估看到的
字段和发布时校验的字段完全一致，不会两边各自实现导致口径不同。

用法: python3 eval/extract.py
输出: eval/data/items.jsonl  （每行一条新闻）
"""
import json
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from validate_briefing import parse_fields, URL_RE  # noqa: E402

ARCHIVE_DIR = os.path.join(REPO_ROOT, 'archive')
OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'items.jsonl')

DATE_RE = re.compile(r'daily-ai-briefing-(\d{4}-\d{2}-\d{2})\.md$')
NEWS_HEADING_RE = re.compile(r'^##\s+今日最值得关注的.*件事')
# 标题形如 "### 1. xxx"，序号可能缺失，两种都接受
TITLE_RE = re.compile(r'^###\s*(?:\d+[.、]\s*)?(.+?)\s*$')

# 抽取的字段：与 validate_briefing.REQUIRED_FIELDS 一致，另加可选的"备注"
CAPTURED_FIELDS = [
    '来源', '链接', '核查状态', '发生了什么',
    '为什么重要', '影响对象', '重要性评分', '可信度', '备注',
]


def find_briefings():
    """返回 [(date, path), ...]，按日期升序。"""
    found = []
    for root, _dirs, files in os.walk(ARCHIVE_DIR):
        for name in files:
            m = DATE_RE.search(name)
            if m:
                found.append((m.group(1), os.path.join(root, name)))
    return sorted(found)


def extract_news_section(text):
    """切出"今日最值得关注的 N 件事"这一节的正文。找不到返回 None。"""
    sections = re.split(r'\n(?=## )', text)
    for s in sections:
        first_line = s.strip().splitlines()[0] if s.strip() else ''
        if NEWS_HEADING_RE.match(first_line):
            return s
    return None


def parse_score(raw):
    """重要性评分可能写成 '7' 或 '7 分'，取开头的整数；解析不出返回 None。"""
    m = re.match(r'^\s*(\d+)', raw or '')
    return int(m.group(1)) if m else None


def extract_items(date, path):
    text = open(path, encoding='utf-8').read()
    # 离线模式当天没有真实新闻，条目为空是合法的，单独标记以免污染统计
    offline = '未能联网获取实时新闻' in text

    section = extract_news_section(text)
    if section is None:
        return [], {'date': date, 'offline': offline, 'section_found': False, 'n_items': 0}

    items = []
    for block in re.split(r'\n(?=### )', section):
        block = block.strip()
        if not block.startswith('###'):
            continue

        lines = block.splitlines()
        title_m = TITLE_RE.match(lines[0])
        fields = parse_fields(block)

        link_raw = fields.get('链接', '')
        url_m = URL_RE.search(link_raw)

        item = {
            'date': date,
            'index': len(items) + 1,
            'title': title_m.group(1) if title_m else lines[0].lstrip('#').strip(),
            # url 是从"链接"字段里真正提取出的 URL；提取不到说明该字段不是合法链接
            'url': url_m.group(0) if url_m else None,
            'source_file': os.path.relpath(path, REPO_ROOT),
        }
        for f in CAPTURED_FIELDS:
            item[f] = fields.get(f)
        item['score'] = parse_score(fields.get('重要性评分'))

        items.append(item)

    return items, {
        'date': date, 'offline': offline,
        'section_found': True, 'n_items': len(items),
    }


def main():
    briefings = find_briefings()
    if not briefings:
        print(f'没有在 {ARCHIVE_DIR} 找到任何简报', file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    all_items = []
    days = []
    for date, path in briefings:
        items, day_meta = extract_items(date, path)
        all_items.extend(items)
        days.append(day_meta)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    days_path = os.path.join(os.path.dirname(OUT_PATH), 'days.jsonl')
    with open(days_path, 'w', encoding='utf-8') as f:
        for d in days:
            f.write(json.dumps(d, ensure_ascii=False) + '\n')

    no_section = [d['date'] for d in days if not d['section_found']]
    print(f'抽取完成：{len(briefings)} 篇简报 → {len(all_items)} 条新闻')
    print(f'  {OUT_PATH}')
    print(f'  {days_path}')
    if no_section:
        print(f'  ⚠ {len(no_section)} 天找不到新闻板块：{", ".join(no_section)}')


if __name__ == '__main__':
    main()
