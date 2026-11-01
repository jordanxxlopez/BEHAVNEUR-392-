from pathlib import Path
from lxml import html, etree
import re, json, hashlib, shutil, zipfile, copy

WORK=Path(__file__).parent
OUT=WORK/'lemon_capture'
turns={}
sources={}
for p in sorted(WORK.glob('*.html')):
    root=html.fromstring(p.read_text())
    for el in root.xpath('//*[@data-content-search-turn-key]'):
        key=el.get('data-content-search-turn-key','')
        if not key.startswith('fallback-turn-'):continue
        n=int(key.rsplit('-',1)[1])
        # Only the rendered conversation subtree; scripts and app state are excluded.
        for bad in el.xpath('.//script|.//style|.//svg|.//input|.//textarea|.//*[@aria-hidden="true"]'):
            if bad.getparent() is not None:bad.drop_tree()
        for b in el.xpath('.//button'):
            text=b.text_content().strip()
            if re.search(r'\.(txt|md|pdf|zip|png|jpg|pptx)\b',text,re.I):b.tag='span';b.attrib.clear()
            else:b.drop_tree()
        score=len(el.text_content())
        if n not in turns or score>turns[n][0]:turns[n]=(score,copy.deepcopy(el),p)
assert set(turns)==set(range(77)),sorted(set(range(77))-set(turns))
images=OUT/'attachments/browser_images';images.mkdir(parents=True,exist_ok=True)
sections=[]
md=['# Lemon — Rewrite for Readability\n\nCaptured from the displayed Edge conversation on 2026-10-31. This is extracted message content, not a summary or native account export. UI formatting and whitespace are normalized. Attachments and unavailable tool-session files are tracked separately.\n']
def markdown(e):
    tag=e.tag if isinstance(e.tag,str) else ''
    body=(e.text or '')+''.join(markdown(c)+(c.tail or '') for c in e)
    if tag=='br':return '\n'
    if tag in ['strong','b']:return '**'+body+'**'
    if tag in ['em','i']:return '*'+body+'*'
    if tag=='a':
        href=e.get('href','')
        return '['+body+']('+href+')' if href.startswith(('https://','http://')) else body
    if tag=='img':return '\n![Chat image]('+e.get('src','')+')\n'
    if re.fullmatch('h[1-6]',tag):return '\n\n'+('#'*int(tag[1]))+' '+body+'\n\n'
    if tag=='li':return '\n- '+body.strip()+'\n'
    if tag=='pre':return '\n\n```\n'+e.text_content()+'\n```\n\n'
    if tag in ['p','div','section','ul','ol','table','tr','blockquote']:return '\n'+body+'\n'
    return body
for n,(_,el,p) in sorted(turns.items()):
    for img in el.xpath('.//img'):
        src=img.get('src','');local=p.parent/src
        if local.is_file():
            raw=local.read_bytes();name=hashlib.sha256(raw).hexdigest()[:20]+local.suffix
            (images/name).write_bytes(raw);img.attrib.clear();img.set('src','../attachments/browser_images/'+name);img.set('alt','Chat image')
        else:img.drop_tree()
    for node in el.iter():
        keep={k:v for k,v in node.attrib.items() if k in ['href','src','alt','data-conversation-role']}
        node.attrib.clear();node.attrib.update(keep)
        if node.tag=='a' and not node.get('href','').startswith(('https://','http://')):node.attrib.pop('href',None)
    sources[str(n)]={'snapshot':p.name,'characters':len(el.text_content()),'roles':el.xpath('.//*[@data-conversation-role]/@data-conversation-role')}
    sections.append('<section id="turn-'+str(n)+'"><h2>Turn '+str(n+1)+'</h2>'+html.tostring(el,encoding='unicode')+'</section>')
    text=re.sub(r'\n[ \t]*\n(?:[ \t]*\n)+','\n\n',markdown(el)).strip()
    md.append('\n\n---\n\n## Turn '+str(n+1)+'\n\n'+text)
(OUT/'conversation/EDGE_CONVERSATION.md').write_text(''.join(md))
(OUT/'conversation/EDGE_CONVERSATION.html').write_text('<!doctype html><meta charset="utf-8"><title>Lemon — Rewrite for Readability</title><style>body{max-width:1000px;margin:40px auto;font:16px/1.6 system-ui;padding:20px}img{max-width:100%}section{border-bottom:1px solid #aaa;padding:24px 0}pre{white-space:pre-wrap}</style><h1>Lemon — Rewrite for Readability</h1>'+''.join(sections))
(OUT/'verification/CONVERSATION_COVERAGE.json').write_text(json.dumps({'turns':len(turns),'missing_turns':[],'capture_method':'Visible conversation DOM saved through Edge Save Page; no hidden app state','sources':sources},indent=2))
shutil.copy2('/Users/jordanlopez/Downloads/Rewrite For Readability.pdf',OUT/'conversation/Rewrite For Readability.pdf')
shutil.copy2(WORK/'Lemon_Edge_Full_Conversation.pdf',OUT/'conversation/Lemon_Edge_Print_137_pages.pdf')
inventory=json.loads((WORK/'inventory.json').read_text())
known={x['name'] for x in inventory['files']}
downloads=Path('/Users/jordanlopez/Downloads')
for p in downloads.iterdir():
    if p.is_file() and p.name in known:shutil.copy2(p,OUT/'attachments'/p.name)
for z in (OUT/'attachments').glob('*.zip'):
    with zipfile.ZipFile(z) as f:
        for info in f.infolist():
            name=Path(info.filename).name
            if not name or name.startswith('.') or info.is_dir():continue
            dest=OUT/'attachments/extracted'/z.stem/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(f.read(info))
shutil.copy2(__file__,OUT/'scripts/build_capture.py')
manifest=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file():manifest.append({'path':str(p.relative_to(OUT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(OUT/'verification/FILES_SHA256.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'turns':len(turns),'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest),'images':len(list(images.iterdir()))}))
