"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C15'
boxes={'102578:1': [0, 0, 1, 0.16], '108134:1': [0, 0, 1, 0.4], '108134:3': [0, 0, 1, 0.18], '108333:1': [0, 0, 1, 0.3], '34593:1': [0, 0, 1, 0.365], '34593:4': [0, 0, 1, 0.32], '48964:3': [0, 0, 0.68, 0.232], '50531:1': [0, 0, 1, 0.46], '51512:1': [0, 0, 1, 0.435], '58737:3': [0, 0, 1, 0.41], '62167:4': [0, 0, 1, 0.48], '78079:1': [0, 0.6, 1, 1], '78079:4': [0, 0, 1, 0.28], '78202:1': [0, 0, 1, 0.3], '78202:5': [0, 0, 1, 0.327], '82809:1': [0, 0, 1, 0.312], '90325:1': [0, 0, 0.5, 0.23], '90325:4': [0, 0, 1, 0.198], '108134:6': [0, 0.505, 0.39, 0.755], '88459:6': [0, 0.65, 1, 1], '34593:6': [0, 0, 0.33, 0.2], '34593:7': [0, 0, 1, 0.38]}
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
