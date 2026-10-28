from pathlib import Path
import json,subprocess,concurrent.futures,io,textwrap
from PIL import Image,ImageDraw,ImageFont
ROOT=Path('/workspace/BEHAVNEUR-392-');Q=ROOT/'qa/media-review';Q.mkdir(parents=True,exist_ok=True)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
for ch in [801]:
 D=ROOT/"chapters/CTE";rows=json.loads((D/'media_sources.json').read_text())['sources'];rows=sorted([m for m in rows if 'error' not in m],key=lambda m:m['slide'])
 def review(m):
  p=D/m['file'];frames=[]
  for t in [.1,.5,.9]:
   b=subprocess.check_output(['ffmpeg','-v','error','-ss',str(m['duration']*t),'-i',str(p),'-frames:v','1','-f','image2pipe','-vcodec','png','-threads','1','-']);im=Image.open(io.BytesIO(b)).convert('RGB');im.thumbnail((290,160));frames.append(im)
  tile=Image.new('RGB',(900,210),'white');draw=ImageDraw.Draw(tile);label=f"Slide {m['slide']} | {m['paper_id']} {m['identifier']} | {m['title']}"
  draw.text((5,1),'\n'.join(textwrap.wrap(label,115)[:2]),font=font,fill='black')
  for i,im in enumerate(frames):tile.paste(im,(i*300+(300-im.width)//2,45+(160-im.height)//2))
  tile.save(Q/f'C{ch}_{m["slide"]:02}.jpg');res=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True,text=True);return dict(slide=m['slide'],file=m['file'],decode_exit=res.returncode,decode_errors=res.stderr)
 with concurrent.futures.ThreadPoolExecutor(3) as e:out=list(e.map(review,rows))
 for start in range(0,len(rows),8):
  part=rows[start:start+8];sheet=Image.new('RGB',(900,210*len(part)),'white')
  for i,m in enumerate(part):sheet.paste(Image.open(Q/f'C{ch}_{m["slide"]:02}.jpg'),(0,210*i))
  sheet.save(Q/f'C{ch}_sheet{start//8+1}.jpg')
 (Q/f'C{ch}_decode.json').write_text(json.dumps(out,indent=2));print(ch,len(out),'review frames/full decode completed',flush=True)
