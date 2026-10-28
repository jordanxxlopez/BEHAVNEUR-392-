"""Give the new lecture's recordings more space while preserving every source aspect ratio."""
from pathlib import Path
import json,zipfile,copy
from lxml import etree as E
D=Path(__file__).resolve().parent/'CTE_Psychology';sp=json.load(open(D/'lecture.json'));ms=json.load(open(D/'media_sources.json'))['sources'];deck=D/sp['output_filename'];ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'};updates={};u=lambda x:str(round(x*914400))
def box(el,x,y,w,h):
 tr=el.find('p:spPr/a:xfrm',ns);off=tr.find('a:off',ns);ext=tr.find('a:ext',ns);off.set('x',u(x));off.set('y',u(y));ext.set('cx',u(w));ext.set('cy',u(h))
with zipfile.ZipFile(deck) as z:
 for m in ms:
  name=f"ppt/slides/slide{m['slide']}.xml";root=E.fromstring(z.read(name));x=7.013;w=5.7
  for pic in root.findall('.//p:pic',ns):
   n=pic.find('p:nvPicPr/p:cNvPr',ns).get('name','');tr=pic.find('p:spPr/a:xfrm',ns);ext=tr.find('a:ext',ns);ar=int(ext.get('cx'))/int(ext.get('cy'))
   movie=n=='Static source-recording poster' or n.startswith('Embedded source recording:');mh=2.65 if movie else 1.8;top=3.65 if movie else 1.35;pw=min(w,mh*ar);ph=pw/ar;box(pic,x+(w-pw)/2,top+(mh-ph)/2,pw,ph)
  for shape in root.findall('.//p:sp',ns):
   n=shape.find('p:nvSpPr/p:cNvPr',ns).get('name','')
   if n=='Figure caption':box(shape,x,3.24,w,.30)
  updates[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(deck.with_suffix('.tmp'),'w') as out:
  for info in z.infolist():out.writestr(copy.copy(info),updates.get(info.filename,z.read(info.filename)))
deck.with_suffix('.tmp').replace(deck);print('All 40 recordings enlarged to a 5.7 by 2.65 inch zone; figures and videos retain their original aspect ratios.')
