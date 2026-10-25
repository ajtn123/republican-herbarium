# Optional asset maintenance utility, requires fontTools. Not part of the production build.
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
import json,re,string
root=Path(__file__).resolve().parents[1]
data=json.loads((root/'src/data/calendar.json').read_text())
text=string.printable+'把时间，还给自然。共和历时间的自然史下一页第旬年月日春夏秋冬'
for key in ['months','days','festivals','decades']:
 for item in data[key]:
  for k in ['zh','fr','root']:
   text+=item.get(k,'')
for p in (root/'src').rglob('*.astro'):
 s=p.read_text()
 for tag in ['h1','h2','h3']:
  text+=''.join(re.findall(r'<'+tag+r'[^>]*>(.*?)</'+tag+r'>',s,re.S))
text+='年季时分秒在两种日期之间往返太阳年的余数时钟第一二三四五六七八九十百千'
f=TTFont('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',fontNumber=2)
o=subset.Options();o.desubroutinize=True
s=subset.Subsetter(options=o);s.populate(text=text);s.subset(f);f.flavor='woff';f.save(root/'public/assets/archive.woff')
print('Font:',(root/'public/assets/archive.woff').stat().st_size)
