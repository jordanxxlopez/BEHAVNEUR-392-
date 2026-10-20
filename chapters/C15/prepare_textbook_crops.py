"""Crop original uploaded pages, preserving published labels and source colors."""
import json,subprocess,hashlib
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
crops=[('15.1', 5, 80, [0.54, 0.135, 0.955, 0.805]), ('15.2', 5, 81, [0.055, 0.14, 0.89, 0.465]), ('15.3', 5, 82, [0.15, 0.195, 0.88, 0.62]), ('15.4', 5, 83, [0.055, 0.153, 0.46, 0.365]), ('15.5', 5, 84, [0.11, 0.8, 0.5, 0.97]), ('15.6', 5, 85, [0.185, 0.115, 0.76, 0.415]), ('15.7', 5, 87, [0.22, 0.27, 0.72, 0.57]), ('15.8', 5, 88, [0.54, 0.63, 0.94, 0.965]), ('15.9', 5, 92, [0.54, 0.19, 0.94, 0.44]), ('15.10', 5, 93, [0.075, 0.18, 0.46, 0.34]), ('15.11', 5, 93, [0.49, 0.19, 0.88, 0.37]), ('15.12', 5, 96, [0.11, 0.17, 0.51, 0.44]), ('15.13', 5, 96, [0.55, 0.7, 0.93, 0.96]), ('15.14', 5, 97, [0.1, 0.185, 0.445, 0.415]), ('15.T1', 5, 89, [0.055, 0.095, 0.94, 0.215])]
out={}
for num,part,page,box in crops:
 pdf=next(Path('/workspace/attachments').glob(f'*/Physiology*Part{part}of6*.pdf'));doc=fitz.open(pdf);obj=doc[page-1];cb=obj.cropbox;mb=obj.mediabox;tb=[(cb.x0+box[0]*cb.width)/mb.width,(cb.y0+box[1]*cb.height)/mb.height,(cb.x0+box[2]*cb.width)/mb.width,(cb.y0+box[3]*cb.height)/mb.height];p=D/'figures'/('book_'+num.replace('.','_')+'.png')
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),str(page),'--dpi','220','--box',*map(str,tb),'-o',str(p)],check=True)
 printed=page+({4:250,5:413}[part]);out[num]={'path':str(p.relative_to(D)),'kind':'textbook','figure_id':num,'pdf_page':page,'printed_page':printed,'part':part,'box':box,'crop_tool_box':tb,'coordinate_basis':'Normalized visible CropBox converted to MediaBox coordinates for crop_figure.py','isbn':'9781292430256','edition':'13th, Global Edition','caption':f'Carlson and Birkett (2022), Fig. {num}, p. {printed}.','source_url':'https://books.google.com/books?vid=ISBN9781292430256','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
out['15.T1']['caption']='Carlson and Birkett (2022), Table 15.1, p. 502.'
(D/'textbook_crops.json').write_text(json.dumps(out,indent=2)+'\n')
