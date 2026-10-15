# Chapter 3 delivery

Mapping the Nervous System: From Brain Structures to Behavior.

75 slides: title, 73 content, and six Key takeaways. The verified scope is Carlson and Birkett (2022), Structure of the Nervous System, printed pp. 68–90. There are 29 foundation slides and 44 research slides, interwoven. Every content slide contains source imagery; 44 use primary-article panels. Arial text uses a mineral blue / paper white theme with black body text, captions, and footers.

Exactly 40 distinct biological recordings are embedded. The two internal quotas each contain 20 recordings. Media-purpose classifications appear only in internal provenance records, never in slide prose, captions, or teaching notes. Every quarter of the content sequence has ten recordings, no gap exceeds three content slides, and the final ten content slides contain five. Source article figures remain on every recording slide.

All delivery recordings fully decode. Native dimensions, source timing, frame rate, and audio status were checked. All 40 recordings retain their exact original publisher H.264 bytes; no delivery re-encoding is used. Poster frames are sampled from actual recording content. Embedded hashes, internal video/media relationships, and native timing entries are verified by embed_media.py.

Every teaching paragraph must pass the actual 5–7-rendered-line audit against the final static PDF, tied to the final spec and PPTX hashes. Generic and course checks include image coverage, teaching balance, media quotas, visible category labels, and video distribution. Source-panel crop boxes and original legends are retained. Source documents remain private and ignored; the full uploaded book is never published.

The editable PPTX is the primary deliverable. The _Static.pdf and Presenton companion use source posters and do not play video. Desktop PowerPoint playback is unavailable in the cloud and remains untested. Open the PPTX in desktop PowerPoint Slide Show and click the recordings to play them.

Rebuild from the repository root after retrieving Git LFS assets:

```bash
python3 tools/build_lecture.py chapters/C03/lecture.json
python3 chapters/C03/embed_media.py
soffice --headless --convert-to pdf --outdir chapters/C03 chapters/C03/Mapping_the_Nervous_System_Chapter_3.pptx
cp chapters/C03/Mapping_the_Nervous_System_Chapter_3.pdf chapters/C03/Mapping_the_Nervous_System_Chapter_3_Static.pdf
python3 tools/check_paragraph_lines.py chapters/C03/lecture.json chapters/C03/Mapping_the_Nervous_System_Chapter_3.pptx chapters/C03/Mapping_the_Nervous_System_Chapter_3_Static.pdf chapters/C03/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C03/Mapping_the_Nervous_System_Chapter_3.pptx --lecture 3 --content-slides 73
python3 tools/check_course.py chapters/C03/lecture.json chapters/C03/Mapping_the_Nervous_System_Chapter_3.pptx chapters/C03/media_sources.json
```

Embed only into a freshly rebuilt base deck. Chapter 1 and Chapter 2 deliverables are unchanged. The new distribution and visible-label rules apply from Chapter 3 onward.

Presenton static companion PDF: https://api.presenton.ai/s/yelwXwXPn1jOTiAg2Uswi5vZ16Bsvg79. The companion and native deck use Arial; the main static PDF is the locally rendered, paragraph-audited native deck.
