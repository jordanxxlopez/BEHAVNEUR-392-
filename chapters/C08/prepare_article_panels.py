"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C08'
boxes={'00425:4': [0, 0, 1, 0.24], '02076:3': [0, 0.25, 1, 0.63], '04885:2': [0, 0, 1, 0.5], '04885:3': [0, 0, 1, 0.33], '106270:5': [0, 0.26, 1, 0.525], '106270:6': [0, 0, 0.68, 0.51], '10774:3': [0.51, 0, 0.665, 0.225], '10774:4': [0.34, 0, 1, 0.325], '14316:5': [0, 0, 1, 0.62], '31627:4': [0, 0, 1, 0.53], '31826:10': [0, 0, 1, 0.47], '31895:6': [0.42, 0.6, 1, 1], '44530:3': [0, 0, 1, 0.42], '53565:5': [0, 0, 0.81, 1], '55177:2': [0, 0.22, 1, 0.56], '55177:6': [0, 0, 1, 0.54], '56374:6': [0, 0, 1, 0.3], '56374:7': [0, 0, 1, 0.25], '65906:5': [0, 0, 1, 0.26], '65906:9': [0, 0, 1, 0.31], '70270:4': [0, 0, 1, 0.36], '71464:4': [0.41, 0, 0.713, 0.65], '71464:7': [0, 0, 1, 0.3], '74478:1': [0, 0, 1, 0.5], '77513:5': [0.45, 0, 1, 0.245], '83108:7': [0, 0, 1, 0.165], '91483:1': [0, 0, 1, 0.27], '91483:6': [0.57, 0.18, 0.772, 0.59]}
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
