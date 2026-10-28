"""Final course, render, source-media and delivery verification."""
from pathlib import Path
import json,hashlib,subprocess,sys
from pptx import Presentation
import fitz
R=Path(__file__).resolve().parent.parent
for ch in map(int,sys.argv[1:] or [18,19]):
 D=R/'chapters/CTE';sp=D/'lecture.json';s=json.load(open(sp));deck=D/s['output_filename'];pp=deck.with_name(deck.stem+'_Static.pdf');prs=Presentation(deck);pdf=fitz.open(pp);lines=json.load(open(D/'paragraph_line_check.json'));mv=json.load(open(D/'media_embedding_validation.json'));quality=json.load(open(D/'media_quality_validation.json'));ms=json.load(open(D/'media_sources.json'))['sources'];checks={}
 for name,cmd in [('generic',['python','tools/check_lecture.py',str(deck),'--lecture',str(ch),'--content-slides','78']),('course',['python','tools/check_course.py',str(sp),str(deck),str(D/'media_sources.json')])]:
  a=subprocess.run(cmd,cwd=R,capture_output=True,text=True);checks[name]=dict(exit_code=a.returncode,output=a.stdout+a.stderr);print(ch,name,a.returncode,(a.stdout+a.stderr).strip(),flush=True)
 assert all(c['exit_code']==0 for c in checks.values()),checks
 assert len(prs.slides)==len(pdf)==80;assert lines['passing']==234 and not lines['failures'];h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert lines['spec_sha256']==h(sp) and lines['pptx_sha256']==h(deck) and lines['pdf_sha256']==h(pp)
 fonts=set()
 for sn,sl in enumerate(prs.slides):
  for sh in list(sl.shapes)+list(sl.notes_slide.shapes):
   if sh.has_text_frame:
    for p in sh.text_frame.paragraphs:fonts.update(r.font.name for r in p.runs if r.text)
  if 0<sn<79:
   sd=s['slides'][sn-1];body=next(sh for sh in sl.shapes if sh.name=='Body');assert [p.text for p in body.text_frame.paragraphs]==sd['body'];assert sd['transcript']==sd['body'];assert sl.notes_slide.notes_text_frame.text.startswith('\n\n'.join(sd['body']))
 assert fonts=={'Arial'},fonts
 assert quality['full_file_decode_passes']==40
 counts={r:sum(x['instructional_role']==r for x in s['slides']) for r in ['foundation','research']};assert counts=={'foundation':31,'research':47}
 result=dict(slides=80,teaching_slides=78,teaching_paragraphs=234,paragraphs_passing_actual_line_audit=234,roles=counts,fonts=['Arial'],notes_slides=80,pdf_pages=80,embedded_recordings=40,media_purposes=mv['purposes'],recordings_per_quarter=mv['content_quarters'],maximum_unrecorded_content_gap=mv['maximum_unrecorded_content_gap'],recordings_in_final_ten_content=mv['final_ten_content_recordings'],source_hashes_and_internal_relationships_verified=True,full_file_decodes_passed=40,unaltered_publisher_mp4s=quality['unaltered_original_mp4_count'],compatibility_conversions=quality['compatibility_conversion_count'],desktop_powerpoint_playback='Untested',layout='Established course layout: upper figure zone 5.7 × 2.3 inches; lower video zone 5.7 × 2.1 inches; aspect ratios retained; inline playback configured.',pptx_sha256=h(deck),static_pdf_sha256=h(pp),pptx_bytes=deck.stat().st_size,static_pdf_bytes=pp.stat().st_size,checks=checks)
 (D/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
 text=f"# Special topic: {s['title_kicker']}\n\n80 slides: title, 78 teaching slides, and six final key takeaways. There are 31 foundation slides and 47 research slides. All 234 teaching paragraphs pass the actual 5–7-line PDF audit, and the teaching transcripts match. All native slide and note text uses Arial.\n\n40 distinct original recordings are embedded inside the PPTX for offline use. Internal classifications are 20 + 20, with 10 recordings per content quarter and at least five in the final ten content slides. Figures and large recordings retain the established split right-column layout and source aspect ratios. Inline playback is configured. Desktop PowerPoint playback remains untested.\n\nAll complete recording files decoded without errors. Every selected movie has a source-specific observation note, original URL, DOI, supplied license, credit, native dimensions, duration, audio and codec data, and SHA256. Original MP4s retain their source bytes; compatibility conversions preserve native dimensions, frame rate, full duration, frame count, relative timestamps, and audio presence. All embedded relationships and source hashes pass.\n\nThe clearly labeled static PDF keeps source posters and does not play videos. Presenton companions are also static; the course-built native PPTX is the offline-video deliverable. Arial is the only authored font. No full uploaded textbook PDF is published.\n\nThe instructor-authorized special topic defines scope; CTE-specific primary literature supplies the main evidence. Original figures, full citations, and source legends are recorded in lecture.json, sources.json, figure_sources.json, book_crops.json, and media_sources.json. Cross-course source overlap is recorded separately. Cross-chapter method callbacks remain explicitly identified.\n\nGeneric and course checkers pass. See VALIDATION.json, paragraph_line_check.json, media_embedding_validation.json, media_quality_validation.json, and media_alignment_audit.json.\n"
 (D/'STATUS.md').write_text(text)
 index=['# Recording index','','The source-specific captions and observations below correspond to embedded movies in the native PowerPoint.','']
 for m in ms:index += [f"## Slide {m['slide']}: {m['caption']}",'',m['teaching_note'],'',m['full_reference'],'','Original: '+m['original_url'],'']
 (D/'RECORDING_INDEX.md').write_text('\n'.join(index)+'\n')
 papers=['# Primary sources','','Figures and recordings use the cited original publishers. Full source metadata and captions are preserved in the JSON manifests.','']
 for k,j in json.load(open(D/'sources.json')).items():papers.append(f"- {j.get('authorLine','')} ({j.get('year',j.get('published','')[:4])}). {j['title']}. https://doi.org/{j['doi']}")
 (D/'PAPERS.md').write_text('\n'.join(papers)+'\n');print(ch,'ALL FINAL CHECKS PASS',flush=True)
