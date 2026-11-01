import datetime, difflib, hashlib, json, pathlib, subprocess
from zoneinfo import ZoneInfo
root=pathlib.Path(__file__).resolve().parent
docs=json.loads((root/'rules_downloaded.json').read_text())
for path in ['AGENTS.md','.claude/skills/neuroethology-lecture/SKILL.md','prompts/make_lecture.md','chatgpt/INSTRUCTIONS.md','chatgpt/lecture_prompt.md','prompts/image_note.md']:
    ref='fa278dba43f4bb18527b3237845da0189a37ec24'
    url=f'https://raw.githubusercontent.com/jordanxxlopez/NEUROETHOLOGY/{ref}/{path}'
    text=subprocess.check_output(['curl','-fLsS','--retry','3','--max-time','60',url]).decode()
    docs.append(dict(path=path,ref=ref,text=text,url=url,neuro=True))
for ref in ['ae568eda8d59773a0e25915051e60950e3453a5d','edea0a2980a2f32ea3ee35f8768c1e7419cf3c6d']:
    url=f'https://api.github.com/repos/jordanxxlopez/BEHAVNEUR-392-/commits/{ref}'
    data=json.loads(subprocess.check_output(['curl','-fLsS','--retry','3',url]))
    text=data['commit']['message']+'\n\n'+'\n\n'.join(f['filename']+'\n'+f.get('patch','[Binary file or patch unavailable]') for f in data['files'])
    docs.append(dict(path='Chapter 16-17 commit record',ref=ref,text=text,url=url,revision=True))
head='b443ca5046590de25eaa2c18614166c2234b430c'
priority=['AGENTS.md','course/TEACHING_STYLE.md','course/policy.json','prompts/make_chapter.md','course/schedule.json','course/themes.json','README.md','downloads/README.md']
groups=[('CURRENT COURSE RULES AND COURSE PLAN',[d for p in priority for d in docs if d['path']==p and d['ref']==head and not d.get('history')]),
('CHAPTER REQUIREMENTS, REVISIONS, SOURCES, AND DELIVERY RECORDS',[d for d in docs if d['ref']==head and d['path'] not in priority and not d['path'].startswith(('tools/','tests/','research/lecture02_guidelines/'))]),
('INHERITED NEUROETHOLOGY REFERENCES - SUBORDINATE TO COURSE OVERRIDES',[d for d in docs if d.get('neuro') or d['path'].startswith('research/lecture02_guidelines/')]),
('EXACT BUILD AND AUTOMATED VALIDATION IMPLEMENTATION',[d for d in docs if d['ref']==head and d['path'].startswith(('tools/','tests/'))]),
('OTHER BRANCH SNAPSHOTS AND CHAPTER 16-17 REVISION RECORDS',[d for d in docs if d.get('revision') or (d['ref']!=head and not d.get('history') and not d.get('neuro'))]),
('HISTORICAL RULE VERSIONS - OLDEST TO NEWEST',sorted([d for d in docs if d.get('history')],key=lambda d:(d['date'],d['path'])))]
intro='''BEHAVIORAL NEUROSCIENCE 392 — COLLECTED CREATION RULES AND HISTORY

One self-contained, searchable UTF-8 text file. Source documents are reproduced
in full, not summarized. Markdown syntax and source-code formatting are preserved.

SCOPE AND AUTHORITY
This compilation gathers the recorded instructions for the 23 lecture collection:
Chapters 1–19, two separate auditory lectures, and two football/CTE lectures.
The principal source is jordanxxlopez/BEHAVNEUR-392-, latest lecture branch
football-psychology-lecture, commit b443ca5046590de25eaa2c18614166c2234b430c.
All six branch trees were checked for additional course-rule snapshots.
The historical appendix contains all returned versions of AGENTS.md,
course/policy.json, course/TEACHING_STYLE.md, and prompts/make_chapter.md
along the latest lecture branch's history. The six Neuroethology reference
documents are pinned to the revision explicitly referenced by the teaching guide.

This is the recoverable repository record, not a transcript of every private chat.
Instructions that were never committed or supplied in this conversation cannot
be recovered here. Status reports record delivered behavior and are distinguished
from authoritative rules; passing checks is not proof of every scientific claim.
Scientific claims and historical award statements in source instructions are
reproduced as instructions, not independently verified by this compilation.

HOW TO APPLY THESE DOCUMENTS
1. Explicit instructor instructions take precedence over inherited course rules.
2. Use the current BEHAVNEUR AGENTS, teaching style, and course policy together.
3. Apply chapter-specific authorizations only to their named chapters.
4. Preserve historical versions for provenance; do not combine contradictory
   old requirements with the current requirements.
5. Inherited Neuroethology materials are reference material where compatible.
   They do not override Behavioral Neuroscience's level, title layout, quotas,
   or paragraph-length rules. Code checks also do not override the instructor.

EXPLICIT SUPERSESSION AND EXCEPTIONS TO WATCH
- Five to seven actual rendered lines per paragraph supersede the earlier
  70–110-word target. Do not import an older Neuroethology sentence quota.
- New Chapter 2 and later decks normally use 40 distinct videos, 20 academic
  plus 20 aesthetic/context; this supersedes the earlier 20–30 range.
- Chapter 1 retains its delivered counts unless specifically revised.
- Chapter 3 onward normally distributes 10 videos per quarter, no gap greater
  than three content slides, and at least five in the final ten content slides.
- Chapter 14's later recording-alignment revision has specific placements in
  policy.json and its audit; do not blindly undo them to satisfy an older plan.
- Chapter 1 history expansion: 90 slides; Chapter 5: 86; Chapter 6: 90;
  Chapter 9: 86. These are local exceptions to the general slide-count rule.
- Peripheral audition is a separate 80-slide lecture. Central audition is
  100 slides, 50 videos (25 plus 25), distributed 13/12/13/12.
- The Chapter 4 writing revision preserves titles, order, layout, figures,
  recordings, captions, credits, and takeaways while replacing teaching prose
  and matching transcripts. It is not authorization to revise other decks.
- Later chapter/special-lecture status and settings records document their
  delivered 80-slide configurations and other specific layout decisions.

LATEST PACKAGING REQUEST FROM THIS CHAT (NOT AN ORIGINAL LECTURE RULE)
Provide the latest 23 distinct lecture versions as complete PDFs in one ZIP,
with EACH PDF below 29 MB. Exclude the three superseded Chapter 1 decks.
PDFs are static and do not play embedded PowerPoint recordings.

SOURCE ORGANIZATION
'''
parts=[intro]
for i,(name,ds) in enumerate(groups,1):
    parts.append(f'{i}. {name} ({len(ds)} source snapshots)\n')
