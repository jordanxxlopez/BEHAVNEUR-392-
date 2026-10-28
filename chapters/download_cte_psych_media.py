"""Retrieve selected original recordings and preserve full source timing and dimensions."""
from pathlib import Path
import sys,json,urllib.request,concurrent.futures,subprocess,hashlib,re
R=Path(__file__).resolve().parent.parent;P=Path('/workspace/.setup/publisher')
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(p)]))
def process(ch,m):
 D=R/'chapters/CTE_Psychology';M=D/'media';M.mkdir(exist_ok=True);orig=M/'originals';orig.mkdir(exist_ok=True);stem=m['paper_id']+'-'+m['identifier'];raw=orig/(stem+'.source');mp4=M/(stem+'.mp4')
 try:
  if not raw.exists():
   req=urllib.request.Request(m['url'],headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=120) as res,raw.open('wb') as f:
    while b:=res.read(1024*1024):f.write(b)
  j=probe(raw);v=next(s for s in j['streams'] if s['codec_type']=='video');audio=[s for s in j['streams'] if s['codec_type']=='audio'];h=hashlib.sha256(raw.read_bytes()).hexdigest();conversion=''
  if not mp4.exists():
   if v['codec_name']=='h264' and m['url'].lower().endswith('.mp4') and all(a['codec_name']=='aac' for a in audio):
    import os;os.link(raw,mp4);conversion='Original publisher MP4 bytes retained.'
   else:
    cmd=['ffmpeg','-v','error','-y','-i',str(raw)]
    if v['codec_name']=='h264':cmd+=['-c:v','copy']
    else:
     assert v['width']%2==0 and v['height']%2==0,('Odd native dimensions; select an alternative source.',v['width'],v['height']);cmd+=['-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-fps_mode','passthrough']
    cmd+=['-c:a','copy' if all(a['codec_name']=='aac' for a in audio) else 'aac','-movflags','+faststart',str(mp4)];subprocess.run(cmd,check=True)
  k=probe(mp4);nv=next(s for s in k['streams'] if s['codec_type']=='video');assert nv['codec_name']=='h264';assert (nv['width'],nv['height'])==(v['width'],v['height']);assert nv['r_frame_rate']==v['r_frame_rate'];assert abs(float(k['format']['duration'])-float(j['format']['duration']))<.25;assert bool(audio)==any(s['codec_type']=='audio' for s in k['streams']);newhash=hashlib.sha256(mp4.read_bytes()).hexdigest()
  conversion='Original publisher MP4 bytes retained.' if h==newhash else 'MP4 container conversion or H.264 compatibility encoding only; native dimensions, frame rate, full duration, audio presence and scientific scenes retained. No trimming, padding, cropping, or speed changes.'
  dur=float(k['format']['duration']);poster=mp4.with_name(stem+'_poster.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(dur*.5),'-i',str(mp4),'-frames:v','1','-q:v','2','-threads','1',str(poster)],check=True)
  if m['paper_id'].isdigit():
   art=json.loads((D/'sources.json').read_text())[m['paper_id']] if (D/'sources.json').exists() else json.loads((P/(m['paper_id']+'.json')).read_text());names=[a.get('name',{}).get('preferred','') for a in art['authors'] if a.get('type')=='person'];credit='; '.join(n for n in names if n)
  else:credit=m.get('author','')
  m.update(file=str(mp4.relative_to(D)),original_file=str(raw.relative_to(D)),poster=str(poster.relative_to(D)),original_url=m['url'],sha256=newhash,original_sha256=h,conversion=conversion,width=nv['width'],height=nv['height'],source_width=v['width'],source_height=v['height'],duration=dur,source_duration=float(j['format']['duration']),frame_rate=nv['r_frame_rate'],source_frame_rate=v['r_frame_rate'],display_aspect_ratio=nv.get('display_aspect_ratio') if nv.get('display_aspect_ratio') not in [None,'0:1'] else f"{nv['width']}:{nv['height']}",codec=nv['codec_name'],pixel_format=nv.get('pix_fmt'),audio=bool(audio),credit=credit,full_reference=f"{credit} ({m['year']}). {m['paper_title']}. "+('https://doi.org/'+m['doi'] if m['doi'] else m.get('source_page',m['url'])),license=m['copyright'],movie_identifier=m['identifier'],source_legend=m['legend'],review_status='Downloaded; original preparation and representative-footage review pending.')
  print(ch,m['slide'],stem,nv['width'],nv['height'],round(dur,1),'seconds',flush=True)
 except Exception as e:m['error']=str(e);print('MEDIA ISSUE',ch,m['slide'],stem,type(e).__name__,str(e)[:120],flush=True)
 return m
for ch in ([int(x) for x in sys.argv[1:]] or [802]):
 D=R/'chapters/CTE_Psychology';rows=json.loads((D/'media_selection.json').read_text())['sources']
 with concurrent.futures.ThreadPoolExecutor(4) as e:out=list(e.map(lambda m:process(ch,m),rows))
 (D/'media_sources.json').write_text(json.dumps({'sources':out},indent=2,ensure_ascii=False)+'\n');print(ch,'complete',len(out),'issues',sum('error' in m for m in out),flush=True)
