# Audition I: From Sound to Neural Signals

The Peripheral Auditory System is the instructor-authorized 80-slide companion to Chapter 7. It contains a title, 78 teaching slides, and six final takeaways. The six regeneration and translation slides occupy slides 74–79 within the 80-slide total.

Coverage follows acoustic pressure through outer- and middle-ear mechanics, cochlear motion, hair-bundle transduction, inner-hair-cell ribbon synapses, and auditory-nerve coding. Injury, existing-cell repair, animal regeneration, experimental mammalian reprogramming, and requirements for human translation are distinguished. Central auditory pathways and binaural computations are reserved for Part II. The brief efferent material concerns peripheral terminals only.

There are 31 foundation slides and 47 primary-research teaching slides, with original source imagery on every teaching slide. Forty distinct source recordings are embedded, ten in each content quarter and six in the final ten teaching slides. Full teaching transcripts, figure legends, source references, licenses, and media provenance are in the PowerPoint notes and accompanying records.

The editable PowerPoint is `From_Sound_to_Neural_Signals_Peripheral_Auditory_System_Part_I.pptx`. Its clearly labeled `_Static.pdf` companion contains source posters. Arial is used throughout. Download the PowerPoint through the GitHub media URL or use Git LFS; a raw LFS pointer is not the presentation.

Validation covers all 234 rendered paragraphs, every source-media hash, complete audiovisual decoding, all embedded media relationships and timing, and both repository validators. See VALIDATION.json and paragraph_line_check.json. All slide layouts and selected source panels were visually reviewed. Actual desktop PowerPoint playback remains untested.

Rebuild with `assemble_spec.py`, the repository `tools/build_lecture.py`, then `embed_media.py`. Use `make_static_pdf.py` to render a temporary copy without movie objects, retaining posters; exporting the multimedia deck directly can place large media objects into the PDF. Rerun `tools/check_paragraph_lines.py`, `tools/check_lecture.py --lecture 71 --content-slides 78`, and `tools/check_course.py` after a change. Keep all full textbook and article downloads private and ignored.

The Presenton static companion and shareable preview are recorded in presenton_preview.json. Presenton links expire after 24 hours; the repository download links remain available.
