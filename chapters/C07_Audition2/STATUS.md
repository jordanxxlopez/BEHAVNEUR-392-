# The Listening Brain: How We Find Meaning in Sound, Speech, and Music

Completed **Audition II: Central Auditory Processing** for Behavioral Neuroscience 392, Fall 2026. Jordan Lopez, Ph.D., Professor of Neurobiology & Biomedical Engineering.

## Downloads

- [Editable PowerPoint with 50 embedded recordings](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System.pptx), 563.3 MB.
- [Static PDF with recording posters](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System_Static.pdf), 13.0 MB.
- [Presenton static PDF companion](https://api.presenton.ai/s/ToIURk-X4y6Wyfg9Pnlc4qQRCxGCu-AI).
- [Presenton browser preview](https://presenton.ai/presentation-preview?t=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiaHRtbC10by1hbnktcHJldmlldyIsImh0bWxfdG9fYW55X2NyZWF0aW9uIjoxOTU4OCwiZXhwIjoxNzkyNTczOTc3fQ.YtB59_RoBx3Y0t0HoDYofq8LQmMl3Xft96UlG3khq0U), available for 24 hours after creation.

## Content

100 slides: title, 98 teaching slides, and six exam-level takeaways. There are 32 foundation slides and 66 primary-research teaching slides, with original article figures on 84 slides. Every teaching slide has three connected explanatory paragraphs and matching speaker-note teaching text. All 294 paragraphs pass the actual-render five-to-seven-line audit. Source credits, full references, and original figure/movie legends accompany the teaching notes.

Coverage includes central brainstem timing, myelin and inhibition, population coding, inferior colliculus, auditory thalamus, core/belt/parabelt cortex, descending feedback, auditory scenes and attention, multisensory speech and illusions, learned predictions, voice and timbre, pitch, musical expectation, beat and movement, comparative rhythm, improvisation, white matter, developmental music experience, cognitive control, music-evoked nostalgia, auditory learning windows, vocal communication, active echolocation, selective recognition deficits, a brief rewired-ferret callback, and reconstruction of heard music from cortical recordings. Four accessible USC Brain and Creativity Institute studies receive explicit coverage. The chapter supplies the central auditory foundation; peripheral anatomy, mechanics, and hair-cell transduction remain in the separate Audition I deck.

## Format and validation

16:9, Arial throughout, white backgrounds, black body/captions/footers, rosewood headings. The title retains the source-image-left/instructor-details-right format. All scientific figures and movies are original source material; no scientific image was generated or redrawn. Source-derived simulations and anatomical reconstructions are identified. Crops were made with tools/crop_figure.py and recorded with original hashes and boxes.

All 100 slides were rendered and reviewed. Generic and course-specific checks report zero failures. Fifty distinct videos are embedded, distributed 13/12/13/12 by content quarter, with five in the final ten teaching slides and no gap exceeding one slide. Every movie passes full-file decoding. All source and embedded hashes match; all package relationships and native media timing entries resolve. Compatibility conversions preserve timing and dimensions, apart from one documented one-pixel edge pad; the minimum first-60-frame SSIM is 0.987010. The static PDF contains 100 pages and no video attachments. The Presenton PDF is a separate static companion; fonts: Arial, system font, no web-font source.

**Desktop PowerPoint playback has not been tested in this environment.** Click a recording in PowerPoint Slide Show. The PDFs and browser companion display static posters.

Read [slide sequence](SLIDE_SPINE.md), [sources](PAPERS.md), [recording index](VIDEO_INDEX.md), and [validation](VALIDATION.json). The original nonauditory Chapter 7 and the separate peripheral lecture are preserved. The complete uploaded book and full papers remain private and ignored. Subscription access to the 2000 ferret paper was not obtained; its abstract and original figure are distinguished from the fully read 1992 anatomy paper.

## Rebuild and checks

```bash
python3 tools/build_lecture.py chapters/C07_Audition2/lecture.json
python3 chapters/C07_Audition2/embed_media.py
python3 chapters/C07_Audition2/render_static.py
python3 tools/check_paragraph_lines.py chapters/C07_Audition2/lecture.json chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System.pptx chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System_Static.pdf chapters/C07_Audition2/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System.pptx --lecture 702 --content-slides 98
python3 tools/check_course.py chapters/C07_Audition2/lecture.json chapters/C07_Audition2/The_Listening_Brain_Central_Auditory_System.pptx chapters/C07_Audition2/media_sources.json
python3 chapters/C07_Audition2/final_integrity.py
```
