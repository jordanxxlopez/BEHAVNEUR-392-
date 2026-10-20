"""Crop intact source panels using the repository crop tool; never redraw data."""
import json,subprocess,concurrent.futures
from pathlib import Path
import fitz
from PIL import Image
D=Path(__file__).resolve().parent;ROOT=D.parents[1];X=ROOT/'research/downloads/C07'
boxes={'108071:7':[0,0,.51,.49],'89287:5':[0,0,.49,.57],'89287:4':[0,.55,1,.85],'31684:2':[0,0,1,.57],'31684:4':[0,0,1,.31],'60299:1':[0,0,1,.34],'60299:2':[0,.30,1,1],'60299:3':[0,0,1,.53],'60299:8':[0,0,1,.63],'84042:2':[0,0,1,.39],'95379:2':[0,0,1,.36],'95379:3':[0,0,1,.34],'49190:6':[0,0,1,.54],'49190:8':[0,.74,1,1],'85760:2':[0,0,1,.43],'85760:4':[0,0,1,.50],'85760:5':[0,0,1,.54],'47677:1':[0,0,1,.38],'101439:6':[0,0,1,.44],'101439:4':[0,0,1,.52],'101440:2':[0,0,1,.34],'45636:1':[0,0,1,.54],'45636:3':[0,0,1,.56],'85521:5':[0,0,1,.65],'85521:6':[0,0,1,.36],'85521:7':[0,0,.51,.70],'85521:8':[0,0,1,.35],'57524:4':[0,0,.68,.36]}
sources=json.loads((D/'figure_sources.json').read_text())
def f(it):
 key,box=it;a=sources[key];src=D/a['path'];im=Image.open(src);w,h=im.size
 # This private PDF is only a container for the unchanged publisher raster.
 pdf=X/(src.stem+'_original_raster.pdf')
 if not pdf.exists():
  doc=fitz.open();page=doc.new_page(width=w*72/220,height=h*72/220);page.insert_image(page.rect,filename=str(src));doc.save(pdf)
 out=D/'figures'/(src.stem+'_panels.png')
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),'1','--dpi','220','--box',*map(str,box),'-o',str(out)],capture_output=True,check=True)
 a.update(display_path=str(out.relative_to(D)),panel_crop_box=box,crop_tool='tools/crop_figure.py; lossless publisher raster in private PDF container',source_dimensions=[w,h]);return key,a
for key,a in concurrent.futures.ThreadPoolExecutor(3).map(f,boxes.items()):sources[key]=a
(D/'figure_sources.json').write_text(json.dumps(sources,indent=2));print('Prepared',len(boxes),'intact source-panel crops.')
