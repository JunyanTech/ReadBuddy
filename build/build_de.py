# -*- coding: utf-8 -*-
"""Build the German edition (ReadBuddy_de.html) from the German template and story data.

Unlike the Chinese build there is no pinyin: German stories are read word by word,
so the payload only needs title/tag/pages.
"""
import json
import os

from stories_de_mc import STORIES_DE_MC
from stories_de_tech import STORIES_DE_TECH
from stories_de_alltag import STORIES_DE_ALLTAG
from stories_de_natur import STORIES_DE_NATUR

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(HERE, 'app_template_de.html')
OUT = os.path.join(HERE, '..', 'ReadBuddy_de.html')

STORIES = STORIES_DE_MC + STORIES_DE_TECH + STORIES_DE_ALLTAG + STORIES_DE_NATUR

# ---------- Content checks ----------
assert len(STORIES) == 80, 'expected 80 stories, got %d' % len(STORIES)
ids = [s['id'] for s in STORIES]
assert len(set(ids)) == len(ids), 'duplicate story ids'
titles = [s['title'] for s in STORIES]
assert len(set(titles)) == len(titles), 'duplicate titles'

TAGS = ['Minecraft', 'Technik', 'Alltag', 'Natur']
for tag in TAGS:
    assert len([s for s in STORIES if s['tag'] == tag]) == 20, 'tag %s must have 20 stories' % tag

for s in STORIES:
    assert 4 <= len(s['pages']) <= 5, '%s: unexpected page count' % s['id']
    assert len(s['title']) <= 60, '%s: title too long' % s['id']
    for i, page in enumerate(s['pages'], 1):
        assert page.strip(), '%s page %d is empty' % (s['id'], i)
        assert '"' not in page, '%s page %d contains a straight double quote' % (s['id'], i)
        assert '\\' not in page, '%s page %d contains a backslash' % (s['id'], i)

payload = json.dumps(STORIES, ensure_ascii=False, separators=(',', ':'))
assert '</script' not in payload.lower()
assert '\u2028' not in payload and '\u2029' not in payload

html = open(TPL, encoding='utf-8').read()
assert '/*__STORIES__*/' in html, 'story placeholder missing in template'
html = html.replace('/*__STORIES__*/', payload)

with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)

pages = sum(len(s['pages']) for s in STORIES)
words = sum(len(p.split()) for s in STORIES for p in s['pages'])
size_kb = os.path.getsize(OUT) / 1024.0
print('stories %d, pages %d, words %d' % (len(STORIES), pages, words))
print('written %s (%.1f KB)' % (os.path.abspath(OUT), size_kb))
