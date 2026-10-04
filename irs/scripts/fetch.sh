#!/usr/bin/env bash
# Re-download the sources used by analyze.py. Small files go to irs/raw/, large PDFs to $P4801_DIR (scratch).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; RAW="$HERE/../raw"
P4801_DIR="${P4801_DIR:-/tmp/irs_p4801}"; mkdir -p "$RAW/irs_soi" "$RAW/ici" "$P4801_DIR"
UA="Mozilla/5.0"
for y in 04 05 06 07 08 09 10 11 12 13 14 15 16; do
  for t in 01 04; do curl -sS -A "$UA" -o "$RAW/irs_soi/${y}in${t}ira.xls" "https://www.irs.gov/pub/irs-soi/${y}in${t}ira.xls"; done; done
for y in 17 18 19 20 21 22 23; do
  for t in 01 04; do curl -sS -A "$UA" -o "$RAW/irs_soi/${y}in${t}ira.xlsx" "https://www.irs.gov/pub/irs-soi/${y}in${t}ira.xlsx"; done; done
for f in 22in01iraci 22in04iraci 23in01iraci 23in04iraci 22in05ira 22in06ira 21in05ira; do
  curl -sS -A "$UA" -o "$RAW/irs_soi/$f.xlsx" "https://www.irs.gov/pub/irs-soi/$f.xlsx"; done
# TY2024 probe (404 on 2026-10-04)
for f in 24in01ira.xlsx 24in04ira.xlsx; do curl -sS -A "$UA" -o /dev/null -w "$f %{http_code}\n" "https://www.irs.gov/pub/irs-soi/$f"; done
# Publication 4801 (Form 1040 line-item estimates), TY2019-2023
for f in irs-prior/p4801--2021.pdf irs-prior/p4801--2022.pdf irs-prior/p4801--2024.pdf irs-prior/p4801--122024.pdf irs-pdf/p4801.pdf; do
  curl -sS -A "$UA" -o "$P4801_DIR/$(basename $f)" "https://www.irs.gov/pub/$f"; done
# ICI files: www.ici.org returns 403 (Akamai) to curl from this machine; they were fetched with WebFetch:
#   https://www.ici.org/statistical-report/ret_26_q2_data.xls  -> raw/ici/ret_26_q2_data.xls
#   https://www.ici.org/system/files/2026-06/per32-07.pdf     -> raw/ici/per32-07.pdf
echo "then: P4801_DIR=$P4801_DIR python $HERE/analyze.py"
