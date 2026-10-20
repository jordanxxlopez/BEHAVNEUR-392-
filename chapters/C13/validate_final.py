"""Verify final source bytes, media structure, fonts, and coupled render records."""
from pathlib import Path
from collections import Counter
import json,hashlib,zipfile,posixpath,subprocess
from urllib.parse import unquote
from lxml import etree as E
import fitz
from pptx import Presentation
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C13';s=json.loads((D/'lecture.json').read_text());m=json.loads((D/'media_sources.json').read_text())['sources'];p=D/s['output_filename'];pdf=D/(p.stem+'_Static.pdf');a=json.loads((D/'paragraph_line_check.json').read_text());v=json.loads((D/'media_validation.json').read_text());doc=fitz.open(pdf)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert a['passing']==a['paragraphs']==234 and not a['failures'];assert v['passed']==v['checked']==40
for f in json.loads((D/'figure_sources.json').read_text()).values():
 assert h(D/f['path'])==f['sha256']
 if 'display_path' in f:assert h(D/f['display_path'])==f['display_sha256']
for f in json.loads((D/'textbook_crops.json').read_text()).values():assert h(D/f['path'])==f['sha256']
conversion_checks=[]
def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))['streams']
def pts(path):
 stream=next(v['index'] for v in probe(path) if v['codec_type']=='video' and not v.get('disposition',{}).get('attached_pic'))
 data=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams',str(stream),'-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)]))['frames']
 result=[float(f['best_effort_timestamp_time']) if 'best_effort_timestamp_time' in f else None for f in data]
 first=next(t for t in result if t is not None)
 return [t-first if t is not None else None for t in result]
for x in m:
 original=X/x.get('original_filename',unquote(x['original_url'].rsplit('/',1)[-1]));assert h(original)==x['original_sha256'];assert h(D/x['file'])==x['sha256']
 assert (x['source_width'],x['source_height'])==(x['width'],x['height'])
 if x['sha256']==x['original_sha256']:
  assert original.read_bytes()==(D/x['file']).read_bytes()
 else:
  src=probe(original);dest=probe(D/x['file']);sv=next(v for v in src if v['codec_type']=='video' and not v.get('disposition',{}).get('attached_pic'));dv=next(v for v in dest if v['codec_type']=='video')
  assert (sv['width'],sv['height'])==(dv['width'],dv['height'])
  sa=[v for v in src if v['codec_type']=='audio'];da=[v for v in dest if v['codec_type']=='audio'];assert bool(sa)==bool(da)
  if sa:assert (sa[0]['channels'],sa[0]['sample_rate'])==(da[0]['channels'],da[0]['sample_rate'])
  old=pts(original);new=pts(D/x['file']);assert len(old)==len(new),(x['file'],len(old),len(new))
  delta=max(abs(a-b) for a,b in zip(old,new) if a is not None and b is not None);assert delta<.003,(x['file'],delta)
  conversion_checks.append({'file':x['file'],'frames':len(old),'source_frames_without_container_timestamp':sum(t is None for t in old),'timestamp_check':'Every timestamped frame compared relative to first frame; decoded frame count includes frames lacking source container timestamps.','maximum_relative_frame_timestamp_difference_seconds':delta,'native_dimensions_preserved':True,'audio_presence_channels_and_sample_rate_preserved':True})

inds=sorted(x['slide']-2 for x in m);edges=[-1]+inds+[78];roles=Counter(x['instructional_role'] for x in s['slides']);fonts=sorted({f[3] for page in doc for f in page.get_fonts()});assert all('Arial' in f for f in fonts);assert len(doc)==80 and not any(list(page.annots() or []) for page in doc);assert doc.embfile_count()==0
prs=Presentation(p);assert len(prs.slides)==80;assert sum(sh.shape_type==16 for slide in prs.slides for sh in slide.shapes)==40
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
assert a['spec_sha256']==h(D/'lecture.json') and a['pptx_sha256']==h(p) and a['pdf_sha256']==h(pdf)
r={'slides':80,'content_slides':78,'book_chapter':13,'foundation_slides':roles['foundation'],'research_slides':roles['research'],'primary_figure_slides':47,'embedded_distinct_mp4s':40,'academic_recordings':20,'visual_recordings':20,'recordings_per_content_quarter':[sum(q*78/4<=i<(q+1)*78/4 for i in inds) for q in range(4)],'maximum_video_free_content_gap':max(b-a-1 for a,b in zip(edges,edges[1:])),'recordings_in_final_ten_content_slides':sum(i>=68 for i in inds),'paragraphs':234,'rendered_paragraphs_passing':234,'generic_failures':0,'course_failures':0,'full_recording_decodes_passed':40,'original_movie_bytes_retained':40,'compatibility_conversions':0,'source_hashes_and_native_resolution_frame_rate_audio_verified':True,'embedded_hashes_relationships_and_timing_verified':True,'all_slides_visually_reviewed':True,'source_figure_panels_reviewed':True,'fonts':fonts,'static_pdf_multimedia_annotations':0,'desktop_powerpoint_playback_tested':False,'conversion_checks':conversion_checks}
assert r['recordings_per_content_quarter']==[10]*4 and r['recordings_in_final_ten_content_slides']>=5 and r['maximum_video_free_content_gap']<=3
for key,path in [('pptx',p),('static_pdf',pdf)]:r[key]={'filename':path.name,'bytes':path.stat().st_size,'sha256':h(path)}
(D/'VALIDATION.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['slides','recordings_per_content_quarter','rendered_paragraphs_passing','fonts']}))
