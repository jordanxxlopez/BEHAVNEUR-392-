# Behavioral Neuroscience 392

Connected repository: https://github.com/jordanxxlopez/BEHAVNEUR-392-.git. The trailing hyphen is part of its name. Neuroethology source tools were copied from the current default branch at commit 5045962, then adapted here without changing NEUR 411.

See AGENTS.md and course/policy.json for course-only requirements. There will be 19 chapter decks, preferably 75 slides each, at most 85; approximately 25% textbook foundations and 75% primary research; 15–20 academic and 5–10 aesthetic embedded videos. The textbook contents and first chapter mapping have been verified. The builder retains Neuroethology content layouts and changes the title slide to white with a source image left and instructor details right.

All six split textbook parts are available in private source storage. Chapter 1 (Introduction, printed pages 15–34) and the table of contents have been reviewed; 19 chapters are confirmed. The prior professor’s three early lectures have been inspected. Three retained EVE excerpts from Neuroethology Lecture 94 have been copied unchanged for reuse. The first deck is complete: 75 slides with 20 embedded videos (15 academic and five aesthetic). See chapters/C01/STATUS.md and VIDEO_INDEX.md. The PPTX is editable; its accompanying PDF is a static preview.

## Commands

- `python -m pip install -r requirements.txt`
- `python tools/crop_figure.py source.pdf PAGE --preview preview.png`
- `python tools/build_lecture.py chapters/C01/lecture.json`
- Embed source videos and record their provenance in `media_sources.json`.
- `python tools/check_lecture.py chapter.pptx --lecture 1 --content-slides 73`
- `python tools/check_course.py chapters/C01/lecture.json chapter.pptx media_sources.json`
- `soffice --headless --convert-to pdf chapter.pptx` for static visual QA.

The blank template intentionally cannot build a final chapter. The generic checker is necessary but insufficient: the course checker also verifies the chapter title’s verified status, total slides, teaching-source balance, imagery, distinct video quotas, and embedded hashes. Actual desktop PowerPoint playback still needs checking after final media integration.
