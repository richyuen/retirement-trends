"""Write dashboard/index.html and dashboard/writes.json (store documents) from
marks.json and blobs.json. Run after build.py: python dashboard/page.py"""
import json, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = 'https://claude.ai/artifact/JTfbBBXQfUrpabgjxiGdqT'
meta = json.load(open(os.path.join(HERE, 'marks.json')))
blobs = json.load(open(os.path.join(HERE, 'blobs.json')))
esc = lambda s: html.escape(s, quote=True)


def enc(s):
    return s.replace('%', '%25').replace('&', '%26').replace('=', '%3D')


def where(r):
    return esc(f"series={enc(r['series'])}&year={enc(r['year'])}")


def cell(m, r, field, cls=''):
    return (f'<span class="{cls}" data-source="{m["id"]}" data-field="{field}" '
            f'data-where="{where(r)}" data-unit="{m["unit"] if field == "value" else ""}">—</span>')


def slug(s):
    return ''.join(c if c.isalnum() else '-' for c in s.lower()).strip('-').replace('--', '-')


parts = []
for m in meta:
    if m['part'] not in parts:
        parts.append(m['part'])

cards = {p: [] for p in parts}
for m in meta:
    h, b = m['head'], m['base']
    out = [f'<article class="rt-card" id="c-{m["id"]}">',
           f'<h3 class="rt-q">{esc(m["q"])}</h3>',
           f'<div class="rt-kpi">{cell(m, h, "value", "rt-big dash-skeleton")}</div>',
           f'<p class="rt-cap">{esc(h["series"])}, {cell(m, h, "year")}</p>']
    if b:
        out.append(f'<p class="rt-from">From {cell(m, b, "value")} in {cell(m, b, "year")}</p>')
    if m['extra']:
        bits = ' · '.join(f'{esc(e["series"])} {cell(m, e, "value")}' for e in m['extra'])
        out.append(f'<p class="rt-from">{bits}</p>')
    out += [f'<div class="rt-legend" data-source="{m["id"]}"></div>',
            f'<div class="rt-chart dash-skeleton" data-source="{m["id"]}" data-id="{m["id"]}"></div>',
            f'<p class="rt-src">{esc(m["desc"])}</p>',
            f'<a class="rt-link" href="{REPORT}#{m["sec"][0]}" target="_blank" rel="noopener">'
            f'In the report: {esc(m["sec"][1])} →</a>',
            '</article>']
    cards[m['part']].append('\n'.join(out))

cfg = {m['id']: {'order': m['order'], 'breaks': m['breaks'], 'unit': m['unit'], 'head': m['head']['series']}
       for m in meta}

nav = ''.join(f'<button class="rt-chip" data-target="p-{slug(p)}">{esc(p)}</button>' for p in parts)
sections = '\n'.join(
    f'<section class="rt-part" id="p-{slug(p)}"><h2 class="rt-h2">{esc(p)}</h2>'
    f'<div class="rt-grid">{"".join(cards[p])}</div></section>' for p in parts)

CSS = open(os.path.join(HERE, 'page.css')).read()
JS = open(os.path.join(HERE, 'page.js')).read()
page = f'''<style>{CSS}</style>
<div class="rt">
<header class="rt-head" id="top">
<h1 class="rt-title">Retirement trends</h1>
<p class="rt-take">Withdrawals follow the required-distribution rules, more workers save in DC plans, and the older cushions (DB pensions, Social Security's trust funds, annuities) keep shrinking while people live and work longer.</p>
<p class="rt-meta">Headline indicators from the <a href="{REPORT}" target="_blank" rel="noopener">Retirement account withdrawals report</a>, each with its trend, source and years. Hover a chart for values.</p>
<nav class="rt-nav">{nav}</nav>
</header>
{sections}
</div>
<script>window.RT_CFG = {json.dumps(cfg, ensure_ascii=False)};</script>
<script>{JS}</script>
'''
open(os.path.join(HERE, 'index.html'), 'w').write(page)

now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
writes = [{'op': 'set', 'collection': 'dash', 'doc_id': 'meta', 'data': {'title': 'Retirement Trends Dashboard'}}]
for m in meta:
    writes.append({'op': 'set', 'collection': 'datasets', 'doc_id': m['id'], 'data': {
        'title': m['title'], 'description': m['desc'] + ' Values as charted in the report (version 17).',
        'source': {'kind': 'file', 'url': blobs[m['id']], 'name': m['id'] + '.json', 'format': 'json'},
        'updated': {'at': now, 'by': 'Claude'}}})
writes.append({'op': 'set', 'collection': 'files', 'doc_id': 'index.html', 'data': {'text': page}})
json.dump(writes, open(os.path.join(HERE, 'writes.json'), 'w'), ensure_ascii=False)
print(len(page), 'bytes;', len(writes), 'writes')
