# Chapters 18 and 19

The native PPTXs contain 40 offline recordings each. Presenton exports are separate static companions.

The source specifications, original figure assets, source captions, three-paragraph teaching transcripts, crop coordinates, and movie provenance are included. The full uploaded textbook is private and excluded. Original publisher movie files can be retrieved using the URLs in media_selection.json; download_media_18_19.py preserves native timing and verifies compatibility.

From the repository root:

1. Install the course's existing Python requirements, ffmpeg/ffprobe, LibreOffice, and Arial fonts.
2. Run `python chapters/download_media_18_19.py 18 19` when the media files are absent.
3. Run `python chapters/assemble_chapters_18_19.py`.
4. Run `python tools/build_lecture.py chapters/C18/lecture.json` and the corresponding C19 command.
5. Run `python chapters/embed_media_18_19.py 18` and the corresponding C19 command.
6. Run `python chapters/finalize_text_18_19.py 18 19`.
7. Run `python chapters/refine_video_posters_18_19.py` to retain the reviewed source-frame posters without changing movie bytes.
8. Render static previews with `python chapters/make_static_pdf_18_19.py 18` and the corresponding C19 command.
9. Run the generic, course, actual paragraph-line, and embedded-media checkers. Any new render needs a fresh line audit. Final delivery hashes are recorded in VALIDATION.json.

Book crops are already supplied. If regenerating them from the uploaded PDF, use the recorded MediaBox fractions with tools/crop_figure.py. The PDF CropBox and MediaBox differ; the separately recorded intended CropBox fractions describe the inspected visible page. Do not substitute those fractions directly into the crop tool.

The large inline layout matches the established course: source figures above the videos, original aspect ratios retained, and full-screen playback configured. Desktop PowerPoint playback has not been tested in this environment.
