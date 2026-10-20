"""Decode complete source recordings, and record current-run results."""
import subprocess,json,concurrent.futures,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent;m=json.loads((D/'media_sources.json').read_text())['sources']
def f(x):
 p=D/x['file'];r=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-map','0:a?','-f','null','-'],capture_output=True,text=True)
 return {'file':x['file'],'sha256_matches':hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],'exit_code':r.returncode,'errors':r.stderr.strip(),'full_decode_pass':r.returncode==0 and not r.stderr.strip()}
a=list(concurrent.futures.ThreadPoolExecutor(3).map(f,m));(D/'media_validation.json').write_text(json.dumps({'checked':len(a),'passed':sum(x['full_decode_pass'] and x['sha256_matches'] for x in a),'results':a},indent=2));print('Full decodes:',sum(x['full_decode_pass'] for x in a),'/',len(a));assert all(x['full_decode_pass'] and x['sha256_matches'] for x in a)
