#!/usr/bin/env python3
"""
Convert daily AI briefing .md to mobile .html
Usage: python3 make_html.py YYYY-MM-DD
Creates: daily-ai-briefing-YYYY-MM-DD-mobile.html
"""
import sys, re, os, html as H

# ── inline markdown ──────────────────────────────────────────────────────────

def inline(text):
    """Convert markdown inline elements to HTML: links, bold."""
    phs = {}
    n = [0]
    def ph(v):
        k = f'_P{n[0]}_'; n[0] += 1; phs[k] = v; return k

    # Extract markdown links [label](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^\)\s]+)\)',
        lambda m: ph(f'<a href="{H.escape(m.group(2), quote=True)}" target="_blank">{H.escape(m.group(1))}</a>'),
        text
    )
    # Extract raw URLs
    text = re.sub(
        r'https?://\S+',
        lambda m: ph(f'<a href="{H.escape(m.group(), quote=True)}" target="_blank">{H.escape(m.group())}</a>'),
        text
    )
    # Escape remaining HTML
    text = H.escape(text)
    # Restore link placeholders
    for k, v in phs.items():
        text = text.replace(k, v)
    # Bold **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text

# ── block renderers ──────────────────────────────────────────────────────────

def render_prose(text):
    """Render multi-paragraph text: paragraphs, numbered/bullet lists."""
    parts = []
    ol_items = []

    for chunk in re.split(r'\n{2,}', text.strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        first = lines[0].strip()

        if re.match(r'^\d+\.', first):
            for line in lines:
                m = re.match(r'^\d+\.\s*(.*)', line.strip())
                if m:
                    ol_items.append(f'<li>{inline(m.group(1))}</li>')
        else:
            if ol_items:
                parts.append(f'<ol>{"".join(ol_items)}</ol>')
                ol_items = []
            if re.match(r'^[-*]\s', first):
                items = [f'<li>{inline(re.sub(r"^[-*]\s+", "", l.strip()))}</li>'
                         for l in lines if re.match(r'^[-*]\s', l.strip())]
                parts.append(f'<ul>{"".join(items)}</ul>')
            else:
                parts.append(f'<p>{inline(chunk)}</p>')

    if ol_items:
        parts.append(f'<ol>{"".join(ol_items)}</ol>')
    return '\n'.join(parts)

def render_summary(text):
    """Render 先说结论 as a bullet list."""
    items = [f'<li>{inline(re.sub(r"^[-*]\s+", "", l.strip()))}</li>'
             for l in text.splitlines() if re.match(r'^[-*\*]\s', l.strip())]
    if items:
        return f'<ul class="summary-list">{"".join(items)}</ul>'
    return f'<p class="summary-list">{inline(text.strip())}</p>'

def parse_news_fields(lines):
    """Parse bullet lines of a news item into a dict."""
    FIELDS = ['来源', '链接', '核查状态', '发生了什么', '为什么重要',
              '影响对象', '重要性评分', '可信度', '备注']
    fields = {}
    for line in lines:
        line = line.strip()
        if not re.match(r'^[-*]\s', line):
            continue
        content = re.sub(r'^[-*]\s+', '', line).strip().strip('*')
        for fname in FIELDS:
            m = re.match(rf'^{re.escape(fname)}\*?[：:]\*?\s*(.*)', content)
            if m:
                fields[fname] = m.group(1).strip().strip('*').strip()
                break
    return fields

def render_news_card(block):
    """Render a ### news item block as an HTML card."""
    lines = block.strip().splitlines()
    title = ''
    bullets = []
    for line in lines:
        s = line.strip()
        if re.match(r'^###\s+', s):
            title = re.sub(r'^###\s+', '', s)
        elif re.match(r'^[-*]\s', s):
            bullets.append(line)

    f = parse_news_fields(bullets)
    what    = f.get('发生了什么', '')
    why     = f.get('为什么重要', '')
    source  = f.get('来源', '')
    link    = f.get('链接', '')
    check   = f.get('核查状态', '')
    affects = f.get('影响对象', '')
    score   = f.get('重要性评分', '')
    trust   = f.get('可信度', '')
    note    = f.get('备注', '')

    meta = []
    if source:  meta.append(f'<li><strong>来源：</strong>{inline(source)}</li>')
    if link:    meta.append(f'<li><strong>链接：</strong>{inline(link)}</li>')
    if check:   meta.append(f'<li><strong>核查状态：</strong>{H.escape(check)}</li>')
    if affects: meta.append(f'<li><strong>影响对象：</strong>{H.escape(affects)}</li>')
    if score:   meta.append(f'<li><strong>重要性评分：</strong>{H.escape(score)}</li>')
    if trust:   meta.append(f'<li><strong>可信度：</strong>{H.escape(trust)}</li>')
    if note:    meta.append(f'<li><strong>备注：</strong>{inline(note)}</li>')

    meta_html = ''
    if meta:
        meta_html = f'''  <details class="meta">
    <summary>来源 · 核查 · 评分</summary>
    <ul>{"".join(meta)}</ul>
  </details>'''

    return f'''<div class="news-card">
  <h3>{inline(title)}</h3>
  {'<p class="what"><strong>发生了什么：</strong>' + inline(what) + '</p>' if what else ''}
  {'<p class="why"><strong>为什么重要：</strong>' + inline(why) + '</p>' if why else ''}
{meta_html}
</div>'''

def render_tracking(text):
    """Render 持续关注 bullet items as tracking cards."""
    cards = []
    for line in text.splitlines():
        s = line.strip()
        if re.match(r'^[-*]\s', s):
            content = re.sub(r'^[-*]\s+', '', s)
            cards.append(f'<div class="tracking-card"><p>{inline(content)}</p></div>')
    return '\n'.join(cards)

def render_sources(text):
    """Render 来源链接 as a numbered list."""
    items = []
    for line in text.splitlines():
        s = line.strip()
        if re.match(r'^\d+\.', s):
            content = re.sub(r'^\d+\.\s*', '', s)
            items.append(f'<li>{inline(content)}</li>')
        elif s:
            items.append(f'<li>{inline(s)}</li>')
    if items:
        return f'<ol class="source-list">{"".join(items)}</ol>'
    return render_prose(text)

# ── CSS ─────────────────────────────────────────────────────────────────────

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
  font-size: 17px;
  line-height: 1.75;
  background: #f2f2f7;
  color: #1c1c1e;
  padding: 16px;
}
.container { max-width: 720px; margin: 0 auto; }
.page-header {
  background: #111;
  color: #fff;
  border-radius: 16px;
  padding: 22px 20px 20px;
  margin-bottom: 16px;
}
.page-header h1 { font-size: 22px; font-weight: 800; margin-bottom: 6px; }
.page-header .meta-info { font-size: 13px; color: rgba(255,255,255,.55); }
.section { margin-bottom: 24px; }
.section-title {
  font-size: 13px;
  font-weight: 700;
  color: #888;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.summary-box {
  background: #fff;
  border-left: 4px solid #0b57d0;
  border-radius: 12px;
  padding: 16px 18px;
}
ul.summary-list { list-style: none; padding: 0; }
ul.summary-list li { padding: 4px 0; font-size: 15px; color: #333; line-height: 1.65; }
ul.summary-list li::before { content: "· "; color: #0b57d0; font-weight: 700; }
.news-card {
  background: #fff;
  border: 1px solid #eee;
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 14px;
}
.news-card h3 { font-size: 16px; font-weight: 700; margin: 0 0 10px; line-height: 1.4; }
.news-card .what, .news-card .why {
  font-size: 15px; color: #333; line-height: 1.7; margin: 6px 0;
}
details.meta { margin-top: 12px; }
details.meta summary {
  font-size: 12px; color: #aaa; cursor: pointer; list-style: none;
  padding: 8px 0 0; border-top: 1px solid #f0f0f0;
  -webkit-tap-highlight-color: transparent;
}
details.meta summary::-webkit-details-marker { display: none; }
details.meta summary::before { content: "▸  "; }
details.meta[open] summary::before { content: "▾  "; }
details.meta ul { margin: 10px 0 0; padding: 0; list-style: none; font-size: 13px; color: #666; line-height: 1.6; }
details.meta ul li { padding: 3px 0; word-break: break-all; }
details.meta a { color: #0b57d0; word-break: break-all; }
.tracking-card {
  background: #f8f8f8; border-radius: 10px; padding: 14px 16px;
  margin-bottom: 10px; font-size: 14px; color: #555; line-height: 1.6;
}
.section-card {
  background: #fff; border-radius: 14px; padding: 18px; margin-bottom: 14px;
  font-size: 15px; color: #333; line-height: 1.7;
}
.section-card p { margin-bottom: 10px; }
.section-card p:last-child { margin-bottom: 0; }
.section-card ol, .section-card ul { padding-left: 20px; margin-bottom: 10px; }
.section-card li { margin-bottom: 6px; }
.judgment-card {
  background: #f0f7ff; border-left: 4px solid #0b57d0; border-radius: 12px;
  padding: 18px; font-size: 15px; color: #1c3a6e; line-height: 1.75;
}
.judgment-card p { margin-bottom: 10px; }
.judgment-card p:last-child { margin-bottom: 0; }
ol.source-list {
  background: #fff; border-radius: 14px; padding: 18px 18px 18px 36px;
  font-size: 13px; color: #555; line-height: 1.7;
}
ol.source-list li { margin-bottom: 8px; word-break: break-all; }
ol.source-list a { color: #0b57d0; }
.check-card {
  background: #fffaf0; border-radius: 12px; padding: 16px 18px;
  font-size: 14px; color: #666; line-height: 1.7;
}
.check-card p { margin-bottom: 8px; }
.check-card p:last-child { margin-bottom: 0; }
.check-card ul { padding-left: 18px; }
.offline-notice {
  background: #fff3cd; color: #856404; border-radius: 12px;
  padding: 14px 16px; margin-bottom: 16px; font-size: 15px;
}
a { color: #0b57d0; word-break: break-all; }
"""

# ── HTML wrapper ─────────────────────────────────────────────────────────────

def make_html(date, body):
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>每日 AI 要闻 - {H.escape(date)}</title>
<style>{CSS}</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>"""

# ── main parser ──────────────────────────────────────────────────────────────

def convert(md_text, date):
    # Split into ## sections; sections[0] is text before first ##
    sections = re.split(r'\n(?=## )', md_text)
    header_block = sections[0]

    doc_date = date
    m = re.search(r'日期[：:]\s*(\d{4}-\d{2}-\d{2})', header_block)
    if m:
        doc_date = m.group(1)

    parts = []

    # Page header
    parts.append(f'''<div class="page-header">
  <h1>每日 AI 要闻</h1>
  <div class="meta-info">{H.escape(doc_date)} &nbsp;|&nbsp; 过去 24 小时</div>
</div>''')

    # Offline notice
    if '本次未能联网获取实时新闻' in header_block:
        parts.append('<div class="offline-notice">⚠️ 本次未能联网获取实时新闻，以下内容不代表真实的过去 24 小时 AI 要闻。</div>')

    for section in sections[1:]:
        lines = section.strip().splitlines()
        if not lines:
            continue
        title = re.sub(r'^##\s+', '', lines[0].strip())
        content = '\n'.join(lines[1:]).strip()

        if '先说结论' in title:
            parts.append(f'''<div class="section">
  <div class="section-title">先说结论</div>
  <div class="summary-box">{render_summary(content)}</div>
</div>''')

        elif '最值得关注' in title or '件事' in title:
            items = re.split(r'\n(?=### )', content)
            note = items[0].strip() if not items[0].strip().startswith('###') else ''
            cards = '\n'.join(render_news_card(i) for i in items if i.strip().startswith('###'))
            note_html = f'<p style="font-size:14px;color:#888;margin-bottom:12px;">{H.escape(note)}</p>' if note else ''
            parts.append(f'''<div class="section">
  <div class="section-title">{H.escape(title)}</div>
  {note_html}
  {cards}
</div>''')

        elif '持续关注' in title:
            tracking = render_tracking(content)
            if tracking:
                parts.append(f'''<div class="section">
  <div class="section-title">持续关注</div>
  {tracking}
</div>''')

        elif '我的判断' in title:
            parts.append(f'''<div class="section">
  <div class="section-title">我的判断</div>
  <div class="judgment-card">{render_prose(content)}</div>
</div>''')

        elif '来源链接' in title:
            parts.append(f'''<div class="section">
  <div class="section-title">来源链接</div>
  {render_sources(content)}
</div>''')

        elif '核查说明' in title:
            parts.append(f'''<div class="section">
  <div class="section-title">核查说明</div>
  <div class="check-card">{render_prose(content)}</div>
</div>''')

        else:
            # Generic section (影响 sections etc.)
            parts.append(f'''<div class="section">
  <div class="section-title">{H.escape(title)}</div>
  <div class="section-card">{render_prose(content)}</div>
</div>''')

    return make_html(date, '\n'.join(parts))


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 make_html.py YYYY-MM-DD', file=sys.stderr)
        sys.exit(1)

    date = sys.argv[1]
    base = os.path.dirname(os.path.abspath(__file__))
    md_path   = os.path.join(base, f'daily-ai-briefing-{date}.md')
    html_path = os.path.join(base, f'daily-ai-briefing-{date}-mobile.html')

    if not os.path.exists(md_path):
        print(f'Error: {md_path} not found', file=sys.stderr)
        sys.exit(1)

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    html_out = convert(md_text, date)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_out)

    print(f'OK: {html_path}')


if __name__ == '__main__':
    main()
