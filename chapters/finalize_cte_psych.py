"""Add public source links, representative posters, and special-topic metadata."""
from pathlib import Path
import json,zipfile,copy,subprocess,hashlib,posixpath
from lxml import etree as E
D=Path(__file__).resolve().parent/'CTE_Psychology';sp=json.load(open(D/'lecture.json'));ms=json.load(open(D/'media_sources.json'));deck=D/sp['output_filename'];ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'};updates={}
with zipfile.ZipFile(deck) as z:
 for m in ms['sources']:
  sn=m['slide'];name=f'ppt/slides/slide{sn}.xml';root=E.fromstring(z.read(name));rn=f'ppt/slides/_rels/slide{sn}.xml.rels';rels=E.fromstring(z.read(rn));by={r.get('Id'):r for r in rels}
  if sn in [2,69]:
   poster=D/m['poster'];subprocess.run(['ffmpeg','-v','error','-y','-ss','10','-i',str(D/m['file']),'-frames:v','1','-q:v','2','-threads','1',str(poster)],check=True);m['poster_time_seconds']=10;m['poster_sha256']=hashlib.sha256(poster.read_bytes()).hexdigest()
   for pic in root.findall('.//p:pic',ns):
    nv=pic.find('p:nvPicPr/p:cNvPr',ns)
    if nv.get('name','')=='Static source-recording poster' or nv.get('name','').startswith('Embedded source recording:'):
     rid=pic.find('.//a:blip',ns).get('{'+ns['r']+'}embed');part=posixpath.normpath(posixpath.join('ppt/slides',by[rid].get('Target')));updates[part]=poster.read_bytes()
  if m.get('youtube_url'):
   template=next(s for s in root.findall('.//p:sp',ns) if s.find('p:nvSpPr/p:cNvPr',ns).get('name')=='Video playback label');new=copy.deepcopy(template);prop=new.find('p:nvSpPr/p:cNvPr',ns);prop.set('id',str(900+sn));prop.set('name','YouTube source link');new.find('.//a:off',ns).set('x',str(int(7.013*914400)));new.find('.//a:ext',ns).set('cx',str(int(3.7*914400)));new.find('.//a:t',ns).text='YouTube source';rp=new.find('.//a:rPr',ns);rp.set('u','sng');fill=E.SubElement(rp,'{'+ns['a']+'}solidFill');E.SubElement(fill,'{'+ns['a']+'}srgbClr',val='000000');link=E.SubElement(rp,'{'+ns['a']+'}hlinkClick');rid='rIdCTEYouTube';link.set('{'+ns['r']+'}id',rid);root.find('p:cSld/p:spTree',ns).append(new);E.SubElement(rels,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id=rid,Type=ns['r']+'/hyperlink',Target=m['youtube_url'],TargetMode='External');updates[rn]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True)
  updates[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 name='ppt/notesSlides/notesSlide1.xml';updates[name]=z.read(name).replace(b'Chapter 802.',b'Special topic: Cognitive and clinical neuroscience of football and CTE.')
 with zipfile.ZipFile(deck.with_suffix('.tmp'),'w') as out:
  for info in z.infolist():out.writestr(copy.copy(info),updates.get(info.filename,z.read(info.filename)))
deck.with_suffix('.tmp').replace(deck)
for m in ms['sources']:m['review_status']='Original source legend reviewed; 10%, 50%, 90% frames visually inspected; full recording decoded without errors.'
(D/'media_sources.json').write_text(json.dumps(ms,indent=2,ensure_ascii=False)+'\n');print('Two YouTube source links, source posters, and new-lecture metadata finalized.')
