# -*- coding: utf-8 -*-
"""Self-check copy: verify that alignment marks only the characters actually read. Results are written into a DOM attribute."""
import io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'ReadBuddy_cn.html')
OUT = os.path.join(HERE, '_align_test.html')

SEED = """if(document.readyState === 'loading'){ document.addEventListener('DOMContentLoaded', boot); }"""

TEST = r"""
setTimeout(function(){
  function reset(){
    R.status = R.chars.map(function(){ return 0; });
    R.manual = {};
    R.cursor = 0; R.hypDone = 0;
    R.heard = ''; R.finalHeard = '';
  }
  function read(t){
    R.heard = t; R.finalHeard = t;
    doAlign();
    var blue = [], red = [];
    for(var k=0;k<R.status.length;k++){
      if(R.status[k]===1) blue.push(k);
      if(R.status[k]===2) red.push(k);
    }
    return { blueN: blue.length, blueMin: blue[0], blueMax: blue[blue.length-1],
             red: red, redChars: red.map(function(i){ return R.chars[i].c; }).join(''),
             cursor: R.cursor, hypDone: R.hypDone };
  }
  var res = {};
  try{
    openReader(STORIES[0].id, false);

    // A：只读一个「一」
    reset();
    res.single = read('一');

    // B：正常读前 20 字，第 10 个读错、第 15 个漏读
    reset();
    var p0 = R.story.pages[0].t;
    var plain = [];
    for(var i=0;i<p0.length;i++){ if(!isPunct(p0.charAt(i))) plain.push(p0.charAt(i)); }
    var t = '';
    for(var j=0;j<20;j++){
      if(j===9) t += '错';
      else if(j===14) continue;
      else t += plain[j];
    }
    res.read20 = read(t);

    // C：接着往后读 10 个字（累计转写）
    var t2 = t;
    for(var j2=20;j2<30;j2++) t2 += plain[j2];
    res.read30 = read(t2);

    // D：重复播报同一段，不应继续变蓝
    res.dup = read(t2);
  }catch(e){ res.err = e.message; }
  document.getElementById('rdSub').setAttribute('data-test', JSON.stringify(res));
}, 0);
"""

s = io.open(SRC, encoding='utf-8').read()
assert SEED in s
io.open(OUT, 'w', encoding='utf-8').write(s.replace(SEED, TEST + '\n' + SEED, 1))
print('ok')
