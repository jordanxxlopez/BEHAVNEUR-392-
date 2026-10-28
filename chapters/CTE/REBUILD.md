# CTE lecture sources and validation

This is an instructor-authorized special-topic lecture, not Chapter 20. The editable native deliverable is in `downloads/Brain_Injury_in_Football_CTE.pptx`; the static PDF is alongside it. Scientific references and source figure legends are in lecture.json, sources.json, and figure_sources.json. Player image credits are in player_images.json. Source movie URLs, licenses, hashes, dimensions, full timing, audio, and compatibility conversion details are in media_sources.json.

Original large source recordings and private uploaded textbooks are not duplicated in this branch. The 40 final MP4s are already embedded inside the PPTX. Rebuilding requires obtaining each original recording from the exact manifest URL and verifying its recorded hash, then applying only the documented compatibility conversion where required.

The course builder creates the base editable deck. The CTE media script embeds the originals, finalization adds source links, and the static render script retains original posters. Final rendered line checks, course checks, and media audits are recorded in VALIDATION.json and the associated JSON reports. All 80 slides use Arial. Desktop PowerPoint playback remains untested.
