# New standalone psychology and cognitive-neuroscience lecture

The native editable PPTX and static PDF are in downloads/. This lecture uses internal special-topic ID 802 and is separate from the neurobiology lecture, ID 801. The course builder reads lecture.json. Source figures, credits, licenses, player records, study details, and movie provenance are retained in the JSON manifests and notes.

Original MP4s are embedded in the native PPTX. Large original downloads and private textbook PDFs are not duplicated in this branch. Rebuilding requires retrieving the exact original media URLs and verifying source hashes before applying documented compatibility conversions. The clinical demonstrations use the highest-resolution public web MP4 renditions identified by the source player's public manifests, retaining native dimensions, full timing, and audio.

Build the base deck, run embed_media_cte_psych.py, finalize_cte_psych.py, sync_notes_cte_psych.py, and enlarge_cte_psych_videos.py, then render the static PDF. Run the paragraph-line, media, generic, and course checks. VALIDATION.json records the final artifact hashes and actual rendered results. All authored slide and note text uses Arial. Native desktop PowerPoint playback remains untested.
