#!/usr/bin/env python3
"""Count actual exported lines of each teaching paragraph, not estimated wraps.
Usage: python tools/check_paragraph_lines.py spec.json deck.pptx rendered.pdf report.json
"""
import json,re,unicodedata,sys,hashlib
from pathlib import Path
import fitz
from pptx import Presentation

def norm(text):
 text=re.sub(r'\*\*|(?<!\w)_|_(?!\w)','',text)
 return ''.join(c for c in unicodedata.normalize('NFKC',text) if not c.isspace() and c!='\u00ad')
def check(spec_path,deck_path,pdf_path,report_path):
 spec=json.loads(Path(spec_path).read_text());prs=Presentation(deck_path);pdf=fitz.open(pdf_path);rows=[]
 for i,sd in enumerate(spec['slides'],1):
  body=next(x for x in prs.slides[i].shapes if x.name=='Body')
  x0,y0,x1,y1=[v/914400*72 for v in (body.left,body.top,body.left+body.width,body.top+body.height)]
  grouped={}
  for block in pdf[i].get_text('dict')['blocks']:
   for line in block.get('lines',[]):
    for span in line['spans']:
     bx0,by0,bx1,by1=span['bbox'];baseline=span['origin'][1]
     if x0-1<=(bx0+bx1)/2<=x1+1 and y0-2<=baseline<=y1+2:
      key=round(baseline*2)/2;grouped.setdefault(key,[]).append((bx0,span['text']))
  lines=[(y,0,''.join(t for _,t in sorted(chunks))) for y,chunks in sorted(grouped.items())]
  combined='';ids=[]
  for lid,(_,_,t) in enumerate(lines):
   t=norm(t);combined+=t;ids += [lid]*len(t)
  offset=0
  for j,p in enumerate(sd['body'],1):
   t=norm(p);start=combined.find(t,offset)
   if start<0:count=None;ys=[]
   else:
    used=set(ids[start:start+len(t)]);count=len(used);ys=[round(lines[n][0],2) for n in sorted(used)];offset=start+len(t)
   rows.append({'slide':i+1,'paragraph':j,'lines':count,'pass':count is not None and 5<=count<=7,'line_top_y':ys})
 report={'spec_sha256':hashlib.sha256(Path(spec_path).read_bytes()).hexdigest(),'pptx_sha256':hashlib.sha256(Path(deck_path).read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256(Path(pdf_path).read_bytes()).hexdigest(),'requirement':'Every content paragraph has 5–7 actual rendered lines. No forced line breaks or blank-line padding.','paragraphs':len(rows),'passing':sum(r['pass'] for r in rows),'failures':[r for r in rows if not r['pass']],'results':rows}
 Path(report_path).write_text(json.dumps(report,indent=2)+'\n');print(f"{report['passing']}/{len(rows)} paragraphs have 5–7 rendered lines; {len(report['failures'])} failures.");return report
if __name__=='__main__':
 if len(sys.argv)!=5:sys.exit(__doc__)
 r=check(*sys.argv[1:]);sys.exit(bool(r['failures']))
