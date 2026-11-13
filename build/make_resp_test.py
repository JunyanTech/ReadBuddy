# -*- coding: utf-8 -*-
"""Build a copy of the app that opens one story automatically, for narrow and wide viewport checks."""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'ReadBuddy_cn.html')
OUT = os.path.join(HERE, '_resp_story.html')

SEED = "if(document.readyState === 'loading'){ document.addEventListener('DOMContentLoaded', boot); }"
INJECT = ("setTimeout(function(){ try{ openReader('tech11', false); }catch(e){} }, 30);\n" + SEED)

s = io.open(SRC, encoding='utf-8').read()
assert SEED in s
io.open(OUT, 'w', encoding='utf-8').write(s.replace(SEED, INJECT, 1))
print('ok')
