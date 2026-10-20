# Reading and Rewriting the Brain: Tools of Discovery and Neuroengineering

Completed Chapter 5 lecture for Behavioral Neuroscience 392, Fall 2026. Jordan Lopez, Ph.D., Professor of Neurobiology & Biomedical Engineering.

The verified source chapter is **Methods and Strategies of Research**, Carlson and Birkett (2022), Global Edition, 13th edition, ISBN 9781292430256, printed pages 119–152 (uploaded Part 2, PDF 39–72). The instructor authorized 80–90 slides and expanded coverage of newer methods and neuroengineering.

## Downloads

- [Editable PowerPoint with 40 embedded recordings](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx), approximately 876 MB.
- [Static PDF with recording posters](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5_Static.pdf), approximately 13.3 MB.
- [Presenton static PDF companion](https://api.presenton.ai/s/gVv6O6WEmWy1tuvCpAjP5uvFL90sT8UR).
- [Presenton browser preview](https://presenton.ai/presentation-preview?t=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiaHRtbC10by1hbnktcHJldmlldyIsImh0bWxfdG9fYW55X2NyZWF0aW9uIjoxOTQ3NCwiZXhwIjoxNzkyNTYzMjg5fQ.uMU0FmYtIEo4Jh3WXsgASyCxn9nXofETr5NEnPs8VUg), expires 24 hours after creation.

## Content and style

86 total slides: one title, 84 teaching slides, and six final takeaways on one closing slide. Foundations (31 slides) are interwoven with research teaching (53 slides). Every teaching slide contains three explanatory paragraphs and matching teaching notes. The writing follows course/TEACHING_STYLE.md and the instructor's corrected Chapter 4 example: defined terms, connected explanations, specific actions and results, and substantive final paragraphs.

Coverage includes lesions, stereotaxy, histology, directional tracing, structural imaging, diffusion imaging, PET, EEG/MEG, extracellular recordings, Neuropixels, BOLD, two-photon microscopy, miniscopes, calcium and voltage indicators, optogenetics, chemogenetics, immunohistochemistry, microdialysis, receptor labeling, activity-associated genes, inherited variation, RNA sequencing, spatial transcriptomics, antisense, CRISPR/CRISPRi, connectomics, automated behavior analysis, real-time neural decoding, speech BCIs, and brain–spine interfaces.

The layout follows Chapter 4: white title slide with original credited image left; title and instructor information right; 16:9; Arial; black body/captions/footers; coordinated restrained navy (dove/oyster) headings. No generated scientific figures or recreated data. [Slide sequence](SLIDE_SPINE.md), [sources](PAPERS.md), and [recordings](VIDEO_INDEX.md) accompany the files.

## Validation

All 252 paragraphs pass the actual-render 5–7-line audit. Generic and course-specific checks pass with zero failures. All 86 slides were rendered and reviewed. All 40 distinct MP4s are embedded, with ten in each content quarter, no gap over three teaching slides, and six recordings in the final ten teaching slides. Classifications remain in provenance records.

All movie hashes and package relationships resolve. All 40 recordings pass full decoding. 35 retain original movie bytes; five require H.264 compatibility conversion. Source dimensions, frame rates, timing, and audio presence are preserved. Conversion quality checks compare the first 60 frames; minimum SSIM is 0.990579. 49 unique original publisher figure assets were re-fetched and hash-verified; crops retain source panels and are documented. Full textbook and article source files remain private/ignored.

Desktop PowerPoint playback is untested in this environment. Click movie objects in PowerPoint Slide Show; PDFs and the browser companion contain static posters. Exact bytes, hashes, and checks are in VALIDATION.json and the accompanying audit files.

## Rebuild

```bash
python3 tools/build_lecture.py chapters/C05/lecture.json
python3 chapters/C05/embed_media.py
soffice --headless --convert-to pdf --outdir chapters/C05 chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx
cp chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pdf chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5_Static.pdf
python3 tools/check_paragraph_lines.py chapters/C05/lecture.json chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5_Static.pdf chapters/C05/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx --lecture 5 --content-slides 84
python3 tools/check_course.py chapters/C05/lecture.json chapters/C05/Reading_and_Rewriting_the_Brain_Chapter_5.pptx chapters/C05/media_sources.json
python3 chapters/C05/final_integrity.py
```
