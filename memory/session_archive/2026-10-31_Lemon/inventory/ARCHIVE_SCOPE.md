# Full-session backup scope and limitations

## Saved into Lemon
- Actual GitHub files representing all 23 lecture PDFs, each under `uploaded/BEHAVNEUR392_All_23_Lectures_PDFs/`, not merely hyperlinks.
- Actual complete creation-rule historical text extracted from the provided archive.
- Exact user-facing Prompt 4 / Prompt 5 texts as MD and TXT; latest user teaching-note prompt; available Prompts 1–3 text.
- Detailed reconstructed conversation history, continuation memory, and metadata for **all ChatGPT conversation file records** including filenames and attachment IDs.
- Original text scripts/manifest/verification files from the course archive where available.
- Directory layout and descriptions of preview image files, ZIPs, attached presentations and PDFs.

## Not fully saved and why
- **Verbatim ChatGPT export:** GitHub has no endpoint to obtain the current ChatGPT conversation's original internal transcript. The saved history is a clearly identified reconstruction; using ChatGPT’s UI **Copy as Markdown** and uploading its result would enable a literal transcript.
- **Private internal chain-of-thought:** not a file with a downloadable raw trace; this record gives high-level conclusions and decision chronology instead.
- **Private ChatGPT deep link:** cannot be read from the screenshot or GitHub. Paste it from ChatGPT “Copy deeplink” to add the actual URL.
- **Newly generated PNG/PDF/ZIP screenshot assets:** complete filenames/metadata are indexed, but the available connected GitHub tool cannot transfer raw binary bytes from ChatGPT conversation files. The original ChatGPT attachments remain available in the conversation for download. These are not falsely claimed to be uploaded.
- **Large final PowerPoint masters:** these exist elsewhere in the same GitHub repo in `Latest_Lecture_PowerPoints` and were not generated/modified during this chat. The conversation's original local copies are too large for this GitHub text/file API to re-upload anew here.
- **The ZIP wrapper of the 23 PDFs:** the full 23 actual PDF bytes are available as individual GitHub files, but the duplicate ZIP wrapper itself isn't uploaded.
- **The local container filesystem:** filesystem inventory below references ChatGPT temporary working paths, not a full snapshot of the user's computer or the model execution environment.

## Why this matters
“Saved everything” is only accurate for data present under Lemon plus explicitly indexed external assets. Do not tell the user all binary attachments or the app’s hidden thinking are in GitHub when they are not.
