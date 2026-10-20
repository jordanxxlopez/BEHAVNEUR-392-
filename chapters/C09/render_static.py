"""Render an attachment-free PDF from a temporary poster-only copy of the native deck."""
from pathlib import Path
import tempfile,subprocess,json,os,shutil
from pptx import Presentation
h=Path(__file__).resolve().parent;s=json.load(open(h/'lecture.json'))
with tempfile.TemporaryDirectory(prefix='c09-render-') as tmp:
 p=Path(tmp)/'The_Rhythmic_Brain_Sleep_and_Biological_Rhythms_Static.pptx';prs=Presentation(h/s['output_filename'])
 for slide in prs.slides:
  for shape in list(slide.shapes):
   if shape.shape_type==16:slide.shapes._spTree.remove(shape._element)
  for rel in list(slide.part.rels.values()):
   if rel.reltype.endswith(('/video','/media')):slide.part.drop_rel(rel.rId)
  for node in list(slide._element):
   if node.tag.endswith('}timing'):slide._element.remove(node)
 prs.save(p)
 env=os.environ.copy();env['FONTCONFIG_FILE']='/workspace/.tools/fonts.conf'
 subprocess.run(['/workspace/.tools/lo/root/opt/libreoffice25.8/program/soffice','-env:UserInstallation=file:///workspace/.tools/lo/profile','--headless','--convert-to','pdf','--outdir',str(h),str(p)],check=True,env=env)
print('Rendered static PDF from poster-only temporary deck; native movies unchanged.')
