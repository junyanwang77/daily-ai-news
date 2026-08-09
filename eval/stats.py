#!/usr/bin/env python3
"""
离线评估：不联网，只看 extract.py 抽出来的数据集本身能说明什么。

核心问题不是"字段填了没有"（validate_briefing.py 已经保证填了），
而是"填进去的值有没有信息量"。一个 95% 都填"高"的可信度字段，
形式上完全合规，实际上等于没填——它无法区分任何东西。

这里用归一化熵来量化这件事：
  1.0 = 取值均匀分布，区分度最大
  0.0 = 永远是同一个值，完全没有信息量

用法: python3 eval/stats.py
输入: eval/data/items.jsonl, eval/data/days.jsonl
"""
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import date as Date, timedelta
from difflib import SequenceMatcher
from urllib.parse import urlparse

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# validate_briefing.py 允许的取值域，用来算归一化熵的分母
ALLOWED = {
    '核查状态': ['已核实', '部分核实', '未完全核实'],
    '可信度': ['高', '中', '低'],
}
REQUIRED_FIELDS = ['来源', '链接', '核查状态', '发生了什么',
                   '为什么重要', '影响对象', '重要性评分', '可信度']

TITLE_DUP_THRESHOLD = 0.75   # 标题相似度超过这个值视为疑似重复报道


def load(name):
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        print(f'找不到 {path}，请先运行 python3 eval/extract.py', file=sys.stderr)
        sys.exit(1)
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def normalized_entropy(counter, n_allowed):
    """归一化熵：0 = 只有一种取值（无信息量），1 = 均匀分布（区分度最大）。"""
    total = sum(counter.values())
    if total == 0 or n_allowed <= 1:
        return 0.0
    h = -sum((c / total) * math.log(c / total) for c in counter.values() if c > 0)
    return h / math.log(n_allowed)


def bar(frac, width=28):
    filled = int(round(frac * width))
    return '█' * filled + '·' * (width - filled)


def section(title):
    print()
    print('─' * 62)
    print(title)
    print('─' * 62)


def report_coverage(items, days):
    section('1. 覆盖度')
    dates = sorted(d['date'] for d in days)
    first, last = dates[0], dates[-1]
    y1, m1, d1 = map(int, first.split('-'))
    y2, m2, d2 = map(int, last.split('-'))
    span = (Date(y2, m2, d2) - Date(y1, m1, d1)).days + 1

    have = set(dates)
    missing = []
    cur = Date(y1, m1, d1)
    while cur <= Date(y2, m2, d2):
        if cur.isoformat() not in have:
            missing.append(cur.isoformat())
        cur += timedelta(days=1)

    offline_days = [d['date'] for d in days if d['offline']]
    empty_days = [d['date'] for d in days if d['n_items'] == 0]

    print(f'日期范围      : {first} → {last}（跨 {span} 天）')
    print(f'实际有简报    : {len(days)} 天（出勤率 {len(days) / span:.0%}）')
    print(f'新闻条目总数  : {len(items)} 条，日均 {len(items) / len(days):.1f} 条')
    if missing:
        print(f'缺失日期      : {len(missing)} 天 — {", ".join(missing[:8])}'
              + (' …' if len(missing) > 8 else ''))
    if offline_days:
        print(f'⚠ 离线降级天数: {len(offline_days)} 天 — {", ".join(offline_days)}')
    if empty_days:
        print(f'⚠ 零条目天数  : {len(empty_days)} 天 — {", ".join(empty_days)}')

    per_day = Counter(len([i for i in items if i["date"] == d["date"]]) for d in days)
    print('\n每天条目数分布：')
    for n in sorted(per_day):
        print(f'  {n} 条 : {per_day[n]:3d} 天  {bar(per_day[n] / len(days))}')


def report_completeness(items):
    section('2. 字段完整性（validate_briefing.py 已保证，此处复核历史存档）')
    missing = Counter()
    for it in items:
        for f in REQUIRED_FIELDS:
            if not it.get(f):
                missing[f] += 1
    no_url = [it for it in items if not it.get('url')]
    bad_score = [it for it in items if it.get('score') is None
                 or not (1 <= it['score'] <= 10)]

    if not missing and not no_url and not bad_score:
        print('✓ 全部 %d 条新闻，8 个必需字段齐全，链接可提取，评分合法' % len(items))
    else:
        for f, c in missing.most_common():
            print(f'⚠ 缺少「{f}」: {c} 条')
        if no_url:
            print(f'⚠ 「链接」字段里提取不到合法 URL: {len(no_url)} 条')
            for it in no_url[:5]:
                print(f'    {it["date"]} #{it["index"]} {it["title"][:40]}')
        if bad_score:
            print(f'⚠ 重要性评分不在 1-10: {len(bad_score)} 条')


