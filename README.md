# Behavioral Neuroscience 392

Connected repository: https://github.com/jordanxxlopez/BEHAVNEUR-392-.git. The trailing hyphen is part of its name. Neuroethology source tools were copied from the current default branch at commit 5045962, then adapted here without changing NEUR 411.

See AGENTS.md and course/policy.json for course-only requirements. There will be 19 chapter decks, preferably 75 slides each, at most 85; 30–40% textbook foundations and 60–70% primary research, interwoven throughout the lecture; exactly 20 academic and 20 aesthetic embedded videos (40 total) for Chapter 2 and subsequent new decks, each aligned with its slide’s subject. Existing Chapter 1 deliveries retain their original media counts. The textbook contents and first chapter mapping have been verified. The builder retains Neuroethology content layouts and changes the title slide to white with a source image left and instructor details right.

[Teaching prose and transcript requirements](course/TEACHING_STYLE.md) apply to every chapter and authorized revision. Follow the instructor's supplied plain-language example: explain terms as they arise, describe what changes in the cell or animal, and develop connected scientific explanations. Generic study wrap-ups and unexplained strings of technical names do not satisfy the teaching requirement. Chapter 4 has been revised throughout; its slide structure, source imagery, and 40 embedded recordings are preserved.

All six split textbook parts are available in private source storage. Chapter 1 (Introduction, printed pages 15–34) and the table of contents have been reviewed; 19 chapters are confirmed. The prior professor’s three early lectures have been inspected. Three retained EVE excerpts from Neuroethology Lecture 94 have been copied unchanged for reuse. The first deck has a separate Version 2: 75 slides with 30 embedded videos (20 academic and ten visual-context), shorter concrete teaching prose, and 39.7% foundations / 60.3% research. Version 1 remains unchanged. See chapters/C01/version2/STATUS.md and VIDEO_INDEX.md. The PPTX is editable; its accompanying PDF is a static preview.

## Commands

- `python -m pip install -r requirements.txt`
- `python tools/crop_figure.py source.pdf PAGE --preview preview.png`
- `python tools/build_lecture.py chapters/C01/lecture.json`
- Embed source videos and record their provenance in `media_sources.json`.
- `python tools/check_lecture.py chapter.pptx --lecture 1 --content-slides 73`
- `python tools/check_course.py chapters/C01/lecture.json chapter.pptx media_sources.json`
- `soffice --headless --convert-to pdf chapter.pptx` for static visual QA.

The blank template intentionally cannot build a final chapter. The generic checker is necessary but insufficient: the course checker also verifies the chapter title’s verified status, total slides, teaching-source balance, imagery, distinct video quotas, and embedded hashes. Actual desktop PowerPoint playback still needs checking after final media integration.

The expanded Version 2 retains the same slide order, study figures and 30 embedded videos. Every content paragraph now has 5–7 actual rendered lines, verified individually by tools/check_paragraph_lines.py. Use chapters/C01/version2/lecture_expanded.json to rebuild this revision, then embed with `python chapters/C01/version2/embed_media.py lecture_expanded.json`. See PARAGRAPH_LINE_CHECK.md in that folder for all 219 counts.

The latest Chapter 1 history-expanded revision is in [chapters/C01/history_revision](chapters/C01/history_revision/STATUS.md): 90 slides under a lecture-specific authorization, preserving all previous content and 30 videos. It adds 15 historical and related research slides. All 264 content paragraphs pass the 5–7 rendered-line audit. See its VIDEO_INDEX.md and NOBEL_STUDY_MAP.md. Other chapters retain the 85-slide maximum.

## Chapter 2

[How Nerve Cells Work: From Electrical Signals to Chemical Communication](chapters/C02/STATUS.md) contains 75 slides and 40 embedded recordings, split equally between academic and aesthetic context. All 219 teaching paragraphs pass the rendered 5–7-line audit. Download the editable PPTX with Git LFS enabled; the accompanying _Static.pdf contains source posters. See the chapter status, recording index, and slide sequence for provenance and rebuild instructions.

## Chapter 3

[Mapping the Nervous System: From Brain Structures to Behavior](chapters/C03/STATUS.md) contains 75 slides and 40 embedded recordings, distributed ten per quarter and five in the final ten content slides. Media-purpose labels are omitted from all slide text, captions, and teaching notes. Download the editable [PPTX](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C03/Mapping_the_Nervous_System_Chapter_3.pptx) or its [static PDF](chapters/C03/Mapping_the_Nervous_System_Chapter_3_Static.pdf). The source index, crop records, and 219-paragraph rendered audit accompany the lecture.

## Chapter 4

[Chemical Control of Behavior: Drugs and Neural Signaling](chapters/C04/STATUS.md) covers Psychopharmacology and Neurotransmitters, printed pp. 91–118. The 75-slide lecture includes teaching notes, credited original figures, and 40 embedded recordings, with ten in each content quarter and five in the final ten content slides. Download the editable [PPTX](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pptx) or [static PDF](chapters/C04/Chemical_Control_of_Behavior_Chapter_4_Static.pdf). All 219 teaching paragraphs pass the rendered 5–7-line audit. Recording classifications remain in internal provenance records.

## Chapter 5

