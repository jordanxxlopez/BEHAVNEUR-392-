"""Render a static copy with movie objects removed and original posters retained."""
from pathlib import Path
import json,os,subprocess,sys
from pptx import Presentation
import fitz
ch=int(sys.argv[1]);D=Path(__file__).resolve().parent/f'C{ch}';ROOT=D.parents[1];QA=ROOT/f'qa/C{ch}';QA.mkdir(parents=True,exist_ok=True)
spec=json.loads((D/'lecture.json').read_text());source=D/spec['output_filename'];copy=QA/f'C{ch}_Static_Render_Copy.pptx';out=QA/f'C{ch}_Static_Render_Copy.pdf';target=D/(source.stem+'_Static.pdf')
prs=Presentation(source);removed=0
for slide in prs.slides:
 for sh in list(slide.shapes):
  if sh.shape_type==16:sh._element.getparent().remove(sh._element);removed+=1
 for rel in list(slide.part.rels.values()):
  if rel.reltype.endswith(('/video','/media')):slide.part.drop_rel(rel.rId)
 for timing in list(slide._element.xpath('./p:timing')):slide._element.remove(timing)
prs.save(copy)
environ=dict(os.environ);environ['FONTCONFIG_FILE']='/workspace/.setup/fonts.conf'
subprocess.run(['soffice',f'-env:UserInstallation=file:///workspace/.setup/lo-profile-C{ch}','--headless','--convert-to','pdf','--outdir',str(QA),str(copy)],env=environ,check=True)
pdf=fitz.open(out);assert len(pdf)==80;assert not any(list(p.annots() or []) for p in pdf);assert pdf.embfile_count()==0
pdf.save(target,garbage=4,deflate=True)
print('Static PDF:',len(pdf),'pages;',removed,'movie objects excluded;',target.stat().st_size,'bytes. Original posters retained.')