def report_self_assessment(items):
    section('3. 自评字段的信息量 ★ 这是本次评估的核心')
    print('validate_briefing.py 只检查这些字段"填了且取值合法"。')
    print('但如果一个字段几乎永远是同一个值，它就无法区分任何东西。\n')

    for field, allowed in ALLOWED.items():
        counts = Counter(_bucket(it.get(field), allowed) for it in items)
        total = sum(counts.values())
        ent = normalized_entropy(counts, len(allowed))
        print(f'「{field}」  归一化熵 = {ent:.3f}')
        for val in allowed + ['(其他/缺失)']:
            c = counts.get(val, 0)
            if c or val in allowed:
                print(f'    {val:<10s} {c:4d}  {c / total:6.1%}  {bar(c / total)}')
        top_val, top_c = counts.most_common(1)[0]
        print(f'    → 最常见取值「{top_val}」占 {top_c / total:.0%}'
              f'{"，该字段几乎不携带信息" if top_c / total > 0.9 else ""}')
        print()

    scores = [it['score'] for it in items if it.get('score') is not None]
    if scores:
        sc = Counter(scores)
        mean = sum(scores) / len(scores)
        ent = normalized_entropy(sc, 10)
        print(f'「重要性评分」 归一化熵 = {ent:.3f}，均值 {mean:.2f}，'
              f'取值范围 {min(scores)}–{max(scores)}')
        for s in range(1, 11):
            if sc.get(s):
                print(f'    {s:2d} 分   {sc[s]:4d}  {sc[s] / len(scores):6.1%}  '
                      f'{bar(sc[s] / len(scores))}')


def _bucket(raw, allowed):
    """把字段原始值归到允许取值之一（取值可能带后缀，如'高（多方交叉）'）。"""
    if not raw:
        return '(其他/缺失)'
    for a in allowed:
        if raw.startswith(a):
            return a
    return '(其他/缺失)'


def report_redundancy(items):
    section('4. 「核查状态」与「可信度」是不是同一个信号')
    print('如果两个字段总是同进同出，其中一个就是冗余的。\n')
    cross = defaultdict(Counter)
    for it in items:
        s = _bucket(it.get('核查状态'), ALLOWED['核查状态'])
        t = _bucket(it.get('可信度'), ALLOWED['可信度'])
        cross[s][t] += 1

    cols = ALLOWED['可信度'] + ['(其他/缺失)']
    print(f'{"核查状态 \\ 可信度":<18s}' + ''.join(f'{c:>10s}' for c in cols))
    agree = 0
    for s in ALLOWED['核查状态'] + ['(其他/缺失)']:
        row = cross.get(s)
        if not row:
            continue
        print(f'{s:<18s}' + ''.join(f'{row.get(c, 0):>10d}' for c in cols))
    # 「已核实 ↔ 高」视为一致
    for it in items:
        s = _bucket(it.get('核查状态'), ALLOWED['核查状态'])
        t = _bucket(it.get('可信度'), ALLOWED['可信度'])
        if (s, t) in (('已核实', '高'), ('部分核实', '中'), ('未完全核实', '低')):
            agree += 1
    print(f'\n对角线一致率: {agree}/{len(items)} = {agree / len(items):.1%}'
          f'{"  → 两个字段高度冗余" if agree / len(items) > 0.9 else ""}')


def report_sources(items):
    section('5. 信源分布')
    domains = Counter()
    for it in items:
        if it.get('url'):
            host = urlparse(it['url']).netloc.lower()
            domains[host.removeprefix('www.')] += 1
    total = sum(domains.values())
    print(f'唯一域名数: {len(domains)}，覆盖 {total} 条有链接的新闻')
    top1 = domains.most_common(1)[0]
    top5_share = sum(c for _, c in domains.most_common(5)) / total
    print(f'最集中域名: {top1[0]} 占 {top1[1] / total:.1%}；前 5 域名合计 {top5_share:.1%}\n')
    for host, c in domains.most_common(15):
        print(f'  {host:<38s} {c:4d}  {c / total:6.1%}  {bar(c / total, 20)}')
    singles = sum(1 for c in domains.values() if c == 1)
    print(f'\n只出现过一次的域名: {singles} 个（占全部域名 {singles / len(domains):.0%}）')


def report_duplicates(items):
    section('6. 重复报道检测')
    by_url = defaultdict(list)
    for it in items:
        if it.get('url'):
            by_url[it['url']].append(it)
    dup_urls = {u: v for u, v in by_url.items() if len(v) > 1}
    print(f'完全相同的链接在不同条目出现: {len(dup_urls)} 组')
    for u, group in list(dup_urls.items())[:5]:
        dates = ', '.join(f'{g["date"]}#{g["index"]}' for g in group)
        print(f'  {u[:70]}\n      → {dates}')

    # 跨天标题相似：只比较相邻 7 天内的条目，避免 O(n²) 噪音
    print(f'\n跨天标题相似度 > {TITLE_DUP_THRESHOLD}（疑似重复报道）：')
    items_sorted = sorted(items, key=lambda x: (x['date'], x['index']))
    pairs = []
    for i, a in enumerate(items_sorted):
        for b in items_sorted[i + 1:]:
            if a['date'] == b['date']:
                continue
            if _daydiff(a['date'], b['date']) > 7:
                break
            r = SequenceMatcher(None, a['title'], b['title']).ratio()
            if r >= TITLE_DUP_THRESHOLD:
                pairs.append((r, a, b))
    pairs.sort(key=lambda x: -x[0])
    if not pairs:
        print('  ✓ 未发现（7 天窗口内）')
    for r, a, b in pairs[:10]:
        print(f'  {r:.2f}  {a["date"]} 《{a["title"][:32]}》')
        print(f'        {b["date"]} 《{b["title"][:32]}》')
    if len(pairs) > 10:
        print(f'  … 另有 {len(pairs) - 10} 组')


