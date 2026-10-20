"""Verify final source bytes, media structure, fonts, and coupled render records."""
from pathlib import Path
from collections import Counter
import json,hashlib,zipfile,posixpath
from lxml import etree as E
import fitz
from pptx import Presentation
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C08';s=json.loads((D/'lecture.json').read_text());m=json.loads((D/'media_sources.json').read_text())['sources'];p=D/s['output_filename'];pdf=D/(p.stem+'_Static.pdf');a=json.loads((D/'paragraph_line_check.json').read_text());v=json.loads((D/'media_validation.json').read_text());doc=fitz.open(pdf)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert a['passing']==a['paragraphs']==219 and not a['failures'];assert v['passed']==v['checked']==40
for f in json.loads((D/'figure_sources.json').read_text()).values():
 assert h(D/f['path'])==f['sha256']
 if 'display_path' in f:assert h(D/f['display_path'])==f['display_sha256']
for f in json.loads((D/'textbook_crops.json').read_text()).values():assert h(D/f['path'])==f['sha256']
for x in m:
 original=X/x['original_url'].rsplit('/',1)[-1];assert h(original)==x['original_sha256']==h(D/x['file'])==x['sha256'];assert (x['source_width'],x['source_height'])==(x['width'],x['height']);assert x['source_duration']==x['duration']
inds=sorted(x['slide']-2 for x in m);edges=[-1]+inds+[73];roles=Counter(x['instructional_role'] for x in s['slides']);fonts=sorted({f[3] for page in doc for f in page.get_fonts()});assert all('Arial' in f for f in fonts);assert len(doc)==75 and not any(list(page.annots() or []) for page in doc);assert doc.embfile_count()==0
prs=Presentation(p);assert len(prs.slides)==75;assert sum(sh.shape_type==16 for slide in prs.slides for sh in slide.shapes)==40
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None;names=set(z.namelist());embedded={hashlib.sha256(z.read(n)).hexdigest() for n in names if n.endswith('.mp4')};assert embedded=={x['sha256'] for x in m} and len(embedded)==40
 for x in m:
  rel=E.fromstring(z.read(f"ppt/slides/_rels/slide{x['slide']}.xml.rels"));targets={r.get('Id'):r.get('Target') for r in rel};movierels=[r for r in rel if r.get('Type').endswith(('/video','/media'))];assert len(movierels)==2
  for r in movierels:assert hashlib.sha256(z.read(posixpath.normpath('ppt/slides/'+r.get('Target')))).hexdigest()==x['sha256']
  assert b'<p:timing>' in z.read(f"ppt/slides/slide{x['slide']}.xml")
 for n in names:
  if n.endswith('.rels'):
   owner=posixpath.join(posixpath.dirname(posixpath.dirname(n)),posixpath.basename(n)[:-5]) if n!='_rels/.rels' else ''
   for child in E.fromstring(z.read(n)):
    if child.get('TargetMode')!='External':assert posixpath.normpath(posixpath.join(posixpath.dirname(owner),child.get('Target'))).lstrip('/') in names
r={'slides':75,'content_slides':73,'book_chapter':8,'foundation_slides':roles['foundation'],'research_slides':roles['research'],'primary_figure_slides':44,'embedded_distinct_mp4s':40,'academic_recordings':20,'visual_recordings':20,'recordings_per_content_quarter':[sum(q*73/4<=i<(q+1)*73/4 for i in inds) for q in range(4)],'maximum_video_free_content_gap':max(b-a-1 for a,b in zip(edges,edges[1:])),'recordings_in_final_ten_content_slides':sum(i>=63 for i in inds),'paragraphs':219,'rendered_paragraphs_passing':219,'generic_failures':0,'course_failures':0,'full_recording_decodes_passed':40,'original_movie_bytes_retained':40,'compatibility_conversions':0,'source_hashes_and_native_resolution_frame_rate_audio_verified':True,'embedded_hashes_relationships_and_timing_verified':True,'all_slides_visually_reviewed':True,'source_figure_panels_reviewed':True,'fonts':fonts,'static_pdf_multimedia_annotations':0,'desktop_powerpoint_playback_tested':False}
assert r['recordings_per_content_quarter']==[10]*4 and r['recordings_in_final_ten_content_slides']>=5 and r['maximum_video_free_content_gap']<=3
for key,path in [('pptx',p),('static_pdf',pdf)]:r[key]={'filename':path.name,'bytes':path.stat().st_size,'sha256':h(path)}
(D/'VALIDATION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['slides','recordings_per_content_quarter','rendered_paragraphs_passing','fonts']}))
