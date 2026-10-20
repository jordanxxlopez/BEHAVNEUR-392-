"""Remove interactive annotations and embedded attachments from LibreOffice PDF."""
from pathlib import Path
import fitz
h=Path(__file__).resolve().parent
p=h/'From_Light_to_Sight_Chapter_6.pdf';d=fitz.open(p)
for page in d:d.xref_set_key(page.xref,'Annots','null')
for name in d.embfile_names():d.embfile_del(name)
# Tagged-PDF structure can retain indirect references after page annotations are removed.
for xref in range(1,d.xref_length()):
 typ=d.xref_get_key(xref,'Type')[1];sub=d.xref_get_key(xref,'Subtype')[1]
 if typ=='/EmbeddedFile':d.update_stream(xref,b'')
 if typ=='/Filespec' or (typ=='/Annot' and sub in ['/Screen','/Movie','/RichMedia']):d.update_object(xref,'null')
d.save(h/'From_Light_to_Sight_Chapter_6_Static.pdf',garbage=4,deflate=True);d.close()
print('Saved static PDF without movie attachments.')
