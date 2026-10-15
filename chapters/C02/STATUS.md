# Chapter 2 delivery

Title: How Nerve Cells Work: From Electrical Signals to Chemical Communication.

75 slides: title, 73 content, six-point Key takeaways. There are 29 foundation slides (39.7%) and 44 research slides (60.3%), interwoven. Every content slide has source imagery; 46 carry primary-article imagery. The independent course theme is Prussian blue / fog; the native text font is Arial.

Exactly 40 distinct recordings are embedded: 20 academic and 20 aesthetic. Duplicate channel exports, alternate motion-correction footage, and a rotating reconstruction were excluded from the count. Context recordings remain labeled separately and are not treated as primary evidence. All 40 delivery files fully decode, and their hashes match the embedded bytes. Native timing and source audio status were checked. Necessary compatibility conversions preserve the scenes and native frame rates; odd dimensions receive only one-pixel edge padding. Sampled conversion SSIM is recorded in media_validation.json; this is a first-60-frame comparison, not a whole-video quality score.

All 219 teaching paragraphs have 5–7 actual rendered lines. The generic deck checker and course checker both report zero failures; the generic checker reports zero warnings. All 75 final slides were rendered and visually reviewed. Crop boxes, figure credits, full references, exact article licenses, and media provenance are retained. The primary-figure threshold in the builder/checker now reads the course policy's 60% minimum rather than an inherited hard-coded 70%. Foundation versus research teaching roles remain independent of the figure type.

The editable PPTX contains the videos. The accompanying _Static.pdf and Presenton web/PDF preview are static and use source posters. Desktop PowerPoint playback was unavailable and remains untested. Use desktop PowerPoint Slide Show to play the embedded recordings.

The final lecture.json is authoritative. teaching_content.txt mirrors the reviewed prose. Source PDFs stay in ignored private storage, and the full uploaded textbook is never published. Existing Chapter 1 decks were not rebuilt.

Rebuild from the repository root:

```bash
python3 tools/build_lecture.py chapters/C02/lecture.json
python3 chapters/C02/embed_media.py
soffice --headless --convert-to pdf --outdir chapters/C02 chapters/C02/How_Nerve_Cells_Work_Chapter_2.pptx
cp chapters/C02/How_Nerve_Cells_Work_Chapter_2.pdf chapters/C02/How_Nerve_Cells_Work_Chapter_2_Static.pdf
python3 tools/check_paragraph_lines.py chapters/C02/lecture.json chapters/C02/How_Nerve_Cells_Work_Chapter_2.pptx chapters/C02/How_Nerve_Cells_Work_Chapter_2_Static.pdf chapters/C02/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C02/How_Nerve_Cells_Work_Chapter_2.pptx --lecture 2 --content-slides 73
python3 tools/check_course.py chapters/C02/lecture.json chapters/C02/How_Nerve_Cells_Work_Chapter_2.pptx chapters/C02/media_sources.json
```

Retrieve Git LFS files before rebuilding. Run embedding only on a freshly rebuilt base deck. The checked paragraph audit is tied to the exact final spec and PPTX hashes.
