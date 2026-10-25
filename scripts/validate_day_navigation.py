"""Check the actual generated calendar reading path, including year boundaries."""
from html.parser import HTMLParser
from pathlib import Path

root=Path(__file__).resolve().parents[1]/'dist'
class Navigation(HTMLParser):
    def __init__(self):
        super().__init__();self.active=False;self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='nav' and 'day-pagination' in attrs.get('class','').split():self.active=True
        if self.active and tag=='a':self.links.append(attrs)
    def handle_endtag(self,tag):
        if tag=='nav':self.active=False

routes={'/'+str(p.parent.relative_to(root))+'/' for folder in ['days','festivals'] for p in (root/folder).glob('*/index.html')}
assert len(routes)==366,f'Expected 366 day pages, found {len(routes)}'
graph={}
for route in routes:
    parser=Navigation();parser.feed((root/route.lstrip('/')/'index.html').read_text())
    links=parser.links
    assert len(links)==3,f'{route}: expected exactly previous/group/next links'
    assert links[0].get('rel')=='prev' and links[2].get('rel')=='next',route
    group='/festivals/' if route.startswith('/festivals/') else '/months/'+route.split('/')[2].rsplit('-',1)[0]+'/'
    assert links[1]['href']==group,f'{route}: wrong overview link'
    graph[route]=(links[0]['href'],links[2]['href'])
for route,(previous,next_) in graph.items():
    assert previous in graph and next_ in graph,f'{route}: navigation skips to a non-day page'
    assert graph[previous][1]==route and graph[next_][0]==route,f'{route}: previous and next are not reciprocal'
start='/days/vendemiaire-01/';current=start;visited=set()
for _ in range(367):
    if current in visited:break
    visited.add(current);current=graph[current][1]
assert current==start and visited==routes,'Reading path must visit all 366 days exactly once before returning'
assert graph['/days/fructidor-30/'][1]=='/festivals/vertu/'
assert graph['/festivals/vertu/'][0]=='/days/fructidor-30/'
assert graph['/festivals/revolution/'][1]==start
assert graph[start][0]=='/festivals/revolution/'
print('Day navigation: complete 366-page cycle, reciprocal links, overview groups and complementary-day boundaries passed.')
