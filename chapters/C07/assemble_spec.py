"""Assemble this nonauditory Chapter 7 lecture from reviewed source records."""
import json,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
sys.path.insert(0,str(D));from write_content import CONTENT
F=[0,1,3,5,8,9,13,15,17,21,23,27,28,31,32,33,35,37,41,43,46,49,51,53,56,60,62,64,66]
book=json.loads((D/'textbook_crops.json').read_text());figs=json.loads((D/'figure_sources.json').read_text());assign=json.loads((D/'figure_assignments.json').read_text())
bookassign={0:'7.21',1:'7.20',3:'7.21',5:'7.23',8:'7.24',9:'7.24',13:'7.24',15:'7.26',17:'7.26',21:'7.25',23:'7.24',27:'7.24',28:'7.24',31:'7.26',32:'7.28',33:'7.29',35:'7.31',37:'7.28',41:'7.31',43:'7.31',46:'7.32',49:'7.35',51:'7.37',53:'7.36',56:'7.38',60:'7.38',62:'7.41',64:'7.40',66:'7.39'}
bookref='Carlson NR, Birkett MA (2022). Physiology of Behavior, Global Edition. 13th edition. Pearson. ISBN 9781292430256. Chapter 7, pp. 210–234; vestibular, somatosensory, gustatory, and olfactory sections only. Audition excluded.'
slides=[]
for i,c in enumerate(CONTENT):
 s=dict(c);s.update(transcript=list(c['body']),layout='figure-right',figure_width=5.7,instructional_role='foundation' if i in F else 'research')
 if i in F:
  s.update(figure=book[bookassign[i]],cite='Carlson & Birkett (2022)',refs=[bookref],primary_source='book')
 else:
  id,num=assign[str(i)];a=figs[f'{id}:{num}'];j=json.loads((ROOT/f'research/downloads/C07/{id}.json').read_text());names=[x for x in j.get('authors',[]) if x.get('type')=='person'];first=names[0]['name']['index'].split(',')[0] if names else a['authors'].split()[0]
  s.update(figure={'path':a.get('display_path',a['path']),'kind':'article','source_url':'https://doi.org/'+a['doi'],'caption':f"{first} et al. ({a['year']}), Fig. {num}.",'credit':a['authors'],'license':a['license']},cite=f"{first} et al. ({a['year']})",refs=[f"{a['authors']} ({a['year']}). {re.sub('<[^>]+>','',a['title'])}. eLife. https://doi.org/{a['doi']}",'Original figure legend: '+a['legend']],primary_source='eLife.'+id)
 if i in [13,14]:s['refs'].append('Moehring et al. (2018). Keratinocytes mediate innocuous and noxious touch via ATP-P2X4 signaling. https://doi.org/10.7554/eLife.31684')
 if i==53:s['refs'].append('Shrestha et al. (2024). Pharyngeal neuronal mechanisms governing sour taste perception in Drosophila melanogaster. https://doi.org/10.7554/eLife.101439. Introduction summarizes mammalian OTOP1 proton-channel evidence; fly receptors are discussed separately.')
 slides.append(s)
spec={'lecture':7,'content_slides':73,'authorized_total_slide_range':[75,75],'theme':'sapphire-silver','output_filename':'Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx','title_kicker':'Balance, Touch, Pain, Taste, and Smell','title_image':book['7.24'],'title_refs':[bookref],'slides':slides,'paragraph_line_requirement':[5,7],'chapter_scope':'Printed pp. 210–234. No audition. Chapter 7 auditory material reserved for a separate future lecture.','takeaways':[
'**Balance combines signals.** Canals detect rotational changes, otolith organs detect gravity and linear acceleration, and vestibular pathways help stabilize gaze and posture.',
'**Touch requires transduction and transmission.** Skin deformation, sensory ending structure, and neuronal excitability determine the signal carried into central pathways.',
'**Pain differs from nociception.** Protective neural responses, reported intensity, unpleasantness, and avoidance measure different components; spinal and descending circuits modify transmission.',
'**Taste begins at receptor cells.** Dissolved chemicals recruit distinct transduction mechanisms, and taste pathways influence perception, feeding, and physiological responses.',
'**Smell uses distributed patterns.** Receptor combinations and glomerular processing distinguish chemicals, while airflow and sampling determine when odor information becomes available.',
'**Flavor combines sensory inputs.** Taste, retronasal smell, texture, temperature, and irritation contribute through distinct receptors; learning and bodily state influence the resulting choices.'
]}
spec['takeaways']={'cite':'Carlson & Birkett (2022); primary studies in notes','refs':[bookref],'items':[{'lead':t.split('**')[1], 'text':t.split('**',2)[2].strip()} for t in spec['takeaways']]}
(D/'lecture.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n')
(D/'SLIDE_SPINE.md').write_text('# Sensing the Body and the Chemical World\n\n1. Title: '+ 'Sensing the Body and the Chemical World: Balance, Touch, Pain, Taste, and Smell\n'+ '\n'.join(f"{i+2}. {s['title']}" for i,s in enumerate(slides))+'\n75. Key takeaways\n')
schedule=ROOT/'course/schedule.json';a=json.loads(schedule.read_text());m=next(x for x in a['lectures'] if x['n']==7);m.update(date='Fall 2026',title='Sensing the Body and the Chemical World: Balance, Touch, Pain, Taste, and Smell',verified=True,book_chapter_title='Audition, the Body Senses, and the Chemical Senses',display_title_authorized=True,display_title_authorization='Instructor requested separate audition and body/chemical senses lectures; this is the 75-slide nonauditory lecture.',textbook_printed_pages='210–234',book_scope_verified_from='Reattached Part3of6, PDF pp. 38–62; Chapter 7 begins printed p.191, and Chapter 8 begins p.235. Audition pp.193–209 excluded.',auditory_lecture_status='Reserved for a separate future deck; not built in this task.')
schedule.write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
print('Assembled',len(slides),'content slides;',len(F),'foundation;',len(slides)-len(F),'research.')
