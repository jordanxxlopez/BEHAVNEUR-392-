#!/usr/bin/env python3
"""Download all 23 BEHAVNEUR 392 lecture PDFs from the October 28, 2026 GitHub snapshot.
No third-party Python dependencies. Run from a computer with network access.
The ZIP is created only if 23 valid PDF files (each below 29 MB) are present.
"""
import csv, json, pathlib, subprocess, sys, urllib.request, urllib.error, zipfile

HERE=pathlib.Path(__file__).resolve().parent
MANIFEST=HERE/'manifest_all_23.json'
FILES=HERE/'BEHAVNEUR392_23_PDFs'
ZIP=HERE/'BEHAVNEUR392_All_23_Lectures_PDFs.zip'
LIMIT=29_000_000
FILES.mkdir(exist_ok=True)
items=json.loads(MANIFEST.read_text(encoding='utf-8'))
assert len(items)==23

def download(url,destination):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (BEHAVNEUR392-archive)', 'Accept':'application/pdf,application/octet-stream,*/*'})
    with urllib.request.urlopen(req,timeout=120) as reply, destination.open('wb') as out:
        while True:
            data=reply.read(1024*1024)
            if not data: break
            out.write(data)

def pdf_pages(path):
    # pdfinfo is optional (for example, `brew install poppler`).
    try:
        c=subprocess.run(['pdfinfo',str(path)],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,text=True,timeout=20)
        if c.returncode==0:
            for line in c.stdout.splitlines():
                if line.startswith('Pages:'): return int(line.split(':',1)[1].strip())
    except (OSError,ValueError,subprocess.TimeoutExpired): pass
    try:
        from pypdf import PdfReader
        return len(PdfReader(path))
    except (ImportError,Exception): return None

fail=[]
for idx,e in enumerate(items,1):
    target=FILES/e['output_pdf']
    print(f'[{idx:02d}/23] {e["title"]}',flush=True)
    valid=target.exists() and 1024<target.stat().st_size<LIMIT and target.open('rb').read(5)==b'%PDF-'
    if not valid:
        tmp=target.with_suffix('.part')
        sources=[e['github_pdf_url'],e['github_pdf_url'].replace('raw.githubusercontent.com/','media.githubusercontent.com/media/')]
        for url in sources:
            try:
                download(url,tmp)
                if 1024 < tmp.stat().st_size < LIMIT and tmp.open('rb').read(5)==b'%PDF-':
                    tmp.replace(target)
                    valid=True
                    break
                else: raise ValueError('Not a complete PDF under 29 MB (possibly an LFS pointer).')
            except Exception as ex:
                print('   Failed source:',str(ex),flush=True)
                tmp.unlink(missing_ok=True)
    if valid:
        pages=pdf_pages(target)
        print(f'   OK: {target.stat().st_size/1e6:.2f} MB' + (f', {pages} pages' if pages else ''),flush=True)
        if e['lecture_id'] in ('16','17') and pages is not None and pages<80:
            print('   WARNING: Layout preview has fewer than 80 pages. A full conversion from the original PowerPoint is required.',flush=True)
            fail.append((e['title'],'Preview is not the full 80-slide deck.'))
    else:
        fail.append((e['title'],'Could not download valid PDF'))

if fail:
    print('\nARCHIVE NOT CREATED because these lecture files need attention:',file=sys.stderr)
    for title,reason in fail: print('  -',title,reason,file=sys.stderr)
    sys.exit(1)

with zipfile.ZipFile(ZIP,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for e in items:
        p=FILES/e['output_pdf']
        z.write(p,arcname=p.name)
    z.write(MANIFEST,arcname='manifest_all_23.json')

with zipfile.ZipFile(ZIP) as z:
    bad=z.testzip(); assert not bad,bad
    pdfs=[n for n in z.namelist() if n.lower().endswith('.pdf')]
    assert len(pdfs)==23,len(pdfs)
    assert all(z.getinfo(n).file_size<LIMIT for n in pdfs)
print(f'\nCOMPLETE: {ZIP} ({ZIP.stat().st_size/1e6:.1f} MB) with 23 PDFs, each under 29 MB.')
