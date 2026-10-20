"""Crop original supplied pages; preserve source colors and labels."""
import json,subprocess,hashlib
import fitz
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
pdf=next(Path('/workspace/attachments').glob('*/Physiology*Part3of6*.pdf'))
crops=[('7.20',39,[.20,.085,.92,.61]),('7.21',40,[.06,.09,.91,.43]),('7.23',41,[.18,.085,.89,.46]),('7.24',43,[.105,.095,.515,.37]),('7.25',44,[.48,.45,.90,.96]),('7.26',47,[.21,.12,.87,.78]),('7.27',48,[.055,.17,.46,.50]),('7.28',49,[.105,.18,.515,.46]),('7.29',49,[.535,.275,.925,.72]),('7.30',50,[.48,.74,.90,.956]),('7.31',51,[.16,.74,.91,.95]),('7.32',52,[.23,.165,.79,.31]),('7.33',52,[.035,.76,.48,.96]),('7.34',52,[.48,.75,.91,.96]),('7.35',55,[.11,.75,.51,.92]),('7.36',56,[.48,.10,.87,.66]),('7.37',57,[.18,.095,.87,.53]),('7.38',59,[.14,.085,.925,.48]),('7.39',60,[.055,.095,.465,.315]),('7.40',60,[.49,.66,.89,.956]),('7.41',61,[.105,.63,.46,.96]),('7.42',61,[.54,.65,.94,.95])]
doc=fitz.open(pdf)
out={}
for num,page,box in crops:
 path=D/'figures'/('book_'+num.replace('.','_')+'.png')
 page_obj=doc[page-1];cb=page_obj.cropbox;mb=page_obj.mediabox
 toolbox=[(cb.x0+box[0]*cb.width)/mb.width,(cb.y0+box[1]*cb.height)/mb.height,(cb.x0+box[2]*cb.width)/mb.width,(cb.y0+box[3]*cb.height)/mb.height]
 subprocess.run(['/workspace/.venvs/behavneur/bin/python',str(ROOT/'tools/crop_figure.py'),str(pdf),str(page),'--dpi','220','--box',*map(str,toolbox),'-o',str(path)],check=True)
 out[num]={'path':str(path.relative_to(D)),'kind':'textbook','figure_id':num,'pdf_page':page,'printed_page':page+172,'part':3,'box':box,'crop_tool_box':toolbox,'coordinate_basis':'Normalized visible CropBox converted to MediaBox coordinates for crop_figure.py / pdftoppm','isbn':'9781292430256','edition':'13th, Global Edition','caption':f'Carlson and Birkett (2022), Fig. {num}, p. {page+172}.','source_url':'https://books.google.com/books?vid=ISBN9781292430256','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
(D/'textbook_crops.json').write_text(json.dumps(out,indent=2))
