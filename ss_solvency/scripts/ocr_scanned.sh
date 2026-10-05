#!/usr/bin/env bash
# The 1995-2000 Trustees Reports (and the 2018 OASDI report, see below) on govinfo are image-only scans (pdftotext gives
# nothing). OCR the front section (highlights / overview / actuarial balance
# summary) and the pages holding worker-beneficiary ratios with tesseract.
# Writes raw/text/<fund>_<year>_ocr.txt.gz with "=== page N ===" markers (PDF page numbers).
# Requires: pdftoppm (poppler), tesseract. PDFs from scripts/fetch_reports.sh in $PDFDIR.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PDFDIR="${PDFDIR:-/tmp/ss_trustees_pdf}"
WORK="$(mktemp -d)"
FIRST="${FIRST:-1}"; LAST="${LAST:-60}"

ocr () {  # $1 fund, $2 year, $3 package
  local out="$HERE/raw/text/$1_$2_ocr.txt.gz" pdf="$PDFDIR/CDOC-$3.pdf"
  [ -s "$out" ] && return 0
  [ -f "$pdf" ] || curl -sS -L --retry 5 -o "$pdf" "https://www.govinfo.gov/content/pkg/CDOC-$3/pdf/CDOC-$3.pdf"
  pdftoppm -r 200 -gray -png -f "$FIRST" -l "$LAST" "$pdf" "$WORK/p"
  # one tesseract per page, 4 in parallel, single-threaded, 120 s cap per page
  ls "$WORK"/p-*.png | OMP_THREAD_LIMIT=1 xargs -P 4 -I{} sh -c 'timeout 120 tesseract "{}" "{}" --psm 6 >/dev/null 2>&1 || echo "[OCR timed out]" > "{}.txt"'
  { for img in $(ls "$WORK"/p-*.png | sort -V); do
      n=$(basename "$img" .png); n=$((10#${n##*-}))
      echo "=== page $n ==="; cat "$img.txt" 2>/dev/null
    done; } | gzip -9 > "$out"
  rm -f "$WORK"/p-*
  echo "$1 $2 OCR pages $FIRST-$LAST -> $(du -h "$out" | cut -f1)"
}
# Optional args "fund:year:package" OCR just those (used for the 2018 OASDI report,
# whose PDF text layer has a broken font encoding).
if [ $# -gt 0 ]; then
  for a in "$@"; do IFS=: read f y p <<< "$a"; ocr "$f" "$y" "$p"; done; rm -rf "$WORK"; exit 0
fi
for x in 1995:104hdoc57 1996:104hdoc228 1997:105hdoc72 1998:105hdoc243 2000:106hdoc221; do
  ocr oasdi "${x%%:*}" "${x#*:}"; done
for x in 1996:104hdoc227 1997:105hdoc73 1998:105hdoc245 2000:106hdoc262; do
  ocr hi "${x%%:*}" "${x#*:}"; done
rm -rf "$WORK"
