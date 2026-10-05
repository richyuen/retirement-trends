#!/usr/bin/env bash
# Download OASDI and HI/SMI Trustees Reports from govinfo.gov (CDOC collection),
# convert to text with pdftotext -layout, and keep gzipped text in raw/text/.
# PDFs go to a scratch dir ($PDFDIR, default /tmp/ss_trustees_pdf) and are NOT kept
# in the project (the 2024 and 2026 OASDI PDFs are 87 and 73 MB).
# Package ids come from raw/govinfo_trustees_index.csv (scripts/find_trustees_docs.py);
# 2017 OASDI (115hdoc54) is missing from govinfo's browse tree but its package exists.
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
PDFDIR="${PDFDIR:-/tmp/ss_trustees_pdf}"
mkdir -p "$PDFDIR" "$HERE/raw/text"

OASDI="1995:104hdoc57 1996:104hdoc228 1997:105hdoc72 1998:105hdoc243 2000:106hdoc221
2001:107hdoc55 2002:107hdoc196 2004:108hdoc176 2005:109hdoc18 2006:109hdoc103
2010:111hdoc137 2011:112hdoc23 2013:113hdoc33 2014:113hdoc139 2015:114hdoc51
2016:114hdoc145 2017:115hdoc54 2018:115hdoc133 2019:116hdoc28 2020:116hdoc123
2021:117hdoc63 2022:117hdoc127 2023:118hdoc21 2024:118hdoc137 2025:119hdoc62 2026:119hdoc163"
HI="1995:104hdoc56 1996:104hdoc227 1997:105hdoc73 1998:105hdoc245 2000:106hdoc262
2001:107hdoc54 2002:107hdoc197 2004:108hdoc177 2005:109hdoc17 2006:109hdoc102
2010:111hdoc138 2011:112hdoc22 2012:112hdoc101 2013:113hdoc34 2014:113hdoc140
2015:114hdoc50 2016:114hdoc146 2017:115hdoc53 2018:115hdoc132 2019:116hdoc29
2020:116hdoc122 2021:117hdoc62 2022:117hdoc126 2023:118hdoc22 2024:118hdoc136
2025:119hdoc63 2026:119hdoc164"

fetch () {  # $1 prefix (oasdi|hi), $2 year:package
  local yr="${2%%:*}" pkg="CDOC-${2#*:}"
  local out="$HERE/raw/text/$1_$yr.txt.gz"
  [ -s "$out" ] && return 0
  local pdf="$PDFDIR/$pkg.pdf"
  curl -sS -L -C - --retry 5 -m 1800 -o "$pdf" \
    "https://www.govinfo.gov/content/pkg/$pkg/pdf/$pkg.pdf" || true
  if ! pdfinfo "$pdf" >/dev/null 2>&1; then echo "BAD PDF $1 $yr $pkg"; return 0; fi
  pdftotext -layout "$pdf" - | gzip -9 > "$out"
  echo "$1 $yr $pkg pages=$(pdfinfo "$pdf" | awk '/^Pages/{print $2}') text=$(du -h "$out" | cut -f1)"
}
for x in $OASDI; do fetch oasdi "$x"; done
for x in $HI; do fetch hi "$x"; done
# 1995-2000 PDFs are image-only and the 2018 OASDI text layer is garbled: drop their
# (empty/garbled) pdftotext output; scripts/ocr_scanned.sh makes *_ocr.txt.gz instead.
rm -f "$HERE"/raw/text/oasdi_199?.txt.gz "$HERE"/raw/text/oasdi_2000.txt.gz "$HERE"/raw/text/oasdi_2018.txt.gz \
      "$HERE"/raw/text/hi_199?.txt.gz "$HERE"/raw/text/hi_2000.txt.gz
