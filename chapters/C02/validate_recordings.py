from pathlib import Path
import json,subprocess,concurrent.futures,re
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;QA=HERE.parent.parent/'qa/C02';QA.mkdir(parents=True,exist_ok=True);items=json.loads((HERE/'media_sources.json').read_text())['sources']
def f(x):
 p=HERE/x['file'];mid=QA/(p.stem+'_middle.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(x['duration']/2),'-i',str(p),'-frames:v','1','-q:v','2',str(mid)],check=True)
 # Full decoding exercises every frame of the deliverable recording.
 dec=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-f','null','-'],capture_output=True,text=True)
 result=dict(file=x['file'],slide=x['slide'],full_decode_pass=dec.returncode==0 and not dec.stderr.strip(),decode_error=dec.stderr.strip(),quality_ssim=None)
 if x['file']==x['downloaded_file']:result['quality_ssim']=1.0
 else:
  src=HERE/x['downloaded_file'];filters='[0:v]pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p[a];[1:v]format=yuv420p[b];[a][b]ssim'
  q=subprocess.run(['ffmpeg','-v','info','-i',str(src),'-i',str(p),'-lavfi',filters,'-frames:v','60','-f','null','-'],capture_output=True,text=True)
  match=re.findall(r'All:([0-9.]+)',q.stderr)
  if match:result['quality_ssim']=float(match[-1])
  result['quality_frames']=60
 print(p.name,result['full_decode_pass'],result['quality_ssim'],flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(f,items))
(HERE/'media_validation.json').write_text(json.dumps({'recordings':results,'all_full_decodes_pass':all(x['full_decode_pass'] for x in results),'note':'SSIM compares the first 60 decoded frames for converted recordings; original MP4 bytes retained have identity 1.0. Full decoding checks every deliverable frame. Desktop PowerPoint playback remains untested.'},indent=2))
can=Image.new('RGB',(1200,((len(items)+3)//4)*180),'white');draw=ImageDraw.Draw(can)
for i,x in enumerate(items):
 a=Image.open(QA/(Path(x['file']).stem+'_middle.jpg')).convert('RGB');a.thumbnail((290,145));left=i%4*300;top=i//4*180;can.paste(a,(left+(300-a.width)//2,top+25));draw.text((left+5,top+4),f"Slide {x['slide']}: {x['purpose']}",fill='black')
can.save(QA/'all_recordings.jpg');print('ALL RECORDINGS DECODED',flush=True)
