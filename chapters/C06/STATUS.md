# From Light to Sight: How the Brain Builds the Visual World

Completed Chapter 6 for Behavioral Neuroscience 392, Fall 2026. Jordan Lopez, Ph.D., Professor of Neurobiology & Biomedical Engineering.

The verified source chapter is **Vision**, Carlson and Birkett (2022), Global Edition, 13th edition, ISBN 9781292430256, printed pp. 153–190. The instructor authorized 85–90 slides with visual illusions and a brief treatment of rewired ferrets and plasticity.

## Downloads

- [Editable PowerPoint with 40 embedded recordings](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/09da057fd13e59af09101e3522edeabda18a609e/chapters/C06/From_Light_to_Sight_Chapter_6.pptx), approximately 407.6 MB.
- [Static PDF with recording posters](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/09da057fd13e59af09101e3522edeabda18a609e/chapters/C06/From_Light_to_Sight_Chapter_6_Static.pdf), approximately 12.4 MB.
- [Presenton static PDF companion](https://api.presenton.ai/s/cA4RETUNGqW_FjazpyOd74-nGWE3cn6c).
- [Presenton browser preview](https://presenton.ai/presentation-preview?t=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiaHRtbC10by1hbnktcHJldmlldyIsImh0bWxfdG9fYW55X2NyZWF0aW9uIjoxOTUzNywiZXhwIjoxNzkyNTY4OTE4fQ.svP7noHTd2H-65APbvI81A5bCOcJk82l8nOvzdVn0sI), expires 24 hours after creation.

## Content and style

90 total slides: one title, 88 teaching slides, and one closing slide with six takeaways. Foundations (32) and research teaching (56) are interwoven. Every teaching slide has three explanatory paragraphs, matching speaker-note teaching text, and credited source imagery. The prose follows the instructor's Chapter 4 correction and course/TEACHING_STYLE.md: define terms, explain mechanisms and observed changes, and use the third paragraph for substantive teaching.

Coverage includes optics, phototransduction, ON/OFF signaling, retinal receptive fields, ganglion-cell imaging, synaptic timing, LGN and cortical maps, visual connectomics, orientation selectivity, spatial frequency, color and adaptation, recognition, infant development, binocular depth, motion and gaze, optogenetic restoration, and intracortical visual prostheses. Illusions include the blind spot, surrounding brightness, scintillating starburst and grids, filtered-image recognition, illusory contours, negative afterimages, face orientation, and double drift.

Four ferret slides (31–34) explain neonatal retinal rerouting through auditory thalamus, visual receptive fields, orientation modules, and behavior. Additional plasticity examples include adult primate opsin gene therapy, infant category development, and visuomotor recalibration after cataract removal. The later audition lecture should make a short callback after its normal pathway.

The 16:9 layout uses Arial, white backgrounds, black body/caption/footer text, and restrained optical-blue headings. The title retains the course's source-image-left/instructor-details-right format. No scientific image or movie was generated, redrawn, or reconstructed. Original panel crops retain the relevant axes, scale bars, and labels. See [slide sequence](SLIDE_SPINE.md), [papers](PAPERS.md), and [recordings](VIDEO_INDEX.md).

## Validation

All 264 paragraphs pass the actual-export 5–7-line audit. Generic and course-specific checks report zero failures. All 90 rendered slides, figure crops, and recording posters were visually reviewed. All 40 distinct recordings are embedded, ten in each content quarter, with no gap beyond three teaching slides and six recordings in the final ten. All source/embedded movie hashes and package relationships resolve. Every movie passes full-file decoding; eight necessary H.264 compatibility conversions preserve native dimensions, timing, and audio. Minimum first-60-frame SSIM: 0.995537.

Source access is documented honestly: open full texts were reviewed, while the two 2000 Nature ferret papers use their public abstracts and original figure panels. Their subscription full text was not accessed. The 1992 ferret paper was read in full. See source_access_review.json and the source notes. The complete uploaded book and paper source files remain private.

Desktop PowerPoint playback has not been tested in this environment. Click movie objects in PowerPoint Slide Show; PDF and browser companions use static source posters. Exact final hashes and sizes are in VALIDATION.json.

## Rebuild

```bash
python3 tools/build_lecture.py chapters/C06/lecture.json
python3 chapters/C06/embed_media.py
soffice --headless --convert-to pdf --outdir chapters/C06 chapters/C06/From_Light_to_Sight_Chapter_6.pptx
python3 chapters/C06/make_static_preview.py
python3 tools/check_paragraph_lines.py chapters/C06/lecture.json chapters/C06/From_Light_to_Sight_Chapter_6.pptx chapters/C06/From_Light_to_Sight_Chapter_6_Static.pdf chapters/C06/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C06/From_Light_to_Sight_Chapter_6.pptx --lecture 6 --content-slides 88
python3 tools/check_course.py chapters/C06/lecture.json chapters/C06/From_Light_to_Sight_Chapter_6.pptx chapters/C06/media_sources.json
python3 chapters/C06/final_integrity.py
```
