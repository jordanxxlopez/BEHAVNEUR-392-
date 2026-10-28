"""Convert inspected CropBox coordinates to crop_figure.py MediaBox fractions."""
from pathlib import Path
import fitz,json,subprocess,sys
R=Path(__file__).resolve().parent.parent;source=next(Path('/workspace/attachments').rglob('*Part6of6*pdf'));pdf=fitz.open(source)
for ch in [18,19]:
 D=R/f'chapters/C{ch}';p=D/'book_crops.json';j=json.load(open(p))
 for name,b in j.items():
  if len(sys.argv)>1 and f'{ch}:{name}' not in sys.argv[1:]:continue
  pg=pdf[b['pdf_page']-1];box=b.get('intended_cropbox_fractions',b['crop_tool_box']);cb=pg.cropbox;mb=pg.mediabox
  actual=[(cb.x0+box[0]*cb.width)/mb.width,(cb.y0+box[1]*cb.height)/mb.height,(cb.x0+box[2]*cb.width)/mb.width,(cb.y0+box[3]*cb.height)/mb.height];b['intended_cropbox_fractions']=box;b['crop_tool_box']=actual;b['coordinate_reference']='MediaBox fractions passed to tools/crop_figure.py; inspected CropBox fractions retained separately.'
  subprocess.run(['python',str(R/'tools/crop_figure.py'),str(source),str(b['pdf_page']),'--box',*map(str,actual),'-o',str(D/b['path'])],check=True,stdout=subprocess.DEVNULL)
 p.write_text(json.dumps(j,indent=2)+'\n')
