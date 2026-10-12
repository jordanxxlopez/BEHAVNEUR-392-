#!/usr/bin/env python3
"""Final course-specific QA, in addition to check_lecture.py.
python tools/check_course.py chapters/C01/lecture.json deck.pptx media_sources.json
"""
import sys,json,zipfile,hashlib,math
from pathlib import Path
from pptx import Presentation

def check(spec,deck,manifest):
 errors=[];slides=spec.get('slides',[]);n=len(slides);total=len(Presentation(deck).slides)
 if not 75<=total<=85:errors.append(f'Total slides {total}; require 75–85.')
 if total!=n+2:errors.append('Spec/deck slide counts differ.')
 roles=[s.get('instructional_role') for s in slides]
 if any(r not in ('foundation','research') for r in roles):errors.append('Each content slide needs instructional_role foundation or research.')
 if n and not .20<=roles.count('foundation')/n<=.30:errors.append('Foundation slide share must be 20–30%.')
 if n and not .70<=roles.count('research')/n<=.80:errors.append('Research slide share must be 70–80%.')
 if any(not s.get('figure') and not s.get('figures') for s in slides):errors.append('Every content slide needs source imagery.')
 sources=manifest.get('sources',[]);purposes=[x.get('purpose') for x in sources]
 if not 15<=purposes.count('academic')<=20:errors.append('Require 15–20 academic video records.')
 if not 5<=purposes.count('aesthetic')<=10:errors.append('Require 5–10 aesthetic video records.')
 if any(p not in ('academic','aesthetic') for p in purposes):errors.append('Each video needs purpose academic or aesthetic.')
 with zipfile.ZipFile(deck) as z:
  embedded={hashlib.sha256(z.read(p)).hexdigest() for p in z.namelist() if p.startswith('ppt/media/') and p.lower().endswith(('.mp4','.mov','.m4v','.avi'))}
 for x in sources:
  if not x.get('original_url') or not x.get('credit'):errors.append(f'Video on slide {x.get("slide")} lacks source URL or credit.')
  if x.get('sha256') not in embedded:errors.append(f'Video on slide {x.get("slide")} is not embedded with its recorded hash.')
  if not isinstance(x.get('slide'),int) or not 2<=x['slide']<total:errors.append('Video slide index must refer to a content slide.')
 if len(set(x.get('sha256') for x in sources))!=len(sources):errors.append('Duplicate movies cannot pad the video quota.')
 if len(embedded)!=len(sources):errors.append('Embedded movie count does not match provenance records.')
 return errors
if __name__=='__main__':
 if len(sys.argv)!=4:sys.exit(__doc__)
 sp=Path(sys.argv[1]);spec=json.loads(sp.read_text());sched=json.loads((Path(__file__).resolve().parent.parent/'course/schedule.json').read_text());meta=next(x for x in sched['lectures'] if x['n']==spec['lecture'])
 errors=check(spec,sys.argv[2],json.loads(Path(sys.argv[3]).read_text()))
 if not meta.get('verified'):errors.append('Exact chapter title has not been verified against the textbook.')
 for e in errors:print('FAIL:',e)
 print(f'{len(errors)} course-specific failures.')
 sys.exit(bool(errors))
