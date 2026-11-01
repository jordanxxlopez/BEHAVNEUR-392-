BEHAVNEUR-392 — SOURCE MANIFEST AND PARTIAL PDF ARCHIVE

The GitHub repository has 23 lecture PDFs, but this workspace does not have direct binary access to all GitHub-hosted assets. The 5 PDFs in the partial archive were converted from original presentations in the user's file library (4 are SHA-256 identical to the repository PPTXs). The full 23-file ZIP could not be built in this environment.

INCLUDED PDFs:
01: History-expanded Chapter 1, 90 pages, from a different locally stored PPTX revision than the latest GitHub SHA. The content is history-expanded but the binary is not identical to the current GitHub PPTX.
02: Chapter 2, exact GitHub PPTX SHA-256 match.
03: Chapter 3, exact GitHub PPTX SHA-256 match.
06: Chapter 6, exact GitHub PPTX SHA-256 match.
07: Chapter 7, exact GitHub PPTX SHA-256 match.

TO FETCH ALL 23:
1. On a Mac with Python 3 and internet access, extract the companion tools ZIP.
2. Double-click Run_Download_All_23.command (or run `python3 download_all_23_pdfs.py` from Terminal).
3. The script downloads the static PDF companions from pinned GitHub commit b443ca5046590de25eaa2c18614166c2234b430c.
4. Every downloaded PDF must be valid and under 29,000,000 bytes; the full ZIP is created only after all 23 pass.

Chapters 16 and 17 are labeled Layout Preview in the GitHub repository. If pdfinfo or pypdf is installed, the script checks they contain 80 pages. If it finds fewer than 80 pages, it will not package them as full lectures.

The GitHub documents are static previews, not playable embedded-video PowerPoints.
