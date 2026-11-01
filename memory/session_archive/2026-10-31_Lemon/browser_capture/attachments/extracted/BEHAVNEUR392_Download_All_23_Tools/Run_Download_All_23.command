#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 download_all_23_pdfs.py
printf '\nPress Enter to close...'
read -r _
