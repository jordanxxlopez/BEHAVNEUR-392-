# Chapter 4 delivery

Chemical Control of Behavior: Drugs and Neural Signaling.

The verified scope is Carlson and Birkett (2022), Psychopharmacology and Neurotransmitters, printed pp. 91–118, ISBN 9781292430256. The lecture contains 75 slides: one title, 73 content, and a final slide with six Key takeaways. It interweaves 29 foundation slides and 44 research slides. Every content slide has source imagery; 44 use primary-article panels. Arial text uses the muted carmine / paper white theme with black body text, captions, and footers.

Exactly 40 distinct source recordings are embedded. Each internal quota contains 20 recordings. Classifications do not appear in visible slides, captions, or teaching notes. There are ten recordings in each content quarter, the longest interval is three content positions, and five recordings occur in the final ten content slides. Article images remain above videos on research slides.

All 40 delivery recordings fully decode. Compatible original H.264 MP4 files retain their exact publisher bytes. One QuickTime file is remuxed losslessly; recordings with incompatible codecs or pixel formats receive necessary H.264 conversion at native frame rate and timing. Two files require a one-pixel edge pad for even dimensions. Source audio presence and frame rates match all delivery files. The minimum first-60-frame SSIM for converted files is 0.988706. Original and final hashes, codec, dimensions, timing, and conversion details appear in media_sources.json and media_validation.json.

Original source-image hashes match all 39 publisher figures. Crops preserve original colors, labels, scales, and axes. Textbook crop records distinguish the PDF CropBox coordinates from the MediaBox coordinates used by the crop tool. Full source PDFs remain private and ignored. The 15 core papers are indexed in PAPERS.md.

The final paragraph audit counts actual rendered PDF baselines: all 219 teaching paragraphs contain 5–7 lines, with no forced line breaks or padding. The audit identifies the exact spec, PPTX, and PDF by SHA256. Generic and course-specific checks pass. Embedded media hashes, internal relationships, and native timing are verified during embedding. All 75 slides were visually inspected.

The editable PPTX is the primary deliverable. The _Static.pdf and Presenton companion contain source posters and do not play video. Desktop PowerPoint playback is unavailable in the cloud and remains untested. Open the PPTX in desktop PowerPoint Slide Show and click recordings to play them.

Rebuild from the repository root after retrieving Git LFS assets:

```bash
python3 tools/build_lecture.py chapters/C04/lecture.json
python3 chapters/C04/embed_media.py
soffice --headless --convert-to pdf --outdir chapters/C04 chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pptx
cp chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pdf chapters/C04/Chemical_Control_of_Behavior_Chapter_4_Static.pdf
python3 tools/check_paragraph_lines.py chapters/C04/lecture.json chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pptx chapters/C04/Chemical_Control_of_Behavior_Chapter_4_Static.pdf chapters/C04/paragraph_line_check.json
python3 tools/check_lecture.py chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pptx --lecture 4 --content-slides 73
python3 tools/check_course.py chapters/C04/lecture.json chapters/C04/Chemical_Control_of_Behavior_Chapter_4.pptx chapters/C04/media_sources.json
```

Embed only into a freshly rebuilt base deck. Chapters 1–3 are unchanged.
