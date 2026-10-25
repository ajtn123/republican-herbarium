"""Check actual rendered serif text against the shipped font, using stdlib only."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'src/data/font-coverage.json').read_text())
font=root/'dist'/manifest['file']
assert hashlib.sha256(font.read_bytes()).hexdigest()==manifest['sha256'],'Font coverage manifest does not match shipped asset'
coverage=set(manifest['codepoints'])
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SERIF_CLASSES={'brand','root-line','dialog-top','today-strip'}
class SerifText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.text=''
    def handle_starttag(self,tag,attrs):
        parent=self.stack[-1][1] if self.stack else False
        classes=set(dict(attrs).get('class','').split())
        active=parent or tag in {'h1','h2','h3','output'} or bool(classes & SERIF_CLASSES)
        if tag in {'script','style'} or 'sun-mark' in classes:active=False
        if tag not in VOID:self.stack.append((tag,active))
    def handle_startendtag(self,tag,attrs):
        pass
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                self.stack=self.stack[:i]
                break
    def handle_data(self,data):
        if self.stack and self.stack[-1][1]:self.text+=data

files=list((root/'dist').rglob('*.html'))
missing={}
for p in files:
    html=p.read_text()
    assert chr(0x2197) not in html,f'Banned northeast arrow remains: {p}'
    parser=SerifText();parser.feed(html)
    absent={c for c in parser.text if c.isprintable() and not c.isspace() and ord(c) not in coverage}
    if absent:missing[str(p.relative_to(root/'dist'))]=''.join(sorted(absent))
for p in (root/'dist').rglob('*.js'):
    s=p.read_text()
    assert chr(0x2197) not in s and '\\u2197' not in s,f'Banned arrow in script: {p}'
assert not missing,'Missing serif glyphs; regenerate with scripts/subset_font.py: '+json.dumps(missing,ensure_ascii=False)
print(f'Typography: all rendered serif text covered across {len(files)} pages; no northeast arrows in HTML or scripts.')
