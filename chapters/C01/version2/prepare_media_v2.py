from pathlib import Path
import json,subprocess,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];ORIG=ROOT/'research/downloads/v2_original_media';M=HERE/'media'
map_={int(k):v for k,v in json.loads((HERE/'slide_order.json').read_text())['original_to_v2'].items()}
old=json.loads((HERE.parent/'media_sources.json').read_text());rows=[x for x in old['sources'] if 'lancaster_video_2' not in x['file']]
for x in rows:
 if x['slide']==17:x['slide']=16
 x['original_slide']=x['slide'];x['slide']=map_[x['slide']]
 x['alignment']='Recording illustrates the named behavior, method, or anatomical context on the adjacent teaching slide.'
refs=json.loads((HERE/'lecture.json').read_text())['slides'];downloads={x['name']:x['url'] for x in json.loads((ORIG/'downloads.json').read_text())}
items=[
(3,'academic','seizure_movie.mp4','Dogra et al. (2025), S2 Movie. Midbrain calcium events in a zebrafish epilepsy model.','https://journals.plos.org/plosbiology/article/file?id=10.1371/journal.pbio.3002499.s015&type=supplementary','10.1371/journal.pbio.3002499','Bright changes identify calcium events in individual cells. This is a zebrafish model with altered slc13a5 genes, not a recording of the human clinical case. The publisher describes 1,000-fps acquisition; its supplied 120-fps, three-second display is preserved.'),
(20,'aesthetic','lancaster_nuclei.mov','Development context: Lancaster et al. (2013), Supplementary Video 1. Nuclear movement in cerebral organoids.',downloads['lancaster_nuclei.mov'],'10.1038/nature12517','The arrow follows the nucleus of a radial glial precursor cell through developing tissue. The original hours:minutes timestamps are retained. This visual example accompanies neural development rather than providing evidence about human brain growth rates.'),
(30,'academic','inagaki_feeding.mov','Inagaki et al. (2014), Supplementary Video 1. Light-triggered proboscis extension.',downloads['inagaki_feeding.mov'],'10.1038/nmeth.2765','The feeding structure extends when sugar-sensing Gr5a neurons expressing ReaChR are stimulated. Compare pulsed and sustained 627-nm illumination. The visible indicator is an infrared LED, not the fly’s visible stimulus.'),
(31,'academic','inagaki_courtship.mov','Inagaki et al. (2014), Supplementary Video 5. P1 and pIP10 activation recruits wing extension.',downloads['inagaki_courtship.mov'],'10.1038/nmeth.2765','Recognize wing extension, a courtship action, during activation of the named neuronal groups. This recording illustrates the evoked behavior; the adjacent study figure supplies the social-history comparison.'),
(33,'aesthetic','antinucci_anatomy.mp4','Anatomy context: Antinucci et al. (2019), Video 1. Zebrafish brain and retinal projection fields.',downloads['antinucci_anatomy.mp4'],'10.7554/elife.48114','The publisher’s z-stack traverses fluorescently labeled larval brain tissue and annotated retinal projection fields. This is the anatomy used for imaging, not a recording of optically evoked hunting.'),
(37,'aesthetic','inagaki_motor.mov','Movement context: Inagaki et al. (2014), Supplementary Video 2. Sideways walking during optical activation.',downloads['inagaki_motor.mov'],'10.1038/nmeth.2765','Recognize sideways walking in the first part and suppressed movement in the second part during HB9-driver activation. This comparison is a different targeted-cell experiment from the Cande descending-neuron study.'),
(44,'aesthetic','vr_mouse_tracking.mp4','Landmark context: Stowers et al. (2017), Supplementary Video 9. Real-time mouse-head tracking.',downloads['vr_mouse_tracking.mp4'],'10.1038/nmeth.4399','Head location is green; body outline and center are magenta. This original tracking demonstration illustrates anatomical landmarks in a distinct method from DeepLabCut.'),
(65,'aesthetic','vr_fish_scene.mp4','Feedback context: Stowers et al. (2017), Supplementary Video 3. Visual scenes around a freely swimming fish.',downloads['vr_fish_scene.mp4'],'10.1038/nmeth.4399','Compare the real fish and the simulated scene. The demonstration illustrates action-dependent visual input in a separate preparation from the cultured-neuron paddle task.'),
(70,'academic','vr_fly_optomotor.mp4','Stowers et al. (2017), Supplementary Video 10. Visual feedback guides free-flight turning.',downloads['vr_fly_optomotor.mp4'],'10.1038/nmeth.4399','A rotating visual scene recruits the optomotor response so the fly follows an imposed figure-eight trajectory. Compare the real animal with the displayed trajectory.'),
(71,'aesthetic','vr_perspective.mp4','Perspective context: Stowers et al. (2017), Supplementary Video 1. Updating a scene for a moving observer.',downloads['vr_perspective.mp4'],'10.1038/nmeth.4399','The demonstration illustrates viewpoint-dependent rendering, not an animal’s preference test. Watch how the apparent object position changes as the camera representing the observer moves.'),
(72,'academic','vr_social_feedback.mp4','Stowers et al. (2017), Supplementary Video 14. Reciprocal movement of real and virtual fish.',downloads['vr_social_feedback.mp4'],'10.1038/nmeth.4399','The virtual fish reacts to the real fish’s position. In the supplied example, omega equals 1, balancing social and goal-oriented behavior. The footage makes reciprocal social feedback visible.')]
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]))
for original_slide,purpose,name,caption,url,doi,note in items:
 src=ORIG/name;raw=probe(src);v=next(x for x in raw['streams'] if x['codec_type']=='video');a=[x for x in raw['streams'] if x['codec_type']=='audio'];dest=M/(Path(name).stem+'.mp4')
 copyvideo=v['codec_name']=='h264' and v.get('pix_fmt')=='yuv420p';copyaudio=all(x['codec_name']=='aac' for x in a)
 if src.suffix=='.mp4' and copyvideo and copyaudio:shutil.copy2(src,dest);conversion='Publisher MP4 retained byte-for-byte.'
 else:
  cmd=['ffmpeg','-y','-v','error','-i',str(src),'-map','0:v:0','-map','0:a?']
  cmd+=['-c:v','copy'] if copyvideo else ['-c:v','libx264','-crf','16','-preset','medium','-pix_fmt','yuv420p']
  cmd+=['-c:a','copy'] if copyaudio else ['-c:a','aac','-b:a','192k']
  cmd+=['-movflags','+faststart',str(dest)];subprocess.run(cmd,check=True)
  conversion='Compatible H.264 video stream remuxed without video re-encoding.' if copyvideo else 'MPEG-4 Part 2 video converted to H.264/yuv420p at CRF 16, native dimensions and frame rate; no cropping or scientific edits.'
  if a and not copyaudio:conversion+=' Audio converted to AAC at 192 kb/s.'
 final=probe(dest);fv=next(x for x in final['streams'] if x['codec_type']=='video');fa=[x for x in final['streams'] if x['codec_type']=='audio']
 assert (fv['width'],fv['height'],fv['avg_frame_rate'])==(v['width'],v['height'],v['avg_frame_rate'])
 assert abs(float(final['format']['duration'])-float(raw['format']['duration']))<.1
 post=M/(dest.stem+'_poster.jpg');t=min(float(final['format']['duration'])/3,10)
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(t),'-i',str(dest),'-frames:v','1',str(post)],check=True)
 credit=next((r for r in refs[map_[original_slide]-2]['refs'] if doi in r),None)
 if not credit:
  credit=('Stowers JR, Hofbauer M, Bastien R, Griessner J, Higgins P, Farooqui S, Fischer RM, Nowikovsky K, Haubensak W, Couzin ID, Tessmar-Raible K, Straw AD (2017). Virtual reality for freely moving animals. Nature Methods 14:995–1002. https://doi.org/'+doi) if '4399' in doi else 'Authors of the identified primary study; original publisher recording.'
 rows.append({'slide':map_[original_slide],'original_slide':original_slide,'purpose':purpose,'file':'media/'+dest.name,'poster':'media/'+post.name,'caption':caption,'original_url':url,'credit':credit,'doi':doi,'license':'Original primary-article supplement; article reuse terms apply. No independent license inferred.','width':fv['width'],'height':fv['height'],'duration_seconds':float(final['format']['duration']),'frame_rate':fv['avg_frame_rate'],'display_aspect_ratio':fv.get('display_aspect_ratio',f"{fv['width']}:{fv['height']}"),'video_codec':fv['codec_name'],'audio_present':bool(fa),'audio_codecs':[x['codec_name'] for x in fa],'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'bytes':dest.stat().st_size,'conversion':conversion,'teaching_note':note,'alignment':note,'retrieval':'Downloaded from primary publisher or PMC during Version 2 revision, not copied from repository media.'})
rows.sort(key=lambda x:x['slide']);assert len(rows)==30;assert len({x['slide'] for x in rows})==30;assert len({x['sha256'] for x in rows})==30
assert sum(x['purpose']=='academic' for x in rows)==20;assert sum(x['purpose']=='aesthetic' for x in rows)==10
for x in rows:
 sd=refs[x['slide']-2]
 x['adjacent_slide_title']=sd['title']
 if x['credit'] not in sd['refs']:sd['refs'].append(x['credit'])
 if x['original_slide']==10:x['teaching_note']='Observe the barreleye’s transparent head and visible eyes beside the explanation of sensory structures and biological function.'
 if x['original_slide']==15:x['teaching_note']='Observe the dragonfish’s visible body and light-producing structures beside the discussion of inherited traits and their biological roles. This footage does not record natural selection occurring.'
 if x['original_slide']==16:x['teaching_note']='Observe the vampire squid’s arms and fine filaments beside the explanation of biological function. This footage illustrates a living structure, not mutation or a selection experiment.'
(HERE/'media_sources.json').write_text(json.dumps({'academic_count':20,'aesthetic_count':10,'embedded_video_count':30,'sources':rows,'playback_note':'Package and full decode checks performed; Microsoft PowerPoint playback is not available here.'},indent=2,ensure_ascii=False)+'\n')
sp=json.loads((HERE/'lecture.json').read_text());sp['slides']=refs;(HERE/'lecture.json').write_text(json.dumps(sp,indent=2,ensure_ascii=False)+'\n')
print('Prepared 30 distinct, slide-matched videos on 30 slides: 20 academic and 10 visual context. Eleven recordings freshly downloaded, one replacing a mismatched prior clip.')
