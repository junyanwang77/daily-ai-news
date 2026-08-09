#!/usr/bin/env python3
"""
联网评估：逐个访问简报里引用的链接，看它到底存不存在。

这是最硬的幻觉指标——prompt 明确禁止编造链接，但没有任何东西
验证过这条禁令是否被遵守。

⚠ 这个检查的天花板（务必理解，否则会误读结果）：
  "链接今天打不开" ≠ "当时是编造的"。新闻页可能被删除、改版、
  搬迁，这属于正常的链接腐烂。所以结果按"简报发布距今天数"分组：
    · 最近 7 天内的简报就已经死链  → 极可能是编造的
    · 两个月前的简报死链          → 可能只是自然腐烂
  这个检查能证伪"链接全都有效"，但不能单独证明某条是编造的。

用法:
  python3 eval/check_links.py                # 检查全部唯一链接
  python3 eval/check_links.py --limit 30     # 先小规模试跑
  python3 eval/check_links.py --since 2026-08-01
如果本机需要代理，先 export：
  export https_proxy=http://127.0.0.1:7897 http_proxy=http://127.0.0.1:7897
"""
import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date as Date
from urllib.parse import urljoin, urlparse

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
IN_PATH = os.path.join(DATA_DIR, 'items.jsonl')
OUT_PATH = os.path.join(DATA_DIR, 'links.jsonl')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/126.0 Safari/537.36')
TIMEOUT = 20
WORKERS = 6          # 并发上限，对被访问的站点保持克制
DELAY = 0.3          # 每个请求前的间隔，避免把对方打疼


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """自己处理跳转，才能看出"跳到首页"这种软 404。"""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _build_opener():
    """只判断可达性，不做证书校验；跳转自己跟，以便识别软 404。"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    # SSL context 必须在构建 opener 时交给 HTTPSHandler，
    # opener.open() 本身不接受 context 参数。
    return urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ctx), NoRedirect)


OPENER = _build_opener()


def fetch(url):
    """返回 {status, final_url, hops, error}。先 HEAD，被拒再 GET。"""
    current = url
    hops = []
    for _ in range(6):
        for method in ('HEAD', 'GET'):
            req = urllib.request.Request(current, method=method,
                                         headers={'User-Agent': UA,
                                                  'Accept': '*/*'})
            try:
                with OPENER.open(req, timeout=TIMEOUT) as r:
                    return {'status': r.status, 'final_url': current,
                            'hops': hops, 'error': None}
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    loc = e.headers.get('Location')
                    if not loc:
                        return {'status': e.code, 'final_url': current,
                                'hops': hops, 'error': 'redirect without Location'}
                    current = urljoin(current, loc)
                    hops.append(current)
                    break                      # 跟一跳，重新开始
                if e.code == 405 and method == 'HEAD':
                    continue                   # HEAD 不被支持，改用 GET
                return {'status': e.code, 'final_url': current,
                        'hops': hops, 'error': None}
            except Exception as e:             # noqa: BLE001 网络层各种异常都归一处理
                if method == 'GET':
                    return {'status': None, 'final_url': current,
                            'hops': hops, 'error': f'{type(e).__name__}: {e}'}
        else:
            break
    return {'status': None, 'final_url': current, 'hops': hops,
            'error': 'too many redirects'}


def is_root(url):
    return urlparse(url).path.rstrip('/') in ('', '/index.html')


def classify(url, res):
    """把原始结果归成人能看懂的判定。"""
    if res['error']:
        return 'unreachable'
    s = res['status']
    if s == 404 or s == 410:
        return 'dead'
    if s and 400 <= s < 500 and s not in (401, 403, 429):
        return 'dead'
    if s in (401, 403, 429):
        return 'blocked'          # 反爬/需登录，无法判定，不能算死链
    if s and s >= 500:
        return 'server_error'
    # 2xx/3xx：进一步看有没有被悄悄跳到首页（软 404）
    if res['hops'] and not is_root(url) and is_root(res['final_url']):
        return 'soft_404_to_root'
    if res['hops'] and urlparse(url).netloc != urlparse(res['final_url']).netloc:
        return 'cross_host_redirect'
    return 'ok'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=None, help='只检查前 N 个唯一链接')
    ap.add_argument('--since', default=None, help='只检查该日期之后的简报，YYYY-MM-DD')
    args = ap.parse_args()

    if not os.path.exists(IN_PATH):
        print(f'找不到 {IN_PATH}，请先运行 python3 eval/extract.py', file=sys.stderr)
        sys.exit(1)

    items = [json.loads(l) for l in open(IN_PATH, encoding='utf-8') if l.strip()]
    if args.since:
        items = [i for i in items if i['date'] >= args.since]

    # 同一个 URL 只请求一次，但记住它被哪些条目引用
    url_to_items = defaultdict(list)
    for it in items:
        if it.get('url'):
            url_to_items[it['url']].append(it)

    urls = sorted(url_to_items)
    if args.limit:
        urls = urls[:args.limit]

    print(f'待检查 {len(urls)} 个唯一链接（来自 {len(items)} 条新闻）')
    if os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY'):
        print(f'使用代理: {os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")}')
    print()

    results = {}
    done = [0]

    def work(u):
        time.sleep(DELAY)
        res = fetch(u)
        res['verdict'] = classify(u, res)
        results[u] = res
        done[0] += 1
        print(f'\r  进度 {done[0]}/{len(urls)}  {res["verdict"]:<20s}', end='', flush=True)

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        list(ex.map(work, urls))
    print('\r' + ' ' * 50)

    with open(OUT_PATH, 'w', encoding='utf-8') as f:
        for u in urls:
            r = results[u]
            f.write(json.dumps({
                'url': u, 'verdict': r['verdict'], 'status': r['status'],
                'final_url': r['final_url'], 'error': r['error'],
                'cited_by': [f'{i["date"]}#{i["index"]}' for i in url_to_items[u]],
            }, ensure_ascii=False) + '\n')

    report(urls, results, url_to_items)
    print(f'\n明细已写入 {OUT_PATH}')


def report(urls, results, url_to_items):
    verdicts = Counter(results[u]['verdict'] for u in urls)
    total = len(urls)
    print('─' * 62)
    print('链接可达性汇总（按唯一链接计）')
    print('─' * 62)
    labels = {
        'ok': '✓ 正常',
        'soft_404_to_root': '✗ 软404：被跳回首页',
        'cross_host_redirect': '? 跨站跳转',
        'dead': '✗ 死链 (4xx)',
        'unreachable': '✗ 无法连接',
        'server_error': '? 对方 5xx',
        'blocked': '? 被拦截(401/403/429)，无法判定',
    }
    for v, n in verdicts.most_common():
        print(f'  {labels.get(v, v):<28s} {n:4d}  {n / total:6.1%}')

    hard_bad = {'dead', 'unreachable', 'soft_404_to_root'}
    bad_urls = [u for u in urls if results[u]['verdict'] in hard_bad]

    # 按"简报发布距今天数"分组——这是区分"编造"和"自然腐烂"的关键
    today = Date.today()
    print('\n按简报发布距今时长分组的失效率：')
    buckets = [('0-14 天（新，失效≈编造）', 0, 14),
               ('15-45 天', 15, 45),
               ('46 天以上（老，可能自然腐烂）', 46, 10 ** 6)]
    for label, lo, hi in buckets:
        tot = bad = 0
        for u in urls:
            ages = [(today - Date(*map(int, i['date'].split('-')))).days
                    for i in url_to_items[u]]
            if not any(lo <= a <= hi for a in ages):
                continue
            tot += 1
            if results[u]['verdict'] in hard_bad:
                bad += 1
        if tot:
            print(f'  {label:<32s} {bad:3d}/{tot:3d} = {bad / tot:6.1%}')

    if bad_urls:
        print(f'\n失效链接明细（共 {len(bad_urls)} 个）：')
        for u in bad_urls[:25]:
            r = results[u]
            cites = ', '.join(f'{i["date"]}#{i["index"]}' for i in url_to_items[u])
            print(f'  [{r["verdict"]}] {u[:72]}')
            print(f'      被引用于 {cites}')
        if len(bad_urls) > 25:
            print(f'  … 另有 {len(bad_urls) - 25} 个')

    print('\n⚠ 天花板：本检查无法区分"当初就是编造的"和"后来被删了"。')
    print('  只有"新简报里就已失效"的链接才是编造的强证据。')


if __name__ == '__main__':
    main()
