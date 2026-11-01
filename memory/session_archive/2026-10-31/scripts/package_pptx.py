import concurrent.futures, hashlib, json, pathlib, re, subprocess, zipfile
root=pathlib.Path(__file__).resolve().parent
ref='b443ca5046590de25eaa2c18614166c2234b430c'
items=json.loads((root/'pptx_sources.json').read_text())
folder=root/'pptx_transfer'
folder.mkdir(exist_ok=True)
def pointer(item):
    url=f"https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/{ref}/{item['path']}"
    data=subprocess.check_output(['curl','-fLsS','--retry','3',url])
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['sha']
    return {**item,'sha256':re.search(rb'oid sha256:(\w+)',data).group(1).decode(),'bytes':int(re.search(rb'size (\d+)',data).group(1))}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    items=list(pool.map(pointer,items))
(root/'pptx_manifest.json').write_text(json.dumps(items,indent=2))
print(json.dumps({'files':len(items),'total_bytes':sum(x['bytes'] for x in items)}),flush=True)
def download(item):
    path=folder/pathlib.Path(item['path']).name
    url=f"https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/{ref}/{item['path']}"
    if not path.exists() or path.stat().st_size!=item['bytes']:
        subprocess.run(['curl','-fL','--retry','4','--retry-delay','2','--connect-timeout','30','--max-time','3600','-sS',url,'-o',str(path)],check=True)
    assert path.stat().st_size==item['bytes'],path
    with path.open('rb') as f: assert hashlib.file_digest(f,'sha256').hexdigest()==item['sha256'],path
    with zipfile.ZipFile(path) as z:
        assert '[Content_Types].xml' in z.namelist() and 'ppt/presentation.xml' in z.namelist()
        slides=sum(bool(re.fullmatch(r'ppt/slides/slide\d+\.xml',n)) for n in z.namelist())
        assert z.testzip() is None
    print(f"Verified {slides} slides; {item['bytes']} bytes: {path.name}",flush=True)
    return {**item,'filename':path.name,'slides':slides}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(download,items))
archive=folder/'BEHAVNEUR392_All_23_Latest_Lecture_PowerPoints.zip'
print('Creating ZIP containing all 23 verified PPTX files.',flush=True)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_STORED,allowZip64=True) as z:
    for item in results: z.write(folder/item['filename'],item['filename'])
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist())==23 and z.testzip() is None
with archive.open('rb') as f: md5=hashlib.file_digest(f,'md5').hexdigest()
(root/'pptx_transfer_verified.json').write_text(json.dumps({'commit':ref,'files':results,'archive':str(archive),'bytes':archive.stat().st_size,'md5':md5},indent=2))
print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'md5':md5}),flush=True)
