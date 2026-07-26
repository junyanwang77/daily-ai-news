#!/usr/bin/env python3
"""
Validate a generated daily briefing Markdown file against structural
and business rules from prompts/daily_ai_briefing.md, before it gets
rendered to HTML and published.

Usage: python3 validate_briefing.py YYYY-MM-DD
Exit code 0 = pass, 1 = fail (errors printed to stderr).
"""
import sys, re, os

REQUIRED_SECTIONS = [
    ('先说结论', r'先说结论'),
    ('今日最值得关注的...件事', r'今日最值得关注的.*件事'),
    ('对普通人的影响', r'对普通人的影响'),
    ('对学习者 / 开发者的影响', r'对学习者\s*/\s*开发者的影响'),
    ('对创业者的影响', r'对创业者的影响'),
    ('我的判断', r'我的判断'),
    ('来源链接', r'来源链接'),
    ('核查说明', r'核查说明'),
]

REQUIRED_FIELDS = ['来源', '链接', '核查状态', '发生了什么', '为什么重要', '影响对象', '重要性评分', '可信度']
CHECK_STATUS_VALUES = ['已核实', '部分核实', '未完全核实']
TRUST_VALUES = ['高', '中', '低']

URL_RE = re.compile(r'https?://[^\s\)\]，；;]+')
FIELD_LINE_RE = re.compile(r'^[-*]\s+\*{0,2}([^*：:]+?)\*{0,2}\s*[：:]\s*(.*)$')


def parse_fields(item_text):
    fields = {}
    for line in item_text.splitlines():
        m = FIELD_LINE_RE.match(line.strip())
        if m:
            value = m.group(2).strip().lstrip('*').strip()
            fields[m.group(1).strip()] = value
    return fields


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 validate_briefing.py YYYY-MM-DD', file=sys.stderr)
        sys.exit(1)

    date = sys.argv[1]
    path = f'daily-ai-briefing-{date}.md'
    errors = []

    if not os.path.exists(path):
        print(f'VALIDATE FAIL: Markdown file not found: {path}', file=sys.stderr)
        sys.exit(1)

    text = open(path, encoding='utf-8').read()

    m = re.search(r'日期[：:]\s*(\d{4}-\d{2}-\d{2})', text)
    if not m:
        errors.append('找不到"日期：YYYY-MM-DD"字段')
    elif m.group(1) != date:
        errors.append(f'日期字段（{m.group(1)}）与预期发布日期（{date}）不一致')

    offline = '未能联网获取实时新闻' in text

    sections = re.split(r'\n(?=## )', text)
    titles = [s.strip().splitlines()[0] for s in sections[1:] if s.strip()]

    for label, pattern in REQUIRED_SECTIONS:
        if not any(re.search(pattern, t) for t in titles):
            errors.append(f'缺少必需板块：{label}')

    news_section = None
    for s in sections[1:]:
        if re.match(r'^##\s+今日最值得关注的.*件事', s.strip().splitlines()[0]):
            news_section = s
            break

    news_items = []
    if news_section:
        for block in re.split(r'\n(?=### )', news_section):
            if block.strip().startswith('###'):
                news_items.append(block)

    if not offline:
        if len(news_items) == 0:
            errors.append('"今日最值得关注"板块没有解析到任何新闻条目')
        if len(news_items) > 5:
            errors.append(f'新闻条目数量超过 5 条（实际 {len(news_items)} 条）')

        for idx, item in enumerate(news_items, 1):
            fields = parse_fields(item)

            for fname in REQUIRED_FIELDS:
                if not fields.get(fname):
                    errors.append(f'第 {idx} 条新闻缺少字段：{fname}')

            status = fields.get('核查状态', '')
            if status and not any(status.startswith(v) for v in CHECK_STATUS_VALUES):
                errors.append(f'第 {idx} 条新闻「核查状态」取值不合法：{status}')

            trust = fields.get('可信度', '')
            if trust and not any(trust.startswith(v) for v in TRUST_VALUES):
                errors.append(f'第 {idx} 条新闻「可信度」取值不合法：{trust}')

            score = fields.get('重要性评分', '')
            score_m = re.match(r'^(\d+)', score)
            if not score_m or not (1 <= int(score_m.group(1)) <= 10):
                errors.append(f'第 {idx} 条新闻「重要性评分」不是 1-10 之间的整数：{score!r}')

            link = fields.get('链接', '')
            if link and not URL_RE.search(link):
                errors.append(f'第 {idx} 条新闻「链接」没有找到有效 URL：{link!r}')

    if errors:
        for e in errors:
            print(f'VALIDATE FAIL: {e}', file=sys.stderr)
        sys.exit(1)

    print(f'OK: {path} 通过校验（{len(news_items)} 条新闻{"，离线模式" if offline else ""}）')


if __name__ == '__main__':
    main()
