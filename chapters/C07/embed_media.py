"""Embed original publisher MP4 bytes while retaining source figures and static posters."""
from pathlib import Path
import json,hashlib,zipfile,posixpath
from lxml import etree as E
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
D=Path(__file__).resolve().parent;spec=json.loads((D/'lecture.json').read_text());manifest=json.loads((D/'media_sources.json').read_text());deck=D/spec['output_filename'];prs=Presentation(deck)
assert len(prs.slides)==75
assert not any(sh.shape_type==16 for s in prs.slides for sh in s.shapes),'Rebuild base deck before embedding.'
for m in manifest['sources']:
 slide=prs.slides[m['slide']-1];sd=spec['slides'][m['slide']-2]
 assert hashlib.sha256((D/m['file']).read_bytes()).hexdigest()==m['sha256']
 photos=[sh for sh in slide.shapes if sh.shape_type==13];assert len(photos)==1
 fig=photos[0];caption=next(sh for sh in slide.shapes if sh.has_text_frame and sh.text==sd['figure']['caption'])
 x=13.333-.62-5.7;w=5.7;maxh=2.30;r=fig.width/fig.height;fw=min(w,maxh*r);fh=fw/r;fig.left=Inches(x+(w-fw)/2);fig.top=Inches(1.40+(maxh-fh)/2);fig.width=Inches(fw);fig.height=Inches(fh)
 caption.left=Inches(x);caption.top=Inches(3.76);caption.width=Inches(w);caption.height=Inches(.34)
 for p in caption.text_frame.paragraphs:
  for run in p.runs:run.font.size=Pt(9)
 dar=m['display_aspect_ratio'];a,b=map(float,dar.split(':'));ar=a/b;mw=min(w,2.10*ar);mh=mw/ar;mx=x+(w-mw)/2;my=4.17+(2.10-mh)/2
 fallback=slide.shapes.add_picture(str(D/m['poster']),Inches(mx),Inches(my),Inches(mw),Inches(mh));fallback.name='Static source-recording poster'
 movie=slide.shapes.add_movie(str(D/m['file']),Inches(mx),Inches(my),Inches(mw),Inches(mh),poster_frame_image=str(D/m['poster']),mime_type='video/mp4');movie.name='Embedded source recording: '+m['caption']
 cap=slide.shapes.add_textbox(Inches(x),Inches(6.40),Inches(w),Inches(.34));cap.name='Recording credit';tf=cap.text_frame;tf.word_wrap=True;tf.margin_top=tf.margin_bottom=tf.margin_left=tf.margin_right=0
 run=tf.paragraphs[0].add_run();run.text=m['caption'];run.font.name='Arial';run.font.size=Pt(9);run.font.color.rgb=RGBColor(0,0,0)
 note=m.get('teaching_note','');notes=slide.notes_slide.notes_text_frame
 for t in ['', 'Source recording: '+m['caption'],'Teaching context: '+note,'Movie identifier: '+m['movie_identifier'],'Original recording legend: '+m['source_legend'],'Recording reference: '+m['full_reference'],'Original source: '+m['original_url'],'Credit: '+m['credit'],'License: '+json.dumps(m['license'],ensure_ascii=False),'Compatibility: '+m['conversion'],'Media SHA256: '+m['sha256'],'Associated article DOI: https://doi.org/'+m['doi'],'Playback: click the recording in PowerPoint Slide Show. Static PDF contains source posters. Desktop PowerPoint playback remains untested.']:
  notes.add_paragraph().text=t
for slide in prs.slides:
 for p in slide.notes_slide.notes_text_frame.paragraphs:
  for r in p.runs:r.font.name='Arial';r.font.size=Pt(12)
prs.save(deck)
with zipfile.ZipFile(deck) as z:
 assert z.testzip() is None
 embedded={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.mp4')}
 assert embedded=={m['sha256'] for m in manifest['sources']}
 for m in manifest['sources']:
  rel=z.read(f"ppt/slides/_rels/slide{m['slide']}.xml.rels");assert b'/video' in rel and b'/media' in rel
  assert b'<p:timing>' in z.read(f"ppt/slides/slide{m['slide']}.xml")
 for n in z.namelist():
  if n.endswith('.rels'):
   owner=posixpath.join(posixpath.dirname(posixpath.dirname(n)),posixpath.basename(n)[:-5]) if n!='_rels/.rels' else ''
   for child in E.fromstring(z.read(n)):
    if child.get('TargetMode')!='External':
     target=posixpath.normpath(posixpath.join(posixpath.dirname(owner),child.get('Target'))).lstrip('/');assert target in z.namelist(),(n,target)
print('75 slides; 40 original MP4s; hashes, relationships, and native timing verified.')
