#!/usr/bin/env python3
"""Set the actual public URL in both language pages (canonical, hreflang, OGP,
Article JSON-LD), sitemap.xml and robots.txt. No packages needed. Safe to re-run."""
import argparse, html, json, re
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree.ElementTree import Element, SubElement, ElementTree, register_namespace

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--url', required=True,
               help='Actual HTTPS site root (Japanese page), including the project directory, '
                    'e.g. the URL shown on the GitHub Pages settings screen')
a = p.parse_args(); u = urlsplit(a.url)
if u.scheme != 'https' or not u.hostname or u.username or u.password or u.query or u.fragment:
    p.error('Use an HTTPS URL without credentials, query or fragment.')
root_url = a.url.rstrip('/') + '/'
if root_url.endswith('/index.html/'):
    p.error('Give the site root, without index.html.')

root = Path(__file__).resolve().parents[1]
PAGES = {
    # lang: (file, page URL, og:image:alt)
    'ja': (root / 'index.html', root_url, '整備後のGHISALLOロードバイク'),
    'en': (root / 'en' / 'index.html', root_url + 'en/', 'GHISALLO road bike after the ST-6600 hood replacement'),
}
image = root_url + 'assets/images/hero.webp'
other = {'ja': 'en', 'en': 'ja'}

for lang, (path, url, alt) in PAGES.items():
    s = path.read_text(encoding='utf-8'); e = lambda v: html.escape(v, quote=True)
    meta = (f'\n<link rel="canonical" href="{e(url)}">'
            f'\n<link rel="alternate" hreflang="ja" href="{e(PAGES["ja"][1])}">'
            f'\n<link rel="alternate" hreflang="en" href="{e(PAGES["en"][1])}">'
            f'\n<link rel="alternate" hreflang="x-default" href="{e(PAGES["en"][1])}">'
            f'\n<meta property="og:url" content="{e(url)}">'
            f'\n<meta property="og:image" content="{e(image)}">'
            f'\n<meta property="og:image:width" content="1600">'
            f'\n<meta property="og:image:height" content="1200">'
            f'\n<meta property="og:image:alt" content="{e(alt)}">\n')
    s, n = re.subn(r'<!-- SITE_URL_META_START -->.*?<!-- SITE_URL_META_END -->',
                   lambda _: '<!-- SITE_URL_META_START -->' + meta + '<!-- SITE_URL_META_END -->', s, flags=re.S)
    if n != 1: raise SystemExit(f'SITE_URL_META markers not found in {path}')
    m = re.search(r'(<script type="application/ld\+json" id="article-data">)(.*?)(</script>)', s, re.S)
    if not m: raise SystemExit(f'Article JSON-LD not found in {path}')
    data = json.loads(m[2])
    data.update({'url': url, 'mainEntityOfPage': {'@type': 'WebPage', '@id': url}, 'image': [image]})
    rel = {'@type': 'Article', 'url': PAGES[other[lang]][1], 'inLanguage': other[lang]}
    # Japanese is the original record; English is its translation.
    data.pop('workTranslation', None); data.pop('translationOfWork', None)
    data['workTranslation' if lang == 'ja' else 'translationOfWork'] = rel
    s = s[:m.start(2)] + json.dumps(data, ensure_ascii=False).replace('<', '\\u003c') + s[m.end(2):]
    path.write_text(s, encoding='utf-8')

ns = 'http://www.sitemaps.org/schemas/sitemap/0.9'; xns = 'http://www.w3.org/1999/xhtml'
register_namespace('', ns); register_namespace('xhtml', xns)
tree = Element('{%s}urlset' % ns)
for lang in ('ja', 'en'):
    entry = SubElement(tree, '{%s}url' % ns)
    SubElement(entry, '{%s}loc' % ns).text = PAGES[lang][1]
    for alt_lang in ('ja', 'en'):
        SubElement(entry, '{%s}link' % xns, rel='alternate', hreflang=alt_lang, href=PAGES[alt_lang][1])
    SubElement(entry, '{%s}link' % xns, rel='alternate', hreflang="x-default", href=PAGES["en"][1])
ElementTree(tree).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
(root / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: ' + root_url + 'sitemap.xml\n', encoding='utf-8')
print('Configured canonical, hreflang, OGP, Article, sitemap.xml and robots.txt for')
for lang in ('ja', 'en'): print(f'  {lang}: {PAGES[lang][1]}')
