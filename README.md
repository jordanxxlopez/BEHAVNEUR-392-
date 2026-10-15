# Behavioral Neuroscience 392

Connected repository: https://github.com/jordanxxlopez/BEHAVNEUR-392-.git. The trailing hyphen is part of its name. Neuroethology source tools were copied from the current default branch at commit 5045962, then adapted here without changing NEUR 411.

See AGENTS.md and course/policy.json for course-only requirements. There will be 19 chapter decks, preferably 75 slides each, at most 85; 30–40% textbook foundations and 60–70% primary research, interwoven throughout the lecture; exactly 20 academic and 20 aesthetic embedded videos (40 total) for Chapter 2 and subsequent new decks, each aligned with its slide’s subject. Existing Chapter 1 deliveries retain their original media counts. The textbook contents and first chapter mapping have been verified. The builder retains Neuroethology content layouts and changes the title slide to white with a source image left and instructor details right.

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
