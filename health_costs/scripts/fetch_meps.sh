#!/bin/sh
# Download MEPS-HC Full Year Consolidated (FYC) files 1996-2024 into a cache dir (default: $MEPS_CACHE or ./meps_cache).
# Files are 5-25MB zipped each; they are NOT stored in raw/ (too large in total, ~400MB). raw/ keeps the slim extracts.
CACHE=${MEPS_CACHE:-./meps_cache}; mkdir -p "$CACHE"
B=https://meps.ahrq.gov/mepsweb/data_files/pufs
for n in 12 20 28 38 50 60 70 79 89 97 105 113 121 129 138 147 155 163 171 181 192; do
  [ -s "$CACHE/h${n}ssp.zip" ] || curl -sS -m 600 -o "$CACHE/h${n}ssp.zip" "$B/h${n}ssp.zip"; done
for n in 201 209 216 224 233 243 251 256; do
  [ -s "$CACHE/h${n}dta.zip" ] || curl -sS -m 600 -o "$CACHE/h${n}dta.zip" "$B/h${n}/h${n}dta.zip"; done
ls -la "$CACHE"
