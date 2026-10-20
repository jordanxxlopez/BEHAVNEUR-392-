"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C14'
boxes={'110320:1': [0, 0, 1, 0.35], '110320:3': [0, 0, 1, 0.248], '25964:1': [0, 0, 1, 0.49], '46015:1': [0, 0, 1, 0.17], '46015:3': [0, 0, 1, 0.325], '54591:2': [0, 0, 1, 0.48], '82088:1': [0, 0.49, 1, 0.66], '82088:3': [0, 0, 1, 0.54], '91327:1': [0, 0, 1, 0.5], '91636:3': [0, 0, 1, 0.25], 'hand:1': [0, 0, 0.55, 0.47], 'speech:1': [0, 0, 1, 0.32], 'speech:2': [0, 0, 1, 0.43], 'synthesis:2': [0, 0, 1, 0.25], 'synthesis:3': [0, 0, 1, 0.75]}
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
