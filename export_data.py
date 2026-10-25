import json
from pathlib import Path
from content import MONTHS, RAW, FESTIVALS, DECADES
assert len(RAW)==12
months=[]; days=[]
for i,(meta,raw) in enumerate(zip(MONTHS,RAW)):
    slug,zh,fr,season,color,subtitle,root,desc,story=meta
    months.append(dict(id=i+1,slug=slug,zh=zh,fr=fr,season=season,color=color,subtitle=subtitle,root=root,desc=desc,story=story))
    rows=raw.strip().splitlines()
    assert len(rows)==30,(slug,len(rows))
    for j,row in enumerate(rows):
        parts=row.split('|'); assert len(parts)==4,(slug,j,parts)
        f,z,a,b=parts
        category='动物' if (j+1)%10==5 else '器物' if (j+1)%10==0 else '大地材料' if i==3 else '植物与产物'
        days.append(dict(id=i*30+j+1,month=i+1,day=j+1,slug=f'{slug}-{j+1:02}',fr=f,zh=z,identity=a,story=b,category=category,decade=(j//10)+1,weekday=DECADES[j%10][2]))
out=dict(months=months,days=days,festivals=[dict(zip(['slug','zh','fr','subtitle','identity','story'],f)) for f in FESTIVALS],decades=[dict(zip(['slug','zh','fr','root','text'],d)) for d in DECADES])
Path('src/data/calendar.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('Prepared 12 months, 360 day essays, 6 festivals, 10 decade names')

search=[dict(title=m['zh'],fr=m['fr'],path='/months/'+m['slug']+'/',type='月份') for m in out['months']]
search += [dict(title=d['zh'],fr=d['fr'],path='/days/'+d['slug']+'/',type=out['months'][d['month']-1]['zh']+' '+str(d['day'])+'日 · '+d['category']) for d in out['days']]
search += [dict(title=f['zh']+'节',fr=f['fr'],path='/festivals/'+f['slug']+'/',type='补充日') for f in out['festivals']]
search += [dict(title=d['zh'],fr=d['fr'],path='/decades/'+d['slug']+'/',type='旬日') for d in out['decades']]
Path('public/search-index.json').write_text(json.dumps(search,ensure_ascii=False,separators=(',',':')))
