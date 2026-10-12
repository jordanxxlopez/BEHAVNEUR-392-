# Behavioral Neuroscience 392

Connected repository: https://github.com/jordanxxlopez/BEHAVNEUR-392-.git. The trailing hyphen is part of its name. Neuroethology source tools were copied from the current default branch at commit 5045962, then adapted here without changing NEUR 411.

See AGENTS.md and course/policy.json for course-only requirements. There will be 19 chapter decks, preferably 75 slides each, at most 85; approximately 25% textbook foundations and 75% primary research; 15–20 academic and 5–10 aesthetic embedded videos. Exact contents and chapter titles are pending direct book verification. The builder retains Neuroethology content layouts and changes the title slide to white with a source image left and instructor details right.

The uploaded full textbook exceeds the execution tool’s 32 MiB transfer limit. It has not been read or cropped. The former professor’s three early lectures have now been inspected; see research/prior_lectures_analysis.md. The new files.zip also exceeds the 32 MiB transfer limit. A smaller contents/Chapter 1 extract is still required before claiming direct textbook review. No final lecture PPTX has been produced.

## Commands

- `python -m pip install -r requirements.txt`
- `python tools/crop_figure.py source.pdf PAGE --preview preview.png`
- `python tools/build_lecture.py chapters/C01/lecture.json`
- Embed source videos and record their provenance in `media_sources.json`.
- `python tools/check_lecture.py chapter.pptx --lecture 1 --content-slides 73`
- `python tools/check_course.py chapters/C01/lecture.json chapter.pptx media_sources.json`
- `soffice --headless --convert-to pdf chapter.pptx` for static visual QA.

The blank template intentionally cannot build a final chapter. The generic checker is necessary but insufficient: the course checker also verifies the chapter title’s verified status, total slides, teaching-source balance, imagery, distinct video quotas, and embedded hashes. Actual desktop PowerPoint playback still needs checking after final media integration.
