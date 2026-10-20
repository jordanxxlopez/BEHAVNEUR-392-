"""Crop original supplied pages; preserve source colors and labels."""
import json,subprocess,hashlib
import fitz
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];D=Path(__file__).resolve().parent
pdf=next(Path('/workspace/attachments').glob('*/Physiology*Part3of6*.pdf'))
crops=[('7.1',21,[.54,.797,.95,.95]),('7.2',22,[.055,.12,.455,.285]),('7.3',22,[.20,.645,.77,.955]),('7.4',23,[.17,.10,.90,.54]),('7.5',24,[.18,.09,.83,.375]),('7.6',25,[.23,.18,.83,.73]),('7.8',27,[.13,.13,.91,.345]),('7.10',29,[.28,.13,.80,.44]),('7.11',30,[.11,.44,.46,.96])]
doc=fitz.open(pdf)
out={}
for num,page,box in crops:
 path=D/'figures'/('book_'+num.replace('.','_')+'.png')
 page_obj=doc[page-1];cb=page_obj.cropbox;mb=page_obj.mediabox
 toolbox=[(cb.x0+box[0]*cb.width)/mb.width,(cb.y0+box[1]*cb.height)/mb.height,(cb.x0+box[2]*cb.width)/mb.width,(cb.y0+box[3]*cb.height)/mb.height]
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),str(page),'--dpi','220','--box',*map(str,toolbox),'-o',str(path)],check=True)
 out[num]={'path':str(path.relative_to(D)),'kind':'textbook','figure_id':num,'pdf_page':page,'printed_page':page+172,'part':3,'box':box,'crop_tool_box':toolbox,'coordinate_basis':'Normalized visible CropBox converted to MediaBox coordinates for crop_figure.py / pdftoppm','isbn':'9781292430256','edition':'13th, Global Edition','caption':f'Carlson and Birkett (2022), Fig. {num}, p. {page+172}.','source_url':'https://books.google.com/books?vid=ISBN9781292430256','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(D/'textbook_crops.json').write_text(json.dumps(out,indent=2))
