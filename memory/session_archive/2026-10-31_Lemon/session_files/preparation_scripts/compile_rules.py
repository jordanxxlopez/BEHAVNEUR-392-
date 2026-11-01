import concurrent.futures, hashlib, json, pathlib, subprocess
root=pathlib.Path(__file__).resolve().parent
sources=json.loads((root/'rule_sources.json').read_text())
cache=root/'rule_sources'
cache.mkdir(exist_ok=True)
def fetch(s):
    url=f"https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/{s['ref']}/{s['path']}"
    p=cache/(hashlib.sha256(url.encode()).hexdigest()+'.txt')
    subprocess.run(['curl','-fLsS','--retry','3','--max-time','60',url,'-o',str(p)],check=True)
    data=p.read_bytes()
    if s.get('sha'):
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==s['sha'],s['path']
    return {**s,'text':data.decode('utf-8'),'url':url}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    docs=list(pool.map(fetch,sources))
(root/'rules_downloaded.json').write_text(json.dumps(docs))
print(f'Downloaded and checked {len(docs)} source snapshots.',flush=True)
