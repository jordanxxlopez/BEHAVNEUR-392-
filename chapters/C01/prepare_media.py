from pathlib import Path
import json,shutil,hashlib,subprocess
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent;NEURO=Path('/workspace/NEUROETHOLOGY');M=HERE/'media';M.mkdir(exist_ok=True);rows=[]
def add(slide,purpose,file,caption,url,credit,doi=None,license='No separate open reuse license stated in the source metadata.',poster=None,note='',source_context=None):
 file=Path(file);dest=M/file.name
 if file.resolve()!=dest.resolve():shutil.copy2(file,dest)
 raw=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(dest)]));v=next(x for x in raw['streams'] if x['codec_type']=='video');a=[x for x in raw['streams'] if x['codec_type']=='audio']
 assert v['codec_name']=='h264' and v.get('pix_fmt')=='yuv420p',(dest,v['codec_name'],v.get('pix_fmt'))
 assert not a or all(x['codec_name']=='aac' for x in a),(dest,a)
 if poster and Path(poster).exists():
  post=M/Path(poster).name
  if Path(poster).resolve()!=post.resolve():shutil.copy2(poster,post)
 else:
  post=M/(dest.stem+'_poster.jpg');duration=float(raw['format']['duration']);ss=min(12,max(.1,duration/3))
  subprocess.run(['ffmpeg','-y','-v','error','-ss',str(ss),'-i',str(dest),'-frames:v','1',str(post)],check=True)
 sha=hashlib.sha256(dest.read_bytes()).hexdigest();row={'slide':slide,'purpose':purpose,'file':'media/'+dest.name,'poster':'media/'+post.name,'caption':caption,'original_url':url,'credit':credit,'doi':doi,'license':license,'width':v['width'],'height':v['height'],'duration_seconds':float(raw['format']['duration']),'frame_rate':v.get('avg_frame_rate'),'display_aspect_ratio':v.get('display_aspect_ratio',str(v['width'])+':'+str(v['height'])),'video_codec':v['codec_name'],'audio_present':bool(a),'audio_codecs':[x['codec_name'] for x in a],'sha256':sha,'bytes':dest.stat().st_size,'conversion':'Retained compatible H.264/AAC MP4 copied byte-for-byte; no resolution, speed, scene, or audio changes. Poster is an unedited source frame.','teaching_note':note}
 if poster and 'figure_poster' in str(poster):row['conversion']='Compatible source MP4 copied byte-for-byte. Poster is an intact credited article-figure fallback, not a generated frame.'
 if source_context:row['source_context']=source_context
 rows.append(row)
# Primary-publisher recordings retrieved for this lecture.
for number,slide,what in [(1,43,'Markerless tracking of a mouse following an odor trail.'),(2,45,'Markerless tracking of fly body parts.'),(3,47,'Mouse digit and wrist tracking during a reaching movement.')]:
 i=number+2;add(slide,'academic',M/f'dlc_video_{number}.mp4',f'Mathis et al. (2018), Supplementary Video {number}. {what}',f'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41593-018-0209-y/MediaObjects/41593_2018_209_MOESM{i}_ESM.mp4','Mathis, Mamidanna, Cury, Abe, Murthy, Mathis, and Bethge','10.1038/s41593-018-0209-y',note=what)
for number,identifier,slide,what in [(1,621,27,'Wireless light delivery to premotor cortex and circling behavior.'),(2,622,34,'Wireless light delivery during running, tube exploration, and social interaction.')]:
 add(slide,'academic',M/f'mont_{identifier}.mp4',f'Montgomery et al. (2015), Supplementary Video {number}. {what}',f'https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fnmeth.3536/MediaObjects/41592_2015_BFnmeth3536_MOESM{identifier}_ESM.mp4','Montgomery and coauthors','10.1038/nmeth.3536',note=what)
# Original peer-reviewed cultured-network recordings, with prior verified provenance.
for lecture,selected in [(71,{'kagan_video_s1.mp4':(66,'academic'),'kagan_video_s2.mp4':(67,'academic'),'lancaster_video_2.mp4':(3,'aesthetic')}),(72,{'cai_video_2.mp4':(68,'academic'),'cai_video_1.mp4':(69,'academic')}),(83,{'NIHMS73580-supplement-Supplementary_Video_13.mp4':(73,'academic'),'NIHMS73580-supplement-Supplementary_Video_8.mp4':(74,'academic')})]:
 folder=NEURO/f'lectures/L{lecture}';data=json.loads((folder/'media_sources.json').read_text())
 for x in data['embedded']:
  name=Path(x['path']).name
  if name in selected:
   slide,purpose=selected[name];caption=x['caption']
   if purpose=='aesthetic':caption='Visual context: '+caption
   add(slide,purpose,folder/x['path'],caption,x.get('original_media_url') or x.get('source_url') or x.get('retrieved_url'),x.get('credit',f'Authors of the cited article, retained from Lecture {lecture}'),x.get('doi'),x.get('license','Article recording; no separate license stated.'),folder/x['poster'] if x.get('poster') else None,x.get('teaching_note','Published original neural or behavioral recording related to the adjacent source figure.'))
