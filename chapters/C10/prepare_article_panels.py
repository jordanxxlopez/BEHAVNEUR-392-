"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C10'
boxes={'107352:5': [0, 0.61, 0.565, 0.96], '47198:6': [0, 0.235, 1, 0.458], '106347:1': [0, 0, 1, 0.17], '109215:8': [0, 0.67, 1, 0.798], '96344:4': [0, 0.57, 0.59, 1], '64680:9': [0, 0.325, 1, 0.52], 'carcea:1': [0, 0.56, 1, 0.75], 'carcea:4': [0, 0, 0.71, 0.17], '33676:1': [0, 0.17, 0.565, 0.44], '86464:3': [0, 0, 1, 0.25], '96543:6': [0, 0, 0.59, 0.4], '103109:2': [0.63, 0.195, 1, 0.714], '87029:3': [0, 0, 1, 0.277]}
sources=json.loads((D/'figure_sources.json').read_text())
for a in sources.values():
 for k in ['display_path','panel_crop_box','crop_tool','source_dimensions','display_sha256']:a.pop(k,None)
def f(it):
 key,box=it;a=sources[key];src=D/a['path'];im=Image.open(src);w,h=im.size;pdf=X/(src.stem+'_original_raster.pdf')
 if not pdf.exists():
  doc=fitz.open();page=doc.new_page(width=w*72/220,height=h*72/220);page.insert_image(page.rect,filename=str(src));doc.save(pdf)
 out=D/'figures'/(src.stem+'_panels.png')
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),'1','--dpi','220','--box',*map(str,box),'-o',str(out)],capture_output=True,check=True)
 a.update(display_path=str(out.relative_to(D)),panel_crop_box=box,crop_tool='tools/crop_figure.py; unchanged publisher raster in private PDF container',source_dimensions=[w,h],display_sha256=hashlib.sha256(out.read_bytes()).hexdigest());return key,a
for key,a in concurrent.futures.ThreadPoolExecutor(3).map(f,boxes.items()):sources[key]=a
(D/'figure_sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n');print('Prepared',len(boxes),'source-panel crops.')
