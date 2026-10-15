"""Crop intact panels from downloaded publisher figure assets with the repository crop tool.
The temporary PDF embeds the unmodified original raster; it is not a reconstructed figure.
"""
from pathlib import Path
import json,subprocess,fitz
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;TMP=ROOT/'research/downloads/C02/figure_wrappers';TMP.mkdir(parents=True,exist_ok=True)
boxes={'PMC4805541_fig1':([0,.25,.81,.40],'b'),'PMC4805541_fig3':([0,0,.48,.28],'a'),'PMC11524473_fig1':([0,0,.49,.27],'a'),'PMC11524473_fig2':([0,0,.65,.27],'a–b'),'PMC11524473_fig3':([0,0,1,.15],'a'),'PMC11524473_fig4':([0,0,1,.31],'a–d'),'PMC10198724_fig2':([0,.115,1,.47],'B–C'),'PMC10198724_fig4':([0,.10,1,.48],'B–C'),'PMC10198724_fig6':([0,0,1,.47],'A'),'PMC11838871_fig1':([0,.46,1,.77],'D'),'PMC11838871_fig2':([0,0,1,.23],'A–C'),'PMC11838871_fig3':([0,0,.34,.28],'A'),'PMC11838871_fig4':([0,0,1,.30],'A–C'),'PMC4199485_fig1':([0,0,1,.25],'A–D'),'PMC10365837_fig1':([0,0,1,.37],'A'),'PMC10746140_fig2':([0,.11,.69,.47],'b–d')}
boxes={key:(row['normalized_box'],row['panels']) for key,row in json.loads((HERE/'article_crops.json').read_text()).items()}
records={}
for stem,(box,panels) in boxes.items():
 src=HERE/'figures'/(stem+'.png');im=Image.open(src);w,h=im.size
 pdf=TMP/(stem+'.pdf');d=fitz.open();page=d.new_page(width=w/3,height=h/3);page.insert_image(page.rect,stream=src.read_bytes());d.save(pdf);d.close();out=HERE/'figures'/(stem+'_panels.png')
 subprocess.run(['python3',str(ROOT/'tools/crop_figure.py'),str(pdf),'1','--box',*map(str,box),'--dpi','216','-o',str(out)],check=True,stdout=subprocess.DEVNULL)
 records[stem]=dict(original_publisher_figure=str(src.relative_to(HERE)),panels=panels,normalized_box=box,wrapper_pdf=str(pdf),wrapper_page=1,note='Original publisher raster embedded unchanged in a temporary PDF for cropping. No scientific content redrawn, recolored, or replotted.')
spec_path=HERE/'lecture.json';spec=json.loads(spec_path.read_text());media=json.loads((HERE/'media_sources.json').read_text());video_slides={m['slide'] for m in media['sources']}
for i,sd in enumerate(spec['slides'],2):
 f=sd['figure'];stem=Path(f['path']).stem
 if stem in records and (i in video_slides or stem=='PMC11524473_fig3'):
  f['path']='figures/'+stem+'_panels.png';f['crop']=records[stem];f['caption']=f['caption'].replace('Fig. '+stem.split('_fig')[1]+'.','Fig. '+stem.split('_fig')[1]+records[stem]['panels']+'.')
spec_path.write_text(json.dumps(spec,indent=2,ensure_ascii=False)+'\n');(HERE/'article_crops.json').write_text(json.dumps(records,indent=2)+'\n');print('Saved',len(records),'intact source-panel crops.')
