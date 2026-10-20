"""Embed verified MP4s while retaining all source figures, without changing pixels."""
from pathlib import Path
import json,hashlib,zipfile,posixpath,sys
from lxml import etree as E
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
HERE=Path(__file__).resolve().parent;spec=json.loads((HERE/(sys.argv[1] if len(sys.argv)>1 else 'lecture.json')).read_text());media=json.loads((HERE/'media_sources.json').read_text());deck=HERE/spec['output_filename'];prs=Presentation(deck)
assert len(prs.slides)==86
assert not any(x.shape_type==16 for s in prs.slides for x in s.shapes),'Rebuild the base deck before embedding.'
for m in media['sources']:
 clip=HERE/m['file'];poster=HERE/m['poster'];assert hashlib.sha256(clip.read_bytes()).hexdigest()==m['sha256'];slide=prs.slides[m['slide']-1]
 pictures=[x for x in slide.shapes if x.shape_type==13];captions=[x for x in slide.shapes if x.has_text_frame and x.name.startswith('Figure caption')];assert len(pictures)==len(captions)
 # Retain scientific figures above the movie, using the full available right column.
 sd=spec['slides'][m['slide']-2];col_w=sd.get('figure_width',5.3);col_x=13.333-.65-col_w;fy=1.35
 if len(pictures)==1:
  pic=pictures[0];r=pic.width/pic.height;pw=min(col_w,2.36*r);ph=pw/r;pic.left=Inches(col_x+(col_w-pw)/2);pic.top=Inches(fy);pic.width=Inches(pw);pic.height=Inches(ph)
  captions[0].left=Inches(col_x);captions[0].top=Inches(fy+ph+.05);captions[0].width=Inches(col_w);captions[0].height=Inches(.44)
 else:
  weights=sd.get('video_figure_weights',[.70,.30]);widths=[col_w*weights[0],col_w*weights[1]-.18];x=col_x
  for pic,caption,pw in zip(pictures,captions,widths):
   r=pic.width/pic.height;pw=min(pw,2.13*r);ph=pw/r;pic.left=Inches(x);pic.top=Inches(fy);pic.width=Inches(pw);pic.height=Inches(ph);caption.left=Inches(x);caption.top=Inches(fy+ph+.05);caption.width=Inches(widths[0] if x==col_x else widths[1]);caption.height=Inches(.65);x=col_x+widths[0]+.18
 for cap in captions:
  for p in cap.text_frame.paragraphs:
   for r in p.runs:r.font.size=Pt(9)
 dar=m['display_aspect_ratio'];a,b=map(float,dar.split(':'));r=a/b;mw=min(col_w,2.10*r);mh=mw/r;mx=col_x+(col_w-mw)/2;my=4.25+(2.10-mh)/2
 # Keep an explicit static source poster underneath the playable native media shape.
 fallback=slide.shapes.add_picture(str(poster),Inches(mx),Inches(my),Inches(mw),Inches(mh));fallback.name='Static source-recording poster'
 movie=slide.shapes.add_movie(str(clip),Inches(mx),Inches(my),Inches(mw),Inches(mh),poster_frame_image=str(poster),mime_type='video/mp4');movie.name='Embedded source recording: '+m['caption']
 cap=slide.shapes.add_textbox(Inches(col_x),Inches(6.4),Inches(col_w),Inches(.43));cap.name='Recording credit';tf=cap.text_frame;tf.word_wrap=True;tf.margin_top=tf.margin_bottom=tf.margin_left=tf.margin_right=0
 run=tf.paragraphs[0].add_run();run.text=m['caption'];run.font.name='Arial';run.font.size=Pt(9);run.font.color.rgb=RGBColor(0,0,0)
 notes=slide.notes_slide.notes_text_frame
 for text in ['','Source recording: '+m['caption'],'Teaching context: '+m['teaching_note'],'Movie identifier: '+m['movie_identifier'],'Original recording legend: '+m['source_legend'],'Recording reference: '+m['full_reference'],'Original source: '+m['original_url'],'Retrieved from: '+m.get('retrieved_from',m['original_url']),'Credit: '+m['credit'],'License: '+m['license'],'Compatibility: '+m['conversion'],'Media SHA256: '+m['sha256'],'Playback: click the recording in PowerPoint Slide Show. Static PDF preview contains source posters and does not play video. Desktop PowerPoint playback has not been tested in this environment.']:
  notes.add_paragraph().text=text
 if m.get('doi'):notes.add_paragraph().text='Associated article DOI: https://doi.org/'+m['doi']
 if m.get('source_context'):notes.add_paragraph().text='Retained upload/excerpt provenance: '+json.dumps(m['source_context'],ensure_ascii=False)
for slide in prs.slides:
 for p in slide.notes_slide.notes_text_frame.paragraphs:
  for run in p.runs:run.font.name="Arial";run.font.size=Pt(12)
prs.save(deck)
with zipfile.ZipFile(deck) as z:
 assert z.testzip() is None
 hashes={hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.mp4')};assert hashes=={x['sha256'] for x in media['sources']}
 for m in media['sources']:
  rel=z.read(f"ppt/slides/_rels/slide{m['slide']}.xml.rels");assert b'/video' in rel and b'/media' in rel
  assert b'<p:timing>' in z.read(f"ppt/slides/slide{m['slide']}.xml")
 for n in z.namelist():
  if n.endswith('.rels'):
   owner=posixpath.join(posixpath.dirname(posixpath.dirname(n)),posixpath.basename(n)[:-5]) if n!='_rels/.rels' else ''
   for x in E.fromstring(z.read(n)):
    if x.get('TargetMode')!='External':
     target=posixpath.normpath(posixpath.join(posixpath.dirname(owner),x.get('Target'))).lstrip('/');assert target in z.namelist(),(n,target)
print('86 slides; all 40 videos embedded with verified bytes, video/media relationships, and native timing entries.')
