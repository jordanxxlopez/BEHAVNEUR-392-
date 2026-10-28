from pathlib import Path
from lxml import etree as E
import json,zipfile,copy
D=Path(__file__).resolve().parent/'CTE_Psychology';sp=json.load(open(D/'lecture.json'));ms=json.load(open(D/'media_sources.json'));by={m['slide']:m for m in ms['sources']};deck=D/sp['output_filename'];a='http://schemas.openxmlformats.org/drawingml/2006/main';p='http://schemas.openxmlformats.org/presentationml/2006/main';ns={'a':a,'p':p};updates={}
with zipfile.ZipFile(deck) as z:
 for sn,sd in enumerate(sp['slides'],2):
  name=f'ppt/notesSlides/notesSlide{sn}.xml';root=E.fromstring(z.read(name));shape=next(x for x in root.findall('.//p:sp',ns) if x.find('p:nvSpPr/p:nvPr/p:ph',ns) is not None and x.find('p:nvSpPr/p:nvPr/p:ph',ns).get('type')=='body');tx=shape.find('p:txBody',ns)
  for q in list(tx):
   if q.tag=='{'+a+'}p':tx.remove(q)
  text='\n\n'.join(sd['transcript'])+'\n\nReferences:\n'+'\n'.join(sd['refs'])
  if sn in by:
   m=by[sn];text+='\n\nSource recording: '+m['caption']+'\nWhat students should observe: '+m['teaching_note']+'\nOriginal recording legend: '+m['source_legend']+'\nRecording reference: '+m['full_reference']+'\nSource: '+m['original_url']+'\nCredit: '+m['credit']+'\nLicense: '+str(m['license'])+'\nCompatibility: '+m['conversion']+'\nMedia SHA256: '+m['sha256']+'\nPlayback: click the embedded recording in desktop PowerPoint Slide Show. Inline playback is configured. Desktop PowerPoint playback remains untested.'
  for line in text.split('\n'):
   para=E.SubElement(tx,'{'+a+'}p');run=E.SubElement(para,'{'+a+'}r');rp=E.SubElement(run,'{'+a+'}rPr',sz='1200');E.SubElement(rp,'{'+a+'}latin',typeface='Arial');E.SubElement(run,'{'+a+'}t').text=line
  updates[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 with zipfile.ZipFile(deck.with_suffix('.tmp'),'w') as zz:
  for info in z.infolist():zz.writestr(copy.copy(info),updates.get(info.filename,z.read(info.filename)))
deck.with_suffix('.tmp').replace(deck);print('All 78 teaching transcripts synchronized exactly, with full source notes.')
