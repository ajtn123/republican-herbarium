"""Regenerate the site's font asset (optional maintenance; requires fontTools).

Collect every source string and data value, including component props and
conditional/dynamic titles. Never limit collection to literal heading tags.
The production build validates rendered serif text against the saved cmap.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset
import hashlib, json, string

root=Path(__file__).resolve().parents[1]
text=string.printable
for p in (root/'src').rglob('*'):
    if p.suffix in {'.astro','.ts','.json'} and p.name!='font-coverage.json':
        text+=p.read_text()
font=TTFont('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc',fontNumber=2)
options=subset.Options()
options.desubroutinize=True
subsetter=subset.Subsetter(options=options)
subsetter.populate(text=text)
subsetter.subset(font)
font.flavor='woff'
coverage=sorted(font.getBestCmap())
asset_dir=root/'public/assets'
temporary=asset_dir/'archive-new.woff'
font.save(temporary)
blob=temporary.read_bytes()
fingerprint=hashlib.sha256(blob).hexdigest()
filename=f'archive-{fingerprint[:12]}.woff'
temporary.replace(asset_dir/filename)
(root/'src/styles/font.css').write_text(
    f"@font-face{{font-family:Archive;src:url('/assets/{filename}') format('woff');font-display:swap;font-style:normal;font-weight:400}}\n"
)
(root/'src/data/font-coverage.json').write_text(json.dumps(
    dict(file=f'assets/{filename}',sha256=fingerprint,codepoints=coverage),
    separators=(',',':')
)+'\n')
for p in asset_dir.glob('archive*.woff'):
    if p.name!=filename:p.unlink()
print(f'Generated {filename}: {len(coverage)} codepoints, {len(blob)} bytes')