def _daydiff(d1, d2):
    a = Date(*map(int, d1.split('-')))
    b = Date(*map(int, d2.split('-')))
    return abs((b - a).days)


def report_source_link_match(items):
    section('7. 「来源」文字与链接域名是否对得上（启发式，需人工抽查）')
    print('例：来源写"Anthropic官方博客"但链接指向第三方转载，属于口径不一致。')
    print('中文媒体名与域名无法自动对齐，这里只报可疑项，不下结论。\n')
    # 只处理能明确对上的常见域名，其余一律不判断
    known = {
        'anthropic.com': ['anthropic'], 'openai.com': ['openai'],
        'deepmind.google': ['deepmind'], 'blog.google': ['google', '谷歌'],
        'huggingface.co': ['hugging'], 'github.com': ['github'],
        'arxiv.org': ['arxiv', '论文'], 'techcrunch.com': ['techcrunch'],
        'theverge.com': ['verge'], 'reuters.com': ['reuters', '路透'],
        'qbitai.com': ['量子位'], 'jiqizhixin.com': ['机器之心'],
        'ithome.com': ['it之家'], 'sina.com.cn': ['新浪'],
        'eastmoney.com': ['东方财富'], '36kr.com': ['36氪'],
    }
    suspicious = []
    checked = 0
    for it in items:
        if not it.get('url') or not it.get('来源'):
            continue
        host = urlparse(it['url']).netloc.lower().removeprefix('www.')
        base = next((k for k in known if host.endswith(k)), None)
        if not base:
            continue
        checked += 1
        src = it['来源'].lower()
        if not any(kw in src for kw in known[base]):
            suspicious.append((it, host))
    print(f'可自动判定的条目: {checked} 条；其中来源文字未提及该域名: {len(suspicious)} 条')
    for it, host in suspicious[:12]:
        print(f'  {it["date"]} #{it["index"]}  域名 {host}')
        print(f'      来源字段：{it["来源"][:50]}')
    if len(suspicious) > 12:
        print(f'  … 另有 {len(suspicious) - 12} 条')


# 这些路径本身是"栏目列表页"，不是某条具体新闻
INDEX_SEGMENTS = {'news', 'blog', 'updates', 'releases', 'research',
                  'posts', 'index.html', 'articles'}


def report_link_specificity(items):
    section('8. 链接具体性：给的是文章页还是栏目首页 ★')
    print('栏目列表页（如 anthropic.com/news）技术上永远 200 OK，')
    print('但内容天天在变，读者点进去找不到对应那条新闻——')
    print('等于没有提供可核实的来源。check_links.py 抓不到这种问题。\n')

    with_url = [it for it in items if it.get('url')]
    shallow = []
    for it in with_url:
        segs = [s for s in urlparse(it['url']).path.strip('/').split('/') if s]
        if len(segs) == 0 or (len(segs) == 1 and segs[0].lower() in INDEX_SEGMENTS):
            shallow.append(it)

    rate = len(shallow) / len(with_url)
    print(f'疑似栏目首页/站点首页: {len(shallow)} / {len(with_url)} = {rate:.1%}')

    if shallow:
        # 这些条目自己标了什么核查状态？标"已核实"的属于自评失准
        bad = [it for it in shallow
               if _bucket(it.get('核查状态'), ALLOWED['核查状态']) == '已核实']
        print(f'  其中自评「核查状态：已核实」的: {len(bad)} 条 ← 自评与证据不符\n')
        counts = Counter(it['url'] for it in shallow)
        for u, n in counts.most_common(10):
            dates = ', '.join(it['date'] for it in shallow if it['url'] == u)
            print(f'  {n}x  {u}')
            print(f'       {dates}')


def main():
    items = load('items.jsonl')
    days = load('days.jsonl')
    print(f'评估数据集: {len(items)} 条新闻 / {len(days)} 天简报')
    report_coverage(items, days)
    report_completeness(items)
    report_self_assessment(items)
    report_redundancy(items)
    report_sources(items)
    report_duplicates(items)
    report_source_link_match(items)
    report_link_specificity(items)
    print()
    print('─' * 62)
    print('以上全部为离线指标，未验证链接是否真实可达。')
    print('下一步: python3 eval/check_links.py')
    print('─' * 62)


if __name__ == '__main__':
    main()