# Verified publisher-supplement excerpt showing EVE target-control training.
folder=NEURO/'lectures/L94';data=json.loads((folder/'media_sources.json').read_text());x=next(x for x in data['eve_excerpts'] if x['slide']==9)
add(54,'academic',folder/x['path'],x.get('caption','Winship et al. (2023), article-provided video excerpt. Initial cursor targeting.'),x['original_media_url'],x['credit'],x['doi'],x['license'],folder/x['poster'],x.get('teaching_note','Directional contact moves the cursor toward the target.'),{'original_filename':x['original_filename'],'original_source_hash':x['original_sha256'],'source_start_seconds':x['source_start_s'],'source_end_seconds':x['source_end_s']})
for oldslide,newslide in [(6,56),(21,59),(22,55)]:
 x=next(x for x in data['additional_uploaded_excerpts'] if x['slide']==oldslide)
 add(newslide,'academic',folder/x['path'],x['caption'],'https://www.youtube.com/watch?v=MMJB4Z7OEL0','Instructor-uploaded Meet_EVE_HD (1).mp4, identified by the instructor as the ASAB Meet EVE recording','10.3390/ani15203007',x['license'],folder/x['poster'],x['teaching_note'],{'original_filename':x['original_filename'],'source_start_seconds':x['source_start_s'],'source_end_seconds':x['source_end_s'],'original_source_hash':x['source_sha256'],'identity_note':'Instructor identified the retained footage as the cited ASAB recording; byte identity with the YouTube upload was not independently checked. Retained excerpt hashes are verified.'})
# Five separately identified aesthetic/context recordings, never counted as academic evidence.
meta=json.loads((NEURO/'lectures/L100/additional_videos/media_sources.json').read_text())
for x in meta.get('added',meta.get('sources',meta.get('embedded',[]))):
 if 'MBARI_' in x.get('path',''):
  slide={'MBARI_barreleye.mp4':(10),'MBARI_dragonfish.mp4':(15),'MBARI_vampire_squid.mp4':(17)}[Path(x['path']).name]
  add(slide,'aesthetic',NEURO/'lectures/L100'/x['path'],'Visual context: '+x['caption'],x['original_media_url'],x['credit'],license=x['license'],poster=NEURO/'lectures/L100'/x['poster'],note='Real animal footage accompanies the textbook discussion of biological function, evolution, and variation. It is visual context and is not experimental evidence for the adjacent claims.')
bimbo=Path('/workspace/sea-lions-uploaded-videos/Sea Lions I/Bimbo_balance.mp4')
add(21,'aesthetic',bimbo,'Visual context: Blackpool Zoo (2009). Bimbo balancing a ball.','https://www.youtube.com/watch?v=aoYOyxJu9EM','Blackpool Zoo; instructor-uploaded retained recording',license='Instructor-uploaded recording; no separate open license established.',note='Real sea-lion behavior supplies managed-animal context. It is not a recording from the EVE research study.')
assert len(rows)==20,(len(rows),[(x['slide'],x['purpose']) for x in rows]);assert sum(x['purpose']=='academic' for x in rows)==15;assert sum(x['purpose']=='aesthetic' for x in rows)==5
assert len(set(x['sha256'] for x in rows))==20
for x in rows:
 if x.get('doi')=='10.1038/s41928-023-01069-w':
  speed=4 if 'video_1' in x['file'] else 10
  x['publisher_display_speed']=str(speed)+'x'
  if speed==4:x['caption']='Cai et al. (2023), Supplementary Video 1. Organoid spike-activity heat map (publisher 4× playback).'
  else:x['caption']='Cai et al. (2023), Supplementary Video 2. Confocal calcium activity (publisher 10× playback).' 
  x['teaching_note']+=' Publisher supplied '+str(speed)+'x display speed and a 100-micrometer scale bar; both are retained unchanged.'
rows.sort(key=lambda x:x['slide']);(HERE/'media_sources.json').write_text(json.dumps({'academic_count':15,'aesthetic_count':5,'embedded_video_count':20,'sources':rows,'playback_note':'Full MP4 decoding and package relationships are checked locally; playback in Microsoft PowerPoint has not been tested.'},indent=2,ensure_ascii=False)+'\n');print('Prepared 20 distinct compatible movies: 15 academic and 5 aesthetic.')
