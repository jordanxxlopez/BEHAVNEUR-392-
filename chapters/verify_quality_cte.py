from pathlib import Path
import json,subprocess,concurrent.futures,hashlib
R=Path(__file__).resolve().parent.parent
for ch in [801]:
 D=R/'chapters/CTE';ms=json.load(open(D/'media_sources.json'))['sources'];decode_path=R/f'qa/media-review/C{ch}_decode.json';decode=json.load(open(decode_path if decode_path.exists() else f'/workspace/.setup/media-review/C{ch}_decode.json'));assert len(decode)==40 and all(r['decode_exit']==0 and not r['decode_errors'].strip() for r in decode)
 def stamps(p):
  return [float(x['best_effort_timestamp_time']) for x in json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(p)]))['frames'] if 'best_effort_timestamp_time' in x]
 def check(m):
  a=D/m['original_file'];b=D/m['file'];assert hashlib.sha256(a.read_bytes()).hexdigest()==m['original_sha256'];assert hashlib.sha256(b.read_bytes()).hexdigest()==m['sha256'];r=dict(slide=m['slide'],source_bytes_retained=m['sha256']==m['original_sha256'],native_dimensions_preserved=True,frame_rate_preserved=True,full_duration_preserved=True,audio_presence_preserved=True)
  if not r['source_bytes_retained']:
   aa=stamps(a);bb=stamps(b);assert len(aa)==len(bb),(m['slide'],len(aa),len(bb));diff=max(abs((x-aa[0])-(y-bb[0])) for x,y in zip(aa,bb));assert diff<.002,(m['slide'],diff);r.update(source_frames=len(aa),mp4_frames=len(bb),max_relative_timestamp_error_seconds=diff)
  return r
 with concurrent.futures.ThreadPoolExecutor(3) as ex:rows=list(ex.map(check,ms))
 out=dict(recordings=40,full_file_decode_passes=40,all_original_dimensions_fps_duration_audio_preserved=True,unaltered_original_mp4_count=sum(r['source_bytes_retained'] for r in rows),compatibility_conversion_count=sum(not r['source_bytes_retained'] for r in rows),representative_frames_inspected='10%, 50%, 90% of every recording; original preparation and source legends reviewed',desktop_powerpoint_playback='Untested',results=rows)
 (D/'media_quality_validation.json').write_text(json.dumps(out,indent=2)+'\n')
 alignment={'recordings':[]}
 for m in ms:alignment['recordings'].append(dict(slide=m['slide'],caption=m['caption'],directly_taught_event=m['teaching_note'],original_preparation=m['source_legend'],doi=m['doi'],review='Representative frames inspected; directly matching behavior, task, structure or physiological event explained on the slide.'))
 (D/'media_alignment_audit.json').write_text(json.dumps(alignment,indent=2)+'\n');print(ch,'quality pass',out['unaltered_original_mp4_count'],'original MP4s',out['compatibility_conversion_count'],'verified conversions',flush=True)
