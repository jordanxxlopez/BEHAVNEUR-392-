from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[1]
pdfs = sorted((root / "PDFs").glob("*.pdf"))
assert len(pdfs) == 23
for p in pdfs:
    assert p.stat().st_size < 29_000_000
    with p.open("rb") as f:
        assert f.read(5) == b"%PDF-"
archive = root / "BEHAVNEUR392_All_23_Lectures_PDFs.zip"
with ZipFile(archive, "w", ZIP_DEFLATED) as z:
    for p in pdfs:
        z.write(p, p.name)
with ZipFile(archive) as z:
    assert z.testzip() is None
print(archive)
