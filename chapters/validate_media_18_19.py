"""Check each slide's native media relationship, source bytes, and distribution."""
from pathlib import Path
import json,zipfile,hashlib,posixpath,sys
from lxml import etree as E
ROOT=Path(__file__).resolve().parent.parent;NS={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
for ch in ([int(x) for x in sys.argv[1:]] or [18,19]):
 D=ROOT/f'chapters/C{ch}';spec=json.loads((D/'lecture.json').read_text());records=json.loads((D/'media_sources.json').read_text())['sources'];deck=D/spec['output_filename'];indices=sorted(m['slide']-2 for m in records);edges=[-1]+indices+[78];out=[]
 with zipfile.ZipFile(deck) as z:
  assert z.testzip() is None;mp4s={n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.endswith('.mp4')};assert len(mp4s)==40
  for m in records:
   sn=m['slide'];rels={r.get('Id'):r for r in E.fromstring(z.read(f'ppt/slides/_rels/slide{sn}.xml.rels'))};xml=E.fromstring(z.read(f'ppt/slides/slide{sn}.xml'));vf=xml.findall('.//a:videoFile',NS);assert len(vf)==1
   rid=vf[0].get('{'+NS['r']+'}link');target=posixpath.normpath(posixpath.join('ppt/slides',rels[rid].get('Target')));assert mp4s[target]==m['sha256']==hashlib.sha256((D/m['file']).read_bytes()).hexdigest();assert rels[rid].get('TargetMode')!='External'
   vids=xml.findall('.//p:video',NS);assert len(vids)==1 and vids[0].get('fullScrn')=='1';assert xml.find('p:timing',NS) is not None
   assert (D/m['poster']).is_file()
   if m.get('original_file'):assert hashlib.sha256((D/m['original_file']).read_bytes()).hexdigest()==m['original_sha256']
   else:assert m['original_sha256']==m['sha256']
   out.append(dict(slide=sn,embedded_part=target,sha256=m['sha256'],internal_video_relationship=True,fullscreen=True,poster_present=True))
 result=dict(slides=80,embedded_recordings=40,purposes={p:sum(m['purpose']==p for m in records) for p in ['academic','aesthetic']},content_quarters=[sum(q*78/4<=i<(q+1)*78/4 for i in indices) for q in range(4)],maximum_unrecorded_content_gap=max(b-a-1 for a,b in zip(edges,edges[1:])),final_ten_content_recordings=sum(i>=68 for i in indices),unique_embedded_hashes=len(set(mp4s.values())),all_relationships_and_source_hashes_verified=True,all_fullscreen_configured=True,desktop_powerpoint_playback='Untested',records=out)
 assert result['purposes']=={'academic':20,'aesthetic':20};assert result['content_quarters']==[10]*4;assert result['maximum_unrecorded_content_gap']<=3;assert result['final_ten_content_recordings']>=5
 (D/'media_embedding_validation.json').write_text(json.dumps(result,indent=2)+'\n');print(ch,'40 internal videos; 20 + 20; quarters 10/10/10/10; all hashes and full-screen timing relationships pass',flush=True)
