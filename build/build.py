# -*- coding: utf-8 -*-
"""Inject the story library and per-character pinyin into the template, then write the single-file HTML app."""
import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pypinyin import pinyin, Style
from stories_mc import STORIES_MC
from stories_tech import STORIES_TECH
from stories_life_nature import STORIES_LIFE, STORIES_NATURE
from stories_extra import STORIES_TECH2, STORIES_LIFE2, STORIES_NATURE2
from stories_page4 import PAGE4

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, '..', 'ReadBuddy_cn.html'))
TPL = os.path.join(HERE, 'app_template.html')

# The original 50 stories had 3 pages each; add a fourth page to every one
for s in STORIES_MC + STORIES_TECH + STORIES_LIFE + STORIES_NATURE:
    if s['id'] in PAGE4 and len(s['pages']) == 3:
        s['pages'].append(PAGE4[s['id']])

ALL = (STORIES_MC + STORIES_TECH + STORIES_TECH2
       + STORIES_LIFE + STORIES_LIFE2
       + STORIES_NATURE + STORIES_NATURE2)


def page_pinyin(text):
    """Return a pinyin array aligned character by character with text; punctuation maps to an empty string."""
    res = pinyin(text, style=Style.TONE, heteronym=False, errors=lambda s: [s])
    flat = [x[0] if x else '' for x in res]
    if len(flat) != len(text):
        # Fallback when lengths do not match: per-character pinyin (loses polyphone context, last resort only)
        flat = []
        for ch in text:
            r = pinyin(ch, style=Style.TONE, heteronym=False, errors=lambda s: [s])
            flat.append(r[0][0] if r and r[0] else ch)
    out = []
    for ch, py in zip(text, flat):
        if re.match(r'[\u4e00-\u9fa5]', ch):
            out.append(py)
        else:
            out.append('')
    return out


def main():
    assert len(ALL) == 80, '故事数量应为 80，实际 %d' % len(ALL)
    ids = set()
    per_tag = {}
    data = []
    for s in ALL:
        assert s['id'] not in ids, '重复 id: ' + s['id']
        ids.add(s['id'])
        assert 4 <= len(s['pages']) <= 5, '%s 页数应为 4 页' % s['id']
        per_tag[s['tag']] = per_tag.get(s['tag'], 0) + 1
        pages = []
        for t in s['pages']:
            for ch in t:
                assert ch != '"', '%s 正文里出现了英文引号' % s['id']
            pages.append({'t': t, 'p': page_pinyin(t)})
        data.append({'id': s['id'], 'title': s['title'], 'tag': s['tag'], 'pages': pages})
    for tag in ['我的世界', '科技', '生活', '自然']:
        assert per_tag.get(tag, 0) == 20, '%s 应有 20 篇，实际 %d' % (tag, per_tag.get(tag, 0))

    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    assert '</script' not in payload, '故事文本里出现了 </script，会破坏页面'
    assert '\u2028' not in payload and '\u2029' not in payload

    with open(TPL, 'r', encoding='utf-8') as f:
        tpl = f.read()
    assert '/*__STORIES__*/' in tpl
    html = tpl.replace('/*__STORIES__*/', payload)

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    chars = sum(len(p['t']) for s in data for p in s['pages'])
    print('故事 %d 篇，页 %d，总字数 %d' % (
        len(data),
        sum(len(s['pages']) for s in data),
        chars))
    print('输出: %s' % OUT)
    print('大小: %.1f KB' % (os.path.getsize(OUT) / 1024.0))


if __name__ == '__main__':
    main()
