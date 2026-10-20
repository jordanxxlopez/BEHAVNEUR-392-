# Sensing the Body and the Chemical World

**Balance, Touch, Pain, Taste, and Smell** — Chapter 7, Behavioral Neuroscience 392.

This is the instructor-authorized **nonauditory** Chapter 7 lecture. Audition and hearing are excluded and reserved for a separate future lecture. The supplied Carlson and Birkett (2022), *Physiology of Behavior*, Global Edition, 13th edition, ISBN 9781292430256, was inspected directly: Chapter 7 is printed pp. 191–234. This deck covers the vestibular, somatosensory, gustatory, and olfactory material on printed pp. **210–234**, Part 3 PDF pp. **38–62**. Chapter 8 starts printed p. 235.

## Downloads

- [Editable PowerPoint, including 40 embedded recordings](https://media.githubusercontent.com/media/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx), approximately 255 MB.
- [Static PDF preview](https://raw.githubusercontent.com/jordanxxlopez/BEHAVNEUR-392-/main/chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7_Static.pdf), approximately 11 MB. Uses source posters; contains no playable video objects.

## Teaching sequence

75 slides: title, 73 teaching slides, and six exam-level takeaways on the closing slide.

| Slides | Coverage |
|---|---|
| 2–9 | Vestibular sensation, hair bundles, canals, otolith organs, gaze stabilization, and coordination |
| 10–28 | Skin receptors, touch, sensory pathways, proprioception, and cortical representations |
| 29–33 | Temperature, itch, scratching, and chemical irritation |
| 34–50 | Nociception, pain, spinal processing, descending modulation, opioids, and attention |
| 51–61 | Taste cells, transduction, pathways, feeding decisions, and flavor |
| 62–74 | Olfactory receptors, glomeruli, circuit development, learning, and odor-guided navigation |

29 foundation slides (39.7%) and 44 research slides (60.3%) are interwoven. The scope retains a brief sensory explanation of muscle spindles without moving the detailed Chapter 8 motor-control material into this deck. Human studies include somatosensory-cortex stimulation, attentional analgesia, and odor-mixture learning. Mammalian and fly receptor mechanisms are distinguished, as are pain and nociception, calcium fluorescence and electrical recordings, and taste and flavor. Five familiar taste qualities and research on oral fatty-acid sensing are distinguished rather than presenting all nutrient preferences as equally established human taste categories.

The 16:9 editable deck uses Arial, a white title slide with the source image left and instructor information right, black body text, and a sapphire/silver theme. Every teaching slide has three substantive paragraphs and a matching teaching transcript before the references in notes. All content slides retain original source imagery; 44 use primary-article figures. Figures are never redrawn or recolored. Original source-panel crops and full legends are recorded in figure_sources.json. Textbook coordinates distinguish the visible CropBox from the MediaBox used by the crop tool.

## Recording and validation evidence

Exactly 40 distinct original publisher MP4s are embedded: 20 academic and 20 visual-context recordings. Purpose classifications appear in the internal manifest and index, not visible teaching or teaching-note labels. Every quarter contains ten recordings; six occur in the final ten teaching slides. No content gap between recordings exceeds one slide.

All 40 movies retain their original bytes, resolution, timing, frame rate, and audio presence; no delivery conversion was necessary. Full FFmpeg decoding passes for all recordings. Embedded hashes, internal video and media relationships, and native PowerPoint timing entries are verified. Source posters are sampled from actual recording content.

All 219 paragraphs pass the 5–7 actual rendered-line requirement using Arial, with no forced line breaks or blank-line padding. The audit identifies the exact final specification, PPTX, and static PDF by SHA256. Generic and course checks report zero failures; the generic checker reports zero warnings. All slides and source-panel sheets were visually reviewed. VALIDATION.json, paragraph_line_check.json, media_validation.json, PAPERS.md, VIDEO_INDEX.md, and SLIDE_SPINE.md retain the evidence.

**Desktop PowerPoint playback remains untested.** Open the PPTX in desktop PowerPoint Slide Show and click movie objects. The PDF and Presenton companion are static. Full textbook PDFs and downloaded article sources remain private and ignored.

## Rebuild

The final **lecture.json is authoritative**. Assembly scripts record initial preparation and must not overwrite later reviewed changes blindly. Retrieve Git LFS assets first. Embed only into a freshly rebuilt base deck.

```bash
cd /workspace/BEHAVNEUR-392-
source /workspace/.venvs/behavneur/bin/activate
export PATH=/workspace/.setup/bin:$PATH
export FONTCONFIG_FILE=/workspace/.setup/fonts.conf
python tools/build_lecture.py chapters/C07/lecture.json
python chapters/C07/embed_media.py
python chapters/C07/make_static_pdf.py
python tools/check_paragraph_lines.py chapters/C07/lecture.json chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7_Static.pdf chapters/C07/paragraph_line_check.json
python tools/check_lecture.py chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx --lecture 7 --content-slides 73
python tools/check_course.py chapters/C07/lecture.json chapters/C07/Sensing_the_Body_and_the_Chemical_World_Chapter_7.pptx chapters/C07/media_sources.json
python chapters/C07/validate_recordings.py
```

The static renderer uses an ignored temporary PowerPoint copy with movie objects removed and original poster shapes retained. This avoids embedding multimedia in the static PDF while preserving native text and layout. It leaves the primary editable PPTX unchanged. On other machines, install the Python requirements plus PyMuPDF, use a compatible LibreOffice installation, and make licensed Arial available before claiming final line-count compliance.

A Presenton static companion is recorded in presenton_preview.json. Its HTML uses the exact final static pages and source credits; full source PDFs were not uploaded. The HTML declares Arial, matching the rendered native text. Presenton download and browser-preview links expire after 24 hours; repository downloads remain the primary deliverables.
