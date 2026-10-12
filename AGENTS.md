# Behavioral Neuroscience 392: course-specific lecture rules

These instructions apply ONLY to this course. The instructor’s request takes precedence over inherited Neuroethology rules. This is the connected BEHAVNEUR-392- GitHub repository at https://github.com/jordanxxlopez/BEHAVNEUR-392-.git. Keep all Behavioral Neuroscience materials in this repository, separate from NEUR 411.

## Deliverables and level

Build 19 chapter PowerPoints, one per verified chapter in Carlson and Birkett, Physiology of Behavior, Global Edition, 13th edition (2022), ISBN 9781292430256. Verify the table of contents before recording chapter mapping. The instructor explicitly requests descriptive lecture titles, not "Chapter 1"; use the authorized topic title in course/schedule.json. Start with Chapter 1 unless directed otherwise. Prefer 75 slides total: 1 title, 73 content, 1 final Key takeaways. Expand only when useful, to at most 85 total. Do not invent a timetable. Each chapter may span several class meetings.

This is an undergraduate Behavioral Neuroscience course, easier than NEUR 411 but intellectually demanding. Define terms at first use. Explain neuronal signaling, pathways, experimental manipulations, and behavioral findings in clear connected prose. Introduce unfamiliar machinery in steps; avoid graduate-level prerequisite knowledge.

## Teaching and balance

Use approximately 20–30% textbook foundations and 70–80% primary-research teaching. At the preferred count, 18 foundation slides and 55 research slides give approximately 25%/75%. Tag each content slide instructional_role as foundation or research; do not count an incidental citation as research teaching. The textbook defines chapter scope and concepts. Teach each concept, then use source-supported study findings to explain how it works. Use a manageable group of core papers across several slides rather than a different paper on every slide. Include current accessible research and foundational work where needed; verify references and quantitative claims.

Every paragraph teaches material. Use three substantive paragraphs per content slide and natural complete-sentence teaching transcripts in notes, adapting depth to this easier class and readable layout. Do not pad paragraphs to meet a sentence count. No agendas, learning objectives, previews, fixed method-result-limitation templates, presentation commentary, or em dashes in visible text. Do not end paragraphs on routine limitations or stock caution. The instructor will discuss limitations and the importance of controls orally. Preserve scientifically necessary distinctions and genuine experimental conditions; do not turn hypotheses into facts. No p-values, error bars quoted in prose, test names, or sample-size bookkeeping. Retain quantities that explain the concept. Finish with 5–6 exam-level takeaways with bold lead phrases.

## Format

16:9, Arial throughout. Preserve the Neuroethology content-slide style. For this course’s TITLE SLIDE ONLY: white background, a large credited source image on the LEFT, and the instructor-approved descriptive lecture title, course/date, Jordan Lopez, Ph.D., and Professor of Neurobiology & Biomedical Engineering on the RIGHT. Do not mirror or recolor the source image. Body text/captions/footers black; titles and bold words use the chapter’s coordinated restrained theme. Separate theme ledger from NEUR 411; no yellow, orange, gold, purple, or green. Record themes after final validation. Never copy the former professor’s slide style. Analyze their slides for existing course coverage only when available.

## Figures

Every content slide has a relevant source image. Prioritize intact primary-article panels. Textbook crops are explicitly allowed for foundations: retain original labels, caption Carlson and Birkett (2022), figure number and printed page, and record PDF page, ISBN, edition, and source. Retain enough context for students to interpret axes, labels, units, and scale bars. Never generate, redraw, replot, recolor, or reconstruct any scientific image, diagram, chart, or animation. Up to 10 genuinely useful credited web images are permitted. Give the full source reference in notes. New crops are made with tools/crop_figure.py; record crop boxes. Do not post the full uploaded textbook to GitHub.

## Videos

Each final chapter deck requires 15–20 distinct useful academic videos PLUS 5–10 distinct aesthetic animal/neuroscience recordings, totaling 20–30 embedded videos. Aim for 15 academic plus 5 aesthetic. Spread them through the material where appropriate; preserve article figures on video slides. Academic web/YouTube recordings by primary researchers and labs are permitted even when not publisher supplementary movies. No news reports, shorts, TikTok-style edits, unrelated entertainment, or fabricated scenes. Verify and accurately credit source authors, original URLs, study DOI when associated, and supplied license. Aesthetic recordings are real footage connected to the chapter, credited and labeled separately, and never counted as primary scientific evidence or toward the academic-video quota. User uploads remain uploads, not fabricated article supplements.

Embed PowerPoint-compatible MP4s. Preserve native resolution, timing, audio, aspect ratio, and scientific scenes. Compress only when necessary and verify quality. Record video purpose (academic/aesthetic), slide, source, DOI if applicable, dimensions, duration, audio, codec, and SHA256. Verify every embedded media relationship and all source hashes; do not count duplicate excerpts as different studies or pad with repetitions. Retain static source posters. Report untested desktop playback honestly.

## Access

If a paper is blocked, find an accessible primary paper teaching the same necessary concept. Request the paper upload only if that particular source is indispensable. If a selected necessary VIDEO is blocked, stop final delivery and give an exact numbered upload list with original URL, source/paper DOI, movie identifier, and teaching purpose. Continue independent preparation. Never claim an inaccessible PDF, book, prior deck, or video was reviewed. The full book was too large to transfer, but all six split PDFs have now been downloaded. The contents and Introduction chapter were read directly; keep the full source PDFs private and ignored.

## Chapter 1 frontier section

Replace Careers in Neuroscience and Strategies for Learning with source-supported future technologies. Do not teach career advice or study strategies. Include fish-operated vehicles, the requested Winship sea-lion cursor study only after exact source verification, DeepLabCut/computer vision, wireless recordings, optogenetics with substantial stepwise coverage, and biological computing. Existing Biocomputing II and Fish-Operated Vehicle II decks are scientific/reference material, not a license to claim unverified games or capabilities. Explain the actual demonstrated task, sensory encoding, feedback, learning, and neuronal mechanism. Claims about Doom require a verified primary source documenting the actual preparation and task. Verify the 2026 Nobel award through authoritative sources before stating recipients or citation; do not infer names from classic optogenetics papers.

## Build and validation

Use tools/build_lecture.py with the verified chapter spec, then embed media and run tools/check_lecture.py and tools/check_course.py. course/policy.json records the explicit course overrides. Generic builder passes do not establish that final video quotas or 20–30%/70–80% balance are satisfied. Render all slides, inspect figures, captions, body fit, and video placement. Save the editable PPTX and a clearly labeled static PDF preview. Deliver a working direct download. Publish into BEHAVNEUR-392-; do not push course materials into the Neuroethology repository.
