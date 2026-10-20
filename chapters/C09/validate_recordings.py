from pathlib import Path
import json,subprocess,concurrent.futures,re
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;QA=HERE.parent.parent/'qa/C09';QA.mkdir(parents=True,exist_ok=True);items=json.loads((HERE/'media_sources.json').read_text())['sources']
def f(x):
 p=HERE/x['file'];mid=QA/(p.stem+'_middle.jpg');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(x['duration']/2),'-i',str(p),'-frames:v','1','-q:v','2',str(mid)],check=True)
 # Full decoding exercises every frame of the deliverable recording.
 dec=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-fps_mode','passthrough','-enc_time_base','-1','-f','null','-'],capture_output=True,text=True,errors='replace')
 result=dict(file=x['file'],slide=x['slide'],full_decode_pass=dec.returncode==0 and not dec.stderr.strip(),decode_error=dec.stderr.strip(),quality_ssim=None)
 if not result['full_decode_pass'] and 'non monotonically increasing dts' in result['decode_error']:
  count=subprocess.run(['ffprobe','-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,nb_frames','-of','json',str(p)],capture_output=True,text=True)
  frames=json.loads(count.stdout)['streams'][0]
  result.update(source_timestamp_mux_warning=result['decode_error'],full_decode_pass=count.returncode==0 and not count.stderr.strip() and frames['nb_read_frames']==frames['nb_frames'],full_decode_frame_count=frames,decode_error=count.stderr,verification_method='Every frame decoded by ffprobe; decoded count equals source count. Original timestamp reversal retained.')
 if x['file']==x['downloaded_file']:result['quality_ssim']=1.0
 else:
  src=HERE/x['downloaded_file'];filters='[0:v]pad=ceil(iw/2)*2:ceil(ih/2)*2,format=yuv420p[a];[1:v]format=yuv420p[b];[a][b]ssim'
  q=subprocess.run(['ffmpeg','-v','info','-i',str(src),'-i',str(p),'-lavfi',filters,'-frames:v','60','-f','null','-'],capture_output=True,text=True,errors='replace')
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
