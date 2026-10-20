"""Crop original uploaded pages, preserving published labels and source colors."""
import json,subprocess,hashlib
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
crops=[('14.1', 5, 45, [0.5, 0.735, 0.915, 0.95]), ('14.2', 5, 46, [0.105, 0.705, 0.945, 0.945]), ('14.3', 5, 47, [0.155, 0.689, 0.79, 0.971]), ('14.5', 5, 49, [0.19, 0.25, 0.78, 0.522]), ('14.7', 5, 50, [0.55, 0.225, 0.96, 0.35]), ('14.8', 5, 52, [0.54, 0.16, 0.88, 0.34]), ('14.9', 5, 54, [0.535, 0.155, 0.94, 0.445]), ('14.12', 5, 56, [0.54, 0.68, 0.94, 0.95]), ('14.14', 5, 58, [0.2, 0.68, 0.86, 0.96]), ('14.18', 5, 61, [0.52, 0.74, 0.96, 0.955]), ('14.20', 5, 63, [0.05, 0.65, 0.47, 0.955]), ('14.21', 5, 64, [0.175, 0.155, 0.875, 0.275]), ('14.24', 5, 67, [0.24, 0.155, 0.71, 0.565]), ('14.26', 5, 68, [0.535, 0.14, 0.95, 0.39]), ('14.27', 5, 69, [0.045, 0.715, 0.47, 0.965]), ('14.28', 5, 70, [0.1, 0.13, 0.51, 0.37]), ('14.30', 5, 71, [0.055, 0.115, 0.46, 0.51]), ('14.31', 5, 72, [0.11, 0.195, 0.505, 0.27]), ('14.34', 5, 75, [0.05, 0.2, 0.37, 0.49])]
out={}
for num,part,page,box in crops:
 pdf=next(Path('/workspace/attachments').glob(f'*/Physiology*Part{part}of6*.pdf'));doc=fitz.open(pdf);obj=doc[page-1];cb=obj.cropbox;mb=obj.mediabox;tb=[(cb.x0+box[0]*cb.width)/mb.width,(cb.y0+box[1]*cb.height)/mb.height,(cb.x0+box[2]*cb.width)/mb.width,(cb.y0+box[3]*cb.height)/mb.height];p=D/'figures'/('book_'+num.replace('.','_')+'.png')
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),str(page),'--dpi','220','--box',*map(str,tb),'-o',str(p)],check=True)
 printed=page+({4:250,5:413}[part]);out[num]={'path':str(p.relative_to(D)),'kind':'textbook','figure_id':num,'pdf_page':page,'printed_page':printed,'part':part,'box':box,'crop_tool_box':tb,'coordinate_basis':'Normalized visible CropBox converted to MediaBox coordinates for crop_figure.py','isbn':'9781292430256','edition':'13th, Global Edition','caption':f'Carlson and Birkett (2022), Fig. {num}, p. {printed}.','source_url':'https://books.google.com/books?vid=ISBN9781292430256','sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(D/'textbook_crops.json').write_text(json.dumps(out,indent=2)+'\n')