parts.append('\nREPOSITORY COMMIT CHRONOLOGY (America/Los_Angeles)\n')
for c in reversed(json.loads((root/'rule_commit_history.json').read_text())):
    dt=datetime.datetime.fromisoformat(c['date'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Los_Angeles'))
    parts.append(f"{dt.isoformat()} | {c['sha']} | {c['message']}\n")
number=0
for gi,(name,ds) in enumerate(groups,1):
    parts.append('\n'+'='*90+f'\nPART {gi}: {name}\n'+'='*90+'\n')
    for d in ds:
        number+=1
        parts.append(f"\nSOURCE {number:03d}: {d['path']}\nRevision: {d['ref']}\nURL: {d['url']}\nSHA256 of source text: {hashlib.sha256(d['text'].encode()).hexdigest()}\n")
        if d.get('date'): parts.append(f"Recorded commit time (UTC): {d['date']}\nCommit message: {d['message']}\n")
        parts.append('\n----- BEGIN ORIGINAL SOURCE -----\n'+d['text']+'\n----- END ORIGINAL SOURCE -----\n')
parts.append(f'\nEND OF COMPILATION — {number} source snapshots.\n')
out=root.parent/'outputs'/'BEHAVNEUR392_All_Creation_Rules_and_History.txt'
out.write_text(''.join(parts),encoding='utf-8')
saved=out.read_text()
assert number==len(docs),(number,len(docs))
assert saved.count('----- BEGIN ORIGINAL SOURCE -----')==number
assert saved.count('----- END ORIGINAL SOURCE -----')==number
for d in docs: assert d['text'] in saved
print(json.dumps(dict(file=str(out),sources=number,bytes=out.stat().st_size,words=len(saved.split()),all_source_texts_preserved=True)))
