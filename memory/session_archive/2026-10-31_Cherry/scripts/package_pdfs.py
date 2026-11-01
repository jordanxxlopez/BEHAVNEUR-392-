import concurrent.futures, hashlib, json, pathlib, re, subprocess, zipfile
root = pathlib.Path(__file__).resolve().parent
items = json.loads((root/'manifest.json').read_text())
ref = 'b443ca5046590de25eaa2c18614166c2234b430c'
def fetch(item):
    target = root/'pdfs'/pathlib.Path(item['path']).name
    url = f"https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/{ref}/{item['path']}"
    subprocess.run(['curl','-fLsS','--retry','3','--max-time','180',url,'-o',str(target)],check=True)
    data = target.read_bytes()
    assert data.startswith(b'%PDF-') and len(data) == item['size'] and len(data) < 29_000_000
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == item['sha']
    info = subprocess.check_output(['pdfinfo',str(target)],text=True)
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    print(f"Verified {pages} pages: {target.name}",flush=True)
    return dict(path=item['path'],filename=target.name,bytes=len(data),pages=pages,sha256=hashlib.sha256(data).hexdigest(),url=url)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch,items))
out = root.parent/'outputs'
archive = out/'BEHAVNEUR392_All_23_Lectures_PDFs.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for item in results:
        z.write(root/'pdfs'/item['filename'],item['filename'])
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==23 and z.testzip() is None
(out/'PDF_Verification_Manifest.json').write_text(json.dumps(dict(commit=ref,files=results),indent=2))
print(json.dumps(dict(pdf_count=len(results),pages=sum(x['pages'] for x in results),largest_bytes=max(x['bytes'] for x in results),zip_bytes=archive.stat().st_size)),flush=True)
