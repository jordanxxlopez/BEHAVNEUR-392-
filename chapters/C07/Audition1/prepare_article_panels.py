"""Preserve selected intact publisher panels; record every normalized source crop."""
import json,subprocess,concurrent.futures,hashlib
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[2];X=ROOT/'research/downloads/Audition1'
boxes={'03564:7': [0, 0, 1, 0.54], '07830:2': [0, 0, 1, 0.29], '08177:2': [0, 0.51, 1, 1], '24318:6': [0, 0, 1, 0.27], '24661:4': [0.55, 0.67, 1, 1], '29275:1': [0.24, 0, 1, 0.263], '37625:1': [0, 0.642, 0.66, 1], '37625:3': [0, 0.716, 0.67, 1], '43736:3': [0, 0.22, 0.51, 0.48], '47667:1': [0, 0.53, 0.34, 1], '61092:3': [0, 0, 1, 0.42], '66547:4': [0.55, 0.608, 1, 0.78], '69264:2': [0, 0.145, 1, 0.634], '72251:1': [0, 0.42, 1, 0.79], '72681:2': [0, 0, 1, 0.248], '72681:7': [0, 0.79, 1, 1], '77628:1': [0, 0, 1, 0.58], '79494:2': [0, 0, 1, 0.617], '89719:7': [0, 0, 1, 0.44], '93749:2': [0, 0, 1, 0.33], '93749:4': [0.665, 0, 1, 0.333]}
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
