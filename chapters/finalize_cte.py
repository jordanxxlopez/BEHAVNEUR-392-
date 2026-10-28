"""Finalize human-readable recording captions and native source links without touching media bytes."""
from pathlib import Path
import json,zipfile,copy,re
from lxml import etree as E
D=Path(__file__).resolve().parent/'CTE';sp=json.loads((D/'lecture.json').read_text());ms=json.loads((D/'media_sources.json').read_text());p=D/sp['output_filename'];ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
labels=['Michigan–Northwestern football plays','Calculated stress after mouse-brain impact','Cultured axon during controlled stretch','Princeton–Yale football, 1903','Elastic recovery of a stretched axon','Normal tau and microtubules in fly neurons','Spectrin/tau-mutant worm axon','Worm axon rotation after laser release','Serial electron images of worm axonal microtubules','Oregon–Washington State football plays','Unseeded control tau reporter cells','Mouse-derived tau seeds in reporter cells','Tau reporter assemblies and cellular extensions','Tau exchange at a nuclear boundary','Tau inclusions during cell death','Recycling synaptic vesicle trajectories','Total synaptic vesicle trajectories','Tau and recycling-vesicle trajectories','Engineered tau condensates and fibrils','Purified TRIAD3A droplets','Zebrafish blood flow after brain injury','Zebrafish seizure-like behavior after injury','Mouse meningeal macrophage calcium','Meningeal calcium before and after cortical disturbance','Electron-microscopy vascular reconstruction','Serial-section vascular reconstruction','Microglial microtubules: control and LPS','Microtubule regrowth after washout','Microglial morphology in brain tissue','Normal mouse microglial response to laser injury','Repopulated microglial response to laser injury','Successful and aborted microglial engulfment','Sequential clearance of dead neurons','Centrosome movement during engulfment','Rab5 endosomes during engulfment','Human 3D microglia respond to tissue damage','Human 3D neural network calcium activity','Human 3D microglia engulf synaptic material','Human 3D microglial surveillance','Human 2D coculture calcium comparison']
old={m['slide']:m['caption'] for m in ms['sources']}
for m,label in zip(ms['sources'],labels):m['caption']=label+'. '+('FOX Sports' if m['paper_id'] in ['football1','football3'] else 'Edison/Library of Congress' if m['paper_id']=='football2' else str(m['credit']).split(' et al')[0].split(';')[0].split(',')[0][:28])+' ('+str(m['year'])+').'
updates={}
with zipfile.ZipFile(p) as z:
 for m in ms['sources']:
  name=f"ppt/slides/slide{m['slide']}.xml";root=E.fromstring(z.read(name));shape=next(s for s in root.findall('.//p:sp',ns) if s.find('p:nvSpPr/p:cNvPr',ns).get('name')=='Recording credit');t=shape.findall('.//a:t',ns);t[0].text=m['caption']
  if m.get('youtube_url'):
   # Add a regular clickable text source, separate from the embedded movie.
   template=next(s for s in root.findall('.//p:sp',ns) if s.find('p:nvSpPr/p:cNvPr',ns).get('name')=='Video playback label');new=copy.deepcopy(template);prop=new.find('p:nvSpPr/p:cNvPr',ns);prop.set('id',str(900+m['slide']));prop.set('name','YouTube source link');new.find('.//a:off',ns).set('x',str(int(7.013*914400)));new.find('.//a:ext',ns).set('cx',str(int(3.7*914400)));new.find('.//a:t',ns).text='YouTube source';rp=new.find('.//a:rPr',ns);rp.set('u','sng');link=E.SubElement(rp,'{'+ns['a']+'}hlinkClick');rid='rIdCTEYouTube';link.set('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id',rid);root.find('p:cSld/p:spTree',ns).append(new)
   rn=f"ppt/slides/_rels/slide{m['slide']}.xml.rels";rr=E.fromstring(z.read(rn));E.SubElement(rr,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id=rid,Type='http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',Target=m['youtube_url'],TargetMode='External');updates[rn]=E.tostring(rr,xml_declaration=True,encoding='UTF-8',standalone=True)
  updates[name]=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 # Title metadata uses special-topic wording, not an invented book chapter.
 name='ppt/notesSlides/notesSlide1.xml';data=z.read(name).replace(b'Chapter 801.',b'Special topic: Neurobiology of CTE.');updates[name]=data
 with zipfile.ZipFile(p.with_suffix('.tmp'),'w',zipfile.ZIP_DEFLATED) as out:
  for item in z.infolist():
   info=copy.copy(item)
   if item.filename.endswith('.mp4'):info.compress_type=zipfile.ZIP_STORED
   out.writestr(info,updates.get(item.filename,z.read(item.filename)))
p.with_suffix('.tmp').replace(p);(D/'media_sources.json').write_text(json.dumps(ms,indent=2,ensure_ascii=False)+'\n');print('Recording captions, two YouTube source links, and special-topic notes finalized.')
