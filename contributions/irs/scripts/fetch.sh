#!/usr/bin/env bash
# Download the IRS SOI files used by this folder into raw/ (untrusted data; parse only with python3 -I).
# Archive PDFs (YYinar.pdf, 25-45 MB each) are NOT kept in the project; values from them are hand-transcribed in f1040_long.py.
set -u
R="$(cd "$(dirname "$0")/.." && pwd)/raw"; S=https://www.irs.gov/pub/irs-soi
mkdir -p "$R/ira" "$R/w2" "$R/f1040"
get(){ curl -sS -L -m 300 -o "$1" "$2" || echo "FAILED $2"; }
for f in 00in01ir.xls 00in02ir.xls 00in03ir.xls 00in04ir.xls 00in05ir.xls 01in01ira.xls 01in02ira.xls 01in03ira.xls 01in04ira.xls 01in05ira.xls \
         02in06ira.xls 02in07ira.xls 02in08ira.xls 02in09ira.xls 02in10ira.xls 04in07ira.xls; do get "$R/ira/$f" "$S/$f"; done
for y in 04 05 06 07 08 09 10 11 12 13 14 15 16; do for t in 01 04 05 06; do get "$R/ira/${y}in${t}ira.xls" "$S/${y}in${t}ira.xls"; done; done
for y in 17 18 19 20 21 22 23; do for t in 01 04 05 06 08; do get "$R/ira/${y}in${t}ira.xlsx" "$S/${y}in${t}ira.xlsx"; done; done
get "$R/w2/18inallw2.xls" "$S/18inallw2.xls"
for y in 19 20; do for t in 1 2 3 4; do get "$R/w2/${y}in0${t}w2all.xlsx" "$S/${y}in0${t}w2all.xlsx"; done; done
get "$R/f1040/histab1.xls" "$S/histab1.xls"
for f in 93in14si.xls 94in14si.xls 95in14ar.xls 96in14si.xls 97in14.xls 98in14ar.xls 99in14ar.xls 16in14ar.xls 17in14ar.xls 18in14ar.xls 19in14ar.xls 20in14ar.xls 21in14ar.xls 22in14ar.xls 23in14ar.xls \
         17in33ar.xls 18in33ar.xls 19in33ar.xls 20in33ar.xls 21in33ar.xls 22in33ar.xls 23in33ar.xls; do get "$R/f1040/$f" "$S/$f"; done
get "$R/cola_prior_years.pdf" https://www.irs.gov/pub/foia/ig/tege/cola-table-dci005ma4578824.pdf
get "$R/page_cola.html" https://www.irs.gov/retirement-plans/cola-increases-for-dollar-limitations-on-benefits-and-contributions