[Reading and Rewriting the Brain: Tools of Discovery and Neuroengineering](chapters/C05/STATUS.md) expands the verified research-methods chapter into 86 slides, with newer measurement, targeting, analysis, and neural-interface methods. Download the [editable PPTX](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx) or [static PDF](chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5_Static.pdf). All 252 teaching paragraphs pass the rendered 5–7-line check. The 40 embedded recordings are distributed ten per quarter, with six in the final ten teaching slides. Source figures, teaching transcripts, recording provenance, and validation accompany the files.

## Chapter 6

[From Light to Sight: How the Brain Builds the Visual World](chapters/C06/STATUS.md) contains 90 slides, including visual illusions, four slides on rewired ferrets, developmental and adult plasticity, active vision, and visual restoration. Download the [editable PPTX](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C06/From_Light_to_Sight_Chapter_6.pptx) or [static PDF](chapters/C06/From_Light_to_Sight_Chapter_6_Static.pdf). All 264 teaching paragraphs pass the rendered 5–7-line check. Forty distinct embedded recordings are distributed ten per quarter, with six in the final ten teaching slides. Original source panels, teaching transcripts, provenance, and validation accompany the files.

## Chapter 7: body and chemical senses

[Sensing the Body and the Chemical World: Balance, Touch, Pain, Taste, and Smell](chapters/C07/STATUS.md) is the instructor-authorized **75-slide nonauditory** Chapter 7 lecture. Peripheral audition is covered in the separate Part I lecture below; the separate central auditory lecture is available below. It covers balance, touch, proprioception, temperature, itch, pain, taste, smell, and flavor, with 29 foundation slides, 44 research slides, and 40 embedded source recordings.

Download the [editable PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx) or [static PDF preview](chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7_Static.pdf). All 219 teaching paragraphs pass the rendered-line audit. The source index, original-media records, slide sequence, and validation accompany the files. Desktop PowerPoint playback remains untested.

## Audition I: peripheral auditory system

[From Sound to Neural Signals: The Peripheral Auditory System](chapters/C07/Audition1/STATUS.md) contains **80 slides**, including six on animal hair-cell regeneration, mammalian reprogramming, synapse repair, and requirements for translation. It covers acoustics, outer- and middle-ear conduction, cochlear mechanics, transduction, ribbon synapses, auditory-nerve coding, and peripheral injury. Central auditory pathways are reserved for Part II.

Download the [editable PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07/Audition1/From_Sound_to_Neural_Signals_Peripheral_Auditory_System_Part_I.pptx) or [static PDF preview](chapters/C07/Audition1/From_Sound_to_Neural_Signals_Peripheral_Auditory_System_Part_I_Static.pdf). The deck contains 31 foundation slides, 47 research slides, full teaching notes, and 40 distinct embedded recordings. All 234 teaching paragraphs pass the rendered five-to-seven-line audit. See the lecture folder for sources, media provenance, and validation.

## Audition II: central auditory system

[The Listening Brain: How We Find Meaning in Sound, Speech, and Music](chapters/C07_Audition2/STATUS.md) contains **100 slides and 50 embedded videos**, distributed across the full lecture. It covers central pathways, localization, auditory scenes and attention, audiovisual illusions, speech, musical prediction and rhythm, comparative behavior, improvisation, USC Brain and Creativity Institute research, memory, plasticity, communication, echolocation, and cortical music decoding. Peripheral mechanics and transduction remain in Audition I.

Download the [editable PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System.pptx) or [static PDF preview](chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System_Static.pdf). There are 32 foundation slides and 66 research slides; all 294 teaching paragraphs pass the rendered five-to-seven-line audit. Full references, matching teaching notes, source media, and validation accompany the files. Desktop PowerPoint playback remains untested.

## Chapter 8: control of movement

[From Intention to Action: The Neural Control of Movement](chapters/C08/STATUS.md) contains **75 slides** covering muscle physiology, spinal circuits, motor planning, basal ganglia, cerebellum, skilled action, and movement disorders. Download the [editable PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C08/From_Intention_to_Action_Control_of_Movement_Chapter_8.pptx) or [static PDF preview](chapters/C08/From_Intention_to_Action_Control_of_Movement_Chapter_8_Static.pdf). The lecture contains 29 foundation slides, 44 research slides, full teaching transcripts, and 40 distinct embedded recordings. All 219 teaching paragraphs pass the rendered five-to-seven-line check. Sources, original-media records, and validation accompany the files.

## Chapter 10: From Reproduction to Care: Hormones, Social Circuits, and Parenting

A separate 80-slide lecture with 78 teaching slides, 40 embedded original recordings, source figures, full teaching notes and credits.

- [Download PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C10/From_Reproduction_to_Care_Chapter_10.pptx)
- [Static PDF](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C10/From_Reproduction_to_Care_Chapter_10_Static.pdf)
- [Sources and validation](chapters/C10/STATUS.md)

## Chapter 11: Feeling and Acting: The Neural Systems of Emotion

A separate 80-slide lecture with 78 teaching slides, 40 embedded original recordings, source figures, full teaching notes and credits.

- [Download PowerPoint](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C11/Feeling_and_Acting_Emotion_Chapter_11.pptx)
- [Static PDF](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C11/Feeling_and_Acting_Emotion_Chapter_11_Static.pdf)
- [Sources and validation](chapters/C11/STATUS.md)
