"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C13'
boxes={'69333:2': [0, 0, 1, 0.465], '105422:3': [0, 0, 1, 0.45], '62390:2': [0, 0, 1, 0.45], '83897:1': [0, 0, 1, 0.41], '105452:5': [0, 0, 1, 0.62], '80661:2': [0, 0, 0.455, 0.31], '70586:5': [0, 0, 1, 0.4], '51972:2': [0, 0, 1, 0.55], '102475:4': [0, 0, 1, 0.52], '57023:4': [0, 0, 1, 0.325], '92860:4': [0, 0, 1, 0.53], '60360:1': [0, 0, 1, 0.325], '103879:2': [0, 0, 1, 0.28], '80622:3': [0, 0, 1, 0.43], '80622:5': [0, 0.51, 1, 1]}
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
