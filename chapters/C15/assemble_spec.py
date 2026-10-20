"""Assemble a separate, source-grounded 80-slide lecture."""
from pathlib import Path
import json,re
from write_content import CONTENT
D=Path(__file__).resolve().parent;ROOT=D.parents[1];cfg=json.loads((D/'settings.json').read_text());ch=int(D.name[1:]);bm=json.loads((D/'foundation_assignments.json').read_text());figs=json.loads((D/'figure_sources.json').read_text());assign=json.loads((D/'figure_assignments.json').read_text());book=json.loads((D/'textbook_crops.json').read_text())
bookref=f"Carlson NR, Birkett MA (2022). Physiology of Behavior, Global Edition. 13th ed. Pearson. ISBN 9781292430256. Chapter {ch}: {cfg['booktitle']}, printed pp.{cfg['pages']}. Verified directly in uploaded Part5of6, PDF pp.{cfg['pdfpages']}."
slides=[]
for i,c in enumerate(CONTENT):
 role='foundation' if str(i) in bm else 'research';s=dict(title=c['title'],body=c['body'],transcript=list(c['body']),layout='figure-right',figure_width=5.7,instructional_role=role)
 if role=='foundation':s.update(figure=book[bm[str(i)]],cite='Carlson & Birkett (2022)',refs=[bookref],primary_source='book')
 else:
  id,n=assign[str(i)];a=figs[f'{id}:{n}'];journal='eLife' if id.isdigit() else 'Nature';s.update(figure=dict(path=a.get('display_path',a['path']),kind='article',source_url='https://doi.org/'+a['doi'],caption=f"{a['first']} et al. ({a['year']}), Fig. {n}.",credit=a['authors'],license=a['license']['license']),cite=f"{a['first']} et al. ({a['year']})",refs=[f"{a['authors']} ({a['year']}). {re.sub('<[^>]+>','',a['title'])}. {journal}. https://doi.org/{a['doi']}",'Original figure legend: '+a['legend'],'Figure provenance: '+json.dumps(a,ensure_ascii=False)],primary_source=journal+'.'+id)
 if str(i) in {'17','18'}:
  id,n=json.loads((D/'foundation_figure_overrides.json').read_text())[str(i)];a=figs[f'{id}:{n}']
  s.update(figure=dict(path=a.get('display_path',a['path']),kind='article',source_url='https://doi.org/'+a['doi'],caption=f"{a['first']} et al. ({a['year']}), Fig. {n}.",credit=a['authors'],license=a['license']['license']),cite='Carlson & Birkett (2022); '+a['first']+' et al. ('+a['year']+')',refs=[bookref,f"{a['authors']} ({a['year']}). {a['title']}. eLife. https://doi.org/{a['doi']}",'Original figure legend: '+a['legend'],'Figure provenance: '+json.dumps(a,ensure_ascii=False)],primary_source='Textbook mechanism; original eLife illustration')
 slides.append(s)
assert len(slides)==78
spec=dict(lecture=ch,book_chapter=ch,content_slides=78,authorized_total_slide_range=[80,80],theme=cfg['theme'],output_filename=cfg['filename'],title_kicker=cfg['kicker'],title_image=book[cfg['image']],title_refs=[bookref],slides=slides,paragraph_line_requirement=[5,7],chapter_scope=bookref,takeaways=dict(cite='Carlson & Birkett (2022); primary studies in notes',refs=[bookref],items=[dict(lead=a,text=b) for a,b in cfg['takeaways']]))
(D/'lecture.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n');(D/'SLIDE_SPINE.md').write_text('# '+cfg['title']+'\n\n80 slides.\n\n1. Title\n'+'\n'.join(f'{i+2}. {s["title"]}' for i,s in enumerate(slides))+'\n80. Key takeaways\n')
p=ROOT/'course/schedule.json';j=json.loads(p.read_text());m=next(x for x in j['lectures'] if x['n']==ch);m.update(date='Fall 2026',title=cfg['title'],verified=True,book_chapter=ch,book_chapter_title=cfg['booktitle'],display_title_authorized=True,display_title_authorization='Instructor requested separate Chapters 14 and 15, exactly 80 total slides each.',textbook_printed_pages=cfg['pages'],book_scope_verified_from='Uploaded Physiology of Behavior Part5of6, PDF pp.'+cfg['pdfpages']);p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n');print('Assembled chapter',ch,len(slides),'teaching slides; 31 foundation, 47 research.')
