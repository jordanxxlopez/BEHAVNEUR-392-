"""Select representative original frames without changing movie bytes or slide XML."""
from pathlib import Path
import json,subprocess,zipfile,posixpath,os,hashlib,copy
from lxml import etree as E
R=Path(__file__).resolve().parent.parent;ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for ch,times in {18:{39:42,57:15,59:28},19:{39:2.7,40:29.7}}.items():
 D=R/f'chapters/C{ch}';s=json.load(open(D/'lecture.json'));mp=D/'media_sources.json';ms=json.load(open(mp));deck=D/s['output_filename'];replacement={}
 with zipfile.ZipFile(deck) as z:
  for m in ms['sources']:
   if m['slide'] not in times:continue
   t=times[m['slide']];poster=D/m['poster'];subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(D/m['file']),'-frames:v','1','-q:v','2','-threads','1',str(poster)],check=True);m['poster_time_seconds']=t;m['poster_sha256']=hashlib.sha256(poster.read_bytes()).hexdigest()
   sn=m['slide'];xml=E.fromstring(z.read(f'ppt/slides/slide{sn}.xml'));rels={r.get('Id'):r for r in E.fromstring(z.read(f'ppt/slides/_rels/slide{sn}.xml.rels'))}
   for pic in xml.findall('.//p:pic',ns):
    nv=pic.find('p:nvPicPr/p:cNvPr',ns);name=nv.get('name','')
    if name=='Static source-recording poster' or name.startswith('Embedded source recording:'):
     blip=pic.find('.//a:blip',ns);rid=blip.get('{'+ns['r']+'}embed');target=posixpath.normpath(posixpath.join('ppt/slides',rels[rid].get('Target')));replacement[target]=poster.read_bytes()
  tmp=deck.with_suffix('.revised.pptx')
  with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as out:
   for item in z.infolist():out.writestr(copy.copy(item),replacement.get(item.filename,z.read(item.filename)))
  with zipfile.ZipFile(tmp) as zz:
   assert all(z.read(n)==zz.read(n) for n in z.namelist() if n.startswith('ppt/slides/'));assert all(z.read(n)==zz.read(n) for n in z.namelist() if n.endswith('.mp4'))
 os.replace(tmp,deck);mp.write_text(json.dumps(ms,indent=2)+'\n');print(ch,'representative posters updated; all slide XML and MP4 bytes unchanged',flush=True)
